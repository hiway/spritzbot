# -*- coding: utf-8 -*-

def process_mention(status, settings):
    print status.user.screen_name,':', status.text.encode('utf-8')
    if status.text.lower() == ('@%s hello' % settings.username):
        return dict(response='Hello, %s!' % status.user.screen_name)

    if status.text.lower() == ('@%s unfollow' % settings.username):
        return dict(unfollow=True, response=u'If you insist… unfollowing.')


def process_follow(status, settings):
    print status.source.screen_name, 'followed.'
    return dict(follow=True, dm='Followed you back!')


def process_dm(status, settings):
    print status.direct_message.sender_screen_name,':', status.direct_message.text.encode('utf-8')
    if status.direct_message.text.lower() == 'hello':
        return dict(dm='Hello, %s!' % status.direct_message.sender_screen_name)
    else:
        return None

def process_status(status, settings):
    print status.user.screen_name,':', status.text.encode('utf-8')
