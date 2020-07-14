#!/bin/bash

/usr/bin/docker run \
    --rm \
    --runtime=nvidia \
    -v /home/username/Development:/**REMOVED**/development \
    -v /**REMOVED**/data:/**REMOVED**/data \
    -v /tmp:/tmp \
    **REMOVED**/sun-eye-os \
    $1
