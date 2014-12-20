#!/bin/bash

HOSTNAME="${1}"
BODY="${2}"

/usr/local/bin/mac_sendmail.sh "Updates available for ${HOSTNAME}" "${BODY}"
