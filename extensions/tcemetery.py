# -*- coding: utf-8 -*-

# NOT SECURE, only an experiment, do NOT run this in production

def process_follow(status, settings):
    return dict(follow=True, dm="Ok, now tell me... (simply DM me 'bye' so I'll unfollow)")


def process_dm(status, settings):
    if status.direct_message.sender_screen_name != settings.username:
        if status.direct_message.text.lower().strip() == 'bye':
            return dict(dm='Cya!', delete_dm=True, force_unfollow=True)

        return dict(post=status.direct_message.text, delete_dm=True)
