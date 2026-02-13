Contributing
============

Merci de votre intérêt pour contribuer à TBurundiGeo !

Comment contribuer
-----------------

1. Fork le projet
2. Créer une branche pour votre fonctionnalité (`git checkout -b feature/amazing-feature`)
3. Commit vos changements (`git commit -m 'Add amazing feature'`)
4. Push vers la branche (`git push origin feature/amazing-feature`)
5. Ouvrir une Pull Request

Développement local
------------------

.. code-block:: bash

   # Cloner le projet
   git clone https://github.com/tresor2004/tburundigeo.git
   cd tburundigeo

   # Créer un environnement virtuel
   python -m venv venv
   source venv/bin/activate  # Sur Windows: venv\Scripts\activate

   # Installer en mode développement
   pip install -e .[dev]

   # Lancer les tests
   pytest

   # Vérifier le typage
   mypy src/tburundigeo

   # Formater le code
   black src/tburundigeo tests
   isort src/tburundigeo tests

Structure du projet
------------------

.. code-block:: text

   tburundigeo/
   ├── src/tburundigeo/
   │   ├── api/           # API publique (facade)
   │   ├── application/   # Services métier
   │   ├── domain/        # Entités et interfaces
   │   ├── infrastructure/ # Implémentations concrètes
   │   ├── data/          # Données administratives
   │   └── cli/           # Interface en ligne de commande
   ├── tests/             # Tests unitaires
   ├── docs/              # Documentation
   └── README.md

Normes de code
---------------

- **Python 3.8+** requis
- **Typage strict** avec mypy
- **Formatage** avec black et isort
- **Tests** avec pytest (couverture > 90%)
- **Documentation** avec docstrings Google/Napoleon

Ajout de données
-----------------

Pour ajouter ou modifier des données administratives:

1. Modifier les fichiers dans ``src/tburundigeo/data/``
2. Mettre à jour les tests correspondants
3. Vérifier la validation des données
4. Ajouter des tests pour les nouvelles données

Signalement de bugs
------------------

Merci de signaler les bugs via:

- **GitHub Issues**: https://github.com/tresor2004/tburundigeo/issues
- **Email**: tresor.getintuch@outlook.com

Veuillez inclure:

- Version de Python
- Version de TBurundiGeo
- Système d'exploitation
- Message d'erreur complet
- Exemple de code reproduisant le problème

Licence
-------

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.
