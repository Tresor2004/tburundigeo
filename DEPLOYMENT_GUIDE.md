# 🚀 Guide de Déploiement - TBurundiGeo

## 📋 Prérequis

- ✅ **Compte PyPI** : https://pypi.org/account/register/
- ✅ **Compte GitHub** : https://github.com/signup
- ✅ **Python 3.8+** et outils de build installés
- ✅ **Package buildé** : `tburundigeo-1.0.0-py3-none-any.whl`

---

## 🐍 Déploiement sur PyPI

### 1️⃣ **Configuration Twine**

```bash
# Installer Twine (déjà fait)
pip install --upgrade twine

# Configurer les identifiants PyPI
twine configure
# Entrer votre username et password PyPI
```

### 2️⃣ **Upload sur PyPI Test**

```bash
# Test sur PyPI Test (recommandé)
twine upload --repository testpypi dist/*

# Vérifier sur https://test.pypi.org/project/tburundigeo/
```

### 3️⃣ **Upload sur PyPI Officiel**

```bash
# Upload sur PyPI officiel
twine upload dist/*

# Vérifier sur https://pypi.org/project/tburundigeo/
```

---

## 🐙 Déploiement sur GitHub

### 1️⃣ **Créer le Repository**

```bash
# Initialiser Git si pas fait
git init
git add .
git commit -m "Initial commit - TBurundiGeo v1.0.0"

# Ajouter remote
git remote add origin https://github.com/tresor2004/tburundigeo.git
git push -u origin main
```

### 2️⃣ **Créer une Release**

1. **Aller sur GitHub** : https://github.com/tresor2004/tburundigeo
2. **Click sur "Releases"** → "Create a new release"
3. **Tag version** : `v1.0.0`
4. **Release title** : `TBurundiGeo v1.0.0`
5. **Description** : Copier depuis CHANGELOG.md
6. **Attach files** :Uploader les fichiers depuis `dist/`
   - `tburundigeo-1.0.0-py3-none-any.whl`
   - `tburundigeo-1.0.0.tar.gz`
7. **Publish release**

---

## 🔗 **Liens Importants**

- **PyPI Officiel** : https://pypi.org/project/tburundigeo/
- **PyPI Test** : https://test.pypi.org/project/tburundigeo/
- **GitHub Repository** : https://github.com/tresor2004/tburundigeo
- **GitHub Releases** : https://github.com/tresor2004/tburundigeo/releases

---

## 📝 **Commandes Rapides**

```bash
# Build complet
python -m build


# Upload test PyPI
twine upload --repository testpypi dist/*

# Upload PyPI officiel
twine upload dist/*

# Git push
git push origin main --tags
```

---

## ✅ **Vérification Post-Déploiement**

### PyPI
```bash
# Installation depuis PyPI
pip install tburundigeo

# Test
python -c "import tburundigeo; print(tburundigeo.__version__)"
```

### GitHub
- ✅ Release visible sur la page des releases
- ✅ Fichiers sources téléchargeables
- ✅ Tags corrects (v1.0.0)

---

**🎉 Félicitations ! Votre package TBurundiGeo est maintenant disponible pour toute la communauté !** 🇧🇮✨
