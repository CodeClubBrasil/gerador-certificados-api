#!/bin/bash
gunicorn --bind 0.0.0.0:80 app:app