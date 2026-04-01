#!/bin/bash

# another way to create folders
if [ $# -eq 0 ]; then
	nbfolders=0
	echo "Combien de dossiers souhaitez-vous créer ?"
	read nbfolders
	
	until ((1 > $nbfolders))
	do
		read -p "Nom du dossier ? " name
		mkdir "$name"
		nbfolders=$(($nbfolders - 1))
	done
	echo "Les dossiers ont été créés"
else
	echo "Le script n'est pas exécuté"

fi

# autres pistes :
# - créer un dossier directement dans le home user
# - créer un dossier dans le home user avec un nom personnalisé (date de création, nom de l'utilisateur, etc.)
# - créer un dossier dans un répertoire spécifique
# - créer un dossier en fonction d'un argument passé au script (ex : ./createfolder.sh nomdossier)