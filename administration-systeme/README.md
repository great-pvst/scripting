# 🛠️ Scripts d’Administration Système (Python 3)

Ce dépôt contient (à cet instant) deux scripts Python 3 destinés à automatiser des tâches courantes d’administration système :

* 📦 Sauvegarde d’un répertoire avec archivage et transfert SFTP
* 🚀 Déploiement d’archives avec détection automatique du format

---

# 📚 Table des matières

* [Prérequis](#-prérequis)
* [Script 1 : Backup SFTP](#-script-1--backup-sftp)
* [Script 2 : Déploiement d’archive](#-script-2--déploiement-darchive)
* [Sécurité](#-sécurité)
* [Améliorations possibles](#-améliorations-possibles)
* [Auteur](#-auteur)

---

# ⚙️ Prérequis

* Python 3.x
* Système Linux (Debian/Ubuntu recommandé)
* Outils installés :

  * `tar`
  * `unzip`
  * `openssh-server` (pour SFTP)

Installation des dépendances Python :

```bash
pip install paramiko 
```
Si environnement non virtuel

```bash
sudo apt install python3-paramiko -y
```
---

# 📦 Script 1 : Backup SFTP

## 🎯 Description

Ce script permet de :

1. Créer une archive `.tar.gz` d’un répertoire
2. Transférer l’archive vers un serveur distant via SFTP

## 🧾 Paramètres

```bash
python3 backup.py <nom_archive> <répertoire> <serveur> <login:password>
```

## 🔄 Fonctionnement

* Compression via `tar`
* Connexion SFTP via `paramiko`
* Envoi dans `/home/<user>/`

---

# 🚀 Script 2 : Déploiement d’archive

## 🎯 Description

Ce script permet de déployer une archive dans un répertoire cible avec vérifications de sécurité.

## 🧾 Paramètres

```bash
python3 deploy.py <archive> <répertoire_destination>
```

### Exemple

```bash
python3 deploy.py app.tar.gz /opt/app
```

## 🔍 Fonctionnalités

* Vérification :
  * existence des fichiers
  * droits d’accès
* Détection du type d’archive :
  * `.zip`
  * `.tar`
  * `.tgz` / `.tar.gz`
* Extraction avec l’outil adapté :
  * `unzip`
  * `tar`

---

# 🔐 Sécurité

Ces scripts implémentent plusieurs bonnes pratiques :

* ❌ Pas d’utilisation de `shell=True`
* ✅ Vérification des droits d’accès
* ✅ Validation des entrées utilisateur
* ✅ Gestion des erreurs

---

# 🔧 Améliorations possibles

* 🔐 Authentification par clé SSH
* 📁 Rotation automatique des sauvegardes
* 📦 Support d’autres formats (7z, rar)

---

# 👨‍💻 Auteur
Projet réalisé dans un contexte d’administration système et réseau.

---

# 📜 Licence
Libre d’utilisation à des fins éducatives et professionnelles.