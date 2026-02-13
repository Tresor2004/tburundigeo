"""Tests complets pour TBurundiGeo - Couverture de toutes les fonctionnalités principales."""

import pytest
import json
from unittest.mock import patch, MagicMock

import sys
import os

# Ajouter le chemin src pour les imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import tburundigeo
from tburundigeo.common.exceptions import (
    TburundiGeoError,
    ProvinceNotFoundError,
    CommuneNotFoundError,
    ZoneNotFoundError,
    QuartierNotFoundError,
    InvalidCodeError,
    ReferentialIntegrityError,
)


class TestTBurundiGeoBasic:
    """Tests basiques de fonctionnement du package."""
    
    def test_package_import(self):
        """Test que le package s'importe correctement."""
        assert tburundigeo.__version__ == "1.0.0"
        assert tburundigeo.__author__ == "NIYOMWUNGERE Tresor"
        assert hasattr(tburundigeo, 'get_all_provinces')
    
    def test_get_all_provinces(self):
        """Test la récupération de toutes les provinces."""
        provinces = tburundigeo.get_all_provinces()
        assert len(provinces) == 5
        assert all(hasattr(p, 'code') for p in provinces)
        assert all(hasattr(p, 'name') for p in provinces)
        assert all(hasattr(p, 'capital') for p in provinces)
    
    def test_get_all_communes(self):
        """Test la récupération de toutes les communes."""
        communes = tburundigeo.get_all_communes()
        assert len(communes) == 42
        assert all(hasattr(c, 'code') for c in communes)
        assert all(hasattr(c, 'name') for c in communes)
        assert all(hasattr(c, 'capital') for c in communes)
    
    def test_get_all_zones(self):
        """Test la récupération de toutes les zones."""
        zones = tburundigeo.get_all_zones()
        assert len(zones) == 451
        assert all(hasattr(z, 'code') for z in zones)
        assert all(hasattr(z, 'name') for z in zones)
        assert all(hasattr(z, 'chief_town') for z in zones)
    
    def test_get_all_quartiers(self):
        """Test la récupération de tous les quartiers."""
        quartiers = tburundigeo.get_all_quartiers()
        assert len(quartiers) == 3044
        assert all(hasattr(q, 'code') for q in quartiers)
        assert all(hasattr(q, 'name') for q in quartiers)


class TestProvincesFunctionality:
    """Tests spécifiques aux fonctionnalités des provinces."""
    
    def test_get_province_valid(self):
        """Test la récupération d'une province valide."""
        province = tburundigeo.get_province("BI-PR-01")
        assert province is not None
        assert province.code == "BI-PR-01"
        assert hasattr(province, 'capital')
    
    def test_get_province_invalid(self):
        """Test la récupération d'une province invalide."""
        with pytest.raises(ProvinceNotFoundError):
            tburundigeo.get_province("INVALID_CODE")
    
    def test_get_province_capital(self):
        """Test la récupération de la capitale d'une province."""
        capital = tburundigeo.get_province_capital("BI-PR-01")
        assert capital is not None
        assert isinstance(capital, str)
        assert len(capital) > 0
    
    def test_search_provinces(self):
        """Test la recherche de provinces."""
        results = tburundigeo.search_provinces("BUJUMBURA")
        assert len(results) > 0
        assert all("BUJUMBURA" in p.name.upper() for p in results)
    
    def test_count_provinces(self):
        """Test le comptage des provinces."""
        count = tburundigeo.count_provinces()
        assert count == 5


class TestCommunesFunctionality:
    """Tests spécifiques aux fonctionnalités des communes."""
    
    def test_get_commune_valid(self):
        """Test la récupération d'une commune valide."""
        commune = tburundigeo.get_commune("BI-CO-01-01")
        assert commune is not None
        assert commune.code == "BI-CO-01-01"
        assert hasattr(commune, 'capital')
    
    def test_get_commune_invalid(self):
        """Test la récupération d'une commune invalide."""
        with pytest.raises(CommuneNotFoundError):
            tburundigeo.get_commune("INVALID")
    
    def test_get_communes_by_province(self):
        """Test la récupération des communes d'une province."""
        communes = tburundigeo.get_communes_by_province("BI-PR-01")
        assert len(communes) == 7
        assert all(c.province_code == "BI-PR-01" for c in communes)
    
    def test_count_communes_in_province(self):
        """Test le comptage des communes dans une province."""
        count = tburundigeo.count_communes_in_province("BI-PR-01")
        assert count == 7


