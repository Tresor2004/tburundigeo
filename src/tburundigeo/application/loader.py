"""Data loader service for loading administrative divisions from various sources."""

import csv
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from tburundigeo.common.exceptions import DataSourceError
from tburundigeo.domain.entities import Province, Commune, Zone, Quartier
from tburundigeo.domain.interfaces import (
    IProvinceRepository,
    ICommuneRepository,
    IZoneRepository,
    IQuartierRepository,
)


class DataLoaderService:
    """Service for loading administrative divisions data from various sources."""
    
    def __init__(
        self,
        province_repo: IProvinceRepository,
        commune_repo: ICommuneRepository,
        zone_repo: IZoneRepository,
        quartier_repo: IQuartierRepository,
    ) -> None:
        """Initialize data loader service with repositories."""
        self._province_repo = province_repo
        self._commune_repo = commune_repo
        self._zone_repo = zone_repo
        self._quartier_repo = quartier_repo
    
    def load_from_json_file(self, file_path: Union[str, Path]) -> Dict[str, List[Dict]]:
        """Load data from a JSON file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            return self._validate_and_normalize_json_data(data)
        
        except FileNotFoundError:
            raise DataSourceError(f"File not found: {file_path}")
        except json.JSONDecodeError as e:
            raise DataSourceError(f"Invalid JSON in file {file_path}: {e}")
        except Exception as e:
            raise DataSourceError(f"Error loading data from {file_path}: {e}")
    
    def load_from_csv_file(self, file_path: Union[str, Path], entity_type: str) -> List[Dict]:
        """Load data from a CSV file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                data = list(reader)
            
            return self._validate_and_normalize_csv_data(data, entity_type)
        
        except FileNotFoundError:
            raise DataSourceError(f"File not found: {file_path}")
        except Exception as e:
            raise DataSourceError(f"Error loading data from {file_path}: {e}")
    
    def load_from_python_file(self, file_path: Union[str, Path]) -> Dict[str, List[Dict]]:
        """Load data from a Python file (expects a 'data' variable with list of dicts)."""
        try:
            import importlib.util
            
            spec = importlib.util.spec_from_file_location("data_module", file_path)
            if spec is None or spec.loader is None:
                raise DataSourceError(f"Cannot load Python file: {file_path}")
            
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            if not hasattr(module, 'data'):
                raise DataSourceError(f"Python file {file_path} must have a 'data' variable")
            
            data = getattr(module, 'data')
            if not isinstance(data, list):
                raise DataSourceError(f"Expected list of dictionaries, got {type(data)}")
            
            # Try to determine entity type from file name
            file_name = Path(file_path).stem.lower()
            if "province" in file_name:
                return {"provinces": data}
            elif "commune" in file_name:
                return {"communes": data}
            elif "zone" in file_name:
                return {"zones": data}
            elif "quartier" in file_name:
                return {"quartiers": data}
            else:
                # Try to auto-detect from data structure
                return self._auto_detect_entity_types(data)
        
        except Exception as e:
            raise DataSourceError(f"Error loading data from {file_path}: {e}")
    
    def load_from_dict(self, data: Dict[str, Any]) -> Dict[str, List[Dict]]:
        """Load data from a dictionary."""
        return self._validate_and_normalize_json_data(data)
    
    def create_entities_from_data(self, data: Dict[str, List[Dict]]) -> Dict[str, List]:
        """Create entity objects from raw data."""
        entities = {
            "provinces": [],
            "communes": [],
            "zones": [],
            "quartiers": []
        }
        
        # Create provinces
        if "provinces" in data:
            for item in data["provinces"]:
                try:
                    province = Province(
                        code=item["code"],
                        name=item["name"]
                    )
                    entities["provinces"].append(province)
                except (KeyError, ValueError) as e:
                    # Skip invalid items but continue
                    continue
        
        # Create communes
        if "communes" in data:
            for item in data["communes"]:
                try:
                    commune = Commune(
                        code=item["code"],
                        name=item["name"],
                        capital=item["capital"],
                        province_code=item["province_code"]
                    )
                    entities["communes"].append(commune)
                except (KeyError, ValueError) as e:
                    continue
        
        # Create zones
        if "zones" in data:
            for item in data["zones"]:
                try:
                    zone = Zone(
                        code=item["code"],
                        name=item["name"],
                        commune_code=item["commune_code"]
                    )
                    entities["zones"].append(zone)
                except (KeyError, ValueError) as e:
                    continue
        
        # Create quartiers
        if "quartiers" in data:
            for item in data["quartiers"]:
                try:
                    quartier = Quartier(
                        code=item["code"],
                        name=item["name"],
                        zone_code=item["zone_code"]
                    )
                    entities["quartiers"].append(quartier)
                except (KeyError, ValueError) as e:
                    continue
        
        return entities
    
    def populate_repositories(self, entities: Dict[str, List]) -> None:
        """Populate repositories with entities (if they support adding)."""
        # This would work with memory repositories or custom implementations
        # For read-only repositories, this would be a no-op
        
        if hasattr(self._province_repo, 'add'):
            for province in entities.get("provinces", []):
                self._province_repo.add(province)
        
        if hasattr(self._commune_repo, 'add'):
            for commune in entities.get("communes", []):
                self._commune_repo.add(commune)
        
        if hasattr(self._zone_repo, 'add'):
            for zone in entities.get("zones", []):
                self._zone_repo.add(zone)
        
        if hasattr(self._quartier_repo, 'add'):
            for quartier in entities.get("quartiers", []):
                self._quartier_repo.add(quartier)
    
    def load_and_populate_from_file(self, file_path: Union[str, Path]) -> Dict[str, List]:
        """Load data from file and create entities."""
        file_path = Path(file_path)
        
        if file_path.suffix.lower() == '.json':
            raw_data = self.load_from_json_file(file_path)
        elif file_path.suffix.lower() == '.csv':
            # For CSV, we need to know the entity type
            entity_type = file_path.stem.lower()
            if "province" in entity_type:
                raw_data = {"provinces": self.load_from_csv_file(file_path, "province")}
            elif "commune" in entity_type:
                raw_data = {"communes": self.load_from_csv_file(file_path, "commune")}
            elif "zone" in entity_type:
                raw_data = {"zones": self.load_from_csv_file(file_path, "zone")}
            elif "quartier" in entity_type:
                raw_data = {"quartiers": self.load_from_csv_file(file_path, "quartier")}
            else:
                raise DataSourceError(f"Cannot determine entity type from CSV file name: {file_path}")
        elif file_path.suffix.lower() == '.py':
            raw_data = self.load_from_python_file(file_path)
        else:
            raise DataSourceError(f"Unsupported file format: {file_path.suffix}")
        
        entities = self.create_entities_from_data(raw_data)
        self.populate_repositories(entities)
        
        return entities
    
    def _validate_and_normalize_json_data(self, data: Dict[str, Any]) -> Dict[str, List[Dict]]:
        """Validate and normalize JSON data structure."""
        normalized = {}
        
        # Handle different possible structures
        if isinstance(data, list):
            # Single list - try to auto-detect type
            return self._auto_detect_entity_types(data)
        elif isinstance(data, dict):
            # Dictionary with entity types as keys
            for key, value in data.items():
                if key.lower() in ["provinces", "province"]:
                    normalized["provinces"] = value if isinstance(value, list) else [value]
                elif key.lower() in ["communes", "commune"]:
                    normalized["communes"] = value if isinstance(value, list) else [value]
                elif key.lower() in ["zones", "zone"]:
                    normalized["zones"] = value if isinstance(value, list) else [value]
                elif key.lower() in ["quartiers", "quartier"]:
                    normalized["quartiers"] = value if isinstance(value, list) else [value]
                else:
                    # Unknown key - try to auto-detect
                    if isinstance(value, list):
                        detected = self._auto_detect_entity_types(value)
                        for detected_key, detected_value in detected.items():
                            if detected_key not in normalized:
                                normalized[detected_key] = detected_value
        
        return normalized
    
    def _validate_and_normalize_csv_data(self, data: List[Dict], entity_type: str) -> List[Dict]:
        """Validate and normalize CSV data structure."""
        if not isinstance(data, list):
            raise DataSourceError(f"Expected list of dictionaries for CSV data, got {type(data)}")
        
        # Define required fields for each entity type
        required_fields = {
            "province": ["code", "name"],
            "commune": ["code", "name", "capital", "province_code"],
            "zone": ["code", "name", "commune_code"],
            "quartier": ["code", "name", "zone_code"]
        }
        
        if entity_type not in required_fields:
            raise DataSourceError(f"Unknown entity type: {entity_type}")
        
        required = required_fields[entity_type]
        validated_data = []
        
        for i, item in enumerate(data):
            if not isinstance(item, dict):
                continue
            
            # Check required fields
            missing_fields = [field for field in required if field not in item]
            if missing_fields:
                continue  # Skip items with missing required fields
            
            # Normalize string fields (strip whitespace)
            normalized_item = {}
            for key, value in item.items():
                if isinstance(value, str):
                    normalized_item[key] = value.strip()
                else:
                    normalized_item[key] = value
            
            validated_data.append(normalized_item)
        
        return validated_data
    
    def _auto_detect_entity_types(self, data: List[Dict]) -> Dict[str, List[Dict]]:
        """Auto-detect entity types from data structure."""
        if not data or not isinstance(data, list):
            return {"provinces": [], "communes": [], "zones": [], "quartiers": []}
        
        # Look at the first item to determine type
        first_item = data[0]
        if not isinstance(first_item, dict):
            return {"provinces": [], "communes": [], "zones": [], "quartiers": []}
        
        keys = set(first_item.keys())
        
        # Determine entity type based on required fields
        if {"code", "name"} == keys or {"code", "name"}.issubset(keys):
            return {"provinces": data}
        elif {"code", "name", "capital", "province_code"}.issubset(keys):
            return {"communes": data}
        elif {"code", "name", "commune_code"}.issubset(keys):
            return {"zones": data}
        elif {"code", "name", "zone_code"}.issubset(keys):
            return {"quartiers": data}
        else:
            # Cannot determine type - return as provinces by default
            return {"provinces": data}
