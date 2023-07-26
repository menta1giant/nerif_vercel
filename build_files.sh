#!/bin/bash

pip install -r requirements.txt

# make migrations
python3.0 manage.py migrate 
python3.9 manage.py collectstatic