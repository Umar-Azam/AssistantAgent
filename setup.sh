#! /usr/bin/bash
echo "Creating a virtual environment ~/.venv"
python3 -m venv ~/.venv
echo "Sourcing virtual environemnt "
source ~/.venv/bin/activate
echo "installing requirements"
pip install -r ./requirements.txt
