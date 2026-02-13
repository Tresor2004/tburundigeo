Examples
========

Exemples d'utilisation avancée
------------------------------

Analyse des données administratives
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from tburundigeo import (
       get_all_provinces, 
       get_all_communes, 
       get_all_zones,
       get_statistics
   )

   # Statistiques complètes
   stats = get_statistics()
   print(f"Nombre de provinces: {stats['provinces']['total']}")
   print(f"Nombre de communes: {stats['communes']['total']}")
   print(f"Nombre de zones: {stats['zones']['total']}")
   print(f"Nombre de quartiers: {stats['quartiers']['total']}")

   # Analyse par province
   provinces = get_all_provinces()
   for province in provinces:
       communes = get_communes_by_province(province.code)
       print(f"{province.name}: {len(communes)} communes")

Export avec pandas
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import pandas as pd
   from tburundigeo import get_all_provinces, get_all_communes

   # Installer d'abord: pip install tburundigeo[pandas]

   # Exporter les provinces en DataFrame
   provinces_data = []
   provinces = get_all_provinces()
   
   for province in provinces:
       provinces_data.append({
           'code': province.code,
           'name': province.name,
           'capital': province.capital
       })
   
   df_provinces = pd.DataFrame(provinces_data)
   df_provinces.to_csv('provinces_burundi.csv', index=False)

   # Exporter les communes en DataFrame
   communes_data = []
   communes = get_all_communes()
   
   for commune in communes:
       communes_data.append({
           'code': commune.code,
           'name': commune.name,
           'capital': commune.capital,
           'province_code': commune.province_code
       })
   
   df_communes = pd.DataFrame(communes_data)
   df_communes.to_excel('communes_burundi.xlsx', index=False)

Recherche avancée
~~~~~~~~~~~~~~~~~

.. code-block:: python

   from tburundigeo import (
       search_provinces,
       search_communes,
       search_zones,
       get_full_hierarchy
   )

   # Rechercher toutes les entités contenant "Gitega"
   provinces = search_provinces("Gitega")
   communes = search_communes("Gitega")
   zones = search_zones("Gitega")

   print(f"Provinces trouvées: {len(provinces)}")
   print(f"Communes trouvées: {len(communes)}")
   print(f"Zones trouvées: {len(zones)}")

   # Obtenir la hiérarchie complète
   hierarchy = get_full_hierarchy()
   
   # Parcourir la hiérarchie
   for province_code, province_data in hierarchy.items():
       print(f"Province: {province_data['name']}")
       for commune_code, commune_data in province_data['communes'].items():
           print(f"  Commune: {commune_data['name']}")
           for zone_code, zone_data in commune_data['zones'].items():
               print(f"    Zone: {zone_data['name']}")
               for quartier_code, quartier_data in zone_data['quartiers'].items():
                   print(f"      Quartier: {quartier_data['name']}")

Validation des données
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from tburundigeo import check_referential_integrity

   # Vérifier l'intégrité des données
   errors = check_referential_integrity()
   
   if not any(errors.values()):
       print("✅ Toutes les données sont valides!")
   else:
       print("❌ Erreurs trouvées:")
       for error_type, error_list in errors.items():
           if error_list:
               print(f"{error_type}: {len(error_list)} erreurs")
               for error in error_list[:5]:  # Afficher les 5 premières erreurs
                   print(f"  - {error}")
