CLI Reference
=============

La CLI TBurundiGeo fournit une interface complète en ligne de commande pour interagir avec les données administratives du Burundi.

Commandes disponibles
--------------------

Provinces
~~~~~~~~~~~

.. code-block:: bash

   # Lister toutes les provinces
   tburundigeo provinces list

   # Lister avec capitales
   tburundigeo provinces list --with-capitals

   # Exporter en JSON
   tburundigeo provinces list --format json --with-capitals

   # Rechercher des provinces
   tburundigeo provinces search "Bujumbura"
   tburundigeo provinces search "BI-PR-01" --by code

Communes
~~~~~~~~~

.. code-block:: bash

   # Lister toutes les communes
   tburundigeo communes list

   # Lister avec capitales
   tburundigeo communes list --with-capitals

   # Filtrer par province
   tburundigeo communes list --province BI-PR-01 --with-capitals

   # Rechercher des communes
   tburundigeo communes search "Gitega"
   tburundigeo communes search "Gitega" --by capital

Zones
~~~~~~

.. code-block:: bash

   # Lister toutes les zones
   tburundigeo zones list

   # Lister avec chefs-lieux
   tburundigeo zones list --with-chief-towns

   # Filtrer par commune
   tburundigeo zones list --commune BI-CO-01-01 --with-chief-towns

   # Rechercher des zones
   tburundigeo zones search "Muha"

Quartiers
~~~~~~~~~

.. code-block:: bash

   # Lister tous les quartiers
   tburundigeo quartiers list

   # Filtrer par zone
   tburundigeo quartiers list --zone BI-ZO-01-01-01

   # Rechercher des quartiers
   tburundigeo quartiers search "Buyenzi"

Commandes utilitaires
--------------------

Statistiques
~~~~~~~~~~~~

.. code-block:: bash

   # Statistiques générales
   tburundigeo stats

   # Statistiques détaillées
   tburundigeo stats --detailed

Export
~~~~~~

.. code-block:: bash

   # Exporter en JSON
   tburundigeo export --format json --output burundi.json

   # Exporter en CSV
   tburundigeo export --format csv --entity provinces --output provinces.csv

   # Exporter en YAML
   tburundigeo export --format yaml --output burundi.yaml

Hiérarchie
~~~~~~~~~~

.. code-block:: bash

   # Hiérarchie complète
   tburundigeo hierarchy

   # Hiérarchie d'une province
   tburundigeo hierarchy --province BI-PR-01

Validation
~~~~~~~~~~

.. code-block:: bash

   # Validation rapide
   tburundigeo validate

   # Validation détaillée
   tburundigeo validate --detailed
