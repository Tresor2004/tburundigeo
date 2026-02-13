"""Common utilities shared across the package."""

from tburundigeo.common.exceptions import (
    TburundiGeoError,
    ProvinceNotFoundError,
    CommuneNotFoundError,
    ZoneNotFoundError,
    QuartierNotFoundError,
    InvalidCodeError,
    ReferentialIntegrityError,
    DataSourceError,
)

from tburundigeo.common.types import (
    AdministrativeLevel,
    ExportFormat,
    CodeType,
)

__all__ = [
    # Exceptions
    "TburundiGeoError",
    "ProvinceNotFoundError",
    "CommuneNotFoundError",
    "ZoneNotFoundError",
    "QuartierNotFoundError",
    "InvalidCodeError",
    "ReferentialIntegrityError",
    "DataSourceError",
    # Types
    "AdministrativeLevel",
    "ExportFormat",
    "CodeType",
]
