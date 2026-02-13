"""Common type definitions for the Burundi Admin package."""

from typing import Literal, TypeAlias, Union

# Administrative levels
AdministrativeLevel: TypeAlias = Literal["province", "commune", "zone", "quartier"]

# Export formats
ExportFormat: TypeAlias = Literal["json", "csv", "yaml"]

# Code types
CodeType: TypeAlias = Union[
    Literal["province_code"],
    Literal["commune_code"], 
    Literal["zone_code"],
    Literal["quartier_code"]
]

# Generic result types for search operations
SearchResult: TypeAlias = dict[str, Union[str, int, float]]

# Hierarchy representation
HierarchyNode: TypeAlias = dict[str, Union[str, dict, list]]

# Statistics summary
StatisticsSummary: TypeAlias = dict[str, Union[int, float, dict]]
