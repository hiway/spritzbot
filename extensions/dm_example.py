def process_dm(status, settings):
    if status.direct_message.text.lower() == 'hello':
        return dict(dm='Hello, world!')
    else:
        return None
    print status.direct_message.text.lower()
