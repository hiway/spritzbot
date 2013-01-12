# -*- coding: utf-8 -*-

# NOT SECURE, only an experiment, do NOT run this in production

def process_follow(status, settings):
    return dict(follow=True, dm="Ok, now tell me... (simply DM me 'bye' so I'll unfollow)")


def process_dm(status, settings):
    if status.direct_message.sender_screen_name != settings.username:
        if status.direct_message.text.lower().strip() == 'bye':
            return dict(dm='Cya!', delete_dm=True, force_unfollow=True)

        # scrape mentions
        text = status.direct_message.text.replace('@','')

        # scrape DMs
        if text[:2] == 'd ' or text[:2] == 'm ':
            text = text[2:]

        trigger_words = ['suicide',
                         'kill myself',
                         'end my life',
                         'end this life',
                         'end it all',
                         "don't want to live",
                         'no reason to live',
                         'unwilling to live',
                         'why must I live',
                         'should i live',
                         'should i die',
                         'want to die',
                         'i could die',
                         'end this life',
                         'kill myself']

        for word in trigger_words:
            if word in text:
                return dict(post=text, dm="I've posted that, but I'm "
                            "concerned, are you alright? Talk to "
                            "someone, talk to me.", delete_dm=True)

        return dict(post=text, delete_dm=True)
