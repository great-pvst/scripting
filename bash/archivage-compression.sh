#!/bin/bash

#erase content of directory backup
if [ -d "/path/which/will/contain/" ]; then
	rm -rf /path/which/will/contain/*
else
	echo "Le répertoire /data/sauve n'existe pas."
	exit 1
fi

#archiving & compressing
tar -czvf /path/to/store/backup_$(date +%Y-%m-%d).tar.gz /file/to/backup