class TestZonesFunctionality:
    """Tests spécifiques aux fonctionnalités des zones."""
    
    def test_get_zone_valid(self):
        """Test la récupération d'une zone valide."""
        zone = tburundigeo.get_zone("BI-ZO-01-01-01")
        assert zone is not None
        assert zone.code == "BI-ZO-01-01-01"
        assert hasattr(zone, 'chief_town')
    
    def test_get_zone_invalid(self):
        """Test la récupération d'une zone invalide."""
        with pytest.raises(ZoneNotFoundError):
            tburundigeo.get_zone("INVALID")
    
    def test_get_zones_by_commune(self):
        """Test la récupération des zones d'une commune."""
        zones = tburundigeo.get_zones_by_commune("BI-CO-01-01")
        assert len(zones) == 5
        assert all(z.commune_code == "BI-CO-01-01" for z in zones)
    
    def test_get_zone_chief_town(self):
        """Test la récupération du chef-lieu d'une zone."""
        chief_town = tburundigeo.get_zone_chief_town("BI-ZO-01-01-01")
        assert chief_town is not None
        assert isinstance(chief_town, str)
        assert len(chief_town) > 0


class TestQuartiersFunctionality:
    """Tests spécifiques aux fonctionnalités des quartiers."""
    
    def test_get_quartier_valid(self):
        """Test la récupération d'un quartier valide."""
        quartier = tburundigeo.get_quartier("BI-QT-01-01-01-01")
        assert quartier is not None
        assert quartier.code == "BI-QT-01-01-01-01"
    
    def test_get_quartier_invalid(self):
        """Test la récupération d'un quartier invalide."""
        with pytest.raises(QuartierNotFoundError):
            tburundigeo.get_quartier("INVALID")
    
    def test_get_quartiers_by_zone(self):
        """Test la récupération des quartiers d'une zone."""
        quartiers = tburundigeo.get_quartiers_by_zone("BI-ZO-01-01-01")
        assert len(quartiers) > 0
        assert all(q.zone_code == "BI-ZO-01-01-01" for q in quartiers)
    
    def test_count_quartiers_in_zone(self):
        """Test le comptage des quartiers dans une zone."""
        count = tburundigeo.count_quartiers_in_zone("BI-ZO-01-01-01")
        assert count > 0


class TestStatisticsFunctionality:
    """Tests des fonctionnalités de statistiques."""
    
    def test_get_statistics(self):
        """Test la récupération des statistiques générales."""
        stats = tburundigeo.get_statistics()
        assert 'summary' in stats
        assert stats['summary']['provinces'] == 5
        assert stats['summary']['communes'] == 42
        assert stats['summary']['zones'] == 451
        assert stats['summary']['quartiers'] == 3044
    
    def test_get_province_statistics(self):
        """Test les statistiques détaillées d'une province."""
        stats = tburundigeo.get_province_statistics("BI-PR-01")
        assert 'province_code' in stats
        assert 'province_name' in stats
        assert 'communes_count' in stats
        assert 'zones_count' in stats
        assert 'quartiers_count' in stats
        assert stats['communes_count'] == 7
    
    def test_get_commune_statistics(self):
        """Test les statistiques détaillées d'une commune."""
        stats = tburundigeo.get_commune_statistics("BI-CO-01-01")
        assert 'commune_code' in stats
        assert 'commune_name' in stats
        assert 'zones_count' in stats
        assert 'quartiers_count' in stats
    
    def test_get_zone_statistics(self):
        """Test les statistiques détaillées d'une zone."""
        stats = tburundigeo.get_zone_statistics("BI-ZO-01-01-01")
        assert 'zone_code' in stats
        assert 'zone_name' in stats
        assert 'quartiers_count' in stats


class TestHierarchyFunctionality:
    """Tests des fonctionnalités de hiérarchie."""
    
    def test_get_full_hierarchy(self):
        """Test la récupération de la hiérarchie complète."""
        hierarchy = tburundigeo.get_full_hierarchy()
        assert isinstance(hierarchy, dict)
        # Vérifier que la hiérarchie contient les provinces par code
        assert 'BI-PR-01' in hierarchy  # Vérifier une province spécifique
        assert 'BI-PR-02' in hierarchy  # Vérifier une autre province
    
    def test_get_parent_province(self):
        """Test la récupération de la province parente."""
        parent = tburundigeo.get_parent_province("BI-CO-01-01")
        assert parent is not None
        assert parent.code == "BI-PR-01"
    
    def test_get_parent_commune(self):
        """Test la récupération de la commune parente."""
        parent = tburundigeo.get_parent_commune("BI-ZO-01-01-01")
        assert parent is not None
        assert parent.code == "BI-CO-01-01"
    
    def test_get_parent_zone(self):
        """Test la récupération de la zone parente."""
        parent = tburundigeo.get_parent_zone("BI-QT-01-01-01-01")
        assert parent is not None
        assert parent.code == "BI-ZO-01-01-01"


