# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

# import cupy_xarray
import sphinx_autosummary_accessors

project = "cupy-xarray"
copyright = "2023, cupy-xarray developers"
author = "cupy-xarray developers"
release = "v0.1"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    # "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.autosummary",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.extlinks",
    "numpydoc",
    # "sphinx_autosummary_accessors",
    "IPython.sphinxext.ipython_directive",
    "sphinx.ext.napoleon",
    "myst_nb",
    # "nbsphinx",
    "sphinx_copybutton",
    "sphinx_design",
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

autosummary_generate = True
autodoc_typehints = "none"

# Napoleon configurations
napoleon_google_docstring = False
napoleon_numpy_docstring = True
napoleon_use_param = False
napoleon_use_rtype = False
napoleon_preprocess_types = True
napoleon_type_aliases = {
    # general terms
    "sequence": ":term:`sequence`",
    "iterable": ":term:`iterable`",
    "callable": ":py:func:`callable`",
    "dict_like": ":term:`dict-like <mapping>`",
    "dict-like": ":term:`dict-like <mapping>`",
    "path-like": ":term:`path-like <path-like object>`",
    "mapping": ":term:`mapping`",
    "file-like": ":term:`file-like <file-like object>`",
    # special terms
    # "same type as caller": "*same type as caller*",  # does not work, yet
    # "same type as values": "*same type as values*",  # does not work, yet
    # stdlib type aliases
    "MutableMapping": "~collections.abc.MutableMapping",
    "sys.stdout": ":obj:`sys.stdout`",
    "timedelta": "~datetime.timedelta",
    "string": ":class:`string <str>`",
    # numpy terms
    "array_like": ":term:`array_like`",
    "array-like": ":term:`array-like <array_like>`",
    "scalar": ":term:`scalar`",
    "array": ":term:`array`",
    "hashable": ":term:`hashable <name>`",
    # matplotlib terms
    "color-like": ":py:func:`color-like <matplotlib.colors.is_color_like>`",
    "matplotlib colormap name": ":doc:`matplotlib colormap name <matplotlib:gallery/color/colormap_reference>`",
    "matplotlib axes object": ":py:class:`matplotlib axes object <matplotlib.axes.Axes>`",
    "colormap": ":py:class:`colormap <matplotlib.colors.Colormap>`",
    # objects without namespace: xarray
    "DataArray": "~xarray.DataArray",
    "Dataset": "~xarray.Dataset",
    "Variable": "~xarray.Variable",
    "DatasetGroupBy": "~xarray.core.groupby.DatasetGroupBy",
    "DataArrayGroupBy": "~xarray.core.groupby.DataArrayGroupBy",
    # objects without namespace: numpy
    "ndarray": "~numpy.ndarray",
    "DaskArray": "~dask.array.Array",
    "MaskedArray": "~numpy.ma.MaskedArray",
    "dtype": "~numpy.dtype",
    "ComplexWarning": "~numpy.ComplexWarning",
    # objects without namespace: pandas
    "Index": "~pandas.Index",
    "MultiIndex": "~pandas.MultiIndex",
    "CategoricalIndex": "~pandas.CategoricalIndex",
    "TimedeltaIndex": "~pandas.TimedeltaIndex",
    "DatetimeIndex": "~pandas.DatetimeIndex",
    "Series": "~pandas.Series",
    "DataFrame": "~pandas.DataFrame",
    "Categorical": "~pandas.Categorical",
    "Path": "~~pathlib.Path",
    # objects with abbreviated namespace (from pandas)
    "pd.Index": "~pandas.Index",
    "pd.NaT": "~pandas.NaT",
}
