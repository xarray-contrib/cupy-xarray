"""
:doc:`kvikIO <kvikio:index>` backend for xarray to read Zarr stores directly into CuPy
arrays in GPU memory.
"""

import os
import warnings

import cupy as cp
import numpy as np
from xarray import Variable
from xarray.backends import zarr as zarr_backend
from xarray.backends.common import _normalize_path  # TODO: can this be public
from xarray.backends.store import StoreBackendEntrypoint
from xarray.backends.zarr import ZarrArrayWrapper, ZarrBackendEntrypoint, ZarrStore
from xarray.core import indexing
from xarray.core.utils import close_on_error  # TODO: can this be public.

try:
    import kvikio.zarr
    import zarr

    has_kvikio = True
except ImportError:
    has_kvikio = False


#  TODO: minimum kvikio version for supporting consolidated
#  TODO: minimum xarray version for ZarrArrayWrapper._array 2023.10.0?


class DummyZarrArrayWrapper(ZarrArrayWrapper):
    def __init__(self, array: np.ndarray):
        assert isinstance(array, np.ndarray)
        self._array = array
        self.filters = None
        self.dtype = array.dtype
        self.shape = array.shape

    def __array__(self):
        return self._array

    def get_array(self):
        return self._array

    def __getitem__(self, key):
        return self._array[key]


class CupyZarrArrayWrapper(ZarrArrayWrapper):
    def __array__(self):
        return self.get_array()


class EagerCupyZarrArrayWrapper(ZarrArrayWrapper):
    """Used to wrap dimension coordinates."""

    def __array__(self):
        return self._array[:].get()

    def get_array(self):
        # total hack: make a numpy array look like a Zarr array
        # this gets us through Xarray's backend layers
        return DummyZarrArrayWrapper(self._array[:].get())


class GDSZarrStore(ZarrStore):
    @classmethod
    def open_group(
        cls,
        store,
        mode="r",
        synchronizer=None,
        group=None,
        consolidated=False,
        consolidate_on_close=False,
        chunk_store=None,
        storage_options=None,
        append_dim=None,
        write_region=None,
        safe_chunks=True,
        stacklevel=2,
    ):
        # zarr doesn't support pathlib.Path objects yet. zarr-python#601
        if isinstance(store, os.PathLike):
            store = os.fspath(store)

        open_kwargs = dict(
            mode=mode,
            synchronizer=synchronizer,
            path=group,
            ########## NEW STUFF
            meta_array=cp.empty(()),
        )
        open_kwargs["storage_options"] = storage_options

        if chunk_store:
            open_kwargs["chunk_store"] = chunk_store
            if consolidated is None:
                consolidated = False

        store = kvikio.zarr.GDSStore(store)

        if consolidated is None:
            try:
                zarr_group = zarr.open_consolidated(store, **open_kwargs)
            except KeyError:
                warnings.warn(
                    "Failed to open Zarr store with consolidated metadata, "
                    "falling back to try reading non-consolidated metadata. "
                    "This is typically much slower for opening a dataset. "
                    "To silence this warning, consider:\n"
                    "1. Consolidating metadata in this existing store with "
                    "zarr.consolidate_metadata().\n"
                    "2. Explicitly setting consolidated=False, to avoid trying "
                    "to read consolidate metadata, or\n"
                    "3. Explicitly setting consolidated=True, to raise an "
                    "error in this case instead of falling back to try "
                    "reading non-consolidated metadata.",
                    RuntimeWarning,
                    stacklevel=stacklevel,
                )
                zarr_group = zarr.open_group(store, **open_kwargs)
        elif consolidated:
            # TODO: an option to pass the metadata_key keyword
            zarr_group = zarr.open_consolidated(store, **open_kwargs)
        else:
            zarr_group = zarr.open_group(store, **open_kwargs)

        return cls(
            zarr_group,
            mode,
            consolidate_on_close,
            append_dim,
            write_region,
            safe_chunks,
        )

    def open_store_variable(self, name, zarr_array):
        try_nczarr = self._mode == "r"
        dimensions, attributes = zarr_backend._get_zarr_dims_and_attrs(
            zarr_array, zarr_backend.DIMENSION_KEY, try_nczarr
        )

        #### Changed from zarr array wrapper
        if name in dimensions:
            # we want indexed dimensions to be loaded eagerly
            # Right now we load in to device and then transfer to host
            # But these should be small-ish arrays
            # TODO: can we tell GDSStore to load as numpy array directly
            # not cupy array?
            array_wrapper = EagerCupyZarrArrayWrapper
        else:
            array_wrapper = CupyZarrArrayWrapper
        data = indexing.LazilyIndexedArray(array_wrapper(zarr_array))

        attributes = dict(attributes)
        encoding = {
            "chunks": zarr_array.chunks,
            "preferred_chunks": dict(zip(dimensions, zarr_array.chunks)),
            "compressor": zarr_array.compressor,
            "filters": zarr_array.filters,
        }
        # _FillValue needs to be in attributes, not encoding, so it will get
        # picked up by decode_cf
        if zarr_array.fill_value is not None:
            attributes["_FillValue"] = zarr_array.fill_value

        return Variable(dimensions, data, attributes, encoding)


class KvikioBackendEntrypoint(ZarrBackendEntrypoint):
    """
    Xarray backend to read Zarr stores using 'kvikio' engine.

    For more information about the underlying library, visit
    :doc:`kvikIO's Zarr page<kvikio:zarr>`.
    """

    available = has_kvikio
    description = "Open zarr files (.zarr) using Kvikio"
    url = "https://docs.rapids.ai/api/kvikio/stable/api/#zarr"

    # disabled by default
    # We need to provide this because of the subclassing from
    # ZarrBackendEntrypoint
    def guess_can_open(self, filename_or_obj):
        return False

    def open_dataset(
        self,
        filename_or_obj,
        mask_and_scale=True,
        decode_times=True,
        concat_characters=True,
        decode_coords=True,
        drop_variables=None,
        use_cftime=None,
        decode_timedelta=None,
        group=None,
        mode="r",
        synchronizer=None,
        consolidated=None,
        chunk_store=None,
        storage_options=None,
        stacklevel=3,
    ):
        filename_or_obj = _normalize_path(filename_or_obj)
        store = GDSZarrStore.open_group(
            filename_or_obj,
            group=group,
            mode=mode,
            synchronizer=synchronizer,
            consolidated=consolidated,
            consolidate_on_close=False,
            chunk_store=chunk_store,
            storage_options=storage_options,
            stacklevel=stacklevel + 1,
        )

        store_entrypoint = StoreBackendEntrypoint()
        with close_on_error(store):
            ds = store_entrypoint.open_dataset(
                store,
                mask_and_scale=mask_and_scale,
                decode_times=decode_times,
                concat_characters=concat_characters,
                decode_coords=decode_coords,
                drop_variables=drop_variables,
                use_cftime=use_cftime,
                decode_timedelta=decode_timedelta,
            )
        return ds
