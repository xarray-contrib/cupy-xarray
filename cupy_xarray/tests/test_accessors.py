"""Tests for cupy-xarray accessors"""
import cupy as cp
import dask.array as da
import numpy as np
import pint_xarray  # noqa: F401 pylint:disable=unused-import
import pytest
import xarray as xr
from xarray.core.pycompat import DuckArrayModule
from xarray.tests import requires_cupy, requires_dask, requires_pint

import cupy_xarray  # noqa: F401 pylint:disable=unused-import

dask_array_type = DuckArrayModule("dask").type
pint_array_type = DuckArrayModule("pint").type
cupy_array_type = DuckArrayModule("cupy").type


@pytest.fixture
def dataarray_numpy():
    """Prepare numpy DataArray"""
    return xr.DataArray(
        np.random.rand(2, 3),
        attrs={"units": "candle"},
    )


@pytest.fixture
def dataarray_cupy():
    """Prepare cupy DataArray"""
    return xr.DataArray(
        cp.random.rand(2, 3),
        attrs={"units": "kelvin"},
    )


@pytest.fixture
def dataarray_dask():
    """Prepare dask DataArray"""
    return xr.DataArray(
        da.asarray(np.random.rand(2, 3)),
        attrs={"units": "mole"},
    )


@pytest.fixture
def dataarray_dask_cupy():
    """Prepare dask(cupy) DataArray"""
    return xr.DataArray(
        da.asarray(cp.random.rand(2, 3)),
        attrs={"units": "mole"},
    )


def to_pint(dataarray):
    """Convert DataArray data to pint"""
    return dataarray.pint.quantify()


@pytest.fixture
def dataarray_pint_numpy(dataarray_numpy):  # pylint:disable=redefined-outer-name
    """Prepare pint(numpy) DataArray"""
    return to_pint(dataarray_numpy)


@pytest.fixture
def dataarray_pint_cupy(dataarray_cupy):  # pylint:disable=redefined-outer-name
    """Prepare pint(cupy) DataArray"""
    return to_pint(dataarray_cupy)


@pytest.fixture
def dataarray_pint_dask(dataarray_dask):  # pylint:disable=redefined-outer-name
    """Prepare pint(dask) DataArray"""
    return to_pint(dataarray_dask)


@pytest.fixture
def dataarray_pint_dask_cupy(dataarray_dask_cupy):  # pylint:disable=redefined-outer-name
    """Prepare pint(dask(cupy)) DataArray"""
    return to_pint(dataarray_dask_cupy)


def to_dataset(dataarray):
    """Convert DataArray to Dataset"""
    return xr.Dataset(data_vars={"foo": dataarray})


@pytest.fixture
def dataset_numpy(dataarray_numpy):  # pylint:disable=redefined-outer-name
    """Prepare numpy Dataset"""
    return to_dataset(dataarray_numpy)


@pytest.fixture
def dataset_cupy(dataarray_cupy):  # pylint:disable=redefined-outer-name
    """Prepare cupy Dataset"""
    return to_dataset(dataarray_cupy)


@pytest.fixture
def dataset_dask(dataarray_dask):  # pylint:disable=redefined-outer-name
    """Prepare dask Dataset"""
    return to_dataset(dataarray_dask)


@pytest.fixture
def dataset_dask_cupy(dataarray_dask_cupy):  # pylint:disable=redefined-outer-name
    """Prepare dask(cupy) Dataset"""
    return to_dataset(dataarray_dask_cupy)


@pytest.fixture
def dataset_pint_numpy(dataarray_pint_numpy):  # pylint:disable=redefined-outer-name
    """Prepare pint(numpy) Dataset"""
    return to_dataset(dataarray_pint_numpy)


@pytest.fixture
def dataset_pint_cupy(dataarray_pint_cupy):  # pylint:disable=redefined-outer-name
    """Prepare pint(cupy) Dataset"""
    return to_dataset(dataarray_pint_cupy)


@pytest.fixture
def dataset_pint_dask(dataarray_pint_dask):  # pylint:disable=redefined-outer-name
    """Prepare pint(dask) Dataset"""
    return to_dataset(dataarray_pint_dask)


@pytest.fixture
def dataset_pint_dask_cupy(dataarray_pint_dask_cupy):  # pylint:disable=redefined-outer-name
    """Prepare pint(dask(cupy)) Dataset"""
    return to_dataset(dataarray_pint_dask_cupy)


