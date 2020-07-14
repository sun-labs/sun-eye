#!/bin/bash

/usr/bin/docker run \
    -it \
    --rm \
    --runtime=nvidia \
    --net=host \
    --ipc=host \
    -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -v /home/username/Development:/**REMOVED**/development \
    -v /**REMOVED**/data:/**REMOVED**/data \
    -v /tmp:/tmp \
    **REMOVED**/sun-eye-os \
    $1
