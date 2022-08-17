# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

# import cupy_xarray
import sphinx_autosummary_accessors

project = "cupy-xarray"
copyright = "2022, cupy-xarray developers"
author = "cupy-xarray developers"
release = "v0.1"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    # "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    # "sphinx.ext.autosummary",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.extlinks",
    "numpydoc",
    # "sphinx_autosummary_accessors",
    "IPython.sphinxext.ipython_directive",
    "myst_nb",
    "sphinx_copybutton",
]


extlinks = {
    "issue": ("https://github.com/xarray-contrib/cupy-xarray/issues/%s", "GH#"),
    "pr": ("https://github.com/xarray-contrib/cupy-xarray/pull/%s", "GH#"),
}

templates_path = ["_templates", sphinx_autosummary_accessors.templates_path]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "api.rst"]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_static_path = ["_static"]


# Myst_nb options
nb_execution_mode = "off"

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "dask": ("https://docs.dask.org/en/latest", None),
    "cupy": ("https://docs.cupy.dev/en/latest", None),
    "xarray": ("http://docs.xarray.dev/en/latest/", None),
}
