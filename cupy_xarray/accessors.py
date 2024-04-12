import cupy as cp
from xarray import Dataset, register_dataarray_accessor, register_dataset_accessor
from xarray.core.pycompat import DuckArrayModule

dask_array_type = DuckArrayModule("dask").type
pint_array_type = DuckArrayModule("pint").type


def _get_datatype(data):
    if isinstance(data, dask_array_type):
        return isinstance(data._meta, cp.ndarray)
    elif isinstance(data, pint_array_type):
        return _get_datatype(data.magnitude)
    return isinstance(data, cp.ndarray)


@register_dataarray_accessor("cupy")
class CupyDataArrayAccessor:
    """
    Access methods for DataArrays using Cupy.
    Methods and attributes can be accessed through the `.cupy` attribute.
    """

    def __init__(self, da):
        self.da = da

    @property
    def is_cupy(self) -> bool:
        """True if the underlying data is a cupy array."""
        return _get_datatype(self.da.data)

    def as_cupy(self):
        """
        Converts the DataArray's underlying array type to cupy.

        For DataArrays which are initially backed by numpy the data
        will be immediately cast to cupy and moved to the GPU. In the case
        that the data was originally a Dask array each chunk will be moved
        to the GPU when the task graph is computed.

        Returns
        -------
        cupy_da: DataArray
            DataArray with underlying data cast to cupy.

        Examples
        --------
        >>> import xarray as xr
        >>> da = xr.tutorial.load_dataset("air_temperature").air
        >>> gda = da.cupy.as_cupy()
        >>> type(gda.data)
        <class 'cupy.core.core.ndarray'>

        """
        return self.da.copy(data=_as_cupy_data(self.da.data))

    def as_numpy(self):
        """
        Converts the DataArray's underlying array type from cupy to numpy.

        Returns
        -------
        da: DataArray
            DataArray with underlying data cast to numpy.

        """
        raise NotImplementedError("Please use .as_numpy DataArray method directly.")

    def get(self):
        return self.da.data.get()


def _as_cupy_data(data):
    if isinstance(data, dask_array_type):
        return data.map_blocks(cp.asarray)
    if isinstance(data, pint_array_type):
        from pint import Quantity  # pylint: disable=import-outside-toplevel

        return Quantity(
            _as_cupy_data(data.magnitude),
            units=data.units,
        )
    return cp.asarray(data)


def _as_numpy_data(data):
    if isinstance(data, dask_array_type):
        return data.map_blocks(lambda block: block.get(), dtype=data._meta.dtype)
    if isinstance(data, pint_array_type):
        from pint import Quantity  # pylint: disable=import-outside-toplevel

        return Quantity(
            _as_numpy_data(data.magnitude),
            units=data.units,
        )
    return data.get() if isinstance(data, cp.ndarray) else data


@register_dataset_accessor("cupy")
class CupyDatasetAccessor:
    """
    Access methods for DataArrays using Cupy.
    Methods and attributes can be accessed through the `.cupy` attribute.
    """

    def __init__(self, ds):
        self.ds = ds

    @property
    def has_cupy(self) -> bool:
        """True if any data variable contains a cupy array."""
        return any([da.cupy.is_cupy for da in self.ds.data_vars.values()])

    @property
    def is_cupy(self) -> bool:
        """True if all data variables contain cupy arrays."""
        return all([da.cupy.is_cupy for da in self.ds.data_vars.values()])

    def as_cupy(self):
        if not self.is_cupy:
            data_vars = {var: da.as_cupy() for var, da in self.ds.data_vars.items()}
            return Dataset(
                data_vars=data_vars,
                coords=self.ds.coords,
                attrs=self.ds.attrs,
            )
        return self.ds

    def as_numpy(self):
        if self.is_cupy:
            data_vars = {var: da.cupy.as_numpy() for var, da in self.ds.data_vars.items()}
            return Dataset(
                data_vars=data_vars,
                coords=self.ds.coords,
                attrs=self.ds.attrs,
            )
        return self.ds


# Attach the `as_cupy` methods to the top level `Dataset` and `Dataarray` objects.
# Would be good to replace this with a less hacky API upstream at some stage where
# libraries like this could register new ``as_`` methods for dispatch.


@register_dataarray_accessor("as_cupy")
def _(da):
    """
    Converts the DataArray's underlying array type to cupy.

    See :meth:`cupy_xarray.CupyDataArrayAccessor.as_cupy`.
    """

    def as_cupy(*args, **kwargs):
        return da.cupy.as_cupy(*args, **kwargs)

    return as_cupy


@register_dataset_accessor("as_cupy")
def _(ds):
    """
    Converts the Dataset's underlying Dataarray's array type to cupy.

    See :meth:`cupy_xarray.CupyDatasetAccessor.as_cupy`.
    """

    def as_cupy(*args, **kwargs):
        return ds.cupy.as_cupy(*args, **kwargs)

    return as_cupy
