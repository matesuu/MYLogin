#!/bin/bash

if ! command -v pip &> /dev/null; then
    echo "pip is not installed. installing..."
    sudo apt-get update
    sudo apt-get install python3-pip -y
fi

echo "installing dependencies..."

pip3 install cryptography

echo "success!"

exit 0
