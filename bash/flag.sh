#!/bin/bash

#	flag game to manipulate files
if [ -z "$1" ] && [ -n "$2" ]; then
	echo "Usage : $0 <nom_du_drapeau>"		
	exit 1
fi

if [ ! -e "$1" ] && [ -z "$2" ]; then
	echo "Erreur, fichier inexistant"
	exit 1
fi

if [ -z "$2" ]; then
	echo "Etat actuel : `cat $1`"
	exit 1
fi


if [ "$2" = "on" ]; then
	echo 1 > $1
	echo "Nouvel etat : `cat $1`"
fi

if [ "$2" = "off" ]; then
	echo 0 > $1
	echo "Nouvel etal : `cat $1`"
fi

if [ "$2" = "flop" ]; then
	if [ ! -e "$1" ]; then 
		echo "Erreur, fichier inexistant"
		exit 1
	elif [ `cat $1` -eq 1 ]; then
		echo 0 > $1
		echo -e "Inversion ok.\nNouvel etat : `cat $1`"
	else
		echo 1 > $1
		echo -e "Inversion ok.\nNouvel etat : `cat $1`"
	fi
fi