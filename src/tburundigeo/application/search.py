"""Search service for finding administrative divisions."""

import re
from typing import List, Optional, Union

from tburundigeo.common.exceptions import InvalidCodeError
from tburundigeo.domain.entities import Province, Commune, Zone, Quartier
from tburundigeo.domain.interfaces import (
    IProvinceRepository,
    ICommuneRepository,
    IZoneRepository,
    IQuartierRepository,
)


class SearchService:
    """Service for searching administrative divisions."""
    
    def __init__(
        self,
        province_repo: IProvinceRepository,
        commune_repo: ICommuneRepository,
        zone_repo: IZoneRepository,
        quartier_repo: IQuartierRepository,
    ) -> None:
        """Initialize search service with repositories."""
        self._province_repo = province_repo
        self._commune_repo = commune_repo
        self._zone_repo = zone_repo
        self._quartier_repo = quartier_repo
    
    def search_provinces(
        self,
        query: str,
        search_by: str = "name"
    ) -> List[Province]:
        """Search provinces by name or code."""
        if search_by == "name":
            return self._province_repo.search_by_name(query)
        elif search_by == "code":
            return self._search_provinces_by_code(query)
        else:
            raise InvalidCodeError(query, f"Invalid search_by parameter: {search_by}")
    
    def search_communes(
        self,
        query: str,
        search_by: str = "name"
    ) -> List[Commune]:
        """Search communes by name, capital, or code."""
        if search_by == "name":
            return self._commune_repo.search_by_name(query)
        elif search_by == "capital":
            return self._commune_repo.search_by_capital(query)
        elif search_by == "code":
            return self._search_communes_by_code(query)
        else:
            raise InvalidCodeError(query, f"Invalid search_by parameter: {search_by}")
    
    def search_zones(
        self,
        query: str,
        search_by: str = "name"
    ) -> List[Zone]:
        """Search zones by name or code."""
        if search_by == "name":
            return self._zone_repo.search_by_name(query)
        elif search_by == "code":
            return self._search_zones_by_code(query)
        else:
            raise InvalidCodeError(query, f"Invalid search_by parameter: {search_by}")
    
    def search_quartiers(
        self,
        query: str,
        search_by: str = "name"
    ) -> List[Quartier]:
        """Search quartiers by name or code."""
        if search_by == "name":
            return self._quartier_repo.search_by_name(query)
        elif search_by == "code":
            return self._search_quartiers_by_code(query)
        else:
            raise InvalidCodeError(query, f"Invalid search_by parameter: {search_by}")
    
    def search_all(
        self,
        query: str,
        search_by: str = "name"
    ) -> dict[str, List[Union[Province, Commune, Zone, Quartier]]]:
        """Search across all administrative levels."""
        results = {
            "provinces": [],
            "communes": [],
            "zones": [],
            "quartiers": []
        }
        
        try:
            results["provinces"] = self.search_provinces(query, search_by)
        except InvalidCodeError:
            pass
        
        try:
            results["communes"] = self.search_communes(query, search_by)
        except InvalidCodeError:
            pass
        
        try:
            results["zones"] = self.search_zones(query, search_by)
        except InvalidCodeError:
            pass
        
        try:
            results["quartiers"] = self.search_quartiers(query, search_by)
        except InvalidCodeError:
            pass
        
        return results
    
    def search_by_code_pattern(self, pattern: str) -> dict[str, List[Union[Province, Commune, Zone, Quartier]]]:
        """Search entities by code pattern (supports wildcards)."""
        # Convert wildcard pattern to regex
        regex_pattern = pattern.replace('*', '.*').replace('?', '.')
        regex_pattern = f"^{regex_pattern}$"
        
        try:
            compiled_pattern = re.compile(regex_pattern, re.IGNORECASE)
        except re.error as e:
            raise InvalidCodeError(pattern, f"Invalid pattern: {e}")
        
        results = {
            "provinces": [],
            "communes": [],
            "zones": [],
            "quartiers": []
        }
        
        # Search provinces
        for province in self._province_repo.get_all():
            if compiled_pattern.match(province.code):
                results["provinces"].append(province)
        
        # Search communes
        for commune in self._commune_repo.get_all():
            if compiled_pattern.match(commune.code):
                results["communes"].append(commune)
        
        # Search zones
        for zone in self._zone_repo.get_all():
            if compiled_pattern.match(zone.code):
                results["zones"].append(zone)
        
        # Search quartiers
        for quartier in self._quartier_repo.get_all():
            if compiled_pattern.match(quartier.code):
                results["quartiers"].append(quartier)
        
        return results
    
    def fuzzy_search(self, query: str, min_similarity: float = 0.6) -> dict[str, List[Union[Province, Commune, Zone, Quartier]]]:
        """Simple fuzzy search based on character similarity."""
        results = {
            "provinces": [],
            "communes": [],
            "zones": [],
            "quartiers": []
        }
        
        query_lower = query.lower()
        
        # Search provinces
        for province in self._province_repo.get_all():
            similarity = self._calculate_similarity(query_lower, province.name.lower())
            if similarity >= min_similarity:
                results["provinces"].append(province)
        
        # Search communes
        for commune in self._commune_repo.get_all():
            name_similarity = self._calculate_similarity(query_lower, commune.name.lower())
            capital_similarity = self._calculate_similarity(query_lower, commune.capital.lower())
            max_similarity = max(name_similarity, capital_similarity)
            
            if max_similarity >= min_similarity:
                results["communes"].append(commune)
        
        # Search zones
        for zone in self._zone_repo.get_all():
            similarity = self._calculate_similarity(query_lower, zone.name.lower())
            if similarity >= min_similarity:
                results["zones"].append(zone)
        
        # Search quartiers
        for quartier in self._quartier_repo.get_all():
            similarity = self._calculate_similarity(query_lower, quartier.name.lower())
            if similarity >= min_similarity:
                results["quartiers"].append(quartier)
        
        return results
    
    def _search_provinces_by_code(self, query: str) -> List[Province]:
        """Search provinces by code pattern."""
        provinces = self._province_repo.get_all()
        query_lower = query.lower()
        
        return [
            province for province in provinces
            if query_lower in province.code.lower()
        ]
    
    def _search_communes_by_code(self, query: str) -> List[Commune]:
        """Search communes by code pattern."""
        communes = self._commune_repo.get_all()
        query_lower = query.lower()
        
        return [
            commune for commune in communes
            if query_lower in commune.code.lower()
        ]
    
    def _search_zones_by_code(self, query: str) -> List[Zone]:
        """Search zones by code pattern."""
        zones = self._zone_repo.get_all()
        query_lower = query.lower()
        
        return [
            zone for zone in zones
            if query_lower in zone.code.lower()
        ]
    
    def _search_quartiers_by_code(self, query: str) -> List[Quartier]:
        """Search quartiers by code pattern."""
        quartiers = self._quartier_repo.get_all()
        query_lower = query.lower()
        
        return [
            quartier for quartier in quartiers
            if query_lower in quartier.code.lower()
        ]
    
    def _calculate_similarity(self, str1: str, str2: str) -> float:
        """Calculate similarity between two strings using simple character matching."""
        if not str1 or not str2:
            return 0.0
        
        # Simple similarity based on common characters and length
        set1 = set(str1)
        set2 = set(str2)
        
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        
        if union == 0:
            return 0.0
        
        # Add bonus for exact matches and prefix matches
        similarity = intersection / union
        
        if str1 == str2:
            similarity = 1.0
        elif str2.startswith(str1) or str1.startswith(str2):
            similarity += 0.2
        
        return min(similarity, 1.0)
