#!/usr/bin/env bash

# this script deploys the current directory to the remote server, ecluding directiries starting with a dot.

REMOTE_IP=192.168.6.215
REMOTE_USER=build
REMOTE_PATH=/home/build/Software/lil_rovr2/
LOCAL_PATH=$(dirname "$0")

echo "Deploying ${LOCAL_PATH} to ${REMOTE_USER}@${REMOTE_IP}:${REMOTE_PATH}"

# deploy 
rsync -avz --progress --exclude '.*' ${LOCAL_PATH} ${REMOTE_USER}@${REMOTE_IP}:${REMOTE_PATH}

# setup SSH known hosts specifically for WSL SSH or Linux: (which ignores the windows home directory ssh keys)
# ssh-copy-id -i ~/.ssh/id_rsa.pub build@192.168.6.215

# URL: http://192.168.6.215:5000/