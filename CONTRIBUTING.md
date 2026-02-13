# Contribuer à TBurundiGeo 🇧🇮

Merci de votre intérêt pour contribuer à TBurundiGeo ! Ce document vous guidera à travers le processus de contribution.

## 🎯 Objectif du Projet

TBurundiGeo est un package Python open source qui fournit un accès structuré et fiable aux données administratives du Burundi (provinces, communes, zones, quartiers) avec une architecture hexagonale moderne.

**Développé par :** NIYOMWUNGERE Tresor (travail solo)  
**Organisation :** TELONA  
**License :** MIT

---

## 🚀 Comment Contribuer

### 📋 Types de Contributions

Nous apprécions particulièrement les contributions dans les domaines suivants :

#### 🏛️ **Amélioration des Données**
- Mise à jour des données administratives
- Correction des incohérences
- Ajout de nouvelles informations (les hôpitaux,les centres de santé,les ecoles ,banks)
- Validation contre les sources officielles

#### 🔧 **Développement Technique**
- Nouvelles fonctionnalités API
- Amélioration des performances
- Refactoring du code
- Tests automatisés

#### 📚 **Documentation**
- Amélioration de la documentation technique
- Traductions (anglais, kirundi, français)
- Exemples d'utilisation
- Tutoriels

#### 🐛 **Rapports de Bugs**
- Identification de problèmes
- Suggestions d'amélioration
- Tests de régression

---

## 🛠️ Processus de Contribution

### 1️⃣ **Préparation**

#### 📋 Vérifier les Issues Existantes
- [Issues ouvertes](https://github.com/tresor2004/tburundigeo/issues)
- [Pull Requests en cours](https://github.com/tresor2004/tburundigeo/pulls)

#### 🔧 Configuration de l'Environnement

```bash
# Cloner le dépôt
git clone https://github.com/tresor2004/tburundigeo.git
cd tburundigeo

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -e ".[dev]"
```

#### 🧪 Installation des Dépendances de Développement

```bash
# Dépendances principales
pip install -e .

# Dépendances de développement
pip install -e ".[dev]"

# Ou manuellement
pip install pytest black isort mypy flake8 coverage pre-commit
```

---

### 2️⃣ **Développement**

#### 📁 Structure du Projet

```
tburundigeo/
├── src/tburundigeo/          # Code source principal
│   ├── api/                  # Interface API publique
│   ├── application/           # Logique métier
│   ├── cli/                  # Interface ligne de commande
│   ├── common/                # Utilitaires communs
│   ├── data/                  # Données administratives
│   ├── domain/                # Entités métier
│   └── infrastructure/        # Implémentations techniques
├── tests/                     # Tests automatisés
├── docs/                      # Documentation
└── examples/                   # Exemples d'utilisation
```

#### 🎨 Normes de Codage

**Python :** 3.8+  
**Style :** Black + isort  
**Typage :** MyPy  
**Tests :** Pytest  

```bash
# Formatter le code
black src/ tests/
isort src/ tests/

# Vérifier le typage
mypy src/

# Lancer les tests
pytest

# Vérifier la qualité
flake8 src/
```

#### 🧪 Écrire des Tests

```python
# tests/test_new_feature.py
import pytest
from tburundigeo import get_all_provinces

def test_get_all_provinces_returns_data():
    """Test que la fonction retourne des données."""
    provinces = get_all_provinces()
    assert len(provinces) > 0
    assert all(hasattr(p, 'code') for p in provinces)
```

---

### 3️⃣ **Soumission**

#### 🌿 Créer une Branche

```bash
# Créer une branche descriptive
git checkout -b feature/nouvelle-fonctionnalite
# ou
git checkout -b fix/correction-bug-123
```

#### 📝 Commit Messages

Utiliser le format [Conventional Commits](https://www.conventionalcommits.org/) :

```
feat: ajouter la recherche par coordonnées GPS
fix: corriger le comptage des quartiers dans Bujumbura
docs: mettre à jour la documentation d'installation
refactor: optimiser les requêtes de base de données
test: ajouter des tests pour les statistiques détaillées
```

#### 🚀 Pull Request

1. **Pousser la branche :**
   ```bash
   git push origin feature/nouvelle-fonctionnalite
   ```

2. **Créer une Pull Request sur GitHub**
   - Titre descriptif
   - Description détaillée
   - Référencer les issues liées
   - Ajouter des captures d'écran si applicable

---

## 🎯 Priorités de Contribution

### 🔥 **Haute Priorité**
- ✅ Corrections de données administratives
- ✅ Rapports de bugs critiques
- ✅ Améliorations de sécurité

### 🔶 **Moyenne Priorité**
- 📊 Nouvelles fonctionnalités statistiques
- 📚 Améliorations documentation
- 🧪 Tests automatisés

### 🔵 **Basse Priorité**
- 🎨 Améliorations UI/UX
- 🌐 Traductions
- 📈 Optimisations performances

---

## 🤝 Recrutement et Partenariats

### 👨‍💻 **Pour les Entreprises**

**TELONA** recherche des partenariats avec :

- 🏢 **Entreprises burundaises** needing reliable administrative data
- 🌍 **Organisations internationales** working on Burundi projects
- 🏛️ **Institutions gouvernementales** seeking digital solutions
- 📊 **Companies de données/GIS** needing African administrative data

**Contact :** `tresor.getintuch@outlook.com`  
**Sujet :** `Partenariat TBurundiGeo`

### 🏛️ **Pour les ONG et Organisations**

**Applications typiques :**
- 🗺️ Systèmes d'information géographique (SIG)
- 📊 Analyse démographique et administrative
- 🏛️ Plateformes de services publics
- 📱 Applications mobiles de localisation
- 🎓 Systèmes éducatifs
- etc

**Avantages :**
- ✅ **Données certifiées** conformes à la loi organique n°1/C5
- ✅ **API robuste** avec architecture hexagonale
- ✅ **Support technique** prioritaire
- ✅ **Mises à jour** régulières
- ✅ **Documentation complète** en français et anglais

---

## 📜 Licence et Droits

**License :** MIT  
**Auteur :** NIYOMWUNGERE Tresor  
**Droits :** Usage commercial, modification, distribution, usage privé autorisés

---

## 🙏 Remerciements

Un grand merci à tous les contributeurs qui améliorent TBurundiGeo !

**Contributeurs principaux :**
- 👨‍💻 **NIYOMWUNGERE Tresor** - Développeur principal et mainteneur
- 🏢 **TELONA** - Organisation supportrice

**Particulièrement reconnaissants pour :**
- 📚 Contributions à la documentation
- 🐛 Rapports de bugs
- 📊 Améliorations des données
- 🌐 Traductions

---

## 📞 Contact

- **Email :** `tresor.getintuch@outlook.com`
- **WhatsApp :** `+25767594226`
- **GitHub :** https://github.com/tresor2004/tburundigeo
- **Documentation :** https://tburundigeo.readthedocs.io

---

**En contribuant à TBurundiGeo, vous aidez à démocratiser l'accès aux données administratives du Burundi !** 🇧🇮✨
