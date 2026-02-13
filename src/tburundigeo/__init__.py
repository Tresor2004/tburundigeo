"""
TBurundiGeo - Package Python pour les Données Administratives du Burundi

============================================================================

TBurundiGeo est un package Python robuste et complet pour exploiter les données 
administratives du Burundi (provinces, communes, zones, quartiers) avec 
leurs capitales et chefs-lieux respectifs.

🏗️ Architecture : Hexagonale (Clean Architecture)
👨‍💻 Développeur : NIYOMWUNGERE Tresor (travail solo)
🏢 Organisation : TELONA
📊 Données : 3044 quartiers, 451 zones, 42 communes, 5 provinces
📜 Conformité : Loi organique n°1/C5 du 16 mars 2023

============================================================================

Fonctionnalités principales :
- 📋 Accès aux données administratives (provinces, communes, zones, quartiers)
- 🏛️ Informations sur les capitales et chefs-lieux
- 🔍 Recherche avancée par nom ou code
- 📊 Statistiques détaillées par entité administrative
- 🌳 Hiérarchie administrative complète
- ✅ Validation de l'intégrité référentielle
- 📤 Export multi-formats (JSON, CSV, YAML)
- 🖥️ Interface CLI complète

============================================================================

Installation rapide :
    pip install tburundigeo

Utilisation simple :
    import tburundigeo
    
    # Obtenir toutes les provinces
    provinces = tburundigeo.get_all_provinces()
    
    # Statistiques détaillées
    stats = tburundigeo.get_province_statistics("BI-PR-01")

============================================================================
"""

__version__ = "1.0.0"
__author__ = "NIYOMWUNGERE Tresor"
__email__ = "tresor.getintuch@outlook.com"
__license__ = "MIT"
__description__ = "Package Python pour les données administratives du Burundi"
__url__ = "https://github.com/tresor2004/tburundigeo"
__documentation__ = "https://tburundigeo.readthedocs.io/"

# =============================================================================
# API PUBLIQUE - Interface principale pour les utilisateurs
# =============================================================================

from tburundigeo.api.facade import (
    # --- Provinces ---
    get_all_provinces,
    get_province,
    get_province_capital,
    search_provinces,
    count_provinces,
    
    # --- Communes ---
    get_all_communes,
    get_commune,
    get_communes_by_province,
    get_commune_capital,
    search_communes,
    count_communes,
    count_communes_in_province,
    
    # --- Zones ---
    get_all_zones,
    get_zone,
    get_zones_by_commune,
    get_zone_chief_town,
    search_zones,
    count_zones,
    count_zones_in_commune,
    
    # --- Quartiers ---
    get_all_quartiers,
    get_quartier,
    get_quartiers_by_zone,
    search_quartiers,
    count_quartiers,
    count_quartiers_in_zone,
    
    # --- Hiérarchie ---
    get_full_hierarchy,
    get_parent_province,
    get_parent_commune,
    get_parent_zone,
    
    # --- Statistiques détaillées ---
    get_province_statistics,
    get_commune_statistics,
    get_zone_statistics,
    get_all_provinces_statistics,
    get_all_communes_statistics,
    get_all_zones_statistics,
    
    # --- Export ---
    export_to_json,
    export_to_csv,
    export_to_yaml,
    
    # --- Validation ---
    validate_code,
    check_referential_integrity,
    
    # --- Configuration ---
    set_data_source,
    
    # --- Utilitaires ---
    get_statistics,
    get_summary,
)

# =============================================================================
# Exceptions publiques
# =============================================================================
from tburundigeo.common.exceptions import (
    TburundiGeoError,
    ProvinceNotFoundError,
    CommuneNotFoundError,
    ZoneNotFoundError,
    QuartierNotFoundError,
    InvalidCodeError,
    ReferentialIntegrityError,
    DataSourceError,
)

# =============================================================================
# Entités (pour les utilisateurs avancés)
# =============================================================================
from tburundigeo.domain.entities import (
    Province,
    Commune,
    Zone,
    Quartier,
)

# =============================================================================
# Export public
# =============================================================================
__all__ = [
    # --- Métadonnées ---
    "__version__",
    "__author__",
    "__email__",
    "__license__",
    "__description__",
    "__url__",
    "__documentation__",
    
    # --- Provinces ---
    "get_all_provinces",
    "get_province",
    "get_province_capital",
    "search_provinces",
    "count_provinces",
    
    # --- Communes ---
    "get_all_communes",
    "get_commune",
    "get_communes_by_province",
    "get_commune_capital",
    "search_communes",
    "count_communes",
    "count_communes_in_province",
    
    # --- Zones ---
    "get_all_zones",
    "get_zone",
    "get_zones_by_commune",
    "get_zone_chief_town",
    "search_zones",
    "count_zones",
    "count_zones_in_commune",
    
    # --- Quartiers ---
    "get_all_quartiers",
    "get_quartier",
    "get_quartiers_by_zone",
    "search_quartiers",
    "count_quartiers",
    "count_quartiers_in_zone",
    
    # --- Hiérarchie ---
    "get_full_hierarchy",
    "get_parent_province",
    "get_parent_commune",
    "get_parent_zone",
    
    # --- Statistiques détaillées ---
    "get_province_statistics",
    "get_commune_statistics",
    "get_zone_statistics",
    "get_all_provinces_statistics",
    "get_all_communes_statistics",
    "get_all_zones_statistics",
    
    # --- Export ---
    "export_to_json",
    "export_to_csv",
    "export_to_yaml",
    
    # --- Validation ---
    "validate_code",
    "check_referential_integrity",
    
    # --- Configuration ---
    "set_data_source",
    
    # --- Utilitaires ---
    "get_statistics",
    "get_summary",
    
    # --- Exceptions ---
    "TburundiGeoError",
    "ProvinceNotFoundError",
    "CommuneNotFoundError",
    "ZoneNotFoundError",
    "QuartierNotFoundError",
    "InvalidCodeError",
    "ReferentialIntegrityError",
    "DataSourceError",
    
    # --- Entités ---
    "Province",
    "Commune",
    "Zone",
    "Quartier",
]

# =============================================================================
# Configuration du logging pour le debug
# =============================================================================
import logging

# Créer un logger spécifique au package
logger = logging.getLogger(__name__)

# Niveau de log par défaut
logger.setLevel(logging.INFO)

# Éviter les logs dupliqués
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
