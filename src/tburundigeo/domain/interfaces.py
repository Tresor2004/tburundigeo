"""Repository interfaces (ports) for the domain layer."""

from abc import ABC, abstractmethod
from typing import List, Optional

from tburundigeo.domain.entities import Province, Commune, Zone, Quartier


class IProvinceRepository(ABC):
    """Interface for province repository operations."""
    
    @abstractmethod
    def get_all(self) -> List[Province]:
        """Get all provinces."""
        pass
    
    @abstractmethod
    def get_by_code(self, code: str) -> Optional[Province]:
        """Get a province by its code."""
        pass
    
    @abstractmethod
    def search_by_name(self, name_substring: str) -> List[Province]:
        """Search provinces by name substring (case-insensitive)."""
        pass
    
    @abstractmethod
    def count(self) -> int:
        """Count total number of provinces."""
        pass
    
    @abstractmethod
    def exists(self, code: str) -> bool:
        """Check if a province with the given code exists."""
        pass


class ICommuneRepository(ABC):
    """Interface for commune repository operations."""
    
    @abstractmethod
    def get_all(self) -> List[Commune]:
        """Get all communes."""
        pass
    
    @abstractmethod
    def get_by_code(self, code: str) -> Optional[Commune]:
        """Get a commune by its code."""
        pass
    
    @abstractmethod
    def search_by_name(self, name_substring: str) -> List[Commune]:
        """Search communes by name substring (case-insensitive)."""
        pass
    
    @abstractmethod
    def search_by_capital(self, capital_substring: str) -> List[Commune]:
        """Search communes by capital substring (case-insensitive)."""
        pass
    
    @abstractmethod
    def get_by_province(self, province_code: str) -> List[Commune]:
        """Get all communes in a province."""
        pass
    
    @abstractmethod
    def count(self) -> int:
        """Count total number of communes."""
        pass
    
    @abstractmethod
    def count_in_province(self, province_code: str) -> int:
        """Count communes in a specific province."""
        pass
    
    @abstractmethod
    def exists(self, code: str) -> bool:
        """Check if a commune with the given code exists."""
        pass


class IZoneRepository(ABC):
    """Interface for zone repository operations."""
    
    @abstractmethod
    def get_all(self) -> List[Zone]:
        """Get all zones."""
        pass
    
    @abstractmethod
    def get_by_code(self, code: str) -> Optional[Zone]:
        """Get a zone by its code."""
        pass
    
    @abstractmethod
    def search_by_name(self, name_substring: str) -> List[Zone]:
        """Search zones by name substring (case-insensitive)."""
        pass
    
    @abstractmethod
    def get_by_commune(self, commune_code: str) -> List[Zone]:
        """Get all zones in a commune."""
        pass
    
    @abstractmethod
    def count(self) -> int:
        """Count total number of zones."""
        pass
    
    @abstractmethod
    def count_in_commune(self, commune_code: str) -> int:
        """Count zones in a specific commune."""
        pass
    
    @abstractmethod
    def exists(self, code: str) -> bool:
        """Check if a zone with the given code exists."""
        pass


class IQuartierRepository(ABC):
    """Interface for quartier repository operations."""
    
    @abstractmethod
    def get_all(self) -> List[Quartier]:
        """Get all quartiers."""
        pass
    
    @abstractmethod
    def get_by_code(self, code: str) -> Optional[Quartier]:
        """Get a quartier by its code."""
        pass
    
    @abstractmethod
    def search_by_name(self, name_substring: str) -> List[Quartier]:
        """Search quartiers by name substring (case-insensitive)."""
        pass
    
    @abstractmethod
    def get_by_zone(self, zone_code: str) -> List[Quartier]:
        """Get all quartiers in a zone."""
        pass
    
    @abstractmethod
    def count(self) -> int:
        """Count total number of quartiers."""
        pass
    
    @abstractmethod
    def count_in_zone(self, zone_code: str) -> int:
        """Count quartiers in a specific zone."""
        pass
    
    @abstractmethod
    def exists(self, code: str) -> bool:
        """Check if a quartier with the given code exists."""
        pass
