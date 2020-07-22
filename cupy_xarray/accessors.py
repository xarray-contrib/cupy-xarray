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


@register_dataset_accessor("cupy")
class CupyDatasetAccessor:
    """
    Access methods for DataArrays using Cupy.
    Methods and attributes can be accessed through the `.cupy` attribute.
    """

    def __init__(self, ds):
        self.ds = ds
