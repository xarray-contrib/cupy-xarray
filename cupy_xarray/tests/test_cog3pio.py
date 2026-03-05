"""
Tests for xarray 'cog3pio' backend engine.
"""

import cupy as cp
import pytest
import xarray as xr

from cupy_xarray.cog3pio import Cog3pioBackendEntrypoint

cog3pio = pytest.importorskip("cog3pio")


def test_entrypoint():
    assert "cog3pio" in xr.backends.list_engines()


def test_xarray_backend_open_dataarray():
    """
    Ensure that passing engine='cog3pio' to xarray.open_dataarray works to read a
    Cloud-optimized GeoTIFF from a http url.
    """
    with xr.open_dataarray(
        filename_or_obj="https://github.com/developmentseed/titiler/raw/1.2.0/src/titiler/mosaic/tests/fixtures/TCI.tif",
        engine=Cog3pioBackendEntrypoint,
        device_id=0,
    ) as da:
        assert isinstance(da.data, cp.ndarray)
        assert da.sizes == {"band": 3, "y": 1098, "x": 1098}
        assert da.x.min() == 700010.0
        assert da.x.max() == 809710.0
        assert da.y.min() == 3490250.0
        assert da.y.max() == 3599950.0
        assert da.dtype == "uint8"
