#!/usr/bin/env python
# -*- coding: utf-8 -*-
##=========================================================
##  pingmt.py                                    7 Mar 2018
##
##  Eli Innis   @Doyousketch2
##  Doyousketch2 @ yahoo.com
##
##  GNU GPLv3                 gnu.org/licenses/gpl-3.0.html
##=========================================================
##  required  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

##  (linux)
##        sudo apt-get install fping

##=========================================================
##  libs  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import json
import urllib
import operator
from time import time
from subprocess import Popen, PIPE
begin  = time()

##=========================================================
##  get json  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

##  how many top servers printed on commandline?
##  read 'pinglist.txt' for the rest
howmany  = 30


url  = 'http://servers.minetest.net/list'
servers  = []
ports = []

response  = urllib .urlopen(url)
data  = json .loads( response .read() )

for key, val in enumerate( data['list'] ):
  addy  = val['address']
  port  = str(val['port'])

  if addy in servers:
    i = 1
    while servers[i] != addy:
      i += 1
    ports[i]  = ports[i] + ', ' + port

  else:
    servers .append( addy )
    ports .append( port )

## for testing purposes...
# servers  = ['192.168.1.1', '192.168.1.2', '192,168.1.255', '8,8,8,8', 'github.com', '192.168.1.1']
# ports  = ['30000', '30001', '30002', '30003', '30004', '30005']
##=========================================================
##  ping 'em  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

print('\nPinging {} servers...\n'.format( len(servers) ))
responses  = []

for server in servers:

  try:
    ping  = Popen( ['fping', '-e', '--timeout=333', server],  stdout=PIPE,  stderr=PIPE)
    stdout, stderr = ping .communicate()

    if stderr is not None and stdout[-12:-1] != 'unreachable' and len(stdout) > 8:
      responses .append( stdout )
      if stdout[-7] == '.' or stdout[-8] == '.':
        print(stdout)

  except:
    pass

##=========================================================
##  sort 'em  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

i = 0
for addr in responses:
  if addr[-8] == '.':
    text = '00' + addr[-10:-4] + 'ms  ' + addr[:-21]
  if addr[-7] == '.':
    text = '0' + addr[-9:-4] + 'ms  ' + addr[:-20]
  else:
    text  = addr[-8:-4] + 'ms  ' + addr[:-19]
  responses[i] = text
  i += 1

combined  = zip(responses, ports)
pingsorted  = sorted( combined, key=lambda x: x[0] )

outputtext = []
for i in range( len(pingsorted) ):
  text  = pingsorted[i][0] .lstrip('0') .lstrip('0') + '  : ' + pingsorted[i][1]
  outputtext .append( text )

##=========================================================
##  save 'em  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

output  = open('./pinglist.txt', 'w')
output .write('{} Minetest servers, sorted by ping speed\n'.format( len(pingsorted) ))
output .write('https://github.com/doyousketch2/Minetest-ping-sort\n\n')

print( 'your top {} servers are:\n'.format(howmany) )

top = 0
for addr in outputtext:
  output .write( '{}\n'.format( addr ))

  if top < howmany :
    print( addr )
    top += 1

output .write('\n')
output .close()

##=========================================================
##  done  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

elapsed  = time() -begin
print( '\nCompleted in {:.3f} seconds.'.format(elapsed) )
print( '\nSee pinglist.txt for sorted server response.' )
