"""Tests for memory repository implementations."""

import pytest

from tburundigeo.domain.entities import Province, Commune, Zone, Quartier
from tburundigeo.infrastructure.repositories.memory import (
    MemoryProvinceRepository,
    MemoryCommuneRepository,
    MemoryZoneRepository,
    MemoryQuartierRepository,
)


class TestMemoryProvinceRepository:
    """Test cases for MemoryProvinceRepository."""
    
    def test_get_all(self, province_repo):
        """Test getting all provinces."""
        provinces = province_repo.get_all()
        assert len(provinces) == 3
        assert all(isinstance(p, Province) for p in provinces)
    
    def test_get_by_code(self, province_repo):
        """Test getting province by code."""
        province = province_repo.get_by_code("BI-PR-01")
        assert province is not None
        assert province.code == "BI-PR-01"
        assert province.name == "Bujumbura Mairie"
        
        # Test non-existent code
        province = province_repo.get_by_code("BI-PR-99")
        assert province is None
    
    def test_search_by_name(self, province_repo):
        """Test searching provinces by name."""
        results = province_repo.search_by_name("bujumbura")
        assert len(results) == 1
        assert results[0].code == "BI-PR-01"
        
        # Test case insensitive search
        results = province_repo.search_by_name("GITEGA")
        assert len(results) == 1
        assert results[0].code == "BI-PR-02"
        
        # Test no results
        results = province_repo.search_by_name("nonexistent")
        assert len(results) == 0
    
    def test_count(self, province_repo):
        """Test counting provinces."""
        assert province_repo.count() == 3
    
    def test_exists(self, province_repo):
        """Test checking if province exists."""
        assert province_repo.exists("BI-PR-01") is True
        assert province_repo.exists("BI-PR-99") is False
    
    def test_add_and_clear(self, province_repo):
        """Test adding and clearing provinces."""
        new_province = Province(code="BI-PR-04", name="Test Province")
        province_repo.add(new_province)
        
        assert province_repo.count() == 4
        assert province_repo.exists("BI-PR-04") is True
        
        province_repo.clear()
        assert province_repo.count() == 0


class TestMemoryCommuneRepository:
    """Test cases for MemoryCommuneRepository."""
    
    def test_get_all(self, commune_repo):
        """Test getting all communes."""
        communes = commune_repo.get_all()
        assert len(communes) == 3
        assert all(isinstance(c, Commune) for c in communes)
    
    def test_get_by_code(self, commune_repo):
        """Test getting commune by code."""
        commune = commune_repo.get_by_code("BI-CO-01-01")
        assert commune is not None
        assert commune.code == "BI-CO-01-01"
        assert commune.name == "Muha"
    
    def test_search_by_name(self, commune_repo):
        """Test searching communes by name."""
        results = commune_repo.search_by_name("muha")
        assert len(results) == 1
        assert results[0].code == "BI-CO-01-01"
    
    def test_search_by_capital(self, commune_repo):
        """Test searching communes by capital."""
        results = commune_repo.search_by_capital("mukaza")
        assert len(results) == 1
        assert results[0].code == "BI-CO-01-02"
    
    def test_get_by_province(self, commune_repo):
        """Test getting communes by province."""
        results = commune_repo.get_by_province("BI-PR-01")
        assert len(results) == 2
        assert all(c.province_code == "BI-PR-01" for c in results)
        
        results = commune_repo.get_by_province("BI-PR-02")
        assert len(results) == 1
        assert results[0].code == "BI-CO-02-01"
        
        # Test non-existent province
        results = commune_repo.get_by_province("BI-PR-99")
        assert len(results) == 0
    
    def test_count(self, commune_repo):
        """Test counting communes."""
        assert commune_repo.count() == 3
    
    def test_count_in_province(self, commune_repo):
        """Test counting communes in province."""
        assert commune_repo.count_in_province("BI-PR-01") == 2
        assert commune_repo.count_in_province("BI-PR-02") == 1
        assert commune_repo.count_in_province("BI-PR-99") == 0


class TestMemoryZoneRepository:
    """Test cases for MemoryZoneRepository."""
    
    def test_get_all(self, zone_repo):
        """Test getting all zones."""
        zones = zone_repo.get_all()
        assert len(zones) == 3
        assert all(isinstance(z, Zone) for z in zones)
    
    def test_get_by_code(self, zone_repo):
        """Test getting zone by code."""
        zone = zone_repo.get_by_code("BI-ZO-01-01-01")
        assert zone is not None
        assert zone.code == "BI-ZO-01-01-01"
        assert zone.name == "Kanyosha"
    
    def test_search_by_name(self, zone_repo):
        """Test searching zones by name."""
        results = zone_repo.search_by_name("kanyosha")
        assert len(results) == 1
        assert results[0].code == "BI-ZO-01-01-01"
    
    def test_get_by_commune(self, zone_repo):
        """Test getting zones by commune."""
        results = zone_repo.get_by_commune("BI-CO-01-01")
        assert len(results) == 2
        assert all(z.commune_code == "BI-CO-01-01" for z in results)
        
        results = zone_repo.get_by_commune("BI-CO-02-01")
        assert len(results) == 1
        assert results[0].code == "BI-ZO-02-01-01"
    
    def test_count(self, zone_repo):
        """Test counting zones."""
        assert zone_repo.count() == 3
    
    def test_count_in_commune(self, zone_repo):
        """Test counting zones in commune."""
        assert zone_repo.count_in_commune("BI-CO-01-01") == 2
        assert zone_repo.count_in_commune("BI-CO-02-01") == 1
        assert zone_repo.count_in_commune("BI-CO-99-99") == 0


class TestMemoryQuartierRepository:
    """Test cases for MemoryQuartierRepository."""
    
    def test_get_all(self, quartier_repo):
        """Test getting all quartiers."""
        quartiers = quartier_repo.get_all()
        assert len(quartiers) == 3
        assert all(isinstance(q, Quartier) for q in quartiers)
    
    def test_get_by_code(self, quartier_repo):
        """Test getting quartier by code."""
        quartier = quartier_repo.get_by_code("BI-QT-01-01-01-01")
        assert quartier is not None
        assert quartier.code == "BI-QT-01-01-01-01"
        assert quartier.name == "Gasekebuye"
    
    def test_search_by_name(self, quartier_repo):
        """Test searching quartiers by name."""
        results = quartier_repo.search_by_name("gasekebuye")
        assert len(results) == 1
        assert results[0].code == "BI-QT-01-01-01-01"
    
    def test_get_by_zone(self, quartier_repo):
        """Test getting quartiers by zone."""
        results = quartier_repo.get_by_zone("BI-ZO-01-01-01")
        assert len(results) == 2
        assert all(q.zone_code == "BI-ZO-01-01-01" for q in results)
        
        results = quartier_repo.get_by_zone("BI-ZO-01-01-02")
        assert len(results) == 1
        assert results[0].code == "BI-QT-01-01-02-01"
    
    def test_count(self, quartier_repo):
        """Test counting quartiers."""
        assert quartier_repo.count() == 3
    
    def test_count_in_zone(self, quartier_repo):
        """Test counting quartiers in zone."""
        assert quartier_repo.count_in_zone("BI-ZO-01-01-01") == 2
        assert quartier_repo.count_in_zone("BI-ZO-01-01-02") == 1
        assert quartier_repo.count_in_zone("BI-ZO-99-99-99") == 0
