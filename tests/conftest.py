"""Pytest configuration and fixtures for tburundigeo tests."""

import pytest
from typing import List

from tburundigeo.domain.entities import Province, Commune, Zone, Quartier
from tburundigeo.infrastructure.repositories.memory import (
    MemoryProvinceRepository,
    MemoryCommuneRepository,
    MemoryZoneRepository,
    MemoryQuartierRepository,
)


@pytest.fixture
def sample_provinces() -> List[Province]:
    """Sample provinces for testing."""
    return [
        Province(code="BI-PR-01", name="Bujumbura Mairie"),
        Province(code="BI-PR-02", name="Gitega"),
        Province(code="BI-PR-03", name="Muyinga"),
    ]


@pytest.fixture
def sample_communes() -> List[Commune]:
    """Sample communes for testing."""
    return [
        Commune(
            code="BI-CO-01-01",
            name="Muha",
            capital="Muha",
            province_code="BI-PR-01"
        ),
        Commune(
            code="BI-CO-01-02",
            name="Mukaza",
            capital="Mukaza",
            province_code="BI-PR-01"
        ),
        Commune(
            code="BI-CO-02-01",
            name="Gitega Centre",
            capital="Gitega",
            province_code="BI-PR-02"
        ),
    ]


@pytest.fixture
def sample_zones() -> List[Zone]:
    """Sample zones for testing."""
    return [
        Zone(
            code="BI-ZO-01-01-01",
            name="Kanyosha",
            commune_code="BI-CO-01-01"
        ),
        Zone(
            code="BI-ZO-01-01-02",
            name="Kinindo",
            commune_code="BI-CO-01-01"
        ),
        Zone(
            code="BI-ZO-02-01-01",
            name="Gitega Centre",
            commune_code="BI-CO-02-01"
        ),
    ]


@pytest.fixture
def sample_quartiers() -> List[Quartier]:
    """Sample quartiers for testing."""
    return [
        Quartier(
            code="BI-QT-01-01-01-01",
            name="Gasekebuye",
            zone_code="BI-ZO-01-01-01"
        ),
        Quartier(
            code="BI-QT-01-01-01-02",
            name="Kigwati",
            zone_code="BI-ZO-01-01-01"
        ),
        Quartier(
            code="BI-QT-01-01-02-01",
            name="Kinindo I",
            zone_code="BI-ZO-01-01-02"
        ),
    ]


@pytest.fixture
def province_repo(sample_provinces: List[Province]) -> MemoryProvinceRepository:
    """Memory province repository with sample data."""
    return MemoryProvinceRepository(sample_provinces)


@pytest.fixture
def commune_repo(sample_communes: List[Commune]) -> MemoryCommuneRepository:
    """Memory commune repository with sample data."""
    return MemoryCommuneRepository(sample_communes)


@pytest.fixture
def zone_repo(sample_zones: List[Zone]) -> MemoryZoneRepository:
    """Memory zone repository with sample data."""
    return MemoryZoneRepository(sample_zones)


@pytest.fixture
def quartier_repo(sample_quartiers: List[Quartier]) -> MemoryQuartierRepository:
    """Memory quartier repository with sample data."""
    return MemoryQuartierRepository(sample_quartiers)
