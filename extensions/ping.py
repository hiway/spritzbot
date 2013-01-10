def process_mention(status, settings):
    print status.user.screen_name,':', status.text
    text = status.text.lower().replace('@'+settings.username, '').strip()
    responses = dict(
        ping='pong',
        pong='err?',
        k='kk',
        kk='kkk',
        kkk='enough!',
        ok='ko',
        ko='okay',
        okay='ok',
    )
    if text in responses:
        return dict(response=responses[text])
