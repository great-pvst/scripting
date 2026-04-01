#!/bin/bash
########### check the HTTP connections on web server by using nagios

# Seuils
WARNING=25000
CRITICAL=35000

# ESTABLISHED connexion account on port 80
con=`snmpwalk -v 1 -c public 192.168.0.204 1.3.6.1.2.1.6.13 | grep '\.80\.' | grep 'INTEGER: 5' | wc -l`

# limit
if [ "$con" -ge "$CRITICAL" ]; then
    exit 2

elif [ "$con" -ge "$WARNING" ]; then
    exit 1
else
    exit 0
fi