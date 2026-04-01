#!/bin/bash

# change end of file (extension)
# shape : filename.extension
if [ $# -ne 2 ]; then
	echo "Usage : $0 <ancienne-extension> <nouvelle-extension>"
	exit 1
fi

for i in *.*
do
	mv "$i" "`basename -s .$1 $i`.$2"
done