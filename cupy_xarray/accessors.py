import cupy as cp

from xarray import (
    DataArray,
    Dataset,
    register_dataarray_accessor,
    register_dataset_accessor,
)


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
        return isinstance(self.da.data, cp.ndarray)

    def as_cupy(self):
        return self.da.copy(data=cp.asarray(self.da.data))

    def as_numpy(self):
        if self.is_cupy:
            return self.da.copy(data=self.da.data.get())
        else:
            return self.da.as_numpy()


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
            return self.ds.copy(
                data={var: da.cupy.as_numpy() for var, da in self.ds.data_vars.items()}
            )
        else:
            return self.ds.as_numpy()


# Attach the `as_cupy` methods to the top level `Dataset` and `Dataarray` objects
@register_dataarray_accessor("as_cupy")
def _(da):
    def as_cupy(*args, **kwargs):
        return da.cupy.as_cupy(*args, **kwargs)

    return as_cupy


@register_dataset_accessor("as_cupy")
def _(ds):
    def as_cupy(*args, **kwargs):
        return ds.cupy.as_cupy(*args, **kwargs)

    return as_cupy
