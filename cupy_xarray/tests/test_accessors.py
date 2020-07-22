import pytest

import xarray as xr
import cupy as cp
import cupy_xarray


@pytest.fixture
def tutorial_ds_air():
    return xr.tutorial.load_dataset("air_temperature")


@pytest.fixture
def tutorial_da_air(tutorial_ds_air):
    return tutorial_ds_air.air


def test_data_set_accessor(tutorial_ds_air):
    ds = tutorial_ds_air
    assert hasattr(ds, "cupy")
    assert not ds.cupy.is_cupy

    ds = ds.as_cupy()
    assert ds.cupy.is_cupy

    ds = ds.cupy.as_numpy()
    assert not ds.cupy.is_cupy


def test_data_array_accessor(tutorial_da_air):
    da = tutorial_da_air
    assert hasattr(da, "cupy")
    assert not da.cupy.is_cupy

    da = da.as_cupy()
    assert da.cupy.is_cupy

    da = da.cupy.as_numpy()
    assert not da.cupy.is_cupy
