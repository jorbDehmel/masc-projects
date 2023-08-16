#!/usr/bin/bash
# Jordan Dehmel, 2023
# jdehmel@outlook.com, jedehmel@mavs.coloradomesa.edu
# github.com/jorbDehmel/masc-projects
# Default raspi username: pi password: raspberry

echo "This script updates the time exhibit when run."

echo "Checking for project updates..."
git pull > /dev/null

echo "Fixing permissions..."
chmod +x ./main.py > /dev/null
chmod +x ./update.sh > /dev/null

echo "Ensuring Python is up to date..."
sudo apt-get install python3 python-tk python3-pil.imagetk > /dev/null
sudo pip install tkinter ttkthemes pillow

echo "Done."
