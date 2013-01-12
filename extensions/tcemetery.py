# -*- coding: utf-8 -*-

# NOT SECURE, only an experiment, do NOT run this in production

def process_follow(status, settings):
    return dict(follow=True, dm='Ok, now tell me...')


def process_dm(status, settings):
    if status.direct_message.sender_screen_name != settings.username:
        return dict(post=status.direct_message.text, delete_dm=True)
