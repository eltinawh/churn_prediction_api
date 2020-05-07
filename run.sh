#!/bin/bash
# To prepare environment and launch the app
# For local test only
# Usage: ./run.sh

# prepare python virtual environment
pip install --uprage pip
pip install pipenv
if [ ! -f 'Pipfile.lock' ]; then
    pipenv --python 3.7
    pipenv shell
    pipenv install -r requirements.txt
fi

# run the app
pipenv run gunicorn --bind 0.0.0.0:5000 server:app & sleep 2 & x-www-browser http://0.0.0.0:5000/health
