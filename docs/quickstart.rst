Quick Start
===========

Utilisation de base
-----------------

.. code-block:: python

   from tburundigeo import (
       get_all_provinces, 
       get_all_communes, 
       get_all_zones,
       get_province_capital,
       get_commune_capital,
       get_zone_chief_town
   )

   # Lister toutes les provinces avec leurs capitales
   provinces = get_all_provinces()
   for province in provinces:
       print(f"{province.name} - Capitale: {province.capital}")

   # Obtenir la capitale d'une province spécifique
   capital = get_province_capital("BI-PR-01")
   print(f"Capitale de Bujumbura Mairie: {capital}")

   # Obtenir le chef-lieu d'une zone
   chief_town = get_zone_chief_town("BI-ZO-01-01-01")
   print(f"Chef-lieu: {chief_town}")

Utilisation de la CLI
--------------------

.. code-block:: bash

   # Lister les provinces avec capitales
   tburundigeo provinces list --with-capitals

   # Lister les communes avec capitales
   tburundigeo communes list --with-capitals

   # Lister les zones avec chefs-lieux
   tburundigeo zones list --with-chief-towns

   # Exporter en JSON
   tburundigeo provinces list --format json --with-capitals

   # Rechercher des entités
   tburundigeo provinces search "Bujumbura"
   tburundigeo communes search "Gitega" --by capital
