#!/usr/bin/env python2

########################################################################################
#   unphp                                                                              #
#   Copyright (C) 2015  Mohamed Aziz Knani                                             #
#                                                                                      #
#   This program is free software; you can redistribute it and/or                      #
#   modify it under the terms of the GNU General Public License                        #
#   as published by the Free Software Foundation; either version 2                     #
#   of the License, or (at your option) any later version.                             #
#                                                                                      #
#   This program is distributed in the hope that it will be useful,                    #
#   but WITHOUT ANY WARRANTY; without even the implied warranty of                     #
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                      #
#   GNU General Public License for more details.                                       #
#                                                                                      #
#   You should have received a copy of the GNU General Public License                  #
#   along with this program; if not, write to the Free Software                        #
#   Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.    #
########################################################################################

import unphp
import argparse
from sys import argv

class Colors():

  PURPLE = '\033[95m'
  CYAN = '\033[96m'
  DARKCYAN = '\033[36m'
  BLUE = '\033[94m'
  GREEN = '\033[92m'
  YELLOW = '\033[93m'
  RED = '\033[91m'
  BOLD = '\033[1m'
  ENDC = '\033[0m'

def output(jsonobj, verbosemode, newfilename) :
  # I used sys.stdout intead of print for printing on the same line
  from sys import stdout
  print '\n'
  if jsonobj['result'] == 'success' :
    print Colors.GREEN+ '[*] Decrypted with success!'+Colors.ENDC
  else :
    print Colors.RED+ '[-] Decryption failed :('+Colors.ENDC
  if verbosemode :
    print '\n'
    def for_out(obj) :
      for x in obj :
        stdout.write(x+' ')
        stdout.flush()
      stdout.write('\n')

    stdout.write('[+] Functions : ')
    for_out(jsonobj['functions'].iterkeys())
    stdout.write('[+] Urls : ')
    for_out(jsonobj['urls'])
    stdout.write('[+] Emails : ')
    for_out(jsonobj['emails'])
    print '[+] MD5 : '+ jsonobj['md5']
    print Colors.CYAN+'Decrypted file -> '+newfilename+Colors.ENDC

def save_decrypted(filename, url) :
  from os.path import splitext
  import requests
  # Getting new filename
  fn, extension = splitext(filename)
  newprefix = fn+'_dec'+extension
  # Get the file
  resp = requests.get(url, stream=True)
  with open(newprefix, 'wb') as out_file :
    out_file.write(resp.text)
  return newprefix

def one(api, filen) :
  # Function to deal with one file
  un = unphp.Unphp(api, filen)
  text = un.send_post()
  jsonobj = un.parser(text)
  newfilename = save_decrypted(filen, jsonobj['output'])
  output(jsonobj, args.verbose is True, newfilename)

class readapi :
  def __init__(self) :
    self.filename = '.key'

  def exist(self) :
    from os.path import exists
    return exists(self.filename)

  def readkey(self) :
    with open(self.filename, 'r') as fn :
      key = fn.read().rstrip()

    return key

  def writekey(self, apikey) :
    with open(self.filename, 'w') as fn :
      fn.write(apikey)

parser = argparse.ArgumentParser()
parser.add_argument('-k', help='Set the unphp.net API key', dest='api')
parser.add_argument('-s', help='Get API key from saved a .key file', action='store_true')
parser.add_argument('-v', '--verbose', help='Increase output verbosity', action='store_true')
parser.add_argument('-f', help='Set file to decrypt', dest='file')
parser.add_argument('-d', help='Set directory to decrypt', dest='directory')
args = parser.parse_args()

if len(argv) == 1 :
  print parser.print_help()

else :
  if args.file and (args.api or (args.s and readapi().exist())) :
    one(args.api or readapi().readkey(), args.file)
  elif args.directory and (args.api or (args.s and readapi().exist()))  :
    import glob
    from os.path import join
    # Get only PHP non decrypted files from directory
    files =  [ f for f in glob.glob(join(args.directory, '*.php')) if '_dec' not in f ]
    for file1 in files :
      one(args.api or readapi().readkey(), file1)

  else :
    print 'Please provide an API key and a PHP file or a directory'
    exit()
