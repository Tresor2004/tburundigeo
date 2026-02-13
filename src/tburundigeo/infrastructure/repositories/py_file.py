"""Repository implementations that read data from Python files."""

import importlib
import importlib.util
import sys
from pathlib import Path
from typing import Dict, List, Optional

from tburundigeo.common.exceptions import (
    DataSourceError,
    ProvinceNotFoundError,
    CommuneNotFoundError,
    ZoneNotFoundError,
    QuartierNotFoundError,
)
from tburundigeo.domain.entities import Province, Commune, Zone, Quartier
from tburundigeo.domain.interfaces import (
    IProvinceRepository,
    ICommuneRepository,
    IZoneRepository,
    IQuartierRepository,
)


class BasePyFileRepository:
    """Base class for Python file-based repositories."""
    
    def __init__(self, data_module_path: str) -> None:
        """Initialize repository with path to data module."""
        self.data_module_path = data_module_path
        self._data_cache: Optional[List[Dict]] = None
        self._indexed_cache: Optional[Dict[str, Dict]] = None
    
    def _load_data(self) -> List[Dict]:
        """Load data from Python file module."""
        if self._data_cache is not None:
            return self._data_cache
        
        try:
            # Try to import as a module first
            if self.data_module_path.startswith('burundi_admin.data.') or self.data_module_path.startswith('tburundigeo.data.'):
                module = importlib.import_module(self.data_module_path)
            else:
                # Load as file path
                spec = importlib.util.spec_from_file_location(
                    "data_module", self.data_module_path
                )
                if spec is None or spec.loader is None:
                    raise DataSourceError(f"Cannot load data module: {self.data_module_path}")
                
                module = importlib.util.module_from_spec(spec)
                sys.modules["data_module"] = module
                spec.loader.exec_module(module)
            
            if not hasattr(module, 'data'):
                raise DataSourceError(f"Module {self.data_module_path} has no 'data' attribute")
            
            data = getattr(module, 'data')
            if not isinstance(data, list):
                raise DataSourceError(f"Expected list of dictionaries, got {type(data)}")
            
            self._data_cache = data
            return data
            
        except ImportError as e:
            raise DataSourceError(f"Failed to import {self.data_module_path}: {e}")
        except Exception as e:
            raise DataSourceError(f"Error loading data from {self.data_module_path}: {e}")
    
    def _build_index(self) -> Dict[str, Dict]:
        """Build index for O(1) lookups by code."""
        if self._indexed_cache is not None:
            return self._indexed_cache
        
        data = self._load_data()
        index = {}
        for item in data:
            if 'code' in item and isinstance(item['code'], str):
                index[item['code']] = item
        
        self._indexed_cache = index
        return index
    
    def _get_by_code_from_index(self, code: str) -> Optional[Dict]:
        """Get item by code using index."""
        index = self._build_index()
        return index.get(code)
    
    def _search_by_field(self, field: str, substring: str) -> List[Dict]:
        """Search items by field containing substring (case-insensitive)."""
        data = self._load_data()
        substring_lower = substring.lower()
        results = []
        
        for item in data:
            if field in item and isinstance(item[field], str):
                if substring_lower in item[field].lower():
                    results.append(item)
        
        return results


class PyFileProvinceRepository(BasePyFileRepository, IProvinceRepository):
    """Repository implementation for provinces using Python files."""
    
    def __init__(self, data_module_path: str = "burundi_admin.data.provinces") -> None:
        super().__init__(data_module_path)
    
    def get_all(self) -> List[Province]:
        """Get all provinces."""
        data = self._load_data()
        provinces = []
        
        for item in data:
            try:
                province = Province(
                    code=item['code'],
                    name=item['name'],
                    capital=item['capital']
                )
                provinces.append(province)
            except (KeyError, ValueError) as e:
                # Skip invalid items but continue processing
                continue
        
        return provinces
    
    def get_by_code(self, code: str) -> Optional[Province]:
        """Get a province by its code."""
        item = self._get_by_code_from_index(code)
        if item is None:
            raise ProvinceNotFoundError(code)
        
        try:
            return Province(
                code=item['code'],
                name=item['name'],
                capital=item.get('capital', '')
            )
        except (KeyError, ValueError) as e:
            raise ProvinceNotFoundError(code) from e
    
    def search_by_name(self, name_substring: str) -> List[Province]:
        """Search provinces by name substring."""
        results = self._search_by_field('name', name_substring)
        provinces = []
        
        for item in results:
            try:
                province = Province(
                    code=item['code'],
                    name=item['name'],
                    capital=item.get('capital', '')
                )
                provinces.append(province)
            except (KeyError, ValueError):
                continue
        
        return provinces
    
    def count(self) -> int:
        """Count total number of provinces."""
        data = self._load_data()
        return len(data)
    
    def exists(self, code: str) -> bool:
        """Check if a province with the given code exists."""
        return self._get_by_code_from_index(code) is not None


