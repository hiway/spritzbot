#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import imp
import json
import requests

from oauth_hook import OAuthHook

class SpritzBot:
    """Twitter bot framework, loads extensions, connects via streaming
    API and hands over incoming statuses/events to extensions after
    converting json to pythonic objects.
    """
    extensions = {} # list of extensions loaded from directory.
    extensions_directory = os.getenv('EXTENSION_DIRECTORY',
                                     default='extensions')

    def __init__(self):
        """Loads all plugins found in ``self.extensions_directory``
        into a dictionary at ``self.extensions``."""
        re_extension = re.compile('[^.].*\.py$') # match => [name].py
        for extension_file in os.listdir(self.extensions_directory):
            if re_extension.match(extension_file):
                name = extension_file[:-3]
                ext_info = imp.find_module(name, [self.extensions_directory])
                extension = imp.load_module(name, *ext_info)
                self.extensions[name] = extension

    def start(self):
        """Connects to Twitter's streaming API"""
        OAuthHook.consumer_key = os.getenv('CONSUMER_KEY')
        OAuthHook.consumer_secret = os.getenv('CONSUMER_SECRET')
        oauth_hook = OAuthHook(os.getenv('ACCESS_TOKEN'),
                               os.getenv('ACCESS_TOKEN_SECRET'))

        session = requests.session(hooks={'pre_request':oauth_hook})
        client = session.post('https://userstream.twitter.com/1.1/user.json',
                              prefetch=False, verify=False)

        for line in client.iter_lines(chunk_size=1, decode_unicode=True):
            if line:
                data = json.loads(line)
                print data

if __name__ == '__main__':
    bot = SpritzBot()
    print bot.extensions
    bot.start()
