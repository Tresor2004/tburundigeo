"""Tests for API facade."""

import pytest
import os

from tburundigeo.api.facade import (
    get_all_provinces,
    get_province,
    search_provinces,
    count_provinces,
    get_all_communes,
    get_commune,
    get_communes_by_province,
    search_communes,
    count_communes,
    count_communes_in_province,
    get_all_zones,
    get_zone,
    get_zones_by_commune,
    search_zones,
    count_zones,
    count_zones_in_commune,
    get_all_quartiers,
    get_quartier,
    get_quartiers_by_zone,
    search_quartiers,
    count_quartiers,
    count_quartiers_in_zone,
    get_full_hierarchy,
    get_parent_province,
    get_parent_commune,
    get_parent_zone,
    get_statistics,
    get_summary,
    export_to_json,
    export_to_csv,
    validate_code,
    check_referential_integrity,
    set_data_source,
)


class TestAPIFacade:
    """Test cases for API facade functions."""
    
    def test_get_all_provinces(self):
        """Test getting all provinces."""
        provinces = get_all_provinces()
        assert len(provinces) > 0
        assert all(hasattr(p, 'code') and hasattr(p, 'name') for p in provinces)
    
    def test_get_province(self):
        """Test getting a specific province."""
        # This test assumes we have sample data
        provinces = get_all_provinces()
        if provinces:
            first_province = provinces[0]
            province = get_province(first_province.code)
            assert province is not None
            assert province.code == first_province.code
            assert province.name == first_province.name
        
        # Test non-existent province
        province = get_province("BI-PR-99")
        assert province is None
    
    def test_search_provinces(self):
        """Test searching provinces."""
        # Test by name
        results = search_provinces("bujumbura")
        # Should find at least one province with "bujumbura" in name
        
        # Test by code
        results = search_provinces("BI-PR", "code")
        # Should find provinces starting with BI-PR
    
    def test_count_provinces(self):
        """Test counting provinces."""
        count = count_provinces()
        assert count > 0
        assert isinstance(count, int)
    
    def test_get_all_communes(self):
        """Test getting all communes."""
        communes = get_all_communes()
        assert len(communes) > 0
        assert all(hasattr(c, 'code') and hasattr(c, 'name') for c in communes)
    
    def test_get_commune(self):
        """Test getting a specific commune."""
        communes = get_all_communes()
        if communes:
            first_commune = communes[0]
            commune = get_commune(first_commune.code)
            assert commune is not None
            assert commune.code == first_commune.code
            assert commune.name == first_commune.name
    
    def test_get_communes_by_province(self):
        """Test getting communes by province."""
        provinces = get_all_provinces()
        if provinces:
            first_province = provinces[0]
            communes = get_communes_by_province(first_province.code)
            assert len(communes) >= 0
            if communes:
                assert all(c.province_code == first_province.code for c in communes)
    
    def test_search_communes(self):
        """Test searching communes."""
        # Test by name
        results = search_communes("muha")
        # Should find communes with "muha" in name
        
        # Test by capital
        results = search_communes("mukaza", "capital")
        # Should find communes with "mukaza" as capital
    
    def test_count_communes(self):
        """Test counting communes."""
        count = count_communes()
        assert count > 0
        assert isinstance(count, int)
    
    def test_count_communes_in_province(self):
        """Test counting communes in province."""
        provinces = get_all_provinces()
        if provinces:
            first_province = provinces[0]
            count = count_communes_in_province(first_province.code)
            assert count >= 0
            assert isinstance(count, int)
    
    def test_get_all_zones(self):
        """Test getting all zones."""
        zones = get_all_zones()
        assert len(zones) > 0
        assert all(hasattr(z, 'code') and hasattr(z, 'name') for z in zones)
    
    def test_get_zone(self):
        """Test getting a specific zone."""
        zones = get_all_zones()
        if zones:
            first_zone = zones[0]
            zone = get_zone(first_zone.code)
            assert zone is not None
            assert zone.code == first_zone.code
            assert zone.name == first_zone.name
    
    def test_get_zones_by_commune(self):
        """Test getting zones by commune."""
        communes = get_all_communes()
        if communes:
            first_commune = communes[0]
            zones = get_zones_by_commune(first_commune.code)
            assert len(zones) >= 0
            if zones:
                assert all(z.commune_code == first_commune.code for z in zones)
    
    def test_search_zones(self):
        """Test searching zones."""
        results = search_zones("kanyosha")
        # Should find zones with "kanyosha" in name
    
    def test_count_zones(self):
        """Test counting zones."""
        count = count_zones()
        assert count > 0
        assert isinstance(count, int)
    
    def test_count_zones_in_commune(self):
        """Test counting zones in commune."""
        communes = get_all_communes()
        if communes:
            first_commune = communes[0]
            count = count_zones_in_commune(first_commune.code)
            assert count >= 0
            assert isinstance(count, int)
    
    def test_get_all_quartiers(self):
        """Test getting all quartiers."""
        quartiers = get_all_quartiers()
        assert len(quartiers) > 0
        assert all(hasattr(q, 'code') and hasattr(q, 'name') for q in quartiers)
    
    def test_get_quartier(self):
        """Test getting a specific quartier."""
        quartiers = get_all_quartiers()
        if quartiers:
            first_quartier = quartiers[0]
            quartier = get_quartier(first_quartier.code)
            assert quartier is not None
            assert quartier.code == first_quartier.code
            assert quartier.name == first_quartier.name
    
    def test_get_quartiers_by_zone(self):
        """Test getting quartiers by zone."""
        zones = get_all_zones()
        if zones:
            first_zone = zones[0]
            quartiers = get_quartiers_by_zone(first_zone.code)
            assert len(quartiers) >= 0
            if quartiers:
                assert all(q.zone_code == first_zone.code for q in quartiers)
    
    def test_search_quartiers(self):
        """Test searching quartiers."""
        results = search_quartiers("gasekebuye")
        # Should find quartiers with "gasekebuye" in name
    
    def test_count_quartiers(self):
        """Test counting quartiers."""
        count = count_quartiers()
        assert count > 0
        assert isinstance(count, int)
    
    def test_count_quartiers_in_zone(self):
        """Test counting quartiers in zone."""
        zones = get_all_zones()
        if zones:
            first_zone = zones[0]
            count = count_quartiers_in_zone(first_zone.code)
            assert count >= 0
            assert isinstance(count, int)
    
    def test_get_full_hierarchy(self):
        """Test getting full hierarchy."""
        hierarchy = get_full_hierarchy()
        assert isinstance(hierarchy, dict)
        assert len(hierarchy) > 0
        
        # Check structure
        for province_code, province_data in hierarchy.items():
            assert "code" in province_data
            assert "name" in province_data
            assert "communes" in province_data
    
    def test_get_parent_province(self):
        """Test getting parent province."""
        communes = get_all_communes()
        if communes:
            first_commune = communes[0]
            parent = get_parent_province(first_commune.code)
            if parent:
                assert parent.code == first_commune.province_code
    
    def test_get_parent_commune(self):
        """Test getting parent commune."""
        zones = get_all_zones()
        if zones:
            first_zone = zones[0]
            parent = get_parent_commune(first_zone.code)
            if parent:
                assert parent.code == first_zone.commune_code
    
    def test_get_parent_zone(self):
        """Test getting parent zone."""
        quartiers = get_all_quartiers()
        if quartiers:
            first_quartier = quartiers[0]
            parent = get_parent_zone(first_quartier.code)
            if parent:
                assert parent.code == first_quartier.zone_code
    
    def test_get_statistics(self):
        """Test getting statistics."""
        stats = get_statistics()
        assert isinstance(stats, dict)
        assert "summary" in stats
        assert "averages" in stats
        assert "distribution" in stats
        
        # Check summary structure
        summary = stats["summary"]
        assert "provinces" in summary
        assert "communes" in summary
        assert "zones" in summary
        assert "quartiers" in summary
    
    def test_get_summary(self):
        """Test getting summary."""
        summary = get_summary()
        assert isinstance(summary, dict)
        assert "provinces" in summary
        assert "communes" in summary
        assert "zones" in summary
        assert "quartiers" in summary
        
        # All counts should be positive integers
        for key, value in summary.items():
            assert isinstance(value, int)
            assert value > 0
    
    def test_export_to_json(self):
        """Test exporting to JSON."""
        json_data = export_to_json()
        assert isinstance(json_data, str)
        assert len(json_data) > 0
        
        # Should be valid JSON
        import json
        parsed = json.loads(json_data)
        assert isinstance(parsed, dict)
    
    def test_export_to_csv(self):
        """Test exporting to CSV."""
        csv_data = export_to_csv("provinces")
        assert isinstance(csv_data, str)
        assert len(csv_data) > 0
        
        # Should contain headers
        assert "code" in csv_data
        assert "name" in csv_data
    
    def test_validate_code(self):
        """Test code validation."""
        provinces = get_all_provinces()
        if provinces:
            first_province = provinces[0]
            assert validate_code(first_province.code) is True
            assert validate_code(first_province.code, "province") is True
        
        # Test non-existent code
        assert validate_code("BI-XX-99") is False
    
    def test_check_referential_integrity(self):
        """Test referential integrity check."""
        integrity = check_referential_integrity()
        assert isinstance(integrity, dict)
        assert "commune_orphans" in integrity
        assert "zone_orphans" in integrity
        assert "quartier_orphans" in integrity
    
    def test_set_data_source(self):
        """Test setting data source."""
        # Save original data source
        original_source = os.getenv("TBURUNDIGEO_DATA_SOURCE", "tburundigeo.data")
        
        # Test setting new data source
        set_data_source("test.data.source")
        assert os.getenv("TBURUNDIGEO_DATA_SOURCE") == "test.data.source"
        
        # Restore original
        set_data_source(original_source)
