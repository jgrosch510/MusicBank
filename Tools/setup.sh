#!/usr/bin/bash

ID=`id -u`
GRP=`id -g`
SITE_DIR="/tmp/usr/local/site"
PWD=`pwd`

sudo touch /tmp/TEST
RC=$?
if [ $RC != 0 ]; then 
    echo "ERROR: you lack sudo privileges."
    echo "Install sudo and do the following command"
    echo "cat <<EOF >> /etc/sudoers"
    echo "${USER} ALL=(ALL) NOPASSWD:ALL"
    echo "EOF"
    exit 1
fi

sudo mkdir -p ${SITE_DIR}/{bin,data,etc,log,repo}
sudo rsync -av ${PWD}/usr/local/site/* ${SITE_DIR}

sudo chown -R root:${GRP} ${SITE_DIR}
sudo chmod -R g+w  ${SITE_DIR}
