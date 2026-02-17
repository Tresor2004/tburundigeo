# 🚀 Configuration GitHub Actions - Publication Automatique

## ✅ **Workflow configuré**

### 📋 **Fichier créé**
- **`.github/workflows/publish.yml`** : Publication automatique sur PyPI/TestPyPI

### 🔧 **Fonctionnalités**
- **Release préliminaire** → Publication sur **TestPyPI**
- **Release finale** → Publication sur **PyPI**
- **Construction automatique** avec Python 3.11
- **Validation** du package avant publication

## 🔑 **Étapes de configuration**

### 1️⃣ **Créer les secrets GitHub**
Allez sur : https://github.com/Tresor2004/tburundigeo/settings/secrets/actions

**Ajoutez ces secrets :**

**TEST_PYPI_API_TOKEN**
1. Allez sur : https://test.pypi.org/manage/account/token/
2. Créez un token pour TestPyPI
3. Copiez le token dans le secret GitHub

**PYPI_API_TOKEN**
1. Allez sur : https://pypi.org/manage/account/token/
2. Créez un token pour PyPI officiel
3. Copiez le token dans le secret GitHub

### 2️⃣ **Comment publier**

**Pour TestPyPI (pré-release) :**
1. GitHub → Releases → "Create a new release"
2. Tag : `v1.0.3-beta.1`
3. ✅ Cochez "This is a pre-release"
4. Publish → Publication automatique sur TestPyPI

**Pour PyPI (officiel) :**
1. GitHub → Releases → "Create a new release"
2. Tag : `v1.0.3`
3. ❌ Ne cochez PAS "pre-release"
4. Publish → Publication automatique sur PyPI

## 🎯 **Avantages**
- ✅ **Plus de `twine upload` manuel**
- ✅ **Publication automatique** via GitHub
- ✅ **Séparation TestPyPI/PyPI** automatique
- ✅ **Validation** du package avant publication
- ✅ **Historique** des releases GitHub

## 📊 **État actuel**
- ✅ **Workflow** configuré et poussé
- ⏳ **Secrets** à configurer
- 🚀 **Prêt** pour publication automatique

---

**Prochaine étape : Configurez les secrets GitHub !** 🇧🇮✨
