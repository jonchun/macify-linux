eval "$(python3 globals.py)"

REPO_NAME="albert"
REPO_URL="https://github.com/Jonchun/albert.git"

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

cd ${SOURCES_DIR}
mkdir -p ${REPO_NAME}-build
cd ${REPO_NAME}-build
cmake ../albert -DCMAKE_INSTALL_PREFIX=/usr/local -DCMAKE_BUILD_TYPE=Debug
make
sudo make install
