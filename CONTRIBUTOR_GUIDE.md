# Fichier de Configuration des Contributeurs

Ce fichier contient des informations utiles pour les contributeurs qui veulent s'impliquer dans le développement de TBurundiGeo.

## 🏗️ Architecture du Projet

```
tburundigeo/
├── 📁 src/tburundigeo/           # Code source principal
│   ├── 📋 api/                  # Interface API publique (facde)
│   ├── ⚙️ application/           # Logique métier (services)
│   ├── 💻 cli/                  # Interface ligne de commande
│   ├── 🔧 common/                # Utilitaires communs (exceptions)
│   ├── 📊 data/                  # Données administratives
│   ├── 🏛️ domain/               # Entités métier
│   └── 🏗️ infrastructure/        # Implémentations techniques (repositories)
├── 🧪 tests/                     # Tests automatisés
├── 📚 docs/                      # Documentation technique
├── 📖 examples/                   # Exemples d'utilisation
└── ⚙️ .github/workflows/          # CI/CD automation
```

## 🛠️ Outils de Développement

### Configuration Requise

```bash
# Python 3.8+ requis
python --version

# Installation des dépendances de développement
pip install -e ".[dev]"

# Ou avec uv (recommandé)
uv add --dev tburundigeo
```

### Outils Utilisés

- **🎨 Formatage :** Black, isort
- **🔍 Analyse statique :** MyPy, Flake8, Bandit
- **🧪 Tests :** Pytest, Coverage
- **📦 Gestion :** UV (recommandé), pip
- **🚀 CI/CD :** GitHub Actions
- **📚 Documentation :** Sphinx, Read the Docs

## 🎯 Normes de Qualité

### Code Style

```bash
# Formatter le code
black src/ tests/
isort src/ tests/

# Vérifier la qualité
flake8 src/ --max-line-length=88
mypy src/ --strict
```

### Tests

```bash
# Lancer tous les tests
pytest

# Tests avec couverture
pytest --cov=src/tburundigeo --cov-report=html

# Tests spécifiques
pytest tests/test_api.py -v
```

### Sécurité

```bash
# Scanner les dépendances
safety check

# Analyse statique de sécurité
bandit -r src/

# Scan de secrets
git-secrets scan
```

## 🔄 Workflow de Développement

### 1️⃣ Fork et Clone

```bash
# Forker sur GitHub puis cloner
git clone https://github.com/VOTRE_USERNAME/tburundigeo.git
cd tburundigeo
git remote add upstream https://github.com/tresor2004/tburundigeo.git
```

### 2️⃣ Branche de Développement

```bash
# Créer une branche feature
git checkout -b feature/votre-fonctionnalite

# Ou une branche de correction
git checkout -b fix/correction-bug-123
```

### 3️⃣ Développement

```bash
# Installer en mode développement
pip install -e .

# Lancer les tests en continu
watchdog --patterns="*.py" --recursive --command="pytest"
```

### 4️⃣ Commit et Push

```bash
# Vérifier le code avant commit
pre-commit run

# Commit avec message conventionnel
git commit -m "feat: ajouter nouvelle fonctionnalité"

# Pusher vers votre fork
git push origin feature/votre-fonctionnalite
```

## 📋 Types de Contributions

### 🆕 Nouvelles Fonctionnalités

- **API :** Nouveaux endpoints, fonctions utilitaires
- **CLI :** Nouvelles commandes, options
- **Données :** Nouvelles sources, mises à jour
- **Export :** Nouveaux formats, améliorations

### 🐛 Corrections de Bugs

- **Données :** Incohérences, erreurs de comptage
- **Code :** Plantages, fuites mémoire
- **Performance :** Lenteurs, surconsommation
- **Interface :** Messages d'erreur, UX

### 📚 Documentation

- **API :** Docstrings, exemples d'utilisation
- **CLI :** Aide en ligne, manuel utilisateur
- **Architecture :** Diagrammes, explications techniques
- **Déploiement :** Guides d'installation, configuration

## 🎯 Priorités du Projet

### 🔥 Haute Priorité

1. **📊 Qualité des données** - Exactitude et complétude
2. **🔒 Sécurité** - Protection des utilisateurs
3. **🚀 Performance** - Rapidité d'exécution
4. **📚 Documentation** - Accessibilité et clarté

### 🔶 Moyenne Priorité

1. **🧪 Tests** - Couverture et fiabilité
2. **🎨 DX/UX** - Expérience développeur/utilisateur
3. **🌐 Internationalisation** - Support multilingue

### 🔵 Basse Priorité

1. **📦 Dépendances** - Mises à jour, optimisations
2. **🔧 Outils** - Amélioration des workflows
3. **📈 Analytics** - Monitoring, métriques

## 🏆 Reconnaissance des Contributions

### 🎖️ Badges et Reconnaissance

- **Contributions significatives** : Mention dans les notes de version
- **Contributions multiples** : Badge "Top Contributor"
- **Innovations** : Mise en avant dans la documentation
- **Qualité exceptionnelle** : Recommandations pour recrutement

### 🎁 Opportunités

- **🏢 TELONA** : Opportunités de collaboration rémunérée
- **🏛️ Partenariats** : Intégrations avec institutions
- **🎓 Formations** : Accès aux ressources d'apprentissage
- **🌍 Événements** : Participation aux conférences

## 📞 Support Technique

### 🏗️ Architecture Questions

```python
# Questions sur l'architecture hexagonale
# Design patterns utilisés
# Choix techniques
```

### 🔧 Implémentation Help

```python
# Questions sur les repositories
# Services métier
# CLI et API
```

### 📊 Data Questions

```python
# Questions sur les données administratives
# Sources officielles
- Validation et intégrité
```

## 🚀 Déploiement et Release

### Versionnement

**Format :** Semantic Versioning (semver)  
**Exemple :** v1.0.0, v1.1.0, v2.0.0

```bash
# Créer un tag de release
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

### Publication Automatisée

Les releases sont automatiquement publiées sur PyPI via GitHub Actions lors des tags.

## 📚 Ressources d'Apprentissage

### 🏗️ Clean Architecture

- [Hexagonal Architecture](https://netflix.github.io/feign/latest/hystrix-circuit-breaker.html)
- [Clean Architecture](https://blog.cleancoder.com/2018/03/05/clean-architecture/)
- [Domain-Driven Design](https://github.com/ddd-crew/ddd-starter-modern)

### 🐍 Python Packaging

- [PyPA Packaging](https://packaging.python.org/)
- [Modern Python Packaging](https://github.com/pypa/hatch)
- [UV Package Manager](https://github.com/astral-sh/uv)

### 📊 Données Burundi

- [Loi organique n°1/C5](https://www.legislation.gov.bi/)
- [Institut National des Statistiques](http://www.statistics.gov.bi/)
- [Minère de l'Intérieur](http://www.interieur.gov.bi/)

---

## 📞 Contact & Support

Pour toute question technique ou problème :

- **Email principal :** `tresor.getintuch@outlook.com`
- **WhatsApp :** `+25767594226`
- **GitHub Issues :** https://github.com/tresor2004/tburundigeo/issues
- **GitHub Discussions :** https://github.com/tresor2004/tburundigeo/discussions

### 🎯 Temps de réponse

- **Urgences/Critiques :** 24-48h
- **Questions générales :** 2-3 jours
- **Pull Requests :** 1-5 jours

---

**Ce fichier est maintenu par la communauté TBurundiGeo. N'hésitez pas à proposer des améliorations !** 🇧🇮✨
