'''
Copyright (c) 2011 Vincent Batts, Vienna, VA, USA

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or
sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

import os
import logging
from ConfigParser import ConfigParser
from pysubsonic import const

log = logging.getLogger('pysubsonic.config')

def build_config(file):
    print 'Generating new configuration file "%s"' % file
    url = raw_input("Enter subsonic server url (i.e."
            " http://subsonic.home.lan:4040/: ")
    username = raw_input("Enter username: ")
    password = raw_input("Enter password: ").encode("hex")

    sect = 'auth'
    config = ConfigParser()
    config.add_section(sect)
    config.set(sect, 'url', url)
    config.set(sect, 'username', username)
    config.set(sect, 'password', password)
    with open(file, 'wb') as configfile:
        config.write(configfile)
    return True

def read_config(file = const.DEFAULT_CONF_FILE):
    configdict = dict()
    file = os.path.expanduser(file)

    if not os.path.exists(file):
        if not build_config(file):
            return False

    config = ConfigParser()
    config.read([file])

    for sect in config.sections():
        configdict[sect] = dict()
        for i in config.items(sect):
            (k,v) = i
            configdict[sect][k] = v

    log.debug(configdict)
    return configdict


