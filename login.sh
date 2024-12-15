#!/bin/bash
python3 -m MY_LOGIN_CLI

pycache="__pycache__"

if [ -d "$pycache" ]; then
    rm -r "$pycache"
    echo "deleted __pycache"

else
    exit 1

fi

exit 0