@requires_pint
@requires_dask
@requires_cupy
def test_is_cupy(
    dataarray_numpy,  # pylint:disable=redefined-outer-name
    dataarray_cupy,  # pylint:disable=redefined-outer-name
    dataarray_dask,  # pylint:disable=redefined-outer-name
    dataarray_dask_cupy,  # pylint:disable=redefined-outer-name
    dataarray_pint_numpy,  # pylint:disable=redefined-outer-name
    dataarray_pint_cupy,  # pylint:disable=redefined-outer-name
    dataarray_pint_dask,  # pylint:disable=redefined-outer-name
    dataarray_pint_dask_cupy,  # pylint:disable=redefined-outer-name
    dataset_numpy,  # pylint:disable=redefined-outer-name
    dataset_cupy,  # pylint:disable=redefined-outer-name
    dataset_dask,  # pylint:disable=redefined-outer-name
    dataset_dask_cupy,  # pylint:disable=redefined-outer-name
    dataset_pint_numpy,  # pylint:disable=redefined-outer-name
    dataset_pint_cupy,  # pylint:disable=redefined-outer-name
    dataset_pint_dask,  # pylint:disable=redefined-outer-name
    dataset_pint_dask_cupy,  # pylint:disable=redefined-outer-name
):
    """Test is_cupy property in cupy xarray accessor"""
    # Test all dataarray types
    assert not dataarray_numpy.cupy.is_cupy
    assert dataarray_cupy.cupy.is_cupy
    assert not dataarray_dask.cupy.is_cupy
    assert dataarray_dask_cupy.cupy.is_cupy

    # Test all pinted dataarray types
    assert not dataarray_pint_numpy.cupy.is_cupy
    assert dataarray_pint_cupy.cupy.is_cupy
    assert not dataarray_pint_dask.cupy.is_cupy
    assert dataarray_pint_dask_cupy.cupy.is_cupy

    # Test all dataset types
    assert not dataset_numpy.cupy.is_cupy
    assert dataset_cupy.cupy.is_cupy
    assert not dataset_dask.cupy.is_cupy
    assert dataset_dask_cupy.cupy.is_cupy

    # Test all pinted dataset types
    assert not dataset_pint_numpy.cupy.is_cupy
    assert dataset_pint_cupy.cupy.is_cupy
    assert not dataset_pint_dask.cupy.is_cupy
    assert dataset_pint_dask_cupy.cupy.is_cupy


