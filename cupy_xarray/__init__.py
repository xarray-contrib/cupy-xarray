from . import _version
from .accessors import CupyDataArrayAccessor, CupyDatasetAccessor  # noqa: F401
from .kvikio import KvikioBackendEntrypoint  # noqa: F401

__version__ = _version.get_versions()["version"]
