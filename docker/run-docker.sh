#!/bin/bash

# LOCALLY
docker run \
    -it \
    --rm \
    --runtime=nvidia \
    --net=host \
    --ipc=host \
    -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -v /home/***REMOVED***/Development:/***REMOVED***/development \
    -v /sky/data:/***REMOVED***/data \
    ***REMOVED***/sun-eye-os

# -v /tmp/.X11-unix:/tmp/.X11-unix \