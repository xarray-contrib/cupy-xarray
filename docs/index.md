# CuPy-Xarray: Xarray on GPUs!

![GitHub Workflow CI Status](https://img.shields.io/github/actions/workflow/status/xarray-contrib/cupy-xarray/pypi-release.yaml?style=flat-square)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/xarray-contrib/cupy-xarray/main.svg)](https://results.pre-commit.ci/latest/github/xarray-contrib/cupy-xarray/main)
[![Documentation Status](https://readthedocs.org/projects/cupy-xarray/badge/?version=latest)](https://cupy-xarray.readthedocs.io/en/latest/?badge=latest)

[![PyPI](https://img.shields.io/pypi/v/cupy-xarray.svg?style=flat)](https://pypi.org/project/cupy-xarray/)
[![Conda-forge](https://img.shields.io/conda/vn/conda-forge/cupy-xarray.svg?style=flat)](https://anaconda.org/conda-forge/cupy-xarray)

[![NASA-80NSSC22K0345](https://img.shields.io/badge/NASA-80NSSC22K0345-blue)](https://science.nasa.gov/open-science-overview)



## Overview

CuPy-Xarray is a Python library that leverages CuPy, a GPU array library, and Xarray, a library for multi-dimensional labeled array computations, to enable fast and efficient data processing on GPUs. By combining the capabilities of CuPy and Xarray, CuPy-Xarray provides a convenient interface for performing accelerated computations and analysis on large multidimensional datasets.

## Installation

CuPy-Xarray can be installed using `pip` or `conda`:

From anaconda:
```bash

conda install cupy-xarray -c conda-forge
```

From PyPI:
```bash
pip install cupy-xarray
```

The latest version from Github:
```bash 
pip install git+https://github.com/xarray-contrib/cupy-xarray.git
```

## Acknowledgements
 Large parts of this documentations comes from [SciPy 2023 Xarray on GPUs tutorial](https://negin513.github.io/cupy-xarray-tutorials/README.html). The original notebook also adapts from the content in [this NCAR tutorial to GPUs](https://github.com/NCAR/GPU_workshop/tree/workshop/13_CuPyAndLegate), and uses it to illustrate cupy-xarray and working with cupy arrays and Xarray objects in general.

## Contents

```{eval-rst}

**User Guide**:

.. toctree::
   :maxdepth: 1
   :caption: User Guide

   source/Notebook0_Introduction
   source/Notebook1_Xarray_Cupy
   source/Notebook2_Xarray_Cupy_BasicOperations
   source/Notebook3_Xarray_Cupy_HighLevel
   source/Notebook4_Xarray_Cupy_ApplyUfunc
   
**Demo**:

.. toctree::
   :maxdepth: 1
   :caption: Demo

   source/Notebook5_Xarray_Cupy_Example

**Contributing**:

.. toctree::
   :maxdepth: 1
   :caption: Contributing

   source/contributing

**API Reference**:

.. toctree::

   :maxdepth: 1
   :caption: API Reference
   source/api

```