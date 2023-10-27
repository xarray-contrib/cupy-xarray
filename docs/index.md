# CuPy-Xarray: Xarray on GPUs!

![GitHub Workflow CI Status](https://img.shields.io/github/actions/workflow/status/xarray-contrib/cupy-xarray/pypi-release.yaml?style=flat-square)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/xarray-contrib/cupy-xarray/main.svg?style=flat-square)](https://results.pre-commit.ci/latest/github/xarray-contrib/cupy-xarray/main)
[![Documentation Status](https://readthedocs.org/projects/cupy-xarray/badge/?version=latest&style=flat-square)](https://cupy-xarray.readthedocs.io)
[![license](https://img.shields.io/github/license/xarray-contrib/cupy-xarray.svg?style=flat-square)](https://github.com/xarray-contrib/cupy-xarray)

[![PyPI](https://img.shields.io/pypi/v/cupy-xarray.svg?style=flat-square)](https://pypi.org/project/cupy-xarray/)
[![Conda-forge](https://img.shields.io/conda/vn/conda-forge/cupy-xarray.svg?style=flat-square)](https://anaconda.org/conda-forge/cupy-xarray)

[![NASA-80NSSC22K0345](https://img.shields.io/badge/NASA-80NSSC22K0345-blue?style=flat-square)](https://science.nasa.gov/open-science-overview)

## Overview

CuPy-Xarray is a Python library that leverages [CuPy](https://cupy.dev/), a GPU array library, and [Xarray](https://docs.xarray.dev/en/stable/), a library for multi-dimensional labeled array computations, to enable fast and efficient data processing on GPUs. By combining the capabilities of CuPy and Xarray, CuPy-Xarray provides a convenient interface for performing accelerated computations and analysis on large multidimensional datasets.

## Installation

CuPy-Xarray can be installed using `pip` or `conda`:

From Conda Forge:

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

Large parts of this documentations comes from [SciPy 2023 Xarray on GPUs tutorial](https://negin513.github.io/cupy-xarray-tutorials/README.html) and [this NCAR tutorial to GPUs](https://github.com/NCAR/GPU_workshop/tree/workshop/13_CuPyAndLegate).

## Contents

```{eval-rst}

**User Guide**:

.. toctree::
   :maxdepth: 1
   :caption: User Guide

   source/cupy-basics
   source/introduction
   source/basic-computations
   source/high-level-api
   source/apply-ufunc
   source/real-example-1


**Tutorials & Presentations**:

.. toctree::
   :maxdepth: 1
   :caption: Tutorials & Presentations

   source/tutorials-and-presentations

**Contributing**:

.. toctree::
   :maxdepth: 1
   :caption: Contributing

   source/contributing


**API Reference**:

.. toctree::
   :maxdepth: 1
   :caption: API Reference

   api
```
