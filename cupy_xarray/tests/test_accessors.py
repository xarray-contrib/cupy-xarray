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
    assert hasattr(tutorial_ds_air, "cupy")

def test_data_array_accessor(tutorial_da_air):
    assert hasattr(tutorial_da_air, "cupy")
