"""Domain layer - core business entities and interfaces."""

from tburundigeo.domain.entities import (
    Province,
    Commune,
    Zone,
    Quartier,
)

from tburundigeo.domain.interfaces import (
    IProvinceRepository,
    ICommuneRepository,
    IZoneRepository,
    IQuartierRepository,
)

__all__ = [
    # Entities
    "Province",
    "Commune", 
    "Zone",
    "Quartier",
    # Interfaces
    "IProvinceRepository",
    "ICommuneRepository",
    "IZoneRepository",
    "IQuartierRepository",
]
