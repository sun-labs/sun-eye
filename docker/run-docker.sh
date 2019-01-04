#!/bin/bash

# LOCALLY
docker run \
    -it \
    --rm \
    --runtime=nvidia \
    --env="DISPLAY" \
    --workdir="/home/$USER" \
    --volume="/home/$USER:/home/$USER" \
    --volume="/etc/group:/etc/group:ro" \
    --volume="/etc/passwd:/etc/passwd:ro" \
    --volume="/etc/shadow:/etc/shadow:ro" \
    --volume="/etc/sudoers.d:/etc/sudoers.d:ro" \
    --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
    -v /home/***REMOVED***/Development:/***REMOVED***/development \
    ***REMOVED***/sun-eye-os

# WITH SSH
docker run \
    -it \
    --rm \
    --runtime=nvidia \
    -v /home/***REMOVED***/Development:/***REMOVED***/development \
    ***REMOVED***/sun-eye-os

# -v /tmp/.X11-unix:/tmp/.X11-unix \