#!/bin/bash

/usr/bin/docker run \
    --rm \
    --runtime=nvidia \
    -v /home/***REMOVED***/Development:/***REMOVED***/development \
    -v /sky/data:/***REMOVED***/data \
    ***REMOVED***/sun-eye-os \
    $1