class PyFileCommuneRepository(BasePyFileRepository, ICommuneRepository):
    """Repository implementation for communes using Python files."""
    
    def __init__(self, data_module_path: str = "burundi_admin.data.communes") -> None:
        super().__init__(data_module_path)
    
    def get_all(self) -> List[Commune]:
        """Get all communes."""
        data = self._load_data()
        communes = []
        
        for item in data:
            try:
                commune = Commune(
                    code=item['code'],
                    name=item['name'],
                    capital=item['capital'],
                    province_code=item['province_code']
                )
                communes.append(commune)
            except (KeyError, ValueError):
                continue
        
        return communes
    
    def get_by_code(self, code: str) -> Optional[Commune]:
        """Get a commune by its code."""
        item = self._get_by_code_from_index(code)
        if item is None:
            raise CommuneNotFoundError(code)
        
        try:
            return Commune(
                code=item['code'],
                name=item['name'],
                capital=item['capital'],
                province_code=item['province_code']
            )
        except (KeyError, ValueError) as e:
            raise CommuneNotFoundError(code) from e
    
    def search_by_name(self, name_substring: str) -> List[Commune]:
        """Search communes by name substring."""
        results = self._search_by_field('name', name_substring)
        communes = []
        
        for item in results:
            try:
                commune = Commune(
                    code=item['code'],
                    name=item['name'],
                    capital=item['capital'],
                    province_code=item['province_code']
                )
                communes.append(commune)
            except (KeyError, ValueError):
                continue
        
        return communes
    
    def search_by_capital(self, capital_substring: str) -> List[Commune]:
        """Search communes by capital substring."""
        results = self._search_by_field('capital', capital_substring)
        communes = []
        
        for item in results:
            try:
                commune = Commune(
                    code=item['code'],
                    name=item['name'],
                    capital=item['capital'],
                    province_code=item['province_code']
                )
                communes.append(commune)
            except (KeyError, ValueError):
                continue
        
        return communes
    
    def get_by_province(self, province_code: str) -> List[Commune]:
        """Get all communes in a province."""
        data = self._load_data()
        communes = []
        
        for item in data:
            if item.get('province_code') == province_code:
                try:
                    commune = Commune(
                        code=item['code'],
                        name=item['name'],
                        capital=item['capital'],
                        province_code=item['province_code']
                    )
                    communes.append(commune)
                except (KeyError, ValueError):
                    continue
        
        return communes
    
    def count(self) -> int:
        """Count total number of communes."""
        data = self._load_data()
        return len(data)
    
    def count_in_province(self, province_code: str) -> int:
        """Count communes in a specific province."""
        data = self._load_data()
        count = 0
        
        for item in data:
            if item.get('province_code') == province_code:
                count += 1
        
        return count
    
    def exists(self, code: str) -> bool:
        """Check if a commune with the given code exists."""
        return self._get_by_code_from_index(code) is not None


