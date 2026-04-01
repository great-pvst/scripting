#!/bin/bash

#no arg accept
if [ -n "$1" ]; then
	echo "Usage : $0"
	exit 1
fi

# print directory content / select the file
echo -n "Vous êtes dans : "; pwd; echo "Voici les fichiers présents"; ls --color=auto

# file ?
echo -e -n "\nLe fichier souhaité est-il présent ? [y/n] "; read bool;
if [ -z "$bool" ]; then
	echo -e "\nVous n'avez rien tapé, le programme ne peut continuer"
	exit 1
fi

if [ "$bool" != "n" ] && [ "$bool" != "y" ]; then
	echo -e "\nChoix non valide, arrêt du programme"
	exit 1
fi

# 
if [ "$bool" = "n" ]; then
	read -p "Entrez le nom du fichier : " new_file; echo -e "Nous recherchons le répertoire..."
# limited search 
	file=`find "$HOME" -path "*/$new_file"`
	# !find
	if [ -z "$file" ]; then
		echo -e "\nFichier à transférer introuvable ! (Veuillez à respecter les maj,min,symboles,etc.)\nFin du programme"
		exit 1
	fi
	#
	# find
	echo -e "\nFichier à transférer : $file";
	#
fi

if [ "$bool" = "y" ]; then
	read -p "Entrez le fichier à transférer : " new_file

#absolute path
file="$HOME/$new_file"
fi

### check the name
for i in `ls`
do
	if [ "$file" = "$i" ]; then
		echo -e "Fichier trouvé !\n"; bool="n" #to skip the bad entry.
	fi
	temp="$i"
done
#bad entry
if [ "$file" != "$temp" ] && [ "$bool" = "y" ]; then
	echo -e "Cette destination n'existe pas, le programme est arrêté."; exit 1
fi

# select the destination
bool=""

echo -e "\nVous allez désigner la destination du fichier"

# local destination ?
read -p "La destination est-elle interne ou externe ? [i/e] " type_stock
if [ -z "$type_stock" ]; then
	echo -e "\nDestination vide, le programme ne peut continuer"
	exit 1
fi

if [ "$type_stock" != "i" ] && [ "$type_stock" != "e" ]; then
	echo -e "\nChoix non valide, arrêt du programme"
	exit 1
fi

if [ "$type_stock" = "e" ]; then
# stockage list
	echo -e "Rassurez-vous d'avoir connecté le stockage externe !\nVoici les destinations possibles : "; ls --color=auto /media/${USER}
# choose disk
	read -p "Entrez le nom de la destination : " stock
# !empty
	if [ -z "$stock" ]; then
		echo -e "Destination vide, arrêt du programme."; exit 1
	fi
#
# check the existence of the name provided
	for dest in `ls /media/${USER}`
	do
		if [ "$dest" = "$stock" ]; then
			echo -e "\nDestination correcte, envoi en cours..."
			rsync -arbpu -E $file /media/${USER}/"$stock" --progress 2> erreurs_rsync
			echo -e "\nFin de l'opération."
			exit 1
		fi
		temp=$dest
	done
	# bad entry
	if [ "$stock" != "$temp" ]; then
		echo -e "Cette destination n'existe pas, le programme s'arrête."; exit 1
	fi
#
fi

# local destination
echo -e "\nVoici votre répertoire : "; ls --color=auto $HOME

read -p "La destination est-elle présente ? [y/n] " bool
if [ -z "$bool" ]; then
	echo -e "\nVous n'avez rien tapé, le programme ne peut continuer."
	exit 1
fi

if [ "$bool" != "n" ] && [ "$bool" != "y" ]; then
	echo -e "\nChoix non valide, arrêt du programme"
	exit 1
fi


if [ "$bool" = "n" ]; then
# navigate on the tree
	while ( "$bool" = "n" )
	do
#
		read -p "Possible destination : " new_stock;
		for dest in `ls`
		do
			if [ "$dest" = "$new_stock" ]; then
				cd ${new_stock}; ls --color=auto; read -p "La destination est-elle présente ? [y/n] " bool
				stock=`find $HOME -path "*/${new_stock}"`
			fi
		done
		echo -e "Pas de correspondance ! "
	done

#
fi

#echo "ok"
if [ "$bool" = "y" ]; then
	read -p "Entrez la destination : " stock;
	for dest in `ls`
	do
		if [ "$dest" = "$stock" ]; then
			echo -e "\nDestination correcte, envoi en cours..."
			rsync -arbpu -E $file "$HOME/$stock" --progress 2> erreurs_rsync
			echo -e "\nFin de l'opération. Arrêt du programme !"
			exit 1
		fi
# only if no correspondance.
	temp=$dest
	done
fi

# bad type
if [ "$temp" != "$stock" ]; then
	echo "Destination incohérente ! Arrêt du programme."; exit 1
fi