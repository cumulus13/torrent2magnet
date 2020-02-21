import sys
import os
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
    magnet = make_magnet_from_file(sys.argv[1])
    print(magnet)