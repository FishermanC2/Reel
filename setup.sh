#!/bin/bash

# Flask setup
echo "FLASK_SECRET_KEY=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)" > app/.env

# Admin user setup
read -p "Enter admin username: " username
read -s -p "Enter admin password: " password

echo "ADMIN_USERNAME=${username}" >> app/.env
echo "ADMIN_PASSWORD=${password}" >> app/.env