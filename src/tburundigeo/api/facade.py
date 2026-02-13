"""Public API facade - simplified interface for end users."""

import os
from typing import Dict, List, Optional, Union

from tburundigeo.application.export import ExportService
from tburundigeo.application.hierarchy import HierarchyService
from tburundigeo.application.search import SearchService
from tburundigeo.application.statistics import StatisticsService
from tburundigeo.application.validation import ValidationService
from tburundigeo.common.exceptions import (
    TburundiGeoError,
    ProvinceNotFoundError,
    CommuneNotFoundError,
    ZoneNotFoundError,
    QuartierNotFoundError,
    InvalidCodeError,
    ReferentialIntegrityError,
)
from tburundigeo.domain.entities import Province, Commune, Zone, Quartier
from tburundigeo.infrastructure.repositories.py_file import (
    PyFileCommuneRepository,
    PyFileProvinceRepository,
    PyFileQuartierRepository,
    PyFileZoneRepository,
)

# Global instances for singleton pattern
_province_repo: Optional[PyFileProvinceRepository] = None
_commune_repo: Optional[PyFileCommuneRepository] = None
_zone_repo: Optional[PyFileZoneRepository] = None
_quartier_repo: Optional[PyFileQuartierRepository] = None

_hierarchy_service: Optional[HierarchyService] = None
_search_service: Optional[SearchService] = None
_statistics_service: Optional[StatisticsService] = None
_export_service: Optional[ExportService] = None
_validation_service: Optional[ValidationService] = None


def _get_repositories():
    """Get or create repository instances."""
    global _province_repo, _commune_repo, _zone_repo, _quartier_repo
    
    if _province_repo is None:
        data_source = os.getenv("TBURUNDIGEO_DATA_SOURCE", "tburundigeo.data")
        
        _province_repo = PyFileProvinceRepository(f"{data_source}.provinces")
        _commune_repo = PyFileCommuneRepository(f"{data_source}.communes")
        _zone_repo = PyFileZoneRepository(f"{data_source}.zones")
        _quartier_repo = PyFileQuartierRepository(f"{data_source}.quartiers")
    
    return _province_repo, _commune_repo, _zone_repo, _quartier_repo


def _get_services():
    """Get or create service instances."""
    global _hierarchy_service, _search_service, _statistics_service, _export_service, _validation_service
    
    province_repo, commune_repo, zone_repo, quartier_repo = _get_repositories()
    
    if _hierarchy_service is None:
        _hierarchy_service = HierarchyService(province_repo, commune_repo, zone_repo, quartier_repo)
        _search_service = SearchService(province_repo, commune_repo, zone_repo, quartier_repo)
        _statistics_service = StatisticsService(province_repo, commune_repo, zone_repo, quartier_repo)
        _export_service = ExportService(province_repo, commune_repo, zone_repo, quartier_repo)
        _validation_service = ValidationService(province_repo, commune_repo, zone_repo, quartier_repo)
    
    return _hierarchy_service, _search_service, _statistics_service, _export_service, _validation_service


def set_data_source(data_source: str) -> None:
    """Set the data source for all repositories."""
    global _province_repo, _commune_repo, _zone_repo, _quartier_repo
    global _hierarchy_service, _search_service, _statistics_service, _export_service, _validation_service
    
    # Reset all instances
    _province_repo = None
    _commune_repo = None
    _zone_repo = None
    _quartier_repo = None
    _hierarchy_service = None
    _search_service = None
    _statistics_service = None
    _export_service = None
    _validation_service = None
    
    # Set environment variable
    os.environ["TBURUNDIGEO_DATA_SOURCE"] = data_source


# Province functions
def get_all_provinces() -> List[Province]:
    """Get all provinces."""
    province_repo, _, _, _ = _get_repositories()
    return province_repo.get_all()

def get_province(code: str) -> Optional[Province]:
    """Get a province by its code."""
    province_repo, _, _, _ = _get_repositories()
    return province_repo.get_by_code(code)

