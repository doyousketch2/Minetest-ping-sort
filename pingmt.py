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

##=========================================================
##  script  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

begin  = time()

url  = 'http://servers.minetest.net/list'
servers  = []

response  = urllib .urlopen(url)
data  = json .loads( response .read() )

for key, val in enumerate( data['list'] ):
  addy  = val['address']
  if addy not in servers:
    servers .append( addy )

##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

print('\nPinging {} servers...\n'.format( len(servers) ))
responses  = []

for server in servers:

  try:
    ping  = Popen( ['fping', '-e', '-t400', server], stdout=PIPE, stderr=PIPE)
    stdout, stderr = ping .communicate()

    if stdout[-12:-1] != 'unreachable':
      responses .append( stdout )
    if stdout[-6] == '.'or stdout[-7] == '.':
      print(stdout)

  except:
    pass

##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

i = 0
for addr in responses:
  if addr[-6] == '.':
    responses[i] = '00' + addr[-10:-4] + 'ms  ' + addr[:-21]
  if addr[-7] == '.':
    responses[i] = '0' + addr[-9:-4] + 'ms  ' + addr[:-20]
  else:
    responses[i] = addr[-8:-4] + 'ms  ' + addr[:-19]
  i += 1

pingsorted  = sorted( responses )

for i in range(len(pingsorted)):
  pingsorted[i]  = pingsorted[i] .lstrip('0')

output  = open('./pinglist.txt', 'w')
output .write('{} Minetest servers, sorted by ping speed\n'.format( len(pingsorted) ))
output .write('https://github.com/doyousketch2/Minetest-ping-sort\n\n')

print('your top 20 servers are:')

top = 0
for addr in pingsorted:
  output .write( '{}\n'.format( addr ))

  if top < 20 :
    print( addr )
    top += 1

output .write('\n')
output .close()

##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

elapsed  = time() -begin
print( '\nCompleted in {:.3f} seconds.'.format(elapsed) )
print( '\nSee pinglist.txt for sorted server response.' )
