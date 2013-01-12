# -*- coding: utf-8 -*-
import random

def process_mention(status, settings):
    text = status.text.lower().replace('@'+settings.username, '').strip()
    tokens = text.split(' ')
    if tokens[0] == 'choose':
        choices = [x.strip() for x in ' '.join(tokens[1:]).split(',')]
        return dict(response=random.choice(choices))
