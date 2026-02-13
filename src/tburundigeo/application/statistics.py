"""Statistics service for administrative divisions analysis."""

from typing import Dict, List, Optional, Tuple

from tburundigeo.common.exceptions import (
    ProvinceNotFoundError,
    CommuneNotFoundError,
    ZoneNotFoundError,
)
from tburundigeo.domain.entities import Province, Commune, Zone, Quartier
from tburundigeo.domain.interfaces import (
    IProvinceRepository,
    ICommuneRepository,
    IZoneRepository,
    IQuartierRepository,
)


class StatisticsService:
    """Service for generating statistics about administrative divisions."""
    
    def __init__(
        self,
        province_repo: IProvinceRepository,
        commune_repo: ICommuneRepository,
        zone_repo: IZoneRepository,
        quartier_repo: IQuartierRepository,
    ) -> None:
        """Initialize statistics service with repositories."""
        self._province_repo = province_repo
        self._commune_repo = commune_repo
        self._zone_repo = zone_repo
        self._quartier_repo = quartier_repo
    
    def get_summary(self) -> Dict[str, int]:
        """Get a global summary of all administrative divisions."""
        return {
            "provinces": self._province_repo.count(),
            "communes": self._commune_repo.count(),
            "zones": self._zone_repo.count(),
            "quartiers": self._quartier_repo.count(),
        }
    
    def count_communes(self, province_code: Optional[str] = None) -> int:
        """Count communes, optionally filtered by province."""
        if province_code is None:
            return self._commune_repo.count()
        else:
            if not self._province_repo.exists(province_code):
                raise ProvinceNotFoundError(province_code)
            return self._commune_repo.count_in_province(province_code)
    
    def count_zones(self, commune_code: Optional[str] = None) -> int:
        """Count zones, optionally filtered by commune."""
        if commune_code is None:
            return self._zone_repo.count()
        else:
            if not self._commune_repo.exists(commune_code):
                raise CommuneNotFoundError(commune_code)
            return self._zone_repo.count_in_commune(commune_code)
    
    def count_quartiers(self, zone_code: Optional[str] = None) -> int:
        """Count quartiers, optionally filtered by zone."""
        if zone_code is None:
            return self._quartier_repo.count()
        else:
            if not self._zone_repo.exists(zone_code):
                raise ZoneNotFoundError(zone_code)
            return self._quartier_repo.count_in_zone(zone_code)
    
    def get_provinces_by_commune_count(self, descending: bool = True) -> List[Tuple[Province, int]]:
        """Get provinces sorted by number of communes."""
        provinces = self._province_repo.get_all()
        province_counts = []
        
        for province in provinces:
            commune_count = self._commune_repo.count_in_province(province.code)
            province_counts.append((province, commune_count))
        
        # Sort by commune count
        province_counts.sort(key=lambda x: x[1], reverse=descending)
        return province_counts
    
    def get_communes_by_zone_count(self, province_code: Optional[str] = None, descending: bool = True) -> List[Tuple[Commune, int]]:
        """Get communes sorted by number of zones."""
        if province_code:
            if not self._province_repo.exists(province_code):
                raise ProvinceNotFoundError(province_code)
            communes = self._commune_repo.get_by_province(province_code)
        else:
            communes = self._commune_repo.get_all()
        
        commune_counts = []
        
        for commune in communes:
            zone_count = self._zone_repo.count_in_commune(commune.code)
            commune_counts.append((commune, zone_count))
        
        # Sort by zone count
        commune_counts.sort(key=lambda x: x[1], reverse=descending)
        return commune_counts
    
    def get_zones_by_quartier_count(self, commune_code: Optional[str] = None, descending: bool = True) -> List[Tuple[Zone, int]]:
        """Get zones sorted by number of quartiers."""
        if commune_code:
            if not self._commune_repo.exists(commune_code):
                raise CommuneNotFoundError(commune_code)
            zones = self._zone_repo.get_by_commune(commune_code)
        else:
            zones = self._zone_repo.get_all()
        
        zone_counts = []
        
        for zone in zones:
            quartier_count = self._quartier_repo.count_in_zone(zone.code)
            zone_counts.append((zone, quartier_count))
        
        # Sort by quartier count
        zone_counts.sort(key=lambda x: x[1], reverse=descending)
        return zone_counts
    
    def get_average_children_per_parent(self) -> Dict[str, float]:
        """Get average number of children per parent at each level."""
        summary = self.get_summary()
        
        averages = {}
        
        if summary["provinces"] > 0:
            averages["communes_per_province"] = summary["communes"] / summary["provinces"]
        
        if summary["communes"] > 0:
            averages["zones_per_commune"] = summary["zones"] / summary["communes"]
        
        if summary["zones"] > 0:
            averages["quartiers_per_zone"] = summary["quartiers"] / summary["zones"]
        
        return averages
    
    def get_distribution_statistics(self) -> Dict[str, Dict[str, float]]:
        """Get distribution statistics (min, max, average, median) for each level."""
        stats = {}
        
        # Province -> Communes distribution
        province_commune_counts = [
            self._commune_repo.count_in_province(province.code)
            for province in self._province_repo.get_all()
        ]
        
        if province_commune_counts:
            stats["communes_per_province"] = self._calculate_distribution_stats(province_commune_counts)
        
        # Commune -> Zones distribution
        commune_zone_counts = [
            self._zone_repo.count_in_commune(commune.code)
            for commune in self._commune_repo.get_all()
        ]
        
        if commune_zone_counts:
            stats["zones_per_commune"] = self._calculate_distribution_stats(commune_zone_counts)
        
        # Zone -> Quartiers distribution
        zone_quartier_counts = [
            self._quartier_repo.count_in_zone(zone.code)
            for zone in self._zone_repo.get_all()
        ]
        
        if zone_quartier_counts:
            stats["quartiers_per_zone"] = self._calculate_distribution_stats(zone_quartier_counts)
        
        return stats
    
    def get_province_statistics(self, province_code: str) -> Dict[str, int]:
        """Get detailed statistics for a specific province."""
        if not self._province_repo.exists(province_code):
            raise ProvinceNotFoundError(province_code)
        
        province = self._province_repo.get_by_code(province_code)
        if province is None:
            raise ProvinceNotFoundError(province_code)
        
        communes = self._commune_repo.get_by_province(province_code)
        total_zones = 0
        total_quartiers = 0
        
        for commune in communes:
            zones = self._zone_repo.get_by_commune(commune.code)
            total_zones += len(zones)
            
            for zone in zones:
                quartiers = self._quartier_repo.get_by_zone(zone.code)
                total_quartiers += len(quartiers)
        
        return {
            "province_code": province_code,
            "province_name": province.name,
            "communes": len(communes),
            "zones": total_zones,
            "quartiers": total_quartiers,
        }
    
    def get_commune_statistics(self, commune_code: str) -> Dict[str, int]:
        """Get detailed statistics for a specific commune."""
        commune = self._commune_repo.get_by_code(commune_code)
        if commune is None:
            raise CommuneNotFoundError(commune_code)
        
        zones = self._zone_repo.get_by_commune(commune_code)
        total_quartiers = 0
        
        for zone in zones:
            quartiers = self._quartier_repo.get_by_zone(zone.code)
            total_quartiers += len(quartiers)
        
        return {
            "commune_code": commune_code,
            "commune_name": commune.name,
            "commune_capital": commune.capital,
            "province_code": commune.province_code,
            "zones": len(zones),
            "quartiers": total_quartiers,
        }
    
    def get_zone_statistics(self, zone_code: str) -> Dict[str, int]:
        """Get detailed statistics for a specific zone."""
        zone = self._zone_repo.get_by_code(zone_code)
        if zone is None:
            raise ZoneNotFoundError(zone_code)
        
        quartiers = self._quartier_repo.get_by_zone(zone_code)
        
        # Find parent commune
        commune = self._commune_repo.get_by_code(zone.commune_code)
        commune_name = commune.name if commune else "Unknown"
        
        return {
            "zone_code": zone_code,
            "zone_name": zone.name,
            "commune_code": zone.commune_code,
            "commune_name": commune_name,
            "quartiers": len(quartiers),
        }
    
    def _calculate_distribution_stats(self, values: List[int]) -> Dict[str, float]:
        """Calculate min, max, average, and median for a list of values."""
        if not values:
            return {}
        
        sorted_values = sorted(values)
        n = len(values)
        
        # Calculate median
        if n % 2 == 0:
            median = (sorted_values[n//2 - 1] + sorted_values[n//2]) / 2
        else:
            median = sorted_values[n//2]
        
        return {
            "min": float(min(values)),
            "max": float(max(values)),
            "average": float(sum(values) / n),
            "median": float(median),
        }
