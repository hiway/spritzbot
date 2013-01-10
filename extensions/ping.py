# -*- coding: utf-8 -*-

def process_mention(status, settings):
    print status.user.screen_name,':', status.text
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
    }

    if text in responses:
        return dict(response=responses[text])
