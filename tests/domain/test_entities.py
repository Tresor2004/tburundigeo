"""Tests for domain entities."""

import pytest

from tburundigeo.domain.entities import Province, Commune, Zone, Quartier


class TestProvince:
    """Test cases for Province entity."""
    
    def test_valid_province_creation(self):
        """Test creating a valid province."""
        province = Province(code="BI-PR-01", name="Bujumbura Mairie")
        
        assert province.code == "BI-PR-01"
        assert province.name == "Bujumbura Mairie"
        assert str(province) == "Province(BI-PR-01: Bujumbura Mairie)"
    
    def test_invalid_province_code_format(self):
        """Test province with invalid code format."""
        with pytest.raises(ValueError, match="Invalid province code format"):
            Province(code="INVALID", name="Test")
        
        with pytest.raises(ValueError, match="Invalid province code format"):
            Province(code="BI-PR-1", name="Test")  # Missing digit
    
    def test_empty_province_code(self):
        """Test province with empty code."""
        with pytest.raises(ValueError, match="Province code must be a non-empty string"):
            Province(code="", name="Test")
    
    def test_empty_province_name(self):
        """Test province with empty name."""
        with pytest.raises(ValueError, match="Province name must be a non-empty string"):
            Province(code="BI-PR-01", name="")
        
        with pytest.raises(ValueError, match="Province name must be at least 2 characters long"):
            Province(code="BI-PR-01", name="A")
    
    def test_province_immutability(self):
        """Test that province is immutable."""
        province = Province(code="BI-PR-01", name="Test")
        
        with pytest.raises(AttributeError):
            province.code = "BI-PR-02"
        
        with pytest.raises(AttributeError):
            province.name = "New Name"


class TestCommune:
    """Test cases for Commune entity."""
    
    def test_valid_commune_creation(self):
        """Test creating a valid commune."""
        commune = Commune(
            code="BI-CO-01-01",
            name="Muha",
            capital="Muha",
            province_code="BI-PR-01"
        )
        
        assert commune.code == "BI-CO-01-01"
        assert commune.name == "Muha"
        assert commune.capital == "Muha"
        assert commune.province_code == "BI-PR-01"
        assert str(commune) == "Commune(BI-CO-01-01: Muha, Capital: Muha)"
    
    def test_invalid_commune_code_format(self):
        """Test commune with invalid code format."""
        with pytest.raises(ValueError, match="Invalid commune code format"):
            Commune(
                code="INVALID",
                name="Test",
                capital="Test",
                province_code="BI-PR-01"
            )
    
    def test_invalid_province_code_reference(self):
        """Test commune with invalid province code format."""
        with pytest.raises(ValueError, match="Invalid province code format"):
            Commune(
                code="BI-CO-01-01",
                name="Test",
                capital="Test",
                province_code="INVALID"
            )
    
    def test_missing_required_fields(self):
        """Test commune with missing required fields."""
        with pytest.raises(ValueError, match="Commune name must be a non-empty string"):
            Commune(
                code="BI-CO-01-01",
                name="",
                capital="Test",
                province_code="BI-PR-01"
            )
        
        with pytest.raises(ValueError, match="Commune capital must be a non-empty string"):
            Commune(
                code="BI-CO-01-01",
                name="Test",
                capital="",
                province_code="BI-PR-01"
            )


class TestZone:
    """Test cases for Zone entity."""
    
    def test_valid_zone_creation(self):
        """Test creating a valid zone."""
        zone = Zone(
            code="BI-ZO-01-01-01",
            name="Kanyosha",
            commune_code="BI-CO-01-01"
        )
        
        assert zone.code == "BI-ZO-01-01-01"
        assert zone.name == "Kanyosha"
        assert zone.commune_code == "BI-CO-01-01"
        assert str(zone) == "Zone(BI-ZO-01-01-01: Kanyosha)"
    
    def test_invalid_zone_code_format(self):
        """Test zone with invalid code format."""
        with pytest.raises(ValueError, match="Invalid zone code format"):
            Zone(
                code="INVALID",
                name="Test",
                commune_code="BI-CO-01-01"
            )
    
    def test_invalid_commune_code_reference(self):
        """Test zone with invalid commune code format."""
        with pytest.raises(ValueError, match="Invalid commune code format"):
            Zone(
                code="BI-ZO-01-01-01",
                name="Test",
                commune_code="INVALID"
            )


class TestQuartier:
    """Test cases for Quartier entity."""
    
    def test_valid_quartier_creation(self):
        """Test creating a valid quartier."""
        quartier = Quartier(
            code="BI-QT-01-01-01-01",
            name="Gasekebuye",
            zone_code="BI-ZO-01-01-01"
        )
        
        assert quartier.code == "BI-QT-01-01-01-01"
        assert quartier.name == "Gasekebuye"
        assert quartier.zone_code == "BI-ZO-01-01-01"
        assert str(quartier) == "Quartier(BI-QT-01-01-01-01: Gasekebuye)"
    
    def test_invalid_quartier_code_format(self):
        """Test quartier with invalid code format."""
        with pytest.raises(ValueError, match="Invalid quartier code format"):
            Quartier(
                code="INVALID",
                name="Test",
                zone_code="BI-ZO-01-01-01"
            )
    
    def test_invalid_zone_code_reference(self):
        """Test quartier with invalid zone code format."""
        with pytest.raises(ValueError, match="Invalid zone code format"):
            Quartier(
                code="BI-QT-01-01-01-01",
                name="Test",
                zone_code="INVALID"
            )
