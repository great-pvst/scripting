#!/usr/bin/env python3

import os
import sys
import subprocess


def check_file_exists(filepath):
    if not os.path.isfile(filepath):
        raise Exception(f"Archive introuvable : {filepath}")

    if not os.access(filepath, os.R_OK):
        raise Exception(f"Pas de droit de lecture sur : {filepath}")


def check_directory(directory):
    if not os.path.isdir(directory):
        raise Exception(f"Répertoire inexistant : {directory}")

    if not os.access(directory, os.W_OK):
        raise Exception(f"Pas de droit d'écriture sur : {directory}")


def detect_archive_type(filename):
    filename = filename.lower()

    if filename.endswith(".zip"):
        return "zip"
    elif filename.endswith(".tar"):
        return "tar"
    elif filename.endswith(".tgz") or filename.endswith(".tar.gz"):
        return "tgz"
    else:
        raise Exception("Type d'archive non supporté (zip, tar, tgz uniquement)")


def extract_archive(archive, archive_type, destination):
    try:
        if archive_type == "zip":
            cmd = ["unzip", "-o", archive, "-d", destination]

        elif archive_type == "tar":
            cmd = ["tar", "-xf", archive, "-C", destination]

        elif archive_type == "tgz":
            cmd = ["tar", "-xzf", archive, "-C", destination]

        else:
            raise Exception("Type d'archive inconnu")

        print(f" Extraction avec : {' '.join(cmd)}")

        subprocess.run(cmd, check=True)

        print("[✓] Extraction terminée")

    except subprocess.CalledProcessError:
        raise Exception("Erreur lors de l'extraction")


def main():
    if len(sys.argv) != 3:
        print("Usage : script.py <archive> <repertoire_destination>")
        sys.exit(1)

    archive = sys.argv[1]
    destination = sys.argv[2]

    try:
        print("... Vérifications...")

        check_file_exists(archive)
        check_directory(destination)

        archive_type = detect_archive_type(archive)
        print(f" Type détecté : {archive_type}")

        extract_archive(archive, archive_type, destination)

        print("[✓] Déploiement réussi")

    except Exception as e:
        print(f"[!] Erreur : {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()