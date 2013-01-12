# -*- coding: utf-8 -*-
import random

def process_mention(status, settings):
    print status.user.screen_name,':', status.text.encode('utf-8')
    text = status.text.lower().replace('@'+settings.username, '').strip()

    responses = {
        'ping':'pong',
        'pong':u'err…',
        'k':'kk',
        'kk':'kkk',
        'kkk':'kkkk',
        'kkkk':'ENOUGH!',
        u'के':u'केके',
        u'केके':u'काय हे?',
        'rock':random.choice(['rock','paper','scissors']),
        'paper':random.choice(['rock','paper','scissors']),
        'scissors':random.choice(['rock','paper','scissors']),
    }

    if text in responses:
        return dict(response=responses[text])