@requires_pint
@requires_dask
@requires_cupy
def test_as_cupy(
    dataarray_numpy,  # pylint:disable=redefined-outer-name
    dataarray_cupy,  # pylint:disable=redefined-outer-name
    dataarray_dask,  # pylint:disable=redefined-outer-name
    dataarray_dask_cupy,  # pylint:disable=redefined-outer-name
    dataarray_pint_numpy,  # pylint:disable=redefined-outer-name
    dataarray_pint_cupy,  # pylint:disable=redefined-outer-name
    dataarray_pint_dask,  # pylint:disable=redefined-outer-name
    dataarray_pint_dask_cupy,  # pylint:disable=redefined-outer-name
    dataset_numpy,  # pylint:disable=redefined-outer-name
    dataset_cupy,  # pylint:disable=redefined-outer-name
    dataset_dask,  # pylint:disable=redefined-outer-name
    dataset_dask_cupy,  # pylint:disable=redefined-outer-name
    dataset_pint_numpy,  # pylint:disable=redefined-outer-name
    dataset_pint_cupy,  # pylint:disable=redefined-outer-name
    dataset_pint_dask,  # pylint:disable=redefined-outer-name
    dataset_pint_dask_cupy,  # pylint:disable=redefined-outer-name
):
    """Test as_cupy() method in cupy xarray accessor"""
    # Apply cupy.as_cupy() to all dataarray types
    dataarray_numpy_as_cupy = dataarray_numpy.cupy.as_cupy()
    dataarray_cupy_as_cupy = dataarray_cupy.cupy.as_cupy()
    dataarray_dask_as_cupy = dataarray_dask.cupy.as_cupy()
    dataarray_dask_cupy_as_cupy = dataarray_dask_cupy.cupy.as_cupy()
    dataarray_pint_numpy_as_cupy = dataarray_pint_numpy.cupy.as_cupy()
    dataarray_pint_cupy_as_cupy = dataarray_pint_cupy.cupy.as_cupy()
    dataarray_pint_dask_as_cupy = dataarray_pint_dask.cupy.as_cupy()
    dataarray_pint_dask_cupy_as_cupy = dataarray_pint_dask_cupy.cupy.as_cupy()
    dataset_numpy_as_cupy = dataset_numpy.cupy.as_cupy()
    dataset_cupy_as_cupy = dataset_cupy.cupy.as_cupy()
    dataset_dask_as_cupy = dataset_dask.cupy.as_cupy()
    dataset_dask_cupy_as_cupy = dataset_dask_cupy.cupy.as_cupy()
    dataset_pint_numpy_as_cupy = dataset_pint_numpy.cupy.as_cupy()
    dataset_pint_cupy_as_cupy = dataset_pint_cupy.cupy.as_cupy()
    dataset_pint_dask_as_cupy = dataset_pint_dask.cupy.as_cupy()
    dataset_pint_dask_cupy_as_cupy = dataset_pint_dask_cupy.cupy.as_cupy()

    # Test that all types are cupy-based
    assert dataarray_numpy_as_cupy.cupy.is_cupy
    assert dataarray_cupy_as_cupy.cupy.is_cupy
    assert dataarray_dask_as_cupy.cupy.is_cupy
    assert dataarray_dask_cupy_as_cupy.cupy.is_cupy
    assert dataarray_pint_numpy_as_cupy.cupy.is_cupy
    assert dataarray_pint_cupy_as_cupy.cupy.is_cupy
    assert dataarray_pint_dask_as_cupy.cupy.is_cupy
    assert dataarray_pint_dask_cupy_as_cupy.cupy.is_cupy
    assert dataset_numpy_as_cupy.cupy.is_cupy
    assert dataset_cupy_as_cupy.cupy.is_cupy
    assert dataset_dask_as_cupy.cupy.is_cupy
    assert dataset_dask_cupy_as_cupy.cupy.is_cupy
    assert dataset_pint_numpy_as_cupy.cupy.is_cupy
    assert dataset_pint_cupy_as_cupy.cupy.is_cupy
    assert dataset_pint_dask_as_cupy.cupy.is_cupy
    assert dataset_pint_dask_cupy_as_cupy.cupy.is_cupy

    # Check that we keep the original data type (except pure numpy)
    assert isinstance(dataarray_numpy_as_cupy.data, cupy_array_type)
    assert isinstance(dataarray_cupy_as_cupy.data, cupy_array_type)
    assert isinstance(dataarray_dask_as_cupy.data, dask_array_type)
    assert isinstance(dataarray_dask_cupy_as_cupy.data, dask_array_type)
    assert isinstance(dataarray_pint_numpy_as_cupy.data, pint_array_type)
    assert isinstance(dataarray_pint_cupy_as_cupy.data, pint_array_type)
    assert isinstance(dataarray_pint_dask_as_cupy.data, pint_array_type)
    assert isinstance(dataarray_pint_dask_cupy_as_cupy.data, pint_array_type)
    assert isinstance(dataset_numpy_as_cupy["foo"].data, cupy_array_type)
    assert isinstance(dataset_cupy_as_cupy["foo"].data, cupy_array_type)
    assert isinstance(dataset_dask_as_cupy["foo"].data, dask_array_type)
    assert isinstance(dataset_dask_cupy_as_cupy["foo"].data, dask_array_type)
    assert isinstance(dataset_pint_numpy_as_cupy["foo"].data, pint_array_type)
    assert isinstance(dataset_pint_cupy_as_cupy["foo"].data, pint_array_type)
    assert isinstance(dataset_pint_dask_as_cupy["foo"].data, pint_array_type)
    assert isinstance(dataset_pint_dask_cupy_as_cupy["foo"].data, pint_array_type)


