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

class Unphp :
  # simple Class for unphp.net API
  def __init__(self, api_key, filetodec) :
    self.api_key = api_key
    self.filetodec = open(filetodec, 'rb')

  def send_post(self) :
    # I will be using requests like in the API example
    import requests
    data = {
          'api_key' : self.api_key
    }
    files = {
              'file' : self.filetodec
    }
    r = requests.post('http://www.unphp.net/api/v2/post', files=files, data=data)
    return r.text

  def parser(self, text) :
    import json
    return json.loads(text)

