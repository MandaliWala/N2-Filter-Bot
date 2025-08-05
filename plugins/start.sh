#!/bin/bash

# Update & upgrade system
apt update && apt upgrade -y

apt install git -y           
pip install -U pip    

# Clone the repo 
if [ -z $UPSTREAM_REPO ]
then
  echo "Cloning main Repository"
  git clone https://github.com/MandaliWala/N2-Filter-Bot /N2FilterBot
else
  echo "Cloning Custom Repo from $UPSTREAM_REPO "
  git clone $UPSTREAM_REPO /N2FilterBot
fi

# Upgrade pip and install requirements
cd /ProfessorBot
pip install -U -r requirements.txt --force-reinstall

# Start bot
echo "Starting Bot....✨"
python3 bot.py