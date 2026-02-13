"""Hierarchy service for navigating administrative divisions."""

from typing import Dict, List, Optional

from tburundigeo.common.exceptions import (
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


class HierarchyService:
    """Service for navigating the administrative hierarchy."""
    
    def __init__(
        self,
        province_repo: IProvinceRepository,
        commune_repo: ICommuneRepository,
        zone_repo: IZoneRepository,
        quartier_repo: IQuartierRepository,
    ) -> None:
        """Initialize hierarchy service with repositories."""
        self._province_repo = province_repo
        self._commune_repo = commune_repo
        self._zone_repo = zone_repo
        self._quartier_repo = quartier_repo
    
    def get_communes_of_province(self, province_code: str) -> List[Commune]:
        """Get all communes in a province."""
        if not self._province_repo.exists(province_code):
            raise ProvinceNotFoundError(province_code)
        
        return self._commune_repo.get_by_province(province_code)
    
    def get_zones_of_commune(self, commune_code: str) -> List[Zone]:
        """Get all zones in a commune."""
        if not self._commune_repo.exists(commune_code):
            raise CommuneNotFoundError(commune_code)
        
        return self._zone_repo.get_by_commune(commune_code)
    
    def get_quartiers_of_zone(self, zone_code: str) -> List[Quartier]:
        """Get all quartiers in a zone."""
        if not self._zone_repo.exists(zone_code):
            raise ZoneNotFoundError(zone_code)
        
        return self._quartier_repo.get_by_zone(zone_code)
    
    def get_parent_province(self, commune_code: str) -> Optional[Province]:
        """Get the parent province of a commune."""
        commune = self._commune_repo.get_by_code(commune_code)
        if commune is None:
            raise CommuneNotFoundError(commune_code)
        
        return self._province_repo.get_by_code(commune.province_code)
    
    def get_parent_commune(self, zone_code: str) -> Optional[Commune]:
        """Get the parent commune of a zone."""
        zone = self._zone_repo.get_by_code(zone_code)
        if zone is None:
            raise ZoneNotFoundError(zone_code)
        
        return self._commune_repo.get_by_code(zone.commune_code)
    
    def get_parent_zone(self, quartier_code: str) -> Optional[Zone]:
        """Get the parent zone of a quartier."""
        quartier = self._quartier_repo.get_by_code(quartier_code)
        if quartier is None:
            raise QuartierNotFoundError(quartier_code)
        
        return self._zone_repo.get_by_code(quartier.zone_code)
    
    def get_full_hierarchy(self) -> Dict[str, Dict]:
        """Get the complete administrative hierarchy as a nested dictionary."""
        hierarchy = {}
        
        # Get all provinces
        provinces = self._province_repo.get_all()
        
        for province in provinces:
            province_data = {
                "code": province.code,
                "name": province.name,
                "communes": {}
            }
            
            # Get communes for this province
            communes = self._commune_repo.get_by_province(province.code)
            
            for commune in communes:
                commune_data = {
                    "code": commune.code,
                    "name": commune.name,
                    "capital": commune.capital,
                    "zones": {}
                }
                
                # Get zones for this commune
                zones = self._zone_repo.get_by_commune(commune.code)
                
                for zone in zones:
                    zone_data = {
                        "code": zone.code,
                        "name": zone.name,
                        "quartiers": {}
                    }
                    
                    # Get quartiers for this zone
                    quartiers = self._quartier_repo.get_by_zone(zone.code)
                    
                    for quartier in quartiers:
                        zone_data["quartiers"][quartier.code] = {
                            "code": quartier.code,
                            "name": quartier.name
                        }
                    
                    commune_data["zones"][zone.code] = zone_data
                
                province_data["communes"][commune.code] = commune_data
            
            hierarchy[province.code] = province_data
        
        return hierarchy
    
    def get_hierarchy_path(self, code: str) -> List[Dict[str, str]]:
        """Get the complete path from province to quartier for any administrative code."""
        path = []
        
        # Try to find the entity by checking each repository
        if self._province_repo.exists(code):
            province = self._province_repo.get_by_code(code)
            if province:
                path.append({"level": "province", "code": province.code, "name": province.name})
        
        elif self._commune_repo.exists(code):
            commune = self._commune_repo.get_by_code(code)
            if commune:
                # Get parent province first
                province = self._province_repo.get_by_code(commune.province_code)
                if province:
                    path.append({"level": "province", "code": province.code, "name": province.name})
                
                path.append({"level": "commune", "code": commune.code, "name": commune.name})
        
        elif self._zone_repo.exists(code):
            zone = self._zone_repo.get_by_code(code)
            if zone:
                # Get parent commune and province
                commune = self._commune_repo.get_by_code(zone.commune_code)
                if commune:
                    province = self._province_repo.get_by_code(commune.province_code)
                    if province:
                        path.append({"level": "province", "code": province.code, "name": province.name})
                    
                    path.append({"level": "commune", "code": commune.code, "name": commune.name})
                
                path.append({"level": "zone", "code": zone.code, "name": zone.name})
        
        elif self._quartier_repo.exists(code):
            quartier = self._quartier_repo.get_by_code(code)
            if quartier:
                # Get parent zone, commune, and province
                zone = self._zone_repo.get_by_code(quartier.zone_code)
                if zone:
                    commune = self._commune_repo.get_by_code(zone.commune_code)
                    if commune:
                        province = self._province_repo.get_by_code(commune.province_code)
                        if province:
                            path.append({"level": "province", "code": province.code, "name": province.name})
                        
                        path.append({"level": "commune", "code": commune.code, "name": commune.name})
                    
                    path.append({"level": "zone", "code": zone.code, "name": zone.name})
                
                path.append({"level": "quartier", "code": quartier.code, "name": quartier.name})
        
        return path
    
    def get_children_count(self, code: str) -> Dict[str, int]:
        """Get the count of direct children for any administrative entity."""
        counts = {}
        
        if self._province_repo.exists(code):
            communes = self._commune_repo.get_by_province(code)
            counts["communes"] = len(communes)
            
            # Count zones and quartiers indirectly
            total_zones = 0
            total_quartiers = 0
            for commune in communes:
                zones = self._zone_repo.get_by_commune(commune.code)
                total_zones += len(zones)
                for zone in zones:
                    quartiers = self._quartier_repo.get_by_zone(zone.code)
                    total_quartiers += len(quartiers)
            
            counts["zones"] = total_zones
            counts["quartiers"] = total_quartiers
        
        elif self._commune_repo.exists(code):
            zones = self._zone_repo.get_by_commune(code)
            counts["zones"] = len(zones)
            
            # Count quartiers indirectly
            total_quartiers = 0
            for zone in zones:
                quartiers = self._quartier_repo.get_by_zone(zone.code)
                total_quartiers += len(quartiers)
            
            counts["quartiers"] = total_quartiers
        
        elif self._zone_repo.exists(code):
            quartiers = self._quartier_repo.get_by_zone(code)
            counts["quartiers"] = len(quartiers)
        
        return counts
