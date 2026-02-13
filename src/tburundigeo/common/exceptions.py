"""Custom exceptions for the TBurundiGeo package."""


class TburundiGeoError(Exception):
    """Base exception for all TBurundiGeo package errors."""
    
    def __init__(self, message: str, code: str | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.code = code


class ProvinceNotFoundError(TburundiGeoError):
    """Raised when a province is not found."""
    
    def __init__(self, province_code: str) -> None:
        super().__init__(f"Province with code '{province_code}' not found", province_code)
        self.province_code = province_code


class CommuneNotFoundError(TburundiGeoError):
    """Raised when a commune is not found."""
    
    def __init__(self, commune_code: str) -> None:
        super().__init__(f"Commune with code '{commune_code}' not found", commune_code)
        self.commune_code = commune_code


class ZoneNotFoundError(TburundiGeoError):
    """Raised when a zone is not found."""
    
    def __init__(self, zone_code: str) -> None:
        super().__init__(f"Zone with code '{zone_code}' not found", zone_code)
        self.zone_code = zone_code


class QuartierNotFoundError(TburundiGeoError):
    """Raised when a quartier is not found."""
    
    def __init__(self, quartier_code: str) -> None:
        super().__init__(f"Quartier with code '{quartier_code}' not found", quartier_code)
        self.quartier_code = quartier_code


class InvalidCodeError(TburundiGeoError):
    """Raised when an administrative code is invalid."""
    
    def __init__(self, code: str, reason: str = "Invalid format") -> None:
        super().__init__(f"Invalid code '{code}': {reason}", code)
        self.code = code
        self.reason = reason


class ReferentialIntegrityError(TburundiGeoError):
    """Raised when referential integrity is violated."""
    
    def __init__(self, message: str) -> None:
        super().__init__(f"Referential integrity error: {message}")


class DataSourceError(TburundiGeoError):
    """Raised when there's an error with the data source."""
    
    def __init__(self, message: str, source: str | None = None) -> None:
        super().__init__(f"Data source error: {message}")
        self.source = source
