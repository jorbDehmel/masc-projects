#!/usr/bin/bash
# Jordan Dehmel, 2023
# jdehmel@outlook.com, jedehmel@mavs.coloradomesa.edu
# github.com/jorbDehmel/masc-projects
# Default raspi username: pi password: raspberry

echo "This script updates the time exhibit when run."
echo "jdehmel@outlook.com, 2023"

# Check for wifi
if ! ping google.com -c 1 > /dev/null ; then echo "ERROR: No internet connection!" ; fi

echo "Checking for project updates..."
git pull > log.txt

echo "Fixing permissions..."
chmod +x ./main.py >> log.txt
chmod +x ./update.sh >> log.txt

echo "Ensuring Python is up to date (this may take a while)..."
sudo apt-get install -y python3 python-tk python3-pil.imagetk

echo "Installing Python packages (this may take a while)..."
sudo pip install ttkthemes pillow

echo "Making app start on system powerup..."

# Copy old crontab
touch newcron
if crontab -l ; then crontab -l > newcron ; fi

# Append new command to it
echo "@reboot python3 "$(pwd)"/main.py" >> newcron

# Put new crontab into place
crontab newcron
rm newcron

echo "Done."
