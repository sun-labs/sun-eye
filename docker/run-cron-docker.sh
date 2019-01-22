#!/bin/bash

/usr/bin/docker run \
    --rm \
    --runtime=nvidia \
    -v /home/***REMOVED***/Development:/***REMOVED***/development \
    -v /sky/data:/***REMOVED***/data \
    -v /tmp:/tmp \
    ***REMOVED***/sun-eye-os \
    $1
