#!/bin/sh

GIT_CMD=$(which git 2>/dev/null)
if [ -z "$GIT_CMD" ]
then
    echo "git not found. need to install it!"
    sudo apt-get install -y git
fi

mkdir -p ~/sources
cd ~/sources
git clone https://github.com/Jonchun/macify-linux.git
cd macify-linux
python3 setup.py