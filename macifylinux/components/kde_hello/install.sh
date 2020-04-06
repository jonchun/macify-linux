#!/bin/bash
eval "$(python3 globals.py)"

REPO_NAME="hello"
REPO_URL="https://github.com/Jonchun/hello.git"

if [ ! -d ${SOURCES_DIR}/${REPO_NAME} ]
then
    # what to do if directory doesn't exist
    cd ${SOURCES_DIR}
    git clone $REPO_URL $REPO_NAME
else
    # what to do if directory already exists
    cd ${SOURCES_DIR}/${REPO_NAME}
    git fetch
fi

# Sorry I am not 100% sure what I'm doing here either. Just copy-pasting from the repos :D
# I didn't even do exactly what was documented and got it to work by mistake I think...
# https://github.com/n4n0GH/hello/issues/41#issuecomment-562063700

REPO_DIR=${SOURCES_DIR}/${REPO_NAME}
cd ${REPO_DIR}/kwin-effects/
mkdir -p build
cd build
cmake ../ -DCMAKE_INSTALL_PREFIX=/usr -DQT5BUILD=ON

cd ${REPO_DIR}
mkdir -p build
cd build
cmake -DCMAKE_INSTALL_PREFIX=/usr ..
make
sudo make install

cd ${REPO_DIR}/window-decoration
bash ./build.sh

# Install hello colors
cp -f ${SOURCES_DIR}/${REPO_NAME}/color-scheme/HelloLight.colors ${COLOR_SCHEMES_DIR}
cp -f ${SOURCES_DIR}/${REPO_NAME}/color-scheme/HelloDark.colors ${COLOR_SCHEMES_DIR}

# Install hello plasma theme
cp -rf ${SOURCES_DIR}/${REPO_NAME}/plasma-theme/hellolight ${PLASMA_DIR}
cp -rf ${SOURCES_DIR}/${REPO_NAME}/plasma-theme/hellodark ${PLASMA_DIR}

kwin_x11 --replace &
plasmashell --replace &