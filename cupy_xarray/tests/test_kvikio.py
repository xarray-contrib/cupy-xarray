import cupy as cp
import numpy as np
import pytest
import xarray as xr

kvikio = pytest.importorskip("kvikio")
zarr = pytest.importorskip("zarr")

import kvikio.zarr  # noqa
import xarray.core.indexing  # noqa
from xarray.core.indexing import ExplicitlyIndexedNDArrayMixin


@pytest.fixture
def store(tmp_path):
    ds = xr.Dataset(
        {
            "a": ("x", np.arange(10), {"foo": "bar"}),
            "scalar": np.array(1),
        },
        coords={"x": ("x", np.arange(-5, 5))},
    )

    for var in ds.variables:
        ds[var].encoding["compressor"] = None

    store_path = tmp_path / "kvikio.zarr"
    ds.to_zarr(store_path, consolidated=True)
    return store_path


def test_entrypoint():
    assert "kvikio" in xr.backends.list_engines()


@pytest.mark.parametrize("consolidated", [True, False])
def test_lazy_load(consolidated, store):
    with xr.open_dataset(store, engine="kvikio", consolidated=consolidated) as ds:
        for _, da in ds.data_vars.items():
            assert isinstance(da.variable._data, ExplicitlyIndexedNDArrayMixin)


@pytest.mark.parametrize("indexer", [slice(None), slice(2, 4), 2, [2, 3, 5]])
def test_lazy_indexing(indexer, store):
    with xr.open_dataset(store, engine="kvikio") as ds:
        ds = ds.isel(x=indexer)
        for _, da in ds.data_vars.items():
            assert isinstance(da.variable._data, ExplicitlyIndexedNDArrayMixin)

        loaded = ds.compute()
        for _, da in loaded.data_vars.items():
            if da.ndim == 0:
                continue
            assert isinstance(da.data, cp.ndarray)
