#!/bin/bash

if [ -f ./django_all_about/requirements.txt ]; then
    echo "SUCCESS: requirements.txt exists!"
else
    echo "FAILURE: requirements.txt does not exist!"
    exit 1
fi