# 🚀 Guide de Publication PyPI v1.0.1

## 🔍 **Problème actuel**
Le token PyPI semble invalide ou expiré.

## 🛠️ **Solution 1 - Nouveau Token**

### 1️⃣ **Générer un nouveau token**
1. Allez sur : https://pypi.org/manage/account/token/
2. Click : **"Add API token"**
3. Nom : `tburundigeo-v1.0.1`
4. Scope : **"Entire account"**
5. Copiez le token généré

### 2️⃣ **Uploader avec le nouveau token**
```bash
twine upload dist/* --username __token__ --password NOUVEAU_TOKEN_ICI
```

## 🛠️ **Solution 2 - Upload Manuel**

### 1️⃣ **Interface PyPI**
1. Allez sur : https://pypi.org/manage/project/tburundigeo/releases/
2. Click : **"Upload new version"**
3. Upload les fichiers :
   - `tburundigeo-1.0.1-py3-none-any.whl`
   - `tburundigeo-1.0.1.tar.gz`

### 2️⃣ **Fichiers à uploader**
Les fichiers sont dans : `c:\Users\M Tech Solutions\Desktop\Package_burundi\dist\`

## ✅ **Vérification post-upload**
```bash
# Désinstaller l'ancienne version
pip uninstall tburundigeo -y

# Installer la nouvelle version
pip install tburundigeo==1.0.1

# Vérifier les données
python -c "import tburundigeo; print('Provinces:', len(tburundigeo.get_all_provinces())); print('Communes:', len(tburundigeo.get_all_communes())); print('Zones:', len(tburundigeo.get_all_zones())); print('Quartiers:', len(tburundigeo.get_all_quartiers()))"
```

## 🎯 **Résultat attendu**
```
Provinces: 5
Communes: 42
Zones: 451
Quartiers: 3044
```

---

**La v1.0.1 contient les données correctes !** 🇧🇮✨
