"""Repository implementations for different data sources."""

from tburundigeo.infrastructure.repositories.py_file import (
    PyFileProvinceRepository,
    PyFileCommuneRepository,
    PyFileZoneRepository,
    PyFileQuartierRepository,
)

from tburundigeo.infrastructure.repositories.memory import (
    MemoryProvinceRepository,
    MemoryCommuneRepository,
    MemoryZoneRepository,
    MemoryQuartierRepository,
)

__all__ = [
    # PyFile repositories
    "PyFileProvinceRepository",
    "PyFileCommuneRepository",
    "PyFileZoneRepository",
    "PyFileQuartierRepository",
    # Memory repositories
    "MemoryProvinceRepository",
    "MemoryCommuneRepository",
    "MemoryZoneRepository",
    "MemoryQuartierRepository",
]
