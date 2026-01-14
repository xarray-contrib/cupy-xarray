"""
:doc:`kvikIO <kvikio:index>` backend for xarray to read Zarr stores directly into CuPy
arrays in GPU memory.
"""

import functools

from xarray.backends.common import _normalize_path  # TODO: can this be public
from xarray.backends.store import StoreBackendEntrypoint
from xarray.backends.zarr import ZarrBackendEntrypoint, ZarrStore
from xarray.core.dataset import Dataset
from xarray.core.utils import close_on_error  # TODO: can this be public.

try:
    import kvikio.zarr
    import zarr

    has_kvikio = True
except ImportError:
    has_kvikio = False


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
        zarr_version=None,
        zarr_format=None,
        store=None,
        engine=None,
        use_zarr_fill_value_as_mask=None,
        cache_members: bool = True,
    ) -> Dataset:
        filename_or_obj = _normalize_path(filename_or_obj)
        if not store:
            with zarr.config.enable_gpu():
                _store = kvikio.zarr.GDSStore(root=filename_or_obj)

                # Override default buffer prototype to be GPU buffer
                # buffer_prototype = zarr.core.buffer.core.default_buffer_prototype()
                buffer_prototype = zarr.core.buffer.gpu.buffer_prototype
                _store.get = functools.partial(_store.get, prototype=buffer_prototype)
                _store.get_partial_values = functools.partial(
                    _store.get_partial_values, prototype=buffer_prototype
                )

                store = ZarrStore.open_group(
                    store=_store,
                    group=group,
                    mode=mode,
                    synchronizer=synchronizer,
                    consolidated=consolidated,
                    consolidate_on_close=False,
                    chunk_store=chunk_store,
                    storage_options=storage_options,
                    zarr_version=zarr_version,
                    use_zarr_fill_value_as_mask=None,
                    zarr_format=zarr_format,
                    cache_members=cache_members,
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
