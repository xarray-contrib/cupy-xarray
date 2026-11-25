"""
Tests for xarray 'rumi' backend engine.
"""

from urllib.request import Request, urlopen

import cupy as cp
import pytest
import xarray as xr

rumi = pytest.importorskip("rumi")

from cupy_xarray.rumi import RumiBackendEntrypoint  # noqa: E402, F401


# %%
def test_entrypoint():
    assert "rumi" in xr.backends.list_engines()


def test_xarray_backend_open_dataarray():
    """
    Ensure that passing engine='rumi' to xarray.open_dataarray works to read a
    rumi file (and its external header loaded as bytes) from a http url.
    """
    header_url = (
        "https://data.source.coop/asterisk-labs/rumi-api-fixtures/headers/s2-00-chunky.header"
    )
    request = Request(url=header_url, headers={"User-Agent": "rumi-example"})
    header: bytes = urlopen(url=request).read()

    with xr.open_dataarray(
        filename_or_obj="https://data.source.coop/asterisk-labs/rumi-api-fixtures/data/s2-00-chunky.rumi",
        header=header,
        engine="rumi",
        device_id=0,
    ) as da:
        assert isinstance(da.data, cp.ndarray)
        assert da.sizes == {"band": 4, "y": 512, "x": 512}
        assert da.x.min() == 384425.0
        assert da.x.max() == 389535.0
        assert da.y.min() == 3947065.0
        assert da.y.max() == 3952175.0
        assert da.dtype == "uint16"
