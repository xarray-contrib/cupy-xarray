# cupy-xarray

> ⚠️ This project is looking for maintainers and contributors. Come help out!

[![GitHub Workflow CI Status](https://img.shields.io/github/workflow/status/xarray-contrib/cupy-xarray/CI?logo=github&style=flat)](https://github.com/xarray-contrib/cupy-xarray/actions)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/xarray-contrib/cupy-xarray/main.svg)](https://results.pre-commit.ci/latest/github/xarray-contrib/cupy-xarray/main)
[![Documentation Status](https://readthedocs.org/projects/cupy-xarray/badge/?version=latest)](https://cupy-xarray.readthedocs.io/en/latest/?badge=latest)

[![PyPI](https://img.shields.io/pypi/v/cupy-xarray.svg?style=flat)](https://pypi.org/project/cupy-xarray/)
[![Conda-forge](https://img.shields.io/conda/vn/conda-forge/cupy-xarray.svg?style=flat)](https://anaconda.org/conda-forge/cupy-xarray)

[![NASA-80NSSC22K0345](https://img.shields.io/badge/NASA-80NSSC22K0345-blue)](https://science.nasa.gov/open-science-overview)

Interface for using cupy in xarray, providing convenience accessors.

## Installation

From anaconda:

```console
conda install cupy-xarray -c conda-forge
```

From PyPI:

```console
pip install cupy-xarray
```

The latest version from Github:

```console
pip install git+https://github.com/xarray-contrib/cupy-xarray.git
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
