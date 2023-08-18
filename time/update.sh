#!/usr/bin/bash
# Jordan Dehmel, 2023
# jdehmel@outlook.com, jedehmel@mavs.coloradomesa.edu
# github.com/jorbDehmel/masc-projects
# Default raspi username: pi password: raspberry

echo "This script updates the time exhibit when run."
echo "jdehmel@outlook.com, 2023"

# Check for wifi
if ! ping google.com -c 1 > /dev/null ; then echo "ERROR: No internet connection!" ; fi

# Pull from git
echo "Checking for project updates..."
git pull > log.txt

# Make main.py and this update script executable
# so you can just double click on them if needed
echo "Fixing permissions..."
chmod +x ./main.py >> log.txt
chmod +x ./update.sh >> log.txt

# Ensure all Python dependancies are met on the system level
echo "Ensuring Python is up to date (this may take a while)..."
sudo apt-get install -y python3 python-tk python3-pil.imagetk

# Ensure all Python dependancies are met on the PIP level
echo "Installing Python packages (this may take a while)..."
sudo pip install ttkthemes pillow

# Install fonts
echo "Installing fonts..."
sudo cp fonts/* ~/.local/share/fonts
fc-cache -vf

echo "Done."
