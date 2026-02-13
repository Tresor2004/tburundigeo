"""In-memory repository implementations for testing and caching."""

from typing import Dict, List, Optional

from tburundigeo.domain.entities import Province, Commune, Zone, Quartier
from tburundigeo.domain.interfaces import (
    IProvinceRepository,
    ICommuneRepository,
    IZoneRepository,
    IQuartierRepository,
)


class MemoryProvinceRepository(IProvinceRepository):
    """In-memory implementation of province repository."""
    
    def __init__(self, provinces: List[Province] | None = None) -> None:
        """Initialize with optional list of provinces."""
        self._provinces: List[Province] = provinces or []
        self._index: Dict[str, Province] = {p.code: p for p in self._provinces}
    
    def get_all(self) -> List[Province]:
        """Get all provinces."""
        return list(self._provinces)
    
    def get_by_code(self, code: str) -> Optional[Province]:
        """Get a province by its code."""
        return self._index.get(code)
    
    def search_by_name(self, name_substring: str) -> List[Province]:
        """Search provinces by name substring (case-insensitive)."""
        substring_lower = name_substring.lower()
        return [
            province for province in self._provinces
            if substring_lower in province.name.lower()
        ]
    
    def count(self) -> int:
        """Count total number of provinces."""
        return len(self._provinces)
    
    def exists(self, code: str) -> bool:
        """Check if a province with the given code exists."""
        return code in self._index
    
    def add(self, province: Province) -> None:
        """Add a province (for testing purposes)."""
        self._provinces.append(province)
        self._index[province.code] = province
    
    def clear(self) -> None:
        """Clear all provinces (for testing purposes)."""
        self._provinces.clear()
        self._index.clear()


class MemoryCommuneRepository(ICommuneRepository):
    """In-memory implementation of commune repository."""
    
    def __init__(self, communes: List[Commune] | None = None) -> None:
        """Initialize with optional list of communes."""
        self._communes: List[Commune] = communes or []
        self._index: Dict[str, Commune] = {c.code: c for c in self._communes}
    
    def get_all(self) -> List[Commune]:
        """Get all communes."""
        return list(self._communes)
    
    def get_by_code(self, code: str) -> Optional[Commune]:
        """Get a commune by its code."""
        return self._index.get(code)
    
    def search_by_name(self, name_substring: str) -> List[Commune]:
        """Search communes by name substring (case-insensitive)."""
        substring_lower = name_substring.lower()
        return [
            commune for commune in self._communes
            if substring_lower in commune.name.lower()
        ]
    
    def search_by_capital(self, capital_substring: str) -> List[Commune]:
        """Search communes by capital substring (case-insensitive)."""
        substring_lower = capital_substring.lower()
        return [
            commune for commune in self._communes
            if substring_lower in commune.capital.lower()
        ]
    
    def get_by_province(self, province_code: str) -> List[Commune]:
        """Get all communes in a province."""
        return [
            commune for commune in self._communes
            if commune.province_code == province_code
        ]
    
    def count(self) -> int:
        """Count total number of communes."""
        return len(self._communes)
    
    def count_in_province(self, province_code: str) -> int:
        """Count communes in a specific province."""
        return len(self.get_by_province(province_code))
    
    def exists(self, code: str) -> bool:
        """Check if a commune with the given code exists."""
        return code in self._index
    
    def add(self, commune: Commune) -> None:
        """Add a commune (for testing purposes)."""
        self._communes.append(commune)
        self._index[commune.code] = commune
    
    def clear(self) -> None:
        """Clear all communes (for testing purposes)."""
        self._communes.clear()
        self._index.clear()


class MemoryZoneRepository(IZoneRepository):
    """In-memory implementation of zone repository."""
    
    def __init__(self, zones: List[Zone] | None = None) -> None:
        """Initialize with optional list of zones."""
        self._zones: List[Zone] = zones or []
        self._index: Dict[str, Zone] = {z.code: z for z in self._zones}
    
    def get_all(self) -> List[Zone]:
        """Get all zones."""
        return list(self._zones)
    
    def get_by_code(self, code: str) -> Optional[Zone]:
        """Get a zone by its code."""
        return self._index.get(code)
    
    def search_by_name(self, name_substring: str) -> List[Zone]:
        """Search zones by name substring (case-insensitive)."""
        substring_lower = name_substring.lower()
        return [
            zone for zone in self._zones
            if substring_lower in zone.name.lower()
        ]
    
    def get_by_commune(self, commune_code: str) -> List[Zone]:
        """Get all zones in a commune."""
        return [
            zone for zone in self._zones
            if zone.commune_code == commune_code
        ]
    
    def count(self) -> int:
        """Count total number of zones."""
        return len(self._zones)
    
    def count_in_commune(self, commune_code: str) -> int:
        """Count zones in a specific commune."""
        return len(self.get_by_commune(commune_code))
    
    def exists(self, code: str) -> bool:
        """Check if a zone with the given code exists."""
        return code in self._index
    
    def add(self, zone: Zone) -> None:
        """Add a zone (for testing purposes)."""
        self._zones.append(zone)
        self._index[zone.code] = zone
    
    def clear(self) -> None:
        """Clear all zones (for testing purposes)."""
        self._zones.clear()
        self._index.clear()


class MemoryQuartierRepository(IQuartierRepository):
    """In-memory implementation of quartier repository."""
    
    def __init__(self, quartiers: List[Quartier] | None = None) -> None:
        """Initialize with optional list of quartiers."""
        self._quartiers: List[Quartier] = quartiers or []
        self._index: Dict[str, Quartier] = {q.code: q for q in self._quartiers}
    
    def get_all(self) -> List[Quartier]:
        """Get all quartiers."""
        return list(self._quartiers)
    
    def get_by_code(self, code: str) -> Optional[Quartier]:
        """Get a quartier by its code."""
        return self._index.get(code)
    
    def search_by_name(self, name_substring: str) -> List[Quartier]:
        """Search quartiers by name substring (case-insensitive)."""
        substring_lower = name_substring.lower()
        return [
            quartier for quartier in self._quartiers
            if substring_lower in quartier.name.lower()
        ]
    
    def get_by_zone(self, zone_code: str) -> List[Quartier]:
        """Get all quartiers in a zone."""
        return [
            quartier for quartier in self._quartiers
            if quartier.zone_code == zone_code
        ]
    
    def count(self) -> int:
        """Count total number of quartiers."""
        return len(self._quartiers)
    
    def count_in_zone(self, zone_code: str) -> int:
        """Count quartiers in a specific zone."""
        return len(self.get_by_zone(zone_code))
    
    def exists(self, code: str) -> bool:
        """Check if a quartier with the given code exists."""
        return code in self._index
    
    def add(self, quartier: Quartier) -> None:
        """Add a quartier (for testing purposes)."""
        self._quartiers.append(quartier)
        self._index[quartier.code] = quartier
    
    def clear(self) -> None:
        """Clear all quartiers (for testing purposes)."""
        self._quartiers.clear()
        self._index.clear()
