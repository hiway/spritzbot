def process_mention(status, settings):
    if status.user.screen_name == settings.username:
        return dict(response='Hello, world!')
    else:
        return None
