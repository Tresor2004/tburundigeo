# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-02-12

### 🌟 Added
- **Capitales des provinces** : Ajout du champ `capital` à l'entité `Province`
- **Chefs-lieux des zones** : Ajout du champ `chief_town` à l'entité `Zone`
- **API étendue** : Nouvelles fonctions `get_province_capital()` et `get_zone_chief_town()`
- **CLI enrichie** : Options `--with-capitals` et `--with-chief-towns`
- **Documentation** : Configuration complète avec Read the Docs
- **Tests** : Couverture de test étendue pour les nouvelles fonctionnalités

### 🔧 Changed
- **Architecture** : Mise à jour de l'architecture hexagonale
- **Package** : Renommage de `burundi_admin` vers `tburundigeo`
- **Dependencies** : Mise à jour des dépendances de développement
- **Build** : Configuration avec `hatchling` et support UV
- **Code cleanup** : Nettoyage complet du code pour open source (travail solo par NIYOMWUNGERE Tresor)

### 📊 Data Updates
- **5 provinces** avec leurs capitales validées
- **42 communes** avec leurs capitales existantes
- **451 zones** avec leurs chefs-lieux ajoutés
- **3044 quartiers** (données complètes et validées)

### 🐛 Fixed
- Correction des imports après renommage du package
- Correction du chargement des données dans les repositories
- Correction des arguments CLI manquants
- Amélioration de la validation des entités

### 📚 Documentation
- Documentation complète avec Sphinx et Read the Docs
- Exemples d'utilisation avec capitales et chefs-lieux
- Guide de contribution détaillé
- Architecture expliquée avec schémas

### 🚀 Performance
- Optimisation du chargement des données
- Amélioration des temps de réponse CLI
- Réduction de l'empreinte mémoire

---

## [0.1.0] - 2026-01-15

### 🌟 Added
- Version initiale du package
- Architecture hexagonale complète
- API de base pour provinces, communes, zones, quartiers
- CLI complète avec toutes les commandes
- Tests unitaires avec >90% de couverture
- Documentation de base

---

## [Unreleased]

### 🚧 Planned
- Support GeoJSON pour l'export géographique
- Validation avancée des coordonnées géographiques
- Interface web pour l'exploration des données
- Intégration avec OpenStreetMap
- Support multilingue (français, anglais, kirundi)
