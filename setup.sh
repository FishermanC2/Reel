#!/bin/bash

# Flask setup
echo "FLASK_SECRET_KEY=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)" > api/.env

# Admin user setup
read -p "Enter admin username: " username
read -s -p "Enter admin password: " password

echo "ADMIN_AUTH_USERNAME=${username}" >> api/.env
echo "ADMIN_AUTH_PASSWORD=${password}" >> api/.env