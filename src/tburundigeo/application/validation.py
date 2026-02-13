"""Validation service for administrative divisions data."""

import re
from typing import Dict, List, Optional, Set

from tburundigeo.common.exceptions import (
    InvalidCodeError,
    ReferentialIntegrityError,
    ProvinceNotFoundError,
    CommuneNotFoundError,
    ZoneNotFoundError,
    QuartierNotFoundError,
)
from tburundigeo.domain.interfaces import (
    IProvinceRepository,
    ICommuneRepository,
    IZoneRepository,
    IQuartierRepository,
)


class ValidationService:
    """Service for validating administrative divisions data."""
    
    def __init__(
        self,
        province_repo: IProvinceRepository,
        commune_repo: ICommuneRepository,
        zone_repo: IZoneRepository,
        quartier_repo: IQuartierRepository,
    ) -> None:
        """Initialize validation service with repositories."""
        self._province_repo = province_repo
        self._commune_repo = commune_repo
        self._zone_repo = zone_repo
        self._quartier_repo = quartier_repo
    
    def validate_code(self, code: str, expected_level: Optional[str] = None) -> bool:
        """Validate if a code exists and optionally matches expected level."""
        exists = False
        
        if expected_level is None or expected_level == "province":
            if self._province_repo.exists(code):
                return expected_level is None or expected_level == "province"
        
        if expected_level is None or expected_level == "commune":
            if self._commune_repo.exists(code):
                return expected_level is None or expected_level == "commune"
        
        if expected_level is None or expected_level == "zone":
            if self._zone_repo.exists(code):
                return expected_level is None or expected_level == "zone"
        
        if expected_level is None or expected_level == "quartier":
            if self._quartier_repo.exists(code):
                return expected_level is None or expected_level == "quartier"
        
        return False
    
    def validate_code_format(self, code: str, expected_level: str) -> bool:
        """Validate the format of an administrative code."""
        patterns = {
            "province": r'^BI-PR-\d{2}$',
            "commune": r'^BI-CO-\d{2}-\d{2}$',
            "zone": r'^BI-ZO-\d{2}-\d{2}-\d{2}$',
            "quartier": r'^BI-QT-\d{2}-\d{2}-\d{2}-\d{2}$'
        }
        
        if expected_level not in patterns:
            raise InvalidCodeError(code, f"Unknown level: {expected_level}")
        
        pattern = patterns[expected_level]
        return bool(re.match(pattern, code))
    
    def check_referential_integrity(self) -> Dict[str, List[str]]:
        """Check referential integrity across all administrative levels."""
        errors = {
            "commune_orphans": [],
            "zone_orphans": [],
            "quartier_orphans": []
        }
        
        # Get all valid parent codes
        province_codes = {province.code for province in self._province_repo.get_all()}
        commune_codes = {commune.code for commune in self._commune_repo.get_all()}
        zone_codes = {zone.code for zone in self._zone_repo.get_all()}
        
        # Check communes
        for commune in self._commune_repo.get_all():
            if commune.province_code not in province_codes:
                errors["commune_orphans"].append(f"Commune {commune.code} references non-existent province {commune.province_code}")
        
        # Check zones
        for zone in self._zone_repo.get_all():
            if zone.commune_code not in commune_codes:
                errors["zone_orphans"].append(f"Zone {zone.code} references non-existent commune {zone.commune_code}")
        
        # Check quartiers
        for quartier in self._quartier_repo.get_all():
            if quartier.zone_code not in zone_codes:
                errors["quartier_orphans"].append(f"Quartier {quartier.code} references non-existent zone {quartier.zone_code}")
        
        return errors
    
    def validate_hierarchy_consistency(self) -> List[str]:
        """Validate that the hierarchy is consistent (no cycles, proper nesting)."""
        issues = []
        
        # Check for code format consistency
        for province in self._province_repo.get_all():
            if not self.validate_code_format(province.code, "province"):
                issues.append(f"Province {province.code} has invalid format")
        
        for commune in self._commune_repo.get_all():
            if not self.validate_code_format(commune.code, "commune"):
                issues.append(f"Commune {commune.code} has invalid format")
            
            # Check that commune code prefix matches province code
            expected_prefix = commune.province_code.replace("PR", "CO").replace("-PR-", "-CO-")
            if not commune.code.startswith(expected_prefix[:8]):  # First 8 chars: BI-CO-XX
                issues.append(f"Commune {commune.code} doesn't match province {commune.province_code} prefix")
        
        for zone in self._zone_repo.get_all():
            if not self.validate_code_format(zone.code, "zone"):
                issues.append(f"Zone {zone.code} has invalid format")
            
            # Check that zone code prefix matches commune code
            expected_prefix = zone.commune_code.replace("CO", "ZO").replace("-CO-", "-ZO-")
            if not zone.code.startswith(expected_prefix[:11]):  # First 11 chars: BI-ZO-XX-YY
                issues.append(f"Zone {zone.code} doesn't match commune {zone.commune_code} prefix")
        
        for quartier in self._quartier_repo.get_all():
            if not self.validate_code_format(quartier.code, "quartier"):
                issues.append(f"Quartier {quartier.code} has invalid format")
            
            # Check that quartier code prefix matches zone code
            expected_prefix = quartier.zone_code.replace("ZO", "QT").replace("-ZO-", "-QT-")
            if not quartier.code.startswith(expected_prefix[:14]):  # First 14 chars: BI-QT-XX-YY-ZZ
                issues.append(f"Quartier {quartier.code} doesn't match zone {quartier.zone_code} prefix")
        
        return issues
    
    def validate_data_completeness(self) -> Dict[str, List[str]]:
        """Validate that all required fields are present and non-empty."""
        issues = {
            "provinces": [],
            "communes": [],
            "zones": [],
            "quartiers": []
        }
        
        # Check provinces
        for province in self._province_repo.get_all():
            if not province.code or not province.code.strip():
                issues["provinces"].append("Province with empty code found")
            if not province.name or not province.name.strip():
                issues["provinces"].append(f"Province {province.code} has empty name")
        
        # Check communes
        for commune in self._commune_repo.get_all():
            if not commune.code or not commune.code.strip():
                issues["communes"].append("Commune with empty code found")
            if not commune.name or not commune.name.strip():
                issues["communes"].append(f"Commune {commune.code} has empty name")
            if not commune.capital or not commune.capital.strip():
                issues["communes"].append(f"Commune {commune.code} has empty capital")
            if not commune.province_code or not commune.province_code.strip():
                issues["communes"].append(f"Commune {commune.code} has empty province_code")
        
        # Check zones
        for zone in self._zone_repo.get_all():
            if not zone.code or not zone.code.strip():
                issues["zones"].append("Zone with empty code found")
            if not zone.name or not zone.name.strip():
                issues["zones"].append(f"Zone {zone.code} has empty name")
            if not zone.commune_code or not zone.commune_code.strip():
                issues["zones"].append(f"Zone {zone.code} has empty commune_code")
        
        # Check quartiers
        for quartier in self._quartier_repo.get_all():
            if not quartier.code or not quartier.code.strip():
                issues["quartiers"].append("Quartier with empty code found")
            if not quartier.name or not quartier.name.strip():
                issues["quartiers"].append(f"Quartier {quartier.code} has empty name")
            if not quartier.zone_code or not quartier.zone_code.strip():
                issues["quartiers"].append(f"Quartier {quartier.code} has empty zone_code")
        
        return issues
    
    def validate_unique_codes(self) -> Dict[str, List[str]]:
        """Validate that all codes are unique within their level."""
        issues = {
            "provinces": [],
            "communes": [],
            "zones": [],
            "quartiers": []
        }
        
        # Check for duplicate province codes
        province_codes = []
        for province in self._province_repo.get_all():
            if province.code in province_codes:
                issues["provinces"].append(f"Duplicate province code: {province.code}")
            else:
                province_codes.append(province.code)
        
        # Check for duplicate commune codes
        commune_codes = []
        for commune in self._commune_repo.get_all():
            if commune.code in commune_codes:
                issues["communes"].append(f"Duplicate commune code: {commune.code}")
            else:
                commune_codes.append(commune.code)
        
        # Check for duplicate zone codes
        zone_codes = []
        for zone in self._zone_repo.get_all():
            if zone.code in zone_codes:
                issues["zones"].append(f"Duplicate zone code: {zone.code}")
            else:
                zone_codes.append(zone.code)
        
        # Check for duplicate quartier codes
        quartier_codes = []
        for quartier in self._quartier_repo.get_all():
            if quartier.code in quartier_codes:
                issues["quartiers"].append(f"Duplicate quartier code: {quartier.code}")
            else:
                quartier_codes.append(quartier.code)
        
        return issues
    
    def get_validation_report(self) -> Dict[str, any]:
        """Get a comprehensive validation report."""
        report = {
            "timestamp": "2026-02-11T10:08:00Z",  # In real implementation, use actual timestamp
            "summary": {},
            "errors": {},
            "warnings": {}
        }
        
        # Run all validations
        referential_errors = self.check_referential_integrity()
        consistency_issues = self.validate_hierarchy_consistency()
        completeness_issues = self.validate_data_completeness()
        uniqueness_issues = self.validate_unique_codes()
        
        # Count total issues
        total_errors = (
            sum(len(errors) for errors in referential_errors.values()) +
            len(consistency_issues) +
            sum(len(errors) for errors in completeness_issues.values()) +
            sum(len(errors) for errors in uniqueness_issues.values())
        )
        
        report["summary"] = {
            "total_errors": total_errors,
            "referential_integrity_errors": sum(len(errors) for errors in referential_errors.values()),
            "consistency_issues": len(consistency_issues),
            "completeness_issues": sum(len(errors) for errors in completeness_issues.values()),
            "uniqueness_issues": sum(len(errors) for errors in uniqueness_issues.values()),
            "is_valid": total_errors == 0
        }
        
        report["errors"] = {
            "referential_integrity": referential_errors,
            "hierarchy_consistency": consistency_issues,
            "data_completeness": completeness_issues,
            "unique_codes": uniqueness_issues
        }
        
        return report
    
    def find_orphaned_entities(self) -> Dict[str, List[str]]:
        """Find all orphaned entities (entities whose parents don't exist)."""
        orphans = {
            "communes": [],
            "zones": [],
            "quartiers": []
        }
        
        # Get all valid parent codes
        province_codes = {province.code for province in self._province_repo.get_all()}
        commune_codes = {commune.code for commune in self._commune_repo.get_all()}
        zone_codes = {zone.code for zone in self._zone_repo.get_all()}
        
        # Find orphaned communes
        for commune in self._commune_repo.get_all():
            if commune.province_code not in province_codes:
                orphans["communes"].append(commune.code)
        
        # Find orphaned zones
        for zone in self._zone_repo.get_all():
            if zone.commune_code not in commune_codes:
                orphans["zones"].append(zone.code)
        
        # Find orphaned quartiers
        for quartier in self._quartier_repo.get_all():
            if quartier.zone_code not in zone_codes:
                orphans["quartiers"].append(quartier.code)
        
        return orphans
