"""
`cog3pio` backend for xarray to read TIFF files directly into CuPy arrays in GPU memory.
"""

import os
from collections.abc import Iterable

import cupy as cp  # type: ignore[import-untyped]
import numpy as np
import xarray as xr
from cog3pio import CudaCogReader
from xarray.backends import BackendEntrypoint


# %%
class Cog3pioBackendEntrypoint(BackendEntrypoint):
    """
    Xarray backend to read GeoTIFF files using 'cog3pio' engine.

    When using :py:func:`xarray.open_dataarray` with ``engine="cog3pio"``, the
    ``device_id`` parameter can be set to the CUDA GPU id to do the decoding on.

    Examples
    --------
    Read a GeoTIFF from a HTTP url into an [xarray.DataArray][]:

    >>> import xarray as xr
    >>> # Read GeoTIFF into an xarray.DataArray
    >>> dataarray: xr.DataArray = xr.open_dataarray(
    ...     filename_or_obj="https://github.com/OSGeo/gdal/raw/v3.11.0/autotest/gcore/data/byte_zstd.tif",
    ...     engine="cog3pio",
    ...     device_id=0,  # cuda:0
    ... )
    >>> dataarray.sizes
    Frozen({'band': 1, 'y': 20, 'x': 20})
    >>> dataarray.dtype
    dtype('uint8')

    """

    description = "Use .tif files in Xarray"
    open_dataset_parameters = ("filename_or_obj", "drop_variables", "device_id")
    url = "https://github.com/weiji14/cog3pio"

    def open_dataset(  # type: ignore[override]
        self,
        filename_or_obj: str,
        *,
        drop_variables: str | Iterable[str] | None = None,
        device_id: int,
        # other backend specific keyword arguments
        # `chunks` and `cache` DO NOT go here, they are handled by xarray
        mask_and_scale=None,
    ) -> xr.Dataset:
        """
        Backend open_dataset method used by Xarray in [xarray.open_dataset][].

        Parameters
        ----------
        filename_or_obj : str
            File path or url to a TIFF (.tif) image file that can be read by the
            nvTIFF or image-tiff backend library.
        device_id : int
            CUDA device ID on which to place the created cupy array.

        Returns
        -------
        xarray.Dataset

        """

        with cp.cuda.Stream(ptds=True):
            cog = CudaCogReader(path=filename_or_obj, device_id=device_id)
            array_: cp.ndarray = cp.from_dlpack(cog)  # 1-D Array
            x_coords, y_coords = cog.xy_coords()  # TODO consider using rasterix
            height, width = (len(y_coords), len(x_coords))
            channels: int = len(array_) // (height * width)
            # TODO make API to get proper 3-D shape directly, or use cuTENSOR
            array_ = array_.reshape(height, width, channels)  # HWC
            array = array_.transpose(2, 0, 1)  # CHW

        dataarray: xr.DataArray = xr.DataArray(
            data=array,
            coords={
                "band": np.arange(channels, dtype=np.uint8),
                "y": y_coords,
                "x": x_coords,
            },
            name=None,
            attrs=None,
        )

        return dataarray.to_dataset(name="raster")

    def guess_can_open(self, filename_or_obj):
        try:
            _, ext = os.path.splitext(filename_or_obj)
        except TypeError:
            return False
        return ext in {".tif", ".tiff"}