def get_province_capital(code: str) -> Optional[str]:
    """Get the capital of a province by its code."""
    province_repo, _, _, _ = _get_repositories()
    province = province_repo.get_by_code(code)
    return province.capital if province else None

def search_provinces(query: str, search_by: str = "name") -> List[Province]:
    """Search provinces by name or code."""
    _, _, _, _ = _get_repositories()
    _, search_service, _, _, _ = _get_services()
    return search_service.search_provinces(query, search_by)

def count_provinces() -> int:
    """Count total number of provinces."""
    province_repo, _, _, _ = _get_repositories()
    return province_repo.count()


# Commune functions
def get_all_communes() -> List[Commune]:
    """Get all communes."""
    _, commune_repo, _, _ = _get_repositories()
    return commune_repo.get_all()


def get_commune(code: str) -> Optional[Commune]:
    """Get a commune by its code."""
    _, commune_repo, _, _ = _get_repositories()
    return commune_repo.get_by_code(code)


def get_communes_by_province(province_code: str) -> List[Commune]:
    """Get all communes in a province."""
    _, _, _, _ = _get_repositories()
    hierarchy_service, _, _, _, _ = _get_services()
    return hierarchy_service.get_communes_of_province(province_code)


def get_commune_capital(code: str) -> Optional[str]:
    """Get the capital of a commune by its code."""
    _, commune_repo, _, _ = _get_repositories()
    commune = commune_repo.get_by_code(code)
    return commune.capital if commune else None

def search_communes(query: str, search_by: str = "name") -> List[Commune]:
    """Search communes by name, capital, or code."""
    _, _, _, _ = _get_repositories()
    _, search_service, _, _, _ = _get_services()
    return search_service.search_communes(query, search_by)

def count_communes() -> int:
    """Count total number of communes."""
    _, commune_repo, _, _ = _get_repositories()
    return commune_repo.count()

def count_communes_in_province(province_code: str) -> int:
    """Count communes in a specific province."""
    _, _, _, _ = _get_repositories()
    _, _, statistics_service, _, _ = _get_services()
    return statistics_service.count_communes(province_code)

# Zone functions
def get_all_zones() -> List[Zone]:
    """Get all zones."""
    _, _, zone_repo, _ = _get_repositories()
    return zone_repo.get_all()


def get_zone(code: str) -> Optional[Zone]:
    """Get a zone by its code."""
    _, _, zone_repo, _ = _get_repositories()
    return zone_repo.get_by_code(code)


def get_zones_by_commune(commune_code: str) -> List[Zone]:
    """Get all zones in a commune."""
    _, _, _, _ = _get_repositories()
    hierarchy_service, _, _, _, _ = _get_services()
    return hierarchy_service.get_zones_of_commune(commune_code)


def get_zone_chief_town(code: str) -> Optional[str]:
    """Get the chief town of a zone by its code."""
    _, _, zone_repo, _ = _get_repositories()
    zone = zone_repo.get_by_code(code)
    return zone.chief_town if zone else None


def search_zones(query: str, search_by: str = "name") -> List[Zone]:
    """Search zones by name, chief town, or code."""
    _, _, _, _ = _get_repositories()
    _, search_service, _, _, _ = _get_services()
    return search_service.search_zones(query, search_by)


def count_zones() -> int:
    """Count total number of zones."""
    _, _, zone_repo, _ = _get_repositories()
    return zone_repo.count()


def count_zones_in_commune(commune_code: str) -> int:
    """Count zones in a specific commune."""
    _, _, _, _ = _get_repositories()
    _, _, statistics_service, _, _ = _get_services()
    return statistics_service.count_zones(commune_code)


# Quartier functions
def get_all_quartiers() -> List[Quartier]:
    """Get all quartiers."""
    _, _, _, quartier_repo = _get_repositories()
    return quartier_repo.get_all()


def get_quartier(code: str) -> Optional[Quartier]:
    """Get a quartier by its code."""
    _, _, _, quartier_repo = _get_repositories()
    return quartier_repo.get_by_code(code)


def get_quartiers_by_zone(zone_code: str) -> List[Quartier]:
    """Get all quartiers in a zone."""
    _, _, _, _ = _get_repositories()
    hierarchy_service, _, _, _, _ = _get_services()
    return hierarchy_service.get_quartiers_of_zone(zone_code)


