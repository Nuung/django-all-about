#!/bin/bash

if [ -f ./django_all_about/requirements.txt ]; then
    echo "SUCCESS: requirements.txt exists!"
else
    echo "FAILURE: requirements.txt does not exist!"
    exit 1
fi

REQUIREMENTS=$(cat ./django_all_about/requirements.txt)
NEW_REQUIREMENTS=$(pip freeze)

if [ "$NEW_REQUIREMENTS" = "$REQUIREMENTS" ]; then
    echo "SUCCESS: requirements.txt is up to date!"
    exit 0
else
    echo "FAILURE: requirements.txt is not up to date!"
    pip freeze > ./django_all_about/requirements.txt
    exit 1
fi