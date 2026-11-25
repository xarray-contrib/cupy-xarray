"""
`rumi` backend for xarray to read rumi files directly into CuPy arrays in GPU memory.
"""

import os
from collections.abc import Iterable

import cupy as cp
import numpy as np
import pandas as pd
import rasterix
import rumi
import xarray as xr
from affine import Affine
from xarray.backends import BackendEntrypoint


# %%
class RumiBackendEntrypoint(BackendEntrypoint):
    """
    Xarray backend to read rumi files using 'rumi' engine.

    When using :py:func:`xarray.open_dataarray` with ``engine="rumi"``, the optional
    ``device_id`` parameter can be set to the CUDA GPU id to do the decoding on.

    """

    description = "Use .rumi files in Xarray"
    open_dataset_parameters = (
        "filename_or_obj",
        "header",
        "drop_variables",
        "device_id",
    )
    url = "https://asterisk.coop/rumi/api-python.html"

    def open_dataset(
        self,
        filename_or_obj: str,
        header: bytes | bytearray | memoryview[int],
        *,
        drop_variables: str | Iterable[str] | None = None,
        device_id: int | None = None,
        # other backend specific keyword arguments
        # `chunks` and `cache` DO NOT go here, they are handled by xarray
        mask_and_scale=None,
    ) -> xr.Dataset:
        """
        Backend open_dataset method used by Xarray in :py:func:`xarray.open_dataset`.

        Parameters
        ----------
        filename_or_obj : str
            File path or url to a rumi (.rumi) image file that can be read by rumi.
        header : bytes | bytearray | memoryview[int]
            Rumi external header loaded as a byte stream.
        device_id : int | None
            CUDA device ID on which to place the created cupy array. Default is None,
            which means device_id will be inferred via
            :py:func:`cupy.cuda.runtime.getDevice`.

        Returns
        -------
        xarray.Dataset

        """
        if device_id is None:
            device_id: int = cp.cuda.runtime.getDevice()

        with cp.cuda.Stream(ptds=True):  # using default stream segfaults
            dlpack = rumi.read(
                source=filename_or_obj,
                header=header,
                pattern=None,  # default is (T, B, Y, X)
                framework="dlpack",
                device=f"cuda:{device_id}",
                decode_backend="auto",
            )
            array: cp.ndarray = cp.from_dlpack(dlpack)

        info = rumi.info(source=filename_or_obj, header=header)
        # Band/Channel coordinates
        match array.ndim:
            case 3:
                bands, height, width = array.shape
                bc_coords = {"band": np.arange(bands, dtype=np.uint8)}
            case 4:
                time, bands, height, width = array.shape
                bc_coords = {
                    "time": pd.Series(info.time),
                    "band": np.arange(bands, dtype=np.uint8),
                }
        # Height/Width coordinates
        try:
            affine = Affine(*info.transform)
            index = rasterix.RasterIndex.from_transform(
                affine=affine, width=width, height=height, crs=info.crs
            )
            xy_coords = xr.Coordinates.from_xindex(index=index)
        except TypeError:  # missing Affine transform
            xy_coords = {"y": np.arange(height), "x": np.arange(width)}

        dataarray: xr.DataArray = xr.DataArray(
            data=array,
            coords=xr.Coordinates(coords={**bc_coords, **xy_coords}),
            name=None,
            attrs=None,
        )
        return dataarray.to_dataset(name="raster")

    def guess_can_open(self, filename_or_obj):
        try:
            _, ext = os.path.splitext(filename_or_obj)
        except TypeError:
            return False
        return ext in {".rumi"}