def search_quartiers(query: str, search_by: str = "name") -> List[Quartier]:
    """Search quartiers by name or code."""
    _, _, _, _ = _get_repositories()
    _, search_service, _, _, _ = _get_services()
    return search_service.search_quartiers(query, search_by)


def count_quartiers() -> int:
    """Count total number of quartiers."""
    _, _, _, quartier_repo = _get_repositories()
    return quartier_repo.count()


def count_quartiers_in_zone(zone_code: str) -> int:
    """Count quartiers in a specific zone."""
    _, _, _, _ = _get_repositories()
    _, _, statistics_service, _, _ = _get_services()
    return statistics_service.count_quartiers(zone_code)


# Hierarchy functions
def get_full_hierarchy() -> Dict:
    """Get the complete administrative hierarchy."""
    _, _, _, _ = _get_repositories()
    hierarchy_service, _, _, _, _ = _get_services()
    return hierarchy_service.get_full_hierarchy()


def get_parent_province(commune_code: str) -> Optional[Province]:
    """Get the parent province of a commune."""
    _, _, _, _ = _get_repositories()
    hierarchy_service, _, _, _, _ = _get_services()
    return hierarchy_service.get_parent_province(commune_code)


def get_parent_commune(zone_code: str) -> Optional[Commune]:
    """Get the parent commune of a zone."""
    _, _, _, _ = _get_repositories()
    hierarchy_service, _, _, _, _ = _get_services()
    return hierarchy_service.get_parent_commune(zone_code)


def get_parent_zone(quartier_code: str) -> Optional[Zone]:
    """Get the parent zone of a quartier."""
    _, _, _, _ = _get_repositories()
    hierarchy_service, _, _, _, _ = _get_services()
    return hierarchy_service.get_parent_zone(quartier_code)


# Statistics functions
def get_statistics() -> Dict[str, int]:
    """Get comprehensive statistics about administrative divisions."""
    _, _, _, _ = _get_repositories()
    _, _, statistics_service, _, _ = _get_services()
    return {
        "summary": statistics_service.get_summary(),
        "averages": statistics_service.get_average_children_per_parent(),
        "distribution": statistics_service.get_distribution_statistics(),
    }


def get_summary() -> Dict[str, int]:
    """Get a quick summary of all administrative divisions."""
    _, _, _, _ = _get_repositories()
    _, _, statistics_service, _, _ = _get_services()
    return statistics_service.get_summary()


# Export functions
def export_to_json(include_hierarchy: bool = False, entity_types: Optional[List[str]] = None) -> str:
    """Export data to JSON format."""
    _, _, _, _ = _get_repositories()
    _, _, _, export_service, _ = _get_services()
    return export_service.export_to_json(include_hierarchy, entity_types)


def export_to_csv(entity_type: str, include_headers: bool = True) -> str:
    """Export data to CSV format."""
    _, _, _, _ = _get_repositories()
    _, _, _, export_service, _ = _get_services()
    return export_service.export_to_csv(entity_type, include_headers)


def export_to_yaml(include_hierarchy: bool = False, entity_types: Optional[List[str]] = None) -> str:
    """Export data to YAML format."""
    _, _, _, _ = _get_repositories()
    _, _, _, export_service, _ = _get_services()
    return export_service.export_to_yaml(include_hierarchy, entity_types)


# Validation functions
def validate_code(code: str, expected_level: Optional[str] = None) -> bool:
    """Validate if a code exists and optionally matches expected level."""
    _, _, _, _ = _get_repositories()
    _, _, _, _, validation_service = _get_services()
    return validation_service.validate_code(code, expected_level)


def check_referential_integrity() -> Dict[str, List[str]]:
    """Check referential integrity across all administrative levels."""
    _, _, _, _ = _get_repositories()
    _, _, _, _, validation_service = _get_services()
    return validation_service.check_referential_integrity()


