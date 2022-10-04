### Meet Addy

I started this project as an exercise to get more familiar with Python, and it has become an ongoing source of inspiration and exploration.

# Commands

[Crypto](/readme/crypto.md)

[General](/readme/general.md)

[Runescape](/readme/runescape.md)

[Watch2Gether](/readme/w2g.md)

# Development

## Install

Installing this application requires Pipenv. To Install Pipenv run `pip3 install pipenv`

```
Pipenv sync
```

## Config

Config is loaded from a .env from the root of the repository. You will need:

```
DISCORD_TOKEN = {your discord bot token here}
Discord_GUILD = {your server name}
ADDY_COMMAND_PREFIX = {preferred command prefix}
W2G_TOKEN = {your watch2gether api key}
DB_CREDENTIALS = {postgres username:password}
DB_HOSTNAME = {postgres hostname}
```

## Scoreboard Creation

For `!crytpohs` to work properly `scheduled.py createscoreboard` must be ran on a regular basis. You can do this manually or with various automated means. Right now i am using a cronjob to do it and if you are running this on a linux system heres how.

    # Edit this file to introduce tasks to be run by cron.
    #
    # Each task to run has to be defined through a single line
    # indicating with different fields when the task will be run
    # and what command to run for the task
    #
    # To define the time you can provide concrete values for
    # minute (m), hour (h), day of month (dom), month (mon),
    # and day of week (dow) or use '*' in these fields (for 'any').
    #
    # Notice that tasks will be started based on the cron's system
    # daemon's notion of time and timezones.
    #
    # Output of the crontab jobs (including errors) is sent through
    # email to the user the crontab file belongs to (unless redirected).
    #
    # For example, you can run a backup of all your user accounts
    # at 5 a.m every week with:
    # 0 5 * * 1 tar -zcf /var/backups/home.tgz /home/
    #
    # For more information see the manual pages of crontab(5) and cron(8)
    #
    # m h  dom mon dow   command
    0 16 * * * /home/larry/Addy/Addy-the-disc-bot/.venv/bin/python3 /home/larry/Addy/Addy-the-disc-bot/scheduled.py createscoreboard > /home/larry/addy.log 2>&1

In the terminal type `crontab -e` to open a crontab file. It may ask you to choose an editor. If you don't already have a preferred, I would recommend nano. Your editor will open up looking something like above. The format for setting up the job is {time to run} {python pathway} {script to run}. You can find help knowing how to set up the time [here](https://crontab.guru/).

## Migrate

To generate a new migration, make sure that the model you are trying to migrate is imported in `addy/models/__init__.py`.

Then run `alembic revision --autogenerate -m "{migration message}"`. Check the contents that are generated in alembic/version, when it is good run `alembic upgrade head`.
