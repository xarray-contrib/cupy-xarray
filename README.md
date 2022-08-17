# cupy-xarray

> ⚠️ This project is looking for maintainers and contributors. Come help out!

Interface for using cupy in xarray, providing convenience accessors.

## Installation

```console
$ pip install git+https://github.com/xarray-contrib/cupy-xarray.git
```

## Usage

```python
import xarray as xr
import cupy_xarray  # This registers the `DataSet.cupy` and `DataArray.cupy` namespaces but is not used directly

ds = xr.tutorial.load_dataset("air_temperature.nc")
type(ds.air.data)  # numpy.ndarray

%timeit ds.air.mean()  # 8.56 ms ± 15.6 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)

ds = ds.cupy.as_cupy()  # Also available via convenience method ds.as_cupy()
type(ds.air.data)  # cupy.core.core.ndarray

%timeit ds.air.mean()  # 2.14 ms ± 21.4 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)

ds = ds.as_numpy()
type(ds.air.data)  # numpy.ndarray
```
