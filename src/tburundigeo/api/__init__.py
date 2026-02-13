"""API layer - public facade for easy usage."""

from tburundigeo.api.facade import (
    # Provinces
    get_all_provinces,
    get_province,
    search_provinces,
    count_provinces,
    # Communes
    get_all_communes,
    get_commune,
    get_communes_by_province,
    search_communes,
    count_communes,
    count_communes_in_province,
    # Zones
    get_all_zones,
    get_zone,
    get_zones_by_commune,
    search_zones,
    count_zones,
    count_zones_in_commune,
    # Quartiers
    get_all_quartiers,
    get_quartier,
    get_quartiers_by_zone,
    search_quartiers,
    count_quartiers,
    count_quartiers_in_zone,
    # Hiérarchie
    get_full_hierarchy,
    get_parent_commune,
    get_parent_zone,
    get_parent_province,
    # Statistiques
    get_statistics,
    get_summary,
    # Export
    export_to_json,
    export_to_csv,
    export_to_yaml,
    # Validation
    validate_code,
    check_referential_integrity,
    # Configuration
    set_data_source,
)

__all__ = [
    # Provinces
    "get_all_provinces",
    "get_province",
    "search_provinces",
    "count_provinces",
    # Communes
    "get_all_communes",
    "get_commune",
    "get_communes_by_province",
    "search_communes",
    "count_communes",
    "count_communes_in_province",
    # Zones
    "get_all_zones",
    "get_zone",
    "get_zones_by_commune",
    "search_zones",
    "count_zones",
    "count_zones_in_commune",
    # Quartiers
    "get_all_quartiers",
    "get_quartier",
    "get_quartiers_by_zone",
    "search_quartiers",
    "count_quartiers",
    "count_quartiers_in_zone",
    # Hiérarchie
    "get_full_hierarchy",
    "get_parent_commune",
    "get_parent_zone",
    "get_parent_province",
    # Statistiques
    "get_statistics",
    "get_summary",
    # Export
    "export_to_json",
    "export_to_csv",
    "export_to_yaml",
    # Validation
    "validate_code",
    "check_referential_integrity",
    # Configuration
    "set_data_source",
]
