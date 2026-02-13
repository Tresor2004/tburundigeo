"""Tests for HierarchyService."""

import pytest

from tburundigeo.application.hierarchy import HierarchyService
from tburundigeo.common.exceptions import (
    ProvinceNotFoundError,
    CommuneNotFoundError,
    ZoneNotFoundError,
)


class TestHierarchyService:
    """Test cases for HierarchyService."""
    
    def test_get_communes_of_province(self, province_repo, commune_repo, zone_repo, quartier_repo):
        """Test getting communes of a province."""
        service = HierarchyService(province_repo, commune_repo, zone_repo, quartier_repo)
        
        communes = service.get_communes_of_province("BI-PR-01")
        assert len(communes) == 2
        assert all(c.province_code == "BI-PR-01" for c in communes)
        
        # Test non-existent province
        with pytest.raises(ProvinceNotFoundError):
            service.get_communes_of_province("BI-PR-99")
    
    def test_get_zones_of_commune(self, province_repo, commune_repo, zone_repo, quartier_repo):
        """Test getting zones of a commune."""
        service = HierarchyService(province_repo, commune_repo, zone_repo, quartier_repo)
        
        zones = service.get_zones_of_commune("BI-CO-01-01")
        assert len(zones) == 2
        assert all(z.commune_code == "BI-CO-01-01" for z in zones)
        
        # Test non-existent commune
        with pytest.raises(CommuneNotFoundError):
            service.get_zones_of_commune("BI-CO-99-99")
    
    def test_get_quartiers_of_zone(self, province_repo, commune_repo, zone_repo, quartier_repo):
        """Test getting quartiers of a zone."""
        service = HierarchyService(province_repo, commune_repo, zone_repo, quartier_repo)
        
        quartiers = service.get_quartiers_of_zone("BI-ZO-01-01-01")
        assert len(quartiers) == 2
        assert all(q.zone_code == "BI-ZO-01-01-01" for q in quartiers)
        
        # Test non-existent zone
        with pytest.raises(ZoneNotFoundError):
            service.get_quartiers_of_zone("BI-ZO-99-99-99")
    
    def test_get_parent_province(self, province_repo, commune_repo, zone_repo, quartier_repo):
        """Test getting parent province of a commune."""
        service = HierarchyService(province_repo, commune_repo, zone_repo, quartier_repo)
        
        province = service.get_parent_province("BI-CO-01-01")
        assert province is not None
        assert province.code == "BI-PR-01"
        assert province.name == "Bujumbura Mairie"
        
        # Test non-existent commune
        with pytest.raises(CommuneNotFoundError):
            service.get_parent_province("BI-CO-99-99")
    
    def test_get_parent_commune(self, province_repo, commune_repo, zone_repo, quartier_repo):
        """Test getting parent commune of a zone."""
        service = HierarchyService(province_repo, commune_repo, zone_repo, quartier_repo)
        
        commune = service.get_parent_commune("BI-ZO-01-01-01")
        assert commune is not None
        assert commune.code == "BI-CO-01-01"
        assert commune.name == "Muha"
        
        # Test non-existent zone
        with pytest.raises(ZoneNotFoundError):
            service.get_parent_commune("BI-ZO-99-99-99")
    
    def test_get_parent_zone(self, province_repo, commune_repo, zone_repo, quartier_repo):
        """Test getting parent zone of a quartier."""
        service = HierarchyService(province_repo, commune_repo, zone_repo, quartier_repo)
        
        zone = service.get_parent_zone("BI-QT-01-01-01-01")
        assert zone is not None
        assert zone.code == "BI-ZO-01-01-01"
        assert zone.name == "Kanyosha"
        
        # Test non-existent quartier
        with pytest.raises(ZoneNotFoundError):
            service.get_parent_zone("BI-QT-99-99-99-99")
    
    def test_get_full_hierarchy(self, province_repo, commune_repo, zone_repo, quartier_repo):
        """Test getting full hierarchy."""
        service = HierarchyService(province_repo, commune_repo, zone_repo, quartier_repo)
        
        hierarchy = service.get_full_hierarchy()
        
        assert "BI-PR-01" in hierarchy
        assert "BI-PR-02" in hierarchy
        assert "BI-PR-03" in hierarchy
        
        # Check structure for BI-PR-01
        province_data = hierarchy["BI-PR-01"]
        assert province_data["code"] == "BI-PR-01"
        assert province_data["name"] == "Bujumbura Mairie"
        assert "communes" in province_data
        
        # Check communes for BI-PR-01
        communes = province_data["communes"]
        assert "BI-CO-01-01" in communes
        assert "BI-CO-01-02" in communes
        
        # Check zones for BI-CO-01-01
        commune_data = communes["BI-CO-01-01"]
        assert commune_data["code"] == "BI-CO-01-01"
        assert "zones" in commune_data
        
        zones = commune_data["zones"]
        assert "BI-ZO-01-01-01" in zones
        assert "BI-ZO-01-01-02" in zones
    
    def test_get_hierarchy_path_province(self, province_repo, commune_repo, zone_repo, quartier_repo):
        """Test getting hierarchy path for province."""
        service = HierarchyService(province_repo, commune_repo, zone_repo, quartier_repo)
        
        path = service.get_hierarchy_path("BI-PR-01")
        assert len(path) == 1
        assert path[0]["level"] == "province"
        assert path[0]["code"] == "BI-PR-01"
        assert path[0]["name"] == "Bujumbura Mairie"
    
    def test_get_hierarchy_path_commune(self, province_repo, commune_repo, zone_repo, quartier_repo):
        """Test getting hierarchy path for commune."""
        service = HierarchyService(province_repo, commune_repo, zone_repo, quartier_repo)
        
        path = service.get_hierarchy_path("BI-CO-01-01")
        assert len(path) == 2
        assert path[0]["level"] == "province"
        assert path[0]["code"] == "BI-PR-01"
        assert path[1]["level"] == "commune"
        assert path[1]["code"] == "BI-CO-01-01"
    
    def test_get_hierarchy_path_zone(self, province_repo, commune_repo, zone_repo, quartier_repo):
        """Test getting hierarchy path for zone."""
        service = HierarchyService(province_repo, commune_repo, zone_repo, quartier_repo)
        
        path = service.get_hierarchy_path("BI-ZO-01-01-01")
        assert len(path) == 3
        assert path[0]["level"] == "province"
        assert path[1]["level"] == "commune"
        assert path[2]["level"] == "zone"
    
    def test_get_hierarchy_path_quartier(self, province_repo, commune_repo, zone_repo, quartier_repo):
        """Test getting hierarchy path for quartier."""
        service = HierarchyService(province_repo, commune_repo, zone_repo, quartier_repo)
        
        path = service.get_hierarchy_path("BI-QT-01-01-01-01")
        assert len(path) == 4
        assert path[0]["level"] == "province"
        assert path[1]["level"] == "commune"
        assert path[2]["level"] == "zone"
        assert path[3]["level"] == "quartier"
    
    def test_get_hierarchy_path_nonexistent(self, province_repo, commune_repo, zone_repo, quartier_repo):
        """Test getting hierarchy path for non-existent code."""
        service = HierarchyService(province_repo, commune_repo, zone_repo, quartier_repo)
        
        path = service.get_hierarchy_path("BI-XX-99-99-99-99")
        assert len(path) == 0
    
    def test_get_children_count_province(self, province_repo, commune_repo, zone_repo, quartier_repo):
        """Test getting children count for province."""
        service = HierarchyService(province_repo, commune_repo, zone_repo, quartier_repo)
        
        counts = service.get_children_count("BI-PR-01")
        assert counts["communes"] == 2
        assert counts["zones"] == 2  # 2 zones in BI-CO-01-01
        assert counts["quartiers"] == 3  # 2 in BI-ZO-01-01-01, 1 in BI-ZO-01-01-02
    
    def test_get_children_count_commune(self, province_repo, commune_repo, zone_repo, quartier_repo):
        """Test getting children count for commune."""
        service = HierarchyService(province_repo, commune_repo, zone_repo, quartier_repo)
        
        counts = service.get_children_count("BI-CO-01-01")
        assert counts["zones"] == 2
        assert counts["quartiers"] == 3  # 2 in BI-ZO-01-01-01, 1 in BI-ZO-01-01-02
    
    def test_get_children_count_zone(self, province_repo, commune_repo, zone_repo, quartier_repo):
        """Test getting children count for zone."""
        service = HierarchyService(province_repo, commune_repo, zone_repo, quartier_repo)
        
        counts = service.get_children_count("BI-ZO-01-01-01")
        assert counts["quartiers"] == 2
    
    def test_get_children_count_nonexistent(self, province_repo, commune_repo, zone_repo, quartier_repo):
        """Test getting children count for non-existent code."""
        service = HierarchyService(province_repo, commune_repo, zone_repo, quartier_repo)
        
        counts = service.get_children_count("BI-XX-99-99-99-99")
        assert counts == {}
