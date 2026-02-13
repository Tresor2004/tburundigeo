"""Data module for tburundigeo package.

This module contains the administrative divisions data for Burundi.
The data is provided as Python files with a 'data' variable containing
lists of dictionaries.
"""

# Import data modules to make them available
from tburundigeo.data import provinces
from tburundigeo.data import communes
from tburundigeo.data import zones
from tburundigeo.data import quartiers

__all__ = [
    "provinces",
    "communes", 
    "zones",
    "quartiers",
]