# Detailed statistics functions
def get_province_statistics(province_code: str) -> Dict[str, int]:
    """Get detailed statistics for a specific province."""
    province_repo, commune_repo, zone_repo, quartier_repo = _get_repositories()
    
    # Check if province exists
    province = province_repo.get_by_code(province_code)
    if not province:
        raise ProvinceNotFoundError(province_code)
    
    # Get communes in province
    communes = commune_repo.get_by_province(province_code)
    
    # Get all zones and quartiers in those communes
    total_zones = 0
    total_quartiers = 0
    
    for commune in communes:
        zones = zone_repo.get_by_commune(commune.code)
        total_zones += len(zones)
        
        for zone in zones:
            quartiers = quartier_repo.get_by_zone(zone.code)
            total_quartiers += len(quartiers)
    
    return {
        "province_code": province_code,
        "province_name": province.name,
        "communes_count": len(communes),
        "zones_count": total_zones,
        "quartiers_count": total_quartiers
    }


def get_commune_statistics(commune_code: str) -> Dict[str, int]:
    """Get detailed statistics for a specific commune."""
    province_repo, commune_repo, zone_repo, quartier_repo = _get_repositories()
    
    # Check if commune exists
    commune = commune_repo.get_by_code(commune_code)
    if not commune:
        raise CommuneNotFoundError(commune_code)
    
    # Get province
    province = province_repo.get_by_code(commune.province_code)
    
    # Get zones and quartiers
    zones = zone_repo.get_by_commune(commune_code)
    total_quartiers = 0
    
    for zone in zones:
        quartiers = quartier_repo.get_by_zone(zone.code)
        total_quartiers += len(quartiers)
    
    return {
        "commune_code": commune_code,
        "commune_name": commune.name,
        "province_code": commune.province_code,
        "province_name": province.name if province else "Unknown",
        "zones_count": len(zones),
        "quartiers_count": total_quartiers
    }


def get_zone_statistics(zone_code: str) -> Dict[str, int]:
    """Get detailed statistics for a specific zone."""
    province_repo, commune_repo, zone_repo, quartier_repo = _get_repositories()
    
    # Check if zone exists
    zone = zone_repo.get_by_code(zone_code)
    if not zone:
        raise ZoneNotFoundError(zone_code)
    
    # Get commune and province
    commune = commune_repo.get_by_code(zone.commune_code)
    province = province_repo.get_by_code(commune.province_code) if commune else None
    
    # Get quartiers
    quartiers = quartier_repo.get_by_zone(zone_code)
    
    return {
        "zone_code": zone_code,
        "zone_name": zone.name,
        "commune_code": zone.commune_code,
        "commune_name": commune.name if commune else "Unknown",
        "province_code": province.code if province else "Unknown",
        "province_name": province.name if province else "Unknown",
        "quartiers_count": len(quartiers)
    }


def get_all_provinces_statistics() -> List[Dict[str, int]]:
    """Get detailed statistics for all provinces."""
    province_repo, _, _, _ = _get_repositories()
    provinces = province_repo.get_all()
    
    statistics = []
    for province in provinces:
        try:
            stats = get_province_statistics(province.code)
            statistics.append(stats)
        except Exception as e:
            print(f"Error getting stats for province {province.code}: {e}")
    
    return statistics


def get_all_communes_statistics() -> List[Dict[str, int]]:
    """Get detailed statistics for all communes."""
    _, commune_repo, _, _ = _get_repositories()
    communes = commune_repo.get_all()
    
    statistics = []
    for commune in communes:
        try:
            stats = get_commune_statistics(commune.code)
            statistics.append(stats)
        except Exception as e:
            print(f"Error getting stats for commune {commune.code}: {e}")
    
    return statistics


def get_all_zones_statistics() -> List[Dict[str, int]]:
    """Get detailed statistics for all zones."""
    _, _, zone_repo, _ = _get_repositories()
    zones = zone_repo.get_all()
    
    statistics = []
    for zone in zones:
        try:
            stats = get_zone_statistics(zone.code)
            statistics.append(stats)
        except Exception as e:
            print(f"Error getting stats for zone {zone.code}: {e}")
    
    return statistics