class PyFileZoneRepository(BasePyFileRepository, IZoneRepository):
    """Repository implementation for zones using Python files."""
    
    def __init__(self, data_module_path: str = "burundi_admin.data.zones") -> None:
        super().__init__(data_module_path)
    
    def get_all(self) -> List[Zone]:
        """Get all zones."""
        data = self._load_data()
        zones = []
        
        for item in data:
            try:
                zone = Zone(
                    code=item['code'],
                    name=item['name'],
                    chief_town=item['chief_town'],
                    commune_code=item['commune_code']
                )
                zones.append(zone)
            except (KeyError, ValueError):
                continue
        
        return zones
    
    def get_by_code(self, code: str) -> Optional[Zone]:
        """Get a zone by its code."""
        item = self._get_by_code_from_index(code)
        if item is None:
            raise ZoneNotFoundError(code)
        
        try:
            return Zone(
                code=item['code'],
                name=item['name'],
                chief_town=item.get('chief_town', ''),
                commune_code=item['commune_code']
            )
        except (KeyError, ValueError) as e:
            raise ZoneNotFoundError(code) from e
    
    def search_by_name(self, name_substring: str) -> List[Zone]:
        """Search zones by name substring."""
        results = self._search_by_field('name', name_substring)
        zones = []
        
        for item in results:
            try:
                zone = Zone(
                    code=item['code'],
                    name=item['name'],
                    chief_town=item['chief_town'],
                    commune_code=item['commune_code']
                )
                zones.append(zone)
            except (KeyError, ValueError):
                continue
        
        return zones
    
    def get_by_commune(self, commune_code: str) -> List[Zone]:
        """Get all zones in a commune."""
        data = self._load_data()
        zones = []
        
        for item in data:
            if item.get('commune_code') == commune_code:
                try:
                    zone = Zone(
                        code=item['code'],
                        name=item['name'],
                        chief_town=item.get('chief_town', ''),
                        commune_code=item['commune_code']
                    )
                    zones.append(zone)
                except (KeyError, ValueError):
                    continue
        
        return zones
    
    def count(self) -> int:
        """Count total number of zones."""
        data = self._load_data()
        return len(data)
    
    def count_in_commune(self, commune_code: str) -> int:
        """Count zones in a specific commune."""
        data = self._load_data()
        count = 0
        
        for item in data:
            if item.get('commune_code') == commune_code:
                count += 1
        
        return count
    
    def exists(self, code: str) -> bool:
        """Check if a zone with the given code exists."""
        return self._get_by_code_from_index(code) is not None


class PyFileQuartierRepository(BasePyFileRepository, IQuartierRepository):
    """Repository implementation for quartiers using Python files."""
    
    def __init__(self, data_module_path: str = "burundi_admin.data.quartiers") -> None:
        super().__init__(data_module_path)
    
    def get_all(self) -> List[Quartier]:
        """Get all quartiers."""
        data = self._load_data()
        quartiers = []
        
        for item in data:
            try:
                quartier = Quartier(
                    code=item['code'],
                    name=item['name'],
                    zone_code=item['zone_code']
                )
                quartiers.append(quartier)
            except (KeyError, ValueError):
                continue
        
        return quartiers
    
    def get_by_code(self, code: str) -> Optional[Quartier]:
        """Get a quartier by its code."""
        item = self._get_by_code_from_index(code)
        if item is None:
            raise QuartierNotFoundError(code)
        
        try:
            return Quartier(
                code=item['code'],
                name=item['name'],
                zone_code=item['zone_code']
            )
        except (KeyError, ValueError) as e:
            raise QuartierNotFoundError(code) from e
    
    def search_by_name(self, name_substring: str) -> List[Quartier]:
        """Search quartiers by name substring."""
        results = self._search_by_field('name', name_substring)
        quartiers = []
        
        for item in results:
            try:
                quartier = Quartier(
                    code=item['code'],
                    name=item['name'],
                    zone_code=item['zone_code']
                )
                quartiers.append(quartier)
            except (KeyError, ValueError):
                continue
        
        return quartiers
    
    def get_by_zone(self, zone_code: str) -> List[Quartier]:
        """Get all quartiers in a zone."""
        data = self._load_data()
        quartiers = []
        
        for item in data:
            if item.get('zone_code') == zone_code:
                try:
                    quartier = Quartier(
                        code=item['code'],
                        name=item['name'],
                        zone_code=item['zone_code']
                    )
                    quartiers.append(quartier)
                except (KeyError, ValueError):
                    continue
        
        return quartiers
    
    def count(self) -> int:
        """Count total number of quartiers."""
        data = self._load_data()
        return len(data)
    
    def count_in_zone(self, zone_code: str) -> int:
        """Count quartiers in a specific zone."""
        data = self._load_data()
        count = 0
        
        for item in data:
            if item.get('zone_code') == zone_code:
                count += 1
        
        return count
    
    def exists(self, code: str) -> bool:
        """Check if a quartier with the given code exists."""
        return self._get_by_code_from_index(code) is not None
