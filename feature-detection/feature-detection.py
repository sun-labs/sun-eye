#!/usr/bin/env python3

import argparse

from lib.SunEye import SunEye


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process weather information from frame / video.')
    parser.add_argument('files', metavar='FILE', type=str, nargs='+')
    parser.add_argument('--atemp')
    parser.add_argument('--ahumid')
    parser.add_argument('--nogui', action='store_true')
    args = parser.parse_args()
    
    se = SunEye(args)
    info = se.processFiles(args.files)

    print(info)