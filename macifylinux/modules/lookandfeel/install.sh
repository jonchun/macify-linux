cd ~/sources/hello/kwin-effects/
mkdir -p qt5build
cd qt5build
cmake ../ -DCMAKE_INSTALL_PREFIX=/usr -DQT5BUILD=ON
cd ..
mkdir -p build
cd build
cmake -DCMAKE_INSTALL_PREFIX=/usr ..
make
sudo make install
kwin_x11 --replace &
plasmashell --replace &