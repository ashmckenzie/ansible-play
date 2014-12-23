#!/bin/bash

SUBJECT="${1}"
BODY="${2}"

echo -e "Subject: ${SUBJECT}\n\n${BODY}" | sendmail -v -F "Ansible" -f admin@the-rebellion.net "Ash McKenzie <ash@the-rebellion.net>"
