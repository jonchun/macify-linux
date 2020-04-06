eval "$(python3 globals.py)"

cd ${SOURCES_DIR}
mkdir -p albert-build
cd albert-build
cmake ../albert -DCMAKE_INSTALL_PREFIX=/usr/local -DCMAKE_BUILD_TYPE=Debug
make
sudo make install
