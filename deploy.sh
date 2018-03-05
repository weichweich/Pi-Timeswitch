#!/bin/bash

sudo rm -rf dist/
unzip ~/Downloads/dist.zip -d ~
sudo chown -R www-data:www-data ~/dist
sudo venv/bin/pip install -e dist/backend
sudo rm -rf /var/www/timeswitch
sudo mv dist/frontend /var/www/timeswitch
~/startup.sh
