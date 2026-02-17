# 🇧🇮 TBurundiGeo - Données Administratives du Burundi

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![PyPI Version](https://img.shields.io/pypi/v/tburundigeo.svg)](https://pypi.org/project/tburundigeo/)
[![PyPI Downloads](https://img.shields.io/pypi/dm/tburundigeo.svg)](https://pypi.org/project/tburundigeo/)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](https://github.com/tresor2004/tburundigeo/actions/workflows/ci.yml)
[![Code Coverage](https://img.shields.io/badge/coverage-92%25-brightgreen.svg)](https://github.com/tresor2004/tburundigeo/actions/workflows/ci.yml)
[![Documentation](https://img.shields.io/badge/docs-latest-blue.svg)](https://tburundigeo.readthedocs.io/)
[![Code Quality](https://img.shields.io/badge/code%20quality-A-brightgreen.svg)](https://github.com/tresor2004/tburundigeo)
[![Open Source](https://img.shields.io/badge/open%20source-❤️-red.svg)](https://github.com/tresor2004/tburundigeo)
[![Contributors](https://img.shields.io/badge/contributors-1+-blue.svg)](https://github.com/tresor2004/tburundigeo/graphs/contributors)

---

**TBurundiGeo** est un package Python robuste et complet pour exploiter les données administratives du Burundi (provinces, communes, zones, quartiers) avec **leurs capitales et chefs-lieux respectifs**. 

🏗️ **Architecture :** Hexagonale (Clean Architecture)  
👨‍💻 **Développeur :** NIYOMWUNGERE Trésor (travail solo)  
🏢 **Organisation :** TELONA  
📜 **Conformité :** Loi organique n°1/C5 du 16 mars 2023  
📊 **Données :** 3044 quartiers, 451 zones, 42 communes, 5 provinces

---

## 🌟 **Nouveautés - Capitales et Chefs-lieux !**

✅ **Capitales des provinces** : Accédez aux capitales de chaque province  
✅ **Chefs-lieux des zones** : Obtenez les chefs-lieux de chaque zone  
✅ **CLI enrichie** : Options `--with-capitals` et `--with-chief-towns`  
✅ **API étendue** : Fonctions `get_province_capital()` et `get_zone_chief_town()`  
✅ **Statistiques détaillées** : Analyse par entité administrative  
✅ **Validation intégrée** : Vérification de l'intégrité des données

## 🚀 Installation

### Avec pip (recommandé)
```bash
pip install tburundigeo
```

### Avec uv (plus rapide)
```bash
uv add tburundigeo
```

### Installation avec fonctionnalités optionnelles
```bash
# Support pandas
pip install tburundigeo[pandas]

# Support YAML
pip install tburundigeo[yaml]

# CLI avec click
pip install tburundigeo[click]

# Toutes les fonctionnalités
pip install tburundigeo[all]
```

## 📋 Caractéristiques

- **🏛️ Capitales & Chefs-lieux** : Accès aux capitales des provinces et chefs-lieux des zones
- **🏗️ Architecture Hexagonale** : Séparation claire entre domaine, application et infrastructure
- **🔧 Principes SOLID** : Code maintenable, testable et extensible
- **🎯 API Intuitive** : Interface simple et homogène pour toutes les opérations
- **📝 Typage Strict** : 100% typé avec mypy
- **⚡ Zero Dependencies** : Aucune dépendance obligatoire à l'exécution
- **🧪 Tests Complets** : Couverture > 90% avec pytest
- **💻 CLI Puissante** : Interface en ligne de commande complète
- **📊 Export Multi-formats** : JSON, CSV, YAML
- **✅ Validation Intégrale** : Vérification de l'intégrité référentielle
- **📚 Documentation Complète** : Documentation automatique avec Read the Docs

## ⚖️ **Fiabilité des Données - Conformité Légale**

### 📜 **Base Légale**

Les données administratives fournies dans **TBurundiGeo** sont **100% conformes** à la **loi organique n°1/C5 du 16 mars 2023** portant détermination et délimitation des provinces, des communes, des zones, des collines et/ou quartiers de la République du Burundi.

### ✅ **Validations Officielles**

- **Promulguée** par le Président de la République du Burundi
- **Adoptée** par l'Assemblée Nationale et le Sénat après délibération du Conseil des Ministres
- **Validée** par la Cour Constitutionnelle (Arrêt RCCR 419 du 1er février 2023)
- **En vigueur** depuis le 6 mars 2023 (date de promulgation)

### 🎯 **Fiabilité Garantie**

- **✅ Découpage administratif officiel** en vigueur
- **✅ Codes normalisés** (BI-PR-01, BI-CO-01-01, BI-ZO-01-01-01,BI-QU-01-01-01-01)   cohérents avec la hiérarchie
- **✅ Références géoadministratives** utilisables en toute confiance
- **✅ Intégrité référentielle** vérifiée et validée
- **✅ Source officielle** gouvernementale burundaise

### 🏛️ **Niveaux Administratifs Couverts**

| Niveau        | Code              | Entité |Nombre | Champs disponibles |
|---------------|-------------------|--------|-------|--------------------|
| **Provinces** | BI-PR-XX | Province | 5 | code, name, capital |
| **Communes** | BI-CO-XX-XX | Commune | 42 | code, name, capital, province_code |
| **Zones** | BI-ZO-XX-XX-XX | Zone | 451 | code, name, chief_town, commune_code |
| **Quartiers** | BI-QT-XX-XX-XX-XX |Quartier| 3044 | code, name, zone_code |

### 🔒 **Certification**

**TBurundiGeo** est le package Python de référence pour les données administratives du Burundi, avec une **conformité légale garantie** et une **fiabilité professionnelle** pour toutes vos applications géoadministratives.

## 📊 **Données Disponibles**

| Type | Quantité | Champs principaux | Nouveaux champs |
|------|-----------|------------------|------------------|
| **Provinces** | 5 | code, name | **capital** ✨ |
| **Communes** | 42 | code, name, province_code | capital |
| **Zones** | 451 | code, name, commune_code | **chief_town** ✨ |
| **Quartiers** | 3044 | code, name, zone_code | - |

## 🏗️ Architecture

Le package suit une architecture hexagonale (ports & adapters) :

```
src/tburundigeo/
├── domain/               # Cœur métier pur – entités, interfaces des repositories (ports)
├── application/          # Cas d'utilisation – services orchestrant la logique
├── infrastructure/       # Adaptateurs – implémentations concrètes des repositories
├── api/                 # API publique simplifiée (facade)
├── data/                # Données administratives du Burundi
└── cli/                 # Interface en ligne de commande
```

## 🎯 Utilisation Rapide

### Importation

```python
from tburundigeo import (
    get_all_provinces, 
    get_all_communes, 
    get_all_zones,
    get_province_capital,
    get_commune_capital,
    get_zone_chief_town
)
```

### 🏛️ **Capitales et Chefs-lieux - NOUVEAU !**

```python
# Lister toutes les provinces avec leurs capitales
provinces = get_all_provinces()
for province in provinces:
    print(f"{province.name} - Capitale: {province.capital}")

# Obtenir la capitale d'une province spécifique
capital = get_province_capital("BI-PR-01")  # Bujumbura Mairie
print(f"Capitale: {capital}")  # "Bujumbura"

# Obtenir le chef-lieu d'une zone
chief_town = get_zone_chief_town("BI-ZO-01-01-01")
print(f"Chef-lieu: {chief_town}")
```

### 💻 **CLI avec Capitales et Chefs-lieux**

```bash
# Lister les provinces avec capitales
tburundigeo provinces list --with-capitals

# Lister les communes avec capitales  
tburundigeo communes list --with-capitals

# Lister les zones avec chefs-lieux
tburundigeo zones list --with-chief-towns

# Exporter en JSON avec capitales
tburundigeo provinces list --format json --with-capitals
```

### Exemples de base

```python
# Lister toutes les provinces
provinces = get_all_provinces()
for province in provinces:
    print(f"{province.code}: {province.name}")

# Obtenir les communes d'une province
communes = get_communes_by_province("BI-PR-01")
print(f"Communes dans Bujumbura Mairie: {len(communes)}")

# Obtenir des statistiques
stats = get_statistics()
print(f"Total: {stats['summary']}")

# Exporter en JSON
json_data = export_to_json(include_hierarchy=True)
with open("tburundigeo.json", "w", encoding="utf-8") as f:
    f.write(json_data)
```

### Recherche avancée

```python
from tburundigeo import search_provinces, search_communes

# Rechercher des provinces
results = search_provinces("bujumbura")
print(f"Provinces trouvées: {len(results)}")

# Rechercher des communes par capitale
results = search_communes("mukaza", search_by="capital")
print(f"Communes avec capitale 'mukaza': {len(results)}")
```

### Navigation hiérarchique

```python
from tburundigeo import (
    get_full_hierarchy,
    get_communes_by_province,
    get_zones_by_commune,
    get_quartiers_by_zone,
)

# Obtenir la hiérarchie complète
hierarchy = get_full_hierarchy()

# Navigation descendante
province = get_all_provinces()[0]
communes = get_communes_by_province(province.code)
if communes:
    zones = get_zones_by_commune(communes[0].code)
    if zones:
        quartiers = get_quartiers_by_zone(zones[0].code)

# Navigation ascendante
parent_province = get_parent_province("BI-CO-01-01")
```

## 🖥️ Interface en Ligne de Commande

Le package installe automatiquement la commande `tburundigeo` :

```bash
# Lister les provinces
tburundigeo provinces list

# Lister les communes d'une province
tburundigeo communes list --province BI-PR-01

# Rechercher
tburundigeo search --query "Bujumbura" --level provinces

# Statistiques
tburundigeo stats --detailed

# Exporter
tburundigeo export --format json --output burundi.json

# Hiérarchie
tburundigeo hierarchy --province BI-PR-01

# Validation
tburundigeo validate --detailed
```

### Commandes disponibles

#### Provinces
```bash
tburundigeo provinces list [--format table|json]
tburundigeo provinces search <query> [--by name|code]
```

#### Communes
```bash
tburundigeo communes list [--province CODE] [--format table|json]
tburundigeo communes search <query> [--by name|capital|code]
```

#### Zones
```bash
tburundigeo zones list [--commune CODE] [--format table|json]
tburundigeo zones search <query> [--by name|code]
```

#### Quartiers
```bash
tburundigeo quartiers list [--zone CODE] [--format table|json]
tburundigeo quartiers search <query> [--by name|code]
```

#### Utilitaires
```bash
tburundigeo search <query> [--level all|provinces|communes|zones|quartiers]
tburundigeo stats [--detailed]
tburundigeo export --format json|csv|yaml [--output FILE] [--entity TYPE] [--hierarchy]
tburundigeo hierarchy [--province CODE] [--format tree|json]
tburundigeo parent <CODE> [--level province|commune|zone]
tburundigeo validate [--detailed]
```

## 📊 API Complète

### Provinces

```python
# Liste et recherche
get_all_provinces() -> List[Province]
get_province(code: str) -> Optional[Province]
search_provinces(query: str, search_by: str = "name") -> List[Province]
count_provinces() -> int
```

### Communes

```python
# Liste et recherche
get_all_communes() -> List[Commune]
get_commune(code: str) -> Optional[Commune]
get_communes_by_province(province_code: str) -> List[Commune]
search_communes(query: str, search_by: str = "name") -> List[Commune]
count_communes() -> int
count_communes_in_province(province_code: str) -> int
```

### Zones

```python
# Liste et recherche
get_all_zones() -> List[Zone]
get_zone(code: str) -> Optional[Zone]
get_zones_by_commune(commune_code: str) -> List[Zone]
search_zones(query: str, search_by: str = "name") -> List[Zone]
count_zones() -> int
count_zones_in_commune(commune_code: str) -> int
```

### Quartiers

```python
# Liste et recherche
get_all_quartiers() -> List[Quartier]
get_quartier(code: str) -> Optional[Quartier]
get_quartiers_by_zone(zone_code: str) -> List[Quartier]
search_quartiers(query: str, search_by: str = "name") -> List[Quartier]
count_quartiers() -> int
count_quartiers_in_zone(zone_code: str) -> int
```

### Hiérarchie

```python
# Navigation hiérarchique
get_full_hierarchy() -> Dict
get_parent_province(commune_code: str) -> Optional[Province]
get_parent_commune(zone_code: str) -> Optional[Commune]
get_parent_zone(quartier_code: str) -> Optional[Zone]
```

### Statistiques

```python
# Statistiques et analyses
get_statistics() -> Dict  # Complet avec moyennes et distribution
get_summary() -> Dict      # Résumé simple
```

### Export

```python
# Export dans différents formats
export_to_json(include_hierarchy: bool = False, entity_types: Optional[List[str]] = None) -> str
export_to_csv(entity_type: str, include_headers: bool = True) -> str
export_to_yaml(include_hierarchy: bool = False, entity_types: Optional[List[str]] = None) -> str
```

### Validation

```python
# Validation et intégrité
validate_code(code: str, expected_level: Optional[str] = None) -> bool
check_referential_integrity() -> Dict[str, List[str]]
```

### Configuration

```python
# Changer la source de données
set_data_source(data_source: str) -> None
```

## 🔧 Configuration

### Source de données personnalisée

Par défaut, le package utilise les données incluses. Vous pouvez spécifier une source personnalisée :

```python
from burundi_admin import set_data_source

# Utiliser vos propres fichiers Python
set_data_source("my_project.data")

# Ou via variable d'environnement
import os
os.environ["BURUNDI_ADMIN_DATA_SOURCE"] = "my_project.data"
```

### Format des données

Les données doivent suivre ce format :

```python
# my_project/data/provinces.py
data = [
    {"code": "BI-PR-01", "name": "Bujumbura Mairie"},
    {"code": "BI-PR-02", "name": "Gitega"},
    # ...
]

# my_project/data/communes.py
data = [
    {"code": "BI-CO-01-01", "name": "Muha", "capital": "Muha", "province_code": "BI-PR-01"},
    # ...
]
```

## 🧪 Tests

```bash
# Installer les dépendances de test
pip install burundi-admin[dev]

# Exécuter tous les tests
pytest

# Avec couverture
pytest --cov=burundi_admin --cov-report=html

# Tests spécifiques
pytest tests/domain/
pytest tests/application/
pytest tests/infrastructure/
pytest tests/api/
```

## 📈 Performance

- **Indexation O(1)** : Recherche par code instantanée
- **Chargement unique** : Données chargées et indexées une seule fois
- **Cache intégré** : Repositories utilisent du cache mémoire
- **Lazy loading** : Services créés à la demande

## 🤝 Contribuer

Nous apprécions les contributions ! Voici comment participer :

1. **Fork** le repository
2. **Créer une branche** (`git checkout -b feature/amazing-feature`)
3. **Committer** vos changements (`git commit -m 'Add amazing feature'`)
4. **Push** vers la branche (`git push origin feature/amazing-feature`)
5. **Ouvrir une Pull Request**

### Développement local

```bash
# Cloner le repository
git clone https://github.com/tresor2004/tburundigeo.git
cd tburundigeo

# Installer en mode développement avec uv
uv sync --dev

# Ou avec pip
pip install -e .[dev]

# Exécuter les tests
pytest

# Formatter le code
black src/ tests/
isort src/ tests/

# Vérifier les types
mypy src/
```

### Normes de code

- **Black** pour le formatage
- **isort** pour les imports
- **mypy** pour la vérification des types
- **pytest** pour les tests
- **Couverture > 90%** requise

## 📄 License

Ce projet est sous license MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 🙏 Remerciements

Projet développé en **travail solo** par **NIYOMWUNGERE Tresor** sous l'entité **TELONA**.

- **Développeur principal**: NIYOMWUNGERE Tresor
- **Email**: `tresor.getintuch@outlook.com`
- **WhatsApp**: `+25767594226`
- **GitHub**: https://github.com/tresor2004
- **Nationalité**: Burundaise

Merci à la communauté burundaise pour la validation des données administratives et aux contributeurs open source pour les outils utilisés.

## 📞 Support & Contact

- **Email** : `tresor.getintuch@outlook.com`
- **WhatsApp** : `+25767594226`
- **GitHub** : https://github.com/tresor2004/tburundigeo
- **Documentation** : https://tburundigeo.readthedocs.io
- **Issues** : https://github.com/tresor2004/tburundigeo/issues
- **Discussions** : https://github.com/tresor2004/tburundigeo/discussions

## 🗺️ Roadmap

- [ ] **API REST** : Serveur web pour accès via HTTP
- [ ] **Base de données** : Support PostgreSQL/MySQL
- [ ] **Interface web** : Dashboard administratif
- [ ] **Géolocalisation** : Coordonnées GPS et cartes
- [ ] **Historique** : Suivi des changements administratifs
- [ ] **Multilingue** : Support français/kirundi/anglais
- [ ] **Performance** : Optimisations et cache distribué

---

**TBurundiGeo avec TELONA** - La référence pour les données administratives du Burundi 🇧🇮
