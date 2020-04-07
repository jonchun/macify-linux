#!/bin/bash
eval "$(python3 globals.py)"

# Sorry I am not 100% sure what I'm doing here either. Just copy-pasting from the repos :D
# I didn't even do exactly what was documented and got it to work by mistake I think...
# https://github.com/n4n0GH/hello/issues/41#issuecomment-562063700

REPO_DIR=${SOURCES_DIR}/hello

# build kwin-effects
cd ${REPO_DIR}/kwin-effects/
mkdir -p build
cd build
cmake ../ -DCMAKE_INSTALL_PREFIX=/usr -DQT5BUILD=ON

# build window-decoration
cd ${REPO_DIR}/window-decoration
bash ./build.sh

# build the entire project
cd ${REPO_DIR}
mkdir -p build
cd build
cmake -DCMAKE_INSTALL_PREFIX=/usr ..
make
sudo make install

# Install hello colors
cp -f ${REPO_DIR}/color-scheme/HelloLight.colors ${COLOR_SCHEMES_DIR}
cp -f ${REPO_DIR}/color-scheme/HelloDark.colors ${COLOR_SCHEMES_DIR}

# Install hello plasma theme
cp -rf ${REPO_DIR}/plasma-theme/hellolight ${PLASMA_DIR}
cp -rf ${REPO_DIR}/plasma-theme/hellodark ${PLASMA_DIR}
