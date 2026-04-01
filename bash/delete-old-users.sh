#!/bin/bash

# Définir la date limite (6 mois en arrière)
date_limite=$(date -d "6 months ago" +"%Y-%m-%d")

# Récupérer la liste des utilisateurs et de leurs dates de création
liste_utilisateurs=$(awk -F: '$3 >= 1000 {print $1,$3}' /etc/passwd)

# Parcourir la liste des utilisateurs pour récuperer la date de création
while read -r utilisateur uid; do
  date_creation=$(chage -l $utilisateur | grep "Last password change" | awk '{print $4}')

  # Convertir la date au format YYYY-MM-DD
  date_creation=$(date -d "$date_creation" +"%Y-%m-%d")

  # Supprimer l'utilisateur si la date de création est antérieure à la date limite
  if [[ $date_creation < $date_limite ]]; then
    userdel -r $utilisateur
    echo "Utilisateur $utilisateur supprimé."
  fi
done <<< "$liste_utilisateurs"