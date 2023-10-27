"""Tests for cupy-xarray accessors"""
import cupy as cp
import numpy as np
import pytest
import xarray as xr
from xarray.tests import requires_dask, requires_pint

import cupy_xarray  # noqa: F401 pylint:disable=unused-import

da = xr.DataArray(np.random.rand(2, 3), attrs={"units": "candle"})
ds = xr.Dataset({"a": da})


@pytest.mark.parametrize("obj", [da, ds])
def test_numpy(obj):
    """Test is_cupy property in cupy xarray accessor"""

    assert not da.cupy.is_cupy
    cpda = da.cupy.as_cupy()
    assert cpda.is_cupy

    as_numpy = cpda.as_numpy()
    assert not cpda.cupy.is_cupy
    if isinstance(as_numpy, xr.DataArray):
        assert isinstance(as_numpy.data, np.ndarray)


@requires_dask
@pytest.mark.parametrize("obj", [da, ds])
def test_dask(obj):
    """Test is_cupy property in cupy xarray accessor"""
    as_dask = obj.chunk()
    assert not as_dask.cupy.is_cupy
    cpda = as_dask.cupy.as_cupy()
    assert cpda.cupy.is_cupy

    if isinstance(cpda, xr.DataArray):
        assert isinstance(cpda.data._meta, cp.ndarray)


@requires_pint
@pytest.mark.parametrize("obj", [da, ds])
def test_pint(obj):
    import pint_xarray  # noqa

    as_pint = obj.pint.quantify()

    assert not as_pint.cupy.is_cupy
    cpda = as_pint.cupy.as_cup()
    assert cpda.cupy.is_cupy

    as_dask = as_pint.chunk()
    assert not as_dask.cupy.is_cupy
    cpda = as_dask.cupy.as_cupy()
    assert cpda.cupy.is_cupy
    if isinstance(cpda, xr.DataArray):
        assert isinstance(cpda.data._meta, cp.ndarray)
