#!/bin/bash
# create venv if it doesn't exist, call the supplied cmd line args once that
# venv is created and activated
service_name=${1}
content_file=${2}
embed_file=${3}

if [ -z "$service_name" ] || [ -z "$content_file" ] || [ -z "$embed_file" ] ; then
    >&2 echo "usage: dvault_serive_status.sh <service_name> <content_file> <embed_file>"
    exit 1
fi

echo "SERVICE_RESULT=$SERVICE_RESULT EXIT_CODE=$EXIT_CODE EXIT_STATUS=$EXIT_STATUS" > $content_file
systemctl status $service_name --user | head -n6 >> $content_file
journalctl -u $service_name --user -n 35 > $embed_file

