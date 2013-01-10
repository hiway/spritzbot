#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import imp
import json
import utils
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
    settings = utils.dotdictify(dict(username=os.getenv('USERNAME')))

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

        # Setup oauth_hook
        OAuthHook.consumer_key = os.getenv('CONSUMER_KEY')
        OAuthHook.consumer_secret = os.getenv('CONSUMER_SECRET')
        self.oauth_hook = OAuthHook(os.getenv('ACCESS_TOKEN'),
                               os.getenv('ACCESS_TOKEN_SECRET'))

    def start(self):
        """Connects to Twitter's streaming API"""
        session = requests.session(hooks={'pre_request':self.oauth_hook})
        client = session.post('https://userstream.twitter.com/1.1/user.json',
                              prefetch=False, verify=False)

        for line in client.iter_lines(chunk_size=1, decode_unicode=True):
            if line:
                data = json.loads(line)
                self.process(data)

    def process(self, data):
        """Processes every status/event coming in through streaming API
        """
        # Convert tweet to pythonic form
        status = utils.dotdictify(data)

        for ext_name in self.extensions:
            extension = self.extensions[ext_name]
            if 'text' in status:
                if '@'+self.settings.username in status.text:
                    if (hasattr(extension, 'process_mention') and
                        callable(getattr(extension, 'process_mention'))):
                        result = extension.process_mention(status,
                                                      settings=self.settings)
                        if result:
                            self.process_response(result, status)

            if 'direct_message' in status:
                if (hasattr(extension, 'process_dm') and
                    callable(getattr(extension, 'process_dm'))):
                    result = extension.process_dm(status,
                                                  settings=self.settings)
                    if result:
                        self.process_response(result, status)

    def process_response(self, result, status):
        result = utils.dotdictify(result)
        if 'direct_message' in status:
            screen_name = status.direct_message.sender_screen_name
        elif 'text' in status:
            screen_name = status.user.screen_name
        else:
            screen_name = ''

        if 'response' in result:
            self.post(result.response,
                      status.id,
                      screen_name)
        if 'message' in result:
            self.post(result.message)
        if 'dm' in result:
            self.post('d %s %s' %(screen_name,
                                  result.dm))


    def post(self, message, in_reply_to=None, mention=None):
        """Sends a tweet. If in_reply_to is set, the tweet is marked
        as in response to that tweet. If mention is set, @[mention] is
        automatically prepended before the tweet. Returns tweet_id if
        successful, None if failed.
        """
        if mention:
            message = '@%s %s' %(mention, message)

        session = requests.session(hooks={'pre_request':self.oauth_hook})
        session.post('http://api.twitter.com/1/statuses/update.json',
                      {'status': message,
                       'in_reply_to_status_id':in_reply_to,
                       'wrap_links': True})


if __name__ == '__main__':
    bot = SpritzBot()
    print bot.extensions
    bot.start()
    #bot.post('Chai time!')
