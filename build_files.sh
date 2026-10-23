#!/usr/bin/env bash
# Vercel build script
pip install -r requirements.txt
python3 manage.py collectstatic --noinput --clear
