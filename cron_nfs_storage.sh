#!/bin/bash

####################################
## Helper script for cron.        ##
## Run xs_nfs_storage.py in venv  ##
##                                ##
## input parameters: run | delete ##
####################################

# configuranble options
INSTALL_PATH="/opt"
VENV_DIR_NAME="xs-venv"

# do not touch
if [ "$1" == "run" ] || [ "$1" == "delete" ]; then
    source $INSTALL_PATH/xs-nfs-storage/$VENV_DIR_NAME/bin/activate
    python3 $INSTALL_PATH/xs-nfs-storage/xs_nfs_storage.py $1
    deactivate
else
    echo
    echo "Usage:"
    echo " cron_nfs_storage.sh [options]"
    echo
    echo " Try 'cron_nfs_storage.sh <run|delete>'"
    echo
fi
