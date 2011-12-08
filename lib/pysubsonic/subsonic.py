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

import urllib
import urllib2
#import json
import logging
from pysubsonic import const

log = logging.getLogger('pysubsonic.subsonic')

class Subsonic:
    '''
    >>> from subsonic import *
    >>> config = read_config()
    >>> s = Subsonic(config['auth']['url'], config['auth']['username'], config['auth']['password'])
    >>> s.ping()
    '{"subsonic-response": {\n "status": "ok",\n "version": "1.6.0",\n "xmlns": "http://subsonic.org/restapi"\n}}'
    '''
    def __init__(self, url, username, password, isenc = True):
        '''
        Creates an instance of a subsonic client connection. 
        +url+ - something like http://subsonic.home.lan:4040/
        +username+ - the user's username
        +password+ - the user's password. By default, expects the hex encoded password.
        +isenc+ - Boolean. Indicates whether +password+ is hex encoded. True by
                default. If set to False, then +password+ will be stored hex encoded.
        '''
        if url.endswith('/'):
            url = url + 'rest'
        elif not url.endswith('/') and not url.endswith('rest'):
            url = url + '/rest'
        self.url = url
        self.username = username
        if isenc:
            self.password = password
        else:
            self.password = password.encode("hex")

    def __mkparams__(self, params = {}):
        '''
        Returns the URL encoded portion of the parameters. Including the base
        information, plus any additional params passed as a dict.
        '''
        base_params = {   
                'u':self.username,
                'p':'enc:' + self.password,
                'v':const.APP_VERSION,
                'c':const.APP_NAME,
                'f':'json'}
        for k in params.keys():
            base_params[k] = params[k]
        return urllib.urlencode(base_params)

    def __get_meth__(self, meth, params):
        '''
        The generic getter for REST method calls.
        +meth+ - the API method
        +params+ - a dict of parameters. This can be {} 
        '''
        return urllib2.urlopen( self.url + '/' + meth, self.__mkparams__(params) ).read()

    def ping(self):
        '''
        Used to test connectivity with the server. Takes no extra parameters.

        Returns an empty <subsonic-response> element on success.
        '''
        return self.__get_meth__('ping', {})

    def getLicense(self):
        '''
        Get details about the software license. Takes no extra parameters.
        Please note that access to the REST API requires that the server has a
        valid license (after a 30-day trial period). To get a license key you
        can give a donation to the Subsonic project.

        Returns a <subsonic-response> element with a nested <license> element on success.
        '''
        return self.__get_meth__('getLicense', {})

    def getMusicFolders(self):
        '''
        Returns all configured top-level music folders. Takes no extra parameters.

        Returns a <subsonic-response> element with a nested <musicFolders> element on
        success.
        '''
        return self.__get_meth__('getMusicFolders', {})

    def getNowPlaying(self):
        '''
        Returns what is currently being played by all users. Takes no extra parameters.

        Returns a <subsonic-response> element with a nested <nowPlaying> element on success.
        '''
        return self.__get_meth__('getNowPlaying', {})

    def getIndexes(self, musicFolderId = None, ifModifiedSince = None):
        '''
        Returns an indexed structure of all artists.

        Parameter	Required	Default	Comment
        musicFolderId	No		If specified, only return artists in the music folder with the given ID. See getMusicFolders.
        ifModifiedSince	No		If specified, only return a result if the artist collection has changed since the given time.

        Returns a <subsonic-response> element with a nested <indexes> element on success.
        '''
        p = {}
        if musicFolderId:
            p['musicFolderId'] = musicFolderId
        if ifModifiedSince:
            p['ifModifiedSince'] = ifModifiedSince
        return self.__get_meth__('getIndexes', p)



