#!/usr/bin/env python3
# File: ../torrent2magnet/torrent2magnet.py
# Author: Hadi Cahyadi <cumulus13@gmail.com>
# Date: 2025-12-10
# Description: 
# License: MIT

import sys
import os
import clipboard
import argparse
try:
    import bencodepy
except ImportError:
    print("Please install bencodepy before !")
    os.system("pip install bencodepy")
    sys.exit(0)
import hashlib
import base64

def make_magnet_from_file(file) :
    metadata = bencodepy.decode_from_file(file)
    #print("metadata =", metadata[b'info'].keys())
    subj = metadata[b'info']
    hashcontents = bencodepy.encode(subj)
    digest = hashlib.sha1(hashcontents).digest()
    b32hash = base64.b32encode(digest).decode()
    return 'magnet:?'\
             + 'xt=urn:btih:' + b32hash\
             + '&dn=' + metadata[b'info'][b'name'].decode()\
             + '&tr=' + metadata[b'announce'].decode()\
             + '&xl=' + str(metadata[b'info'][b'piece length'])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='t2m')
    parser.add_argument("FILE", help="File *.torrent")
    parser.add_argument('-c', '--clip', help='Copy result to clipboard', action='store_true')
    
    if len(sys.argv) == 1:
        parser.print_help()
    else:
        args = parser.parse_args()

        magnet = make_magnet_from_file(args.FILE)
        if args.clip:
            clipboard.copy(magnet)
        print(magnet)
