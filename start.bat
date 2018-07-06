@echo off
title Initialize Database and set Flask app
echo Starting up...
set FLASK_APP=daser.py
start flask run
exit