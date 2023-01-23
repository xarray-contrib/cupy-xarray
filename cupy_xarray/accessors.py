import cupy as cp
from xarray import (
    DataArray,
    Dataset,
    register_dataarray_accessor,
    register_dataset_accessor,
)
from xarray.core.pycompat import DuckArrayModule

dask_array_type = DuckArrayModule("dask").type
pint_array_type = DuckArrayModule("pint").type


@register_dataarray_accessor("cupy")
class CupyDataArrayAccessor:
    """
    Access methods for DataArrays using Cupy.
    Methods and attributes can be accessed through the `.cupy` attribute.
    """

    def __init__(self, da):
        self.da = da

    @property
    def is_cupy(self):
        """bool: The underlying data is a cupy array."""
        if isinstance(self.da.data, dask_array_type):
            return isinstance(self.da.data._meta, cp.ndarray)
        if isinstance(self.da.data, pint_array_type):
            return isinstance(self.da.data.magnitude, cp.ndarray)
        return isinstance(self.da.data, cp.ndarray)

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
        if isinstance(self.da.data, dask_array_type):
            return self._as_dataarray(
                data=self.da.data.map_blocks(cp.asarray),
            )
        if isinstance(self.da.data, pint_array_type):
            from pint import Quantity
            return self._as_dataarray(
                data=Quantity(cp.asarray(self.da.data.magnitude), units=self.da.data.units),
            )
        return self._as_dataarray(data=cp.asarray(self.da.data))

    def as_numpy(self):
        """
        Converts the DataArray's underlying array type from cupy to numpy.

        Returns
        -------
        da: DataArray
            DataArray with underlying data cast to numpy.

        """
        if self.is_cupy:
            if isinstance(self.da.data, dask_array_type):
                return self._as_dataarray(
                    data=self.da.data.map_blocks(
                        lambda block: block.get(), dtype=self.da.data._meta.dtype
                    ),
                )
            return self._as_dataarray(data=self.da.data.get())
        return self.da.as_numpy()

    def get(self):
        return self.da.data.get()

    def _as_dataarray(self, data):
        return DataArray(
            data=data,
            coords=self.da.coords,
            dims=self.da.dims,
            name=self.da.name,
            attrs=self.da.attrs,
        )


@register_dataset_accessor("cupy")
class CupyDatasetAccessor:
    """
    Access methods for DataArrays using Cupy.
    Methods and attributes can be accessed through the `.cupy` attribute.
    """

    def __init__(self, ds):
        self.ds = ds

    @property
    def is_cupy(self):
        return all([da.cupy.is_cupy for da in self.ds.data_vars.values()])

    def as_cupy(self):
        data_vars = {var: da.as_cupy() for var, da in self.ds.data_vars.items()}
        return Dataset(data_vars=data_vars, coords=self.ds.coords, attrs=self.ds.attrs)

    def as_numpy(self):
        if self.is_cupy:
            data_vars = {var: da.cupy.as_numpy() for var, da in self.ds.data_vars.items()}
            return Dataset(
                data_vars=data_vars,
                coords=self.ds.coords,
                attrs=self.ds.attrs,
            )
        else:
            return self.ds.as_numpy()


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
