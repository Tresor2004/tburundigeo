"""Export service for administrative divisions data."""

import csv
import json
from io import StringIO
from typing import Any, Dict, List, Optional, Union

from tburundigeo.common.exceptions import InvalidCodeError
from tburundigeo.common.types import ExportFormat
from tburundigeo.domain.entities import Province, Commune, Zone, Quartier
from tburundigeo.domain.interfaces import (
    IProvinceRepository,
    ICommuneRepository,
    IZoneRepository,
    IQuartierRepository,
)


class ExportService:
    """Service for exporting administrative divisions data."""
    
    def __init__(
        self,
        province_repo: IProvinceRepository,
        commune_repo: ICommuneRepository,
        zone_repo: IZoneRepository,
        quartier_repo: IQuartierRepository,
    ) -> None:
        """Initialize export service with repositories."""
        self._province_repo = province_repo
        self._commune_repo = commune_repo
        self._zone_repo = zone_repo
        self._quartier_repo = quartier_repo
    
    def export_to_json(
        self,
        include_hierarchy: bool = False,
        entity_types: Optional[List[str]] = None
    ) -> str:
        """Export data to JSON format."""
        if entity_types is None:
            entity_types = ["provinces", "communes", "zones", "quartiers"]
        
        data: Dict[str, Any] = {}
        
        if "provinces" in entity_types:
            data["provinces"] = [
                {
                    "code": province.code,
                    "name": province.name
                }
                for province in self._province_repo.get_all()
            ]
        
        if "communes" in entity_types:
            data["communes"] = [
                {
                    "code": commune.code,
                    "name": commune.name,
                    "capital": commune.capital,
                    "province_code": commune.province_code
                }
                for commune in self._commune_repo.get_all()
            ]
        
        if "zones" in entity_types:
            data["zones"] = [
                {
                    "code": zone.code,
                    "name": zone.name,
                    "commune_code": zone.commune_code
                }
                for zone in self._zone_repo.get_all()
            ]
        
        if "quartiers" in entity_types:
            data["quartiers"] = [
                {
                    "code": quartier.code,
                    "name": quartier.name,
                    "zone_code": quartier.zone_code
                }
                for quartier in self._quartier_repo.get_all()
            ]
        
        if include_hierarchy:
            # Import here to avoid circular imports
            from tburundigeo.application.hierarchy import HierarchyService
            
            hierarchy_service = HierarchyService(
                self._province_repo,
                self._commune_repo,
                self._zone_repo,
                self._quartier_repo
            )
            data["hierarchy"] = hierarchy_service.get_full_hierarchy()
        
        return json.dumps(data, indent=2, ensure_ascii=False)
    
    def export_to_csv(
        self,
        entity_type: str,
        include_headers: bool = True
    ) -> str:
        """Export data to CSV format."""
        output = StringIO()
        writer = None
        
        if entity_type == "provinces":
            if include_headers:
                writer = csv.DictWriter(output, fieldnames=["code", "name"])
                writer.writeheader()
            else:
                writer = csv.DictWriter(output, fieldnames=["code", "name"])
            
            for province in self._province_repo.get_all():
                writer.writerow({
                    "code": province.code,
                    "name": province.name
                })
        
        elif entity_type == "communes":
            if include_headers:
                writer = csv.DictWriter(output, fieldnames=["code", "name", "capital", "province_code"])
                writer.writeheader()
            else:
                writer = csv.DictWriter(output, fieldnames=["code", "name", "capital", "province_code"])
            
            for commune in self._commune_repo.get_all():
                writer.writerow({
                    "code": commune.code,
                    "name": commune.name,
                    "capital": commune.capital,
                    "province_code": commune.province_code
                })
        
        elif entity_type == "zones":
            if include_headers:
                writer = csv.DictWriter(output, fieldnames=["code", "name", "commune_code"])
                writer.writeheader()
            else:
                writer = csv.DictWriter(output, fieldnames=["code", "name", "commune_code"])
            
            for zone in self._zone_repo.get_all():
                writer.writerow({
                    "code": zone.code,
                    "name": zone.name,
                    "commune_code": zone.commune_code
                })
        
        elif entity_type == "quartiers":
            if include_headers:
                writer = csv.DictWriter(output, fieldnames=["code", "name", "zone_code"])
                writer.writeheader()
            else:
                writer = csv.DictWriter(output, fieldnames=["code", "name", "zone_code"])
            
            for quartier in self._quartier_repo.get_all():
                writer.writerow({
                    "code": quartier.code,
                    "name": quartier.name,
                    "zone_code": quartier.zone_code
                })
        
        else:
            raise InvalidCodeError(entity_type, f"Unknown entity type: {entity_type}")
        
        output.seek(0)
        return output.read()
    
    def export_to_yaml(
        self,
        include_hierarchy: bool = False,
        entity_types: Optional[List[str]] = None
    ) -> str:
        """Export data to YAML format."""
        try:
            import yaml
        except ImportError:
            raise ImportError("PyYAML is required for YAML export. Install with: pip install tburundigeo[yaml]")
        
        # Get JSON data first
        json_data = json.loads(self.export_to_json(include_hierarchy, entity_types))
        
        return yaml.dump(json_data, default_flow_style=False, allow_unicode=True)
    
    def export_to_geojson(self, entity_type: str) -> str:
        """Export data to GeoJSON format (simplified, without actual geometry)."""
        features = []
        
        if entity_type == "provinces":
            for province in self._province_repo.get_all():
                feature = {
                    "type": "Feature",
                    "properties": {
                        "code": province.code,
                        "name": province.name,
                        "level": "province"
                    },
                    "geometry": None  # Would need actual geometry data
                }
                features.append(feature)
        
        elif entity_type == "communes":
            for commune in self._commune_repo.get_all():
                feature = {
                    "type": "Feature",
                    "properties": {
                        "code": commune.code,
                        "name": commune.name,
                        "capital": commune.capital,
                        "province_code": commune.province_code,
                        "level": "commune"
                    },
                    "geometry": None
                }
                features.append(feature)
        
        elif entity_type == "zones":
            for zone in self._zone_repo.get_all():
                feature = {
                    "type": "Feature",
                    "properties": {
                        "code": zone.code,
                        "name": zone.name,
                        "commune_code": zone.commune_code,
                        "level": "zone"
                    },
                    "geometry": None
                }
                features.append(feature)
        
        elif entity_type == "quartiers":
            for quartier in self._quartier_repo.get_all():
                feature = {
                    "type": "Feature",
                    "properties": {
                        "code": quartier.code,
                        "name": quartier.name,
                        "zone_code": quartier.zone_code,
                        "level": "quartier"
                    },
                    "geometry": None
                }
                features.append(feature)
        
        else:
            raise InvalidCodeError(entity_type, f"Unknown entity type: {entity_type}")
        
        geojson = {
            "type": "FeatureCollection",
            "features": features
        }
        
        return json.dumps(geojson, indent=2, ensure_ascii=False)
    
    def export_hierarchy_flat(self) -> str:
        """Export hierarchy as a flat table with parent relationships."""
        data = []
        
        # Provinces
        for province in self._province_repo.get_all():
            data.append({
                "code": province.code,
                "name": province.name,
                "level": "province",
                "parent_code": None,
                "parent_name": None
            })
        
        # Communes
        for commune in self._commune_repo.get_all():
            parent_province = self._province_repo.get_by_code(commune.province_code)
            data.append({
                "code": commune.code,
                "name": commune.name,
                "level": "commune",
                "parent_code": commune.province_code,
                "parent_name": parent_province.name if parent_province else None
            })
        
        # Zones
        for zone in self._zone_repo.get_all():
            parent_commune = self._commune_repo.get_by_code(zone.commune_code)
            data.append({
                "code": zone.code,
                "name": zone.name,
                "level": "zone",
                "parent_code": zone.commune_code,
                "parent_name": parent_commune.name if parent_commune else None
            })
        
        # Quartiers
        for quartier in self._quartier_repo.get_all():
            parent_zone = self._zone_repo.get_by_code(quartier.zone_code)
            data.append({
                "code": quartier.code,
                "name": quartier.name,
                "level": "quartier",
                "parent_code": quartier.zone_code,
                "parent_name": parent_zone.name if parent_zone else None
            })
        
        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=["code", "name", "level", "parent_code", "parent_name"])
        writer.writeheader()
        writer.writerows(data)
        
        output.seek(0)
        return output.read()
    
    def export_summary_statistics(self) -> str:
        """Export summary statistics as JSON."""
        from tburundigeo.application.statistics import StatisticsService
        
        stats_service = StatisticsService(
            self._province_repo,
            self._commune_repo,
            self._zone_repo,
            self._quartier_repo
        )
        
        summary = stats_service.get_summary()
        averages = stats_service.get_average_children_per_parent()
        distribution = stats_service.get_distribution_statistics()
        
        data = {
            "summary": summary,
            "averages": averages,
            "distribution": distribution
        }
        
        return json.dumps(data, indent=2, ensure_ascii=False)
    
    def export_to_dataframe(self, entity_type: str):
        """Export data to pandas DataFrame (optional dependency)."""
        try:
            import pandas as pd
        except ImportError:
            raise ImportError("pandas is required for DataFrame export. Install with: pip install tburundigeo[pandas]")
        
        if entity_type == "provinces":
            data = [
                {
                    "code": province.code,
                    "name": province.name
                }
                for province in self._province_repo.get_all()
            ]
        
        elif entity_type == "communes":
            data = [
                {
                    "code": commune.code,
                    "name": commune.name,
                    "capital": commune.capital,
                    "province_code": commune.province_code
                }
                for commune in self._commune_repo.get_all()
            ]
        
        elif entity_type == "zones":
            data = [
                {
                    "code": zone.code,
                    "name": zone.name,
                    "commune_code": zone.commune_code
                }
                for zone in self._zone_repo.get_all()
            ]
        
        elif entity_type == "quartiers":
            data = [
                {
                    "code": quartier.code,
                    "name": quartier.name,
                    "zone_code": quartier.zone_code
                }
                for quartier in self._quartier_repo.get_all()
            ]
        
        else:
            raise InvalidCodeError(entity_type, f"Unknown entity type: {entity_type}")
        
        return pd.DataFrame(data)
