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
    settings = utils.dotdictify(dict(
                    username=os.getenv('USERNAME'),
                    extensions=[],
                    ))

    def __init__(self, extensions):
        """Loads all plugins found in ``self.extensions_directory``
        into a dictionary at ``self.extensions``."""
        self.settings.extensions.extend(extensions)
        re_extension = re.compile('[^.].*\.py$') # match => [name].py
        for extension_file in os.listdir(self.extensions_directory):
            if re_extension.match(extension_file):
                name = extension_file[:-3]
                if name in self.settings.extensions:
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
                              prefetch=False, verify=True)

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

                elif (hasattr(extension, 'process_status') and
                    callable(getattr(extension, 'process_status'))):
                    result = extension.process_status(status,
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

            if ('event' in status and 'follow' in status.event and
                self.settings.username == status.target.screen_name):
                if (hasattr(extension, 'process_follow') and
                    callable(getattr(extension, 'process_follow'))):
                    result = extension.process_follow(status,
                                                  settings=self.settings)
                    if result:
                        self.process_response(result, status)

    def process_response(self, result, status):
        """Processes response from extensions."""
        result = utils.dotdictify(result)
        # Wrap twitter's various methods to return screen_name
        if 'direct_message' in status:
            screen_name = status.direct_message.sender_screen_name
        elif 'text' in status:
            screen_name = status.user.screen_name
        elif 'event' in status:
            screen_name = status.source.screen_name
        else:
            screen_name = ''

        if 'response' in result:
            self.post(result.response,
                      status.id,
                      screen_name)

        if 'post' in result:
            self.post(result.post)

        if 'dm' in result:
            self.post(u'd %s %s' %(screen_name,
                                  result.dm))

        if 'follow' in result:
            # follow user
            self.follow(screen_name, follow=True)

        if 'unfollow' in result:
            # unfollow user
            self.follow(screen_name, follow=False)

        if 'delete_dm' in result:
            self.delete_dm(status.direct_message.id)

        if 'force_unfollow' in result:
            self.force_unfollow(screen_name)


    def post(self, message, in_reply_to=None, mention=None):
        """Sends a tweet. If in_reply_to is set, the tweet is marked
        as in response to that tweet. If mention is set, @[mention] is
        automatically prepended before the tweet. Returns tweet_id if
        successful, None if failed.
        """
        if mention:
            message = u'@%s %s' %(mention, message)

        session = requests.session(hooks={'pre_request':self.oauth_hook})
        try:
            request = session.post('http://api.twitter.com/1.1/statuses/update.json',
                          {'status': message,
                           'in_reply_to_status_id':in_reply_to,
                           'wrap_links': True})
            return json.loads(request.text)['id']
        except:
            return None

    def follow(self, screen_name, follow=True):
        if follow:
            url = 'https://api.twitter.com/1.1/friendships/create.json'
        else:
            url = 'https://api.twitter.com/1.1/friendships/destroy.json'

        session = requests.session(hooks={'pre_request':self.oauth_hook})
        request = session.post(url,{'screen_name': screen_name})

    def delete_dm(self, id):
        url =  'https://api.twitter.com/1.1/direct_messages/destroy.json'
        session = requests.session(hooks={'pre_request':self.oauth_hook})
        request = session.post(url,{'id': id})

    def force_unfollow(self, screen_name):
        url_block = 'https://api.twitter.com/1.1/blocks/create.json'
        url_unblock = 'https://api.twitter.com/1.1/blocks/destroy.json'
        session = requests.session(hooks={'pre_request':self.oauth_hook})
        request = session.post(url_block,{'screen_name': screen_name})
        request = session.post(url_unblock,{'screen_name': screen_name})


if __name__ == '__main__':
    bot = SpritzBot(extensions=os.getenv('SPRITZBOT_EXTENSIONS',
                                         default='hello').split(','))
    print bot.extensions
    bot.start()