class TestExportFunctionality:
    """Tests des fonctionnalités d'export."""
    
    def test_export_to_json(self):
        """Test l'export en JSON."""
        result = tburundigeo.export_to_json()
        assert isinstance(result, str)
        data = json.loads(result)
        assert 'provinces' in data
    
    def test_export_to_csv(self):
        """Test l'export en CSV."""
        result = tburundigeo.export_to_csv("provinces")
        assert isinstance(result, str)
        assert "code,name" in result  # En-tête sans capital pour provinces
        assert len(result.split('\n')) > 5  # Au moins 5 lignes (header + 5 provinces)


class TestValidationFunctionality:
    """Tests des fonctionnalités de validation."""
    
    def test_validate_code_valid(self):
        """Test la validation d'un code valide."""
        assert tburundigeo.validate_code("BI-PR-01", "province")
        assert tburundigeo.validate_code("BI-CO-01-01", "commune")
        assert tburundigeo.validate_code("BI-ZO-01-01-01", "zone")
        assert tburundigeo.validate_code("BI-QT-01-01-01-01", "quartier")
    
    def test_validate_code_invalid(self):
        """Test la validation d'un code invalide."""
        assert not tburundigeo.validate_code("INVALID")
        assert not tburundigeo.validate_code("BI-PR-01", "commune")  # Mauvais niveau
    
    def test_check_referential_integrity(self):
        """Test la vérification de l'intégrité référentielle."""
        integrity = tburundigeo.check_referential_integrity()
        assert isinstance(integrity, dict)
        # Ne devrait pas avoir d'erreurs avec les données corrigées
        total_errors = sum(len(errors) for errors in integrity.values())
        assert total_errors == 0


class TestErrorHandling:
    """Tests de gestion des erreurs."""
    
    def test_province_not_found_error(self):
        """Test l'erreur ProvinceNotFoundError."""
        error = ProvinceNotFoundError("BI-PR-99")
        assert "BI-PR-99" in str(error)
        assert error.code == "BI-PR-99"
    
    def test_commune_not_found_error(self):
        """Test l'erreur CommuneNotFoundError."""
        error = CommuneNotFoundError("BI-CO-99-99")
        assert "BI-CO-99-99" in str(error)
        assert error.code == "BI-CO-99-99"
    
    def test_zone_not_found_error(self):
        """Test l'erreur ZoneNotFoundError."""
        error = ZoneNotFoundError("BI-ZO-99-99-99")
        assert "BI-ZO-99-99-99" in str(error)
        assert error.code == "BI-ZO-99-99-99"
    
    def test_quartier_not_found_error(self):
        """Test l'erreur QuartierNotFoundError."""
        error = QuartierNotFoundError("BI-QT-99-99-99-99")
        assert "BI-QT-99-99-99-99" in str(error)
        assert error.code == "BI-QT-99-99-99-99"


class TestPerformance:
    """Tests de performance."""
    
    def test_performance_get_all_provinces(self):
        """Test les performances de récupération des provinces."""
        import time
        start_time = time.time()
        provinces = tburundigeo.get_all_provinces()
        end_time = time.time()
        assert len(provinces) == 5
        assert (end_time - start_time) < 0.1  # Moins de 100ms
    
    def test_performance_get_all_communes(self):
        """Test les performances de récupération des communes."""
        import time
        start_time = time.time()
        communes = tburundigeo.get_all_communes()
        end_time = time.time()
        assert len(communes) == 42
        assert (end_time - start_time) < 0.5  # Moins de 500ms
    
    def test_performance_get_all_quartiers(self):
        """Test les performances de récupération des quartiers."""
        import time
        start_time = time.time()
        quartiers = tburundigeo.get_all_quartiers()
        end_time = time.time()
        assert len(quartiers) == 3044
        assert (end_time - start_time) < 2.0  # Moins de 2s


if __name__ == "__main__":
    pytest.main([__file__])
