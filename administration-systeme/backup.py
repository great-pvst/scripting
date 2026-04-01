#!/usr/bin/env python3

import os
import sys
import subprocess
import paramiko


def create_archive(archive_name, directory):
    """    Crée une archive tar.gz du répertoire spécifié    """
    if not os.path.isdir(directory):
        raise Exception(f"Le répertoire {directory} n'existe pas.")

    archive_file = f"{archive_name}.tar.gz"

    try:
        subprocess.run(
            ["tar", "-czf", archive_file, directory],
            check=True
        )
        print(f" Archive créée : {archive_file}")
    except subprocess.CalledProcessError:
        raise Exception("Erreur lors de la création de l'archive")

    return archive_file


def send_sftp(server, username, password, local_file):
    """    Envoie le fichier via SFTP    """
    try:
        transport = paramiko.Transport((server, 22))
        transport.connect(username=username, password=password)

        sftp = paramiko.SFTPClient.from_transport(transport)

        remote_path = f"/home/{username}/{os.path.basename(local_file)}"

        sftp.put(local_file, remote_path)

        print(f" Fichier envoyé sur {server}:{remote_path}")

        sftp.close()
        transport.close()

    except Exception as e:
        raise Exception(f"Erreur SFTP : {e}")


def main():
    if len(sys.argv) != 5:
        print("Usage : script.py <archive_name> <directory> <server> <user:password>")
        sys.exit(1)

    archive_name = sys.argv[1]
    directory = sys.argv[2]
    server = sys.argv[3]

    credentials = sys.argv[4]
    if ":" not in credentials:
        print("Format login:password requis")
        sys.exit(1)

    username, password = credentials.split(":", 1)

    try:
        archive_file = create_archive(archive_name, directory)
        send_sftp(server, username, password, archive_file)

        print("[✓] Sauvegarde terminée avec succès")

    except Exception as e:
        print(f"[!] Erreur : {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()