@requires_pint
@requires_dask
@requires_cupy
def test_as_numpy(
    dataarray_numpy,  # pylint:disable=redefined-outer-name
    dataarray_cupy,  # pylint:disable=redefined-outer-name
    dataarray_dask,  # pylint:disable=redefined-outer-name
    dataarray_dask_cupy,  # pylint:disable=redefined-outer-name
    dataarray_pint_numpy,  # pylint:disable=redefined-outer-name
    dataarray_pint_cupy,  # pylint:disable=redefined-outer-name
    dataarray_pint_dask,  # pylint:disable=redefined-outer-name
    dataarray_pint_dask_cupy,  # pylint:disable=redefined-outer-name
    dataset_numpy,  # pylint:disable=redefined-outer-name
    dataset_cupy,  # pylint:disable=redefined-outer-name
    dataset_dask,  # pylint:disable=redefined-outer-name
    dataset_dask_cupy,  # pylint:disable=redefined-outer-name
    dataset_pint_numpy,  # pylint:disable=redefined-outer-name
    dataset_pint_cupy,  # pylint:disable=redefined-outer-name
    dataset_pint_dask,  # pylint:disable=redefined-outer-name
    dataset_pint_dask_cupy,  # pylint:disable=redefined-outer-name
):
    """Test as_numpy() method in cupy xarray accessor"""
    # Apply cupy.as_numpy() to all dataarray types
    dataarray_numpy_as_numpy = dataarray_numpy.cupy.as_numpy()
    dataarray_cupy_as_numpy = dataarray_cupy.cupy.as_numpy()
    dataarray_dask_as_numpy = dataarray_dask.cupy.as_numpy()
    dataarray_dask_cupy_as_numpy = dataarray_dask_cupy.cupy.as_numpy()
    dataarray_pint_numpy_as_numpy = dataarray_pint_numpy.cupy.as_numpy()
    dataarray_pint_cupy_as_numpy = dataarray_pint_cupy.cupy.as_numpy()
    dataarray_pint_dask_as_numpy = dataarray_pint_dask.cupy.as_numpy()
    dataarray_pint_dask_cupy_as_numpy = dataarray_pint_dask_cupy.cupy.as_numpy()
    dataset_numpy_as_numpy = dataset_numpy.cupy.as_numpy()
    dataset_cupy_as_numpy = dataset_cupy.cupy.as_numpy()
    dataset_dask_as_numpy = dataset_dask.cupy.as_numpy()
    dataset_dask_cupy_as_numpy = dataset_dask_cupy.cupy.as_numpy()
    dataset_pint_numpy_as_numpy = dataset_pint_numpy.cupy.as_numpy()
    dataset_pint_cupy_as_numpy = dataset_pint_cupy.cupy.as_numpy()
    dataset_pint_dask_as_numpy = dataset_pint_dask.cupy.as_numpy()
    dataset_pint_dask_cupy_as_numpy = dataset_pint_dask_cupy.cupy.as_numpy()

    # Test that all types are not cupy-based
    assert not dataarray_numpy_as_numpy.cupy.is_cupy
    assert not dataarray_cupy_as_numpy.cupy.is_cupy
    assert not dataarray_dask_as_numpy.cupy.is_cupy
    assert not dataarray_dask_cupy_as_numpy.cupy.is_cupy
    assert not dataarray_pint_numpy_as_numpy.cupy.is_cupy
    assert not dataarray_pint_cupy_as_numpy.cupy.is_cupy
    assert not dataarray_pint_dask_as_numpy.cupy.is_cupy
    assert not dataarray_pint_dask_cupy_as_numpy.cupy.is_cupy
    assert not dataset_numpy_as_numpy.cupy.is_cupy
    assert not dataset_cupy_as_numpy.cupy.is_cupy
    assert not dataset_dask_as_numpy.cupy.is_cupy
    assert not dataset_dask_cupy_as_numpy.cupy.is_cupy
    assert not dataset_pint_numpy_as_numpy.cupy.is_cupy
    assert not dataset_pint_cupy_as_numpy.cupy.is_cupy
    assert not dataset_pint_dask_as_numpy.cupy.is_cupy
    assert not dataset_pint_dask_cupy_as_numpy.cupy.is_cupy

    # Check that we keep the original data type (except pure numpy)
    assert isinstance(dataarray_numpy_as_numpy.data, np.ndarray)
    assert isinstance(dataarray_cupy_as_numpy.data, np.ndarray)
    assert isinstance(dataarray_dask_as_numpy.data, dask_array_type)
    assert isinstance(dataarray_dask_cupy_as_numpy.data, dask_array_type)
    assert isinstance(dataarray_pint_numpy_as_numpy.data, pint_array_type)
    assert isinstance(dataarray_pint_cupy_as_numpy.data, pint_array_type)
    assert isinstance(dataarray_pint_dask_as_numpy.data, pint_array_type)
    assert isinstance(dataarray_pint_dask_cupy_as_numpy.data, pint_array_type)
    assert isinstance(dataset_numpy_as_numpy["foo"].data, np.ndarray)
    assert isinstance(dataset_cupy_as_numpy["foo"].data, np.ndarray)
    assert isinstance(dataset_dask_as_numpy["foo"].data, dask_array_type)
    assert isinstance(dataset_dask_cupy_as_numpy["foo"].data, dask_array_type)
    assert isinstance(dataset_pint_numpy_as_numpy["foo"].data, pint_array_type)
    assert isinstance(dataset_pint_cupy_as_numpy["foo"].data, pint_array_type)
    assert isinstance(dataset_pint_dask_as_numpy["foo"].data, pint_array_type)
    assert isinstance(dataset_pint_dask_cupy_as_numpy["foo"].data, pint_array_type)
