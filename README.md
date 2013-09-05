spritzbot
=========

Twitter bot framework that uses streaming API and is simple to extend.

## Setting up

Create a virtual environment, install requirements.

```
$ virtualenv --distribute --no-site-packages venv
$ source venv/bin/activate
(venv)$ pip install -r requirements.txt
```

Edit ``credentials.sh`` and put in your details from dev.twitter.com, then
``$ source credentials.sh``

Finally run ``$ python spritzbot.py``


## Tutorial

Create a new file in 'extensions' directory, call it ``hello.py``,
Create a function named ``process_mention`` that expects ``status`` and
``settings`` as arguments.

```
def process_mention(status, settings):
    if status.text.lower() == ('@%s hello' % settings.username):
        return dict(response='Hello, world!')
    else:
        return None
```

This will automatically respond to the user who mentioned you.

You can use ``post='Hello, world!'`` instead of
``response='Hello, world!'`` to send a tweet out to your timeline.

``dm='Hello, world!'`` will send a direct message.

``follow=True`` will follow the user, similarly: ``unfollow=True``

You can use all the above options simultaneously in one response.

Create functions named ``process_dm``, ``process_follow`` to process
direct messages and follow-notifications.

## Running on Heroku

Deploy to Heroku, setup the prerequisites and local workstation setup
as laid out on: https://devcenter.heroku.com/articles/python

Run a `heroku config:set ` command with all the environment variables in `credentials.sh` 

Then skip over to deploy your app to heroku, finally issue
``heroku ps:scale bot=1``. Do NOT scale to more than 1.

Now confirm we're up - check logs with ``heroku logs --tail``

Finally, ask a friend to send you a @mention or a dm with just 'hello'.

Spritzbot does not have a web interface, so you will not see anything
if you visit the app url.
