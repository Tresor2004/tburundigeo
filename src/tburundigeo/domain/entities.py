"""Core business entities for Burundi administrative divisions."""

import re
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Province:
    """Represents a province in Burundi."""
    
    code: str
    name: str
    capital: str
    
    def __post_init__(self) -> None:
        """Validate province data after initialization."""
        self._validate_code(self.code)
        self._validate_name(self.name)
        self._validate_capital(self.capital)
    
    def _validate_code(self, code: str) -> None:
        """Validate province code format."""
        if not code or not isinstance(code, str):
            raise ValueError("Province code must be a non-empty string")
        
        # Expected format: BI-PR-XX (where XX is a number)
        if not re.match(r'^BI-PR-\d{2}$', code):
            raise ValueError(f"Invalid province code format: {code}")
    
    def _validate_name(self, name: str) -> None:
        """Validate province name."""
        if not name or not isinstance(name, str):
            raise ValueError("Province name must be a non-empty string")
        
        if len(name.strip()) < 2:
            raise ValueError("Province name must be at least 2 characters long")
    
    def _validate_capital(self, capital: str) -> None:
        """Validate province capital."""
        if not capital or not isinstance(capital, str):
            raise ValueError("Province capital must be a non-empty string")
        
        if len(capital.strip()) < 2:
            raise ValueError("Province capital must be at least 2 characters long")
    
    def __str__(self) -> str:
        """String representation of the province."""
        return f"Province({self.code}: {self.name}, Capital: {self.capital})"


@dataclass(frozen=True)
class Commune:
    """Represents a commune in Burundi."""
    
    code: str
    name: str
    capital: str
    province_code: str
    
    def __post_init__(self) -> None:
        """Validate commune data after initialization."""
        self._validate_code(self.code)
        self._validate_name(self.name)
        self._validate_capital(self.capital)
        self._validate_province_code(self.province_code)
    
    def _validate_code(self, code: str) -> None:
        """Validate commune code format."""
        if not code or not isinstance(code, str):
            raise ValueError("Commune code must be a non-empty string")
        
        # Expected format: BI-CO-XX-YY (where XX is province, YY is commune)
        if not re.match(r'^BI-CO-\d{2}-\d{2}$', code):
            raise ValueError(f"Invalid commune code format: {code}")
    
    def _validate_name(self, name: str) -> None:
        """Validate commune name."""
        if not name or not isinstance(name, str):
            raise ValueError("Commune name must be a non-empty string")
        
        if len(name.strip()) < 2:
            raise ValueError("Commune name must be at least 2 characters long")
    
    def _validate_capital(self, capital: str) -> None:
        """Validate commune capital."""
        if not capital or not isinstance(capital, str):
            raise ValueError("Commune capital must be a non-empty string")
        
        if len(capital.strip()) < 2:
            raise ValueError("Commune capital must be at least 2 characters long")
    
    def _validate_province_code(self, province_code: str) -> None:
        """Validate province code reference."""
        if not province_code or not isinstance(province_code, str):
            raise ValueError("Province code must be a non-empty string")
        
        # Should match province code format
        if not re.match(r'^BI-PR-\d{2}$', province_code):
            raise ValueError(f"Invalid province code format: {province_code}")
    
    def __str__(self) -> str:
        """String representation of the commune."""
        return f"Commune({self.code}: {self.name}, Capital: {self.capital})"


@dataclass(frozen=True)
class Zone:
    """Represents a zone in Burundi."""
    
    code: str
    name: str
    chief_town: str
    commune_code: str
    
    def __post_init__(self) -> None:
        """Validate zone data after initialization."""
        self._validate_code(self.code)
        self._validate_name(self.name)
        self._validate_chief_town(self.chief_town)
        self._validate_commune_code(self.commune_code)
    
    def _validate_code(self, code: str) -> None:
        """Validate zone code format."""
        if not code or not isinstance(code, str):
            raise ValueError("Zone code must be a non-empty string")
        
        # Expected format: BI-ZO-XX-XX-XX (where XX are numbers)
        if not re.match(r'^BI-ZO-\d{2}-\d{2}-\d{2}$', code):
            raise ValueError(f"Invalid zone code format: {code}")
    
    def _validate_name(self, name: str) -> None:
        """Validate zone name."""
        if not name or not isinstance(name, str):
            raise ValueError("Zone name must be a non-empty string")
        
        if len(name.strip()) < 2:
            raise ValueError("Zone name must be at least 2 characters long")
    
    def _validate_chief_town(self, chief_town: str) -> None:
        """Validate zone chief town."""
        if not chief_town or not isinstance(chief_town, str):
            raise ValueError("Zone chief town must be a non-empty string")
        
        if len(chief_town.strip()) < 2:
            raise ValueError("Zone chief town must be at least 2 characters long")
    
    def _validate_commune_code(self, commune_code: str) -> None:
        """Validate commune code reference."""
        if not commune_code or not isinstance(commune_code, str):
            raise ValueError("Commune code must be a non-empty string")
        
        # Should match commune code format
        if not re.match(r'^BI-CO-\d{2}-\d{2}$', commune_code):
            raise ValueError(f"Invalid commune code format: {commune_code}")
    
    def __str__(self) -> str:
        """String representation of the zone."""
        return f"Zone({self.code}: {self.name}, Chief town: {self.chief_town})"


@dataclass(frozen=True)
class Quartier:
    """Represents a quartier (neighborhood) in Burundi."""
    
    code: str
    name: str
    zone_code: str
    
    def __post_init__(self) -> None:
        """Validate quartier data after initialization."""
        self._validate_code(self.code)
        self._validate_name(self.name)
        self._validate_zone_code(self.zone_code)
    
    def _validate_code(self, code: str) -> None:
        """Validate quartier code format."""
        if not code or not isinstance(code, str):
            raise ValueError("Quartier code must be a non-empty string")
        
        # Expected format: BI-QT-XX-YY-ZZ-WW
        if not re.match(r'^BI-QT-\d{2}-\d{2}-\d{2}-\d{2}$', code):
            raise ValueError(f"Invalid quartier code format: {code}")
    
    def _validate_name(self, name: str) -> None:
        """Validate quartier name."""
        if not name or not isinstance(name, str):
            raise ValueError("Quartier name must be a non-empty string")
        
        if len(name.strip()) < 2:
            raise ValueError("Quartier name must be at least 2 characters long")
    
    def _validate_zone_code(self, zone_code: str) -> None:
        """Validate zone code reference."""
        if not zone_code or not isinstance(zone_code, str):
            raise ValueError("Zone code must be a non-empty string")
        
        # Should match zone code format
        if not re.match(r'^BI-ZO-\d{2}-\d{2}-\d{2}$', zone_code):
            raise ValueError(f"Invalid zone code format: {zone_code}")
    
    def __str__(self) -> str:
        """String representation of the quartier."""
        return f"Quartier({self.code}: {self.name})"
