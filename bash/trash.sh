#!/bin/bash

# simulate a bin
if [ -z $1 ]; then
	echo "Usage : $0 <arg(s)> (-h pour l'aide)"
	exit 1
fi

if [ "$1" = "-c" ]; then
	shift
	mkdir ~/Poubelle
	du -h ~/Poubelle
	exit 0
fi

if [ "$*" = "-e" ]; then
	shift
	mkdir ~/Poubelle
	rm ~/Poubelle/*
	echo "Le répertoire Trash a été vidé"
	exit 0
fi

if [ "$1" = "-h" -o "$1" = "--help" ]; then
	shift
	echo -e "Usage de la commande trash : $0 fichier(s)\tou\t$0 OPTION"
	echo -e "\nOptions :\n-h, --help : afficher cette aide.\n-c : afficher la taille du répertoire Trash.\n-e : vider le répertoire Trash."
	echo -e "Remarque : Utilisez les options sans préciser de fichiers."
	exit 0
fi

for i in $*
do
	if [ "$i" = "-c" ]; then
		shift
	elif [ "$i" = "-e" ]; then
		shift
	fi
	mv "$i" ~/Poubelle
done