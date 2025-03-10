"""
:doc:`kvikIO <kvikio:index>` backend for xarray to read Zarr stores directly into CuPy
arrays in GPU memory.
"""

import os
import warnings

import cupy as cp
from xarray.backends.common import _normalize_path  # TODO: can this be public
from xarray.backends.store import StoreBackendEntrypoint
from xarray.backends.zarr import ZarrBackendEntrypoint, ZarrStore
from xarray.core.utils import close_on_error  # TODO: can this be public.

try:
    import kvikio.zarr
    import zarr

    has_kvikio = True
except ImportError:
    has_kvikio = False


#  TODO: minimum kvikio version for supporting consolidated
#  TODO: minimum xarray version for ZarrArrayWrapper._array 2023.10.0?


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

        open_kwargs = {
            "mode": mode,
            "synchronizer": synchronizer,
            "path": group,
            ########## NEW STUFF
            "meta_array": cp.empty(()),
        }
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
