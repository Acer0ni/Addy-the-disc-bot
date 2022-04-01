### Meet Addy

I started this project as an exercise to get more familiar with Python, and it has become an ongoing source of inspiration and exploration.

# Commands

[crypto](/readme/crypto.md)

[general](/readme/general.md)

[runescape](/readme/runescape.md)

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

## Migrate

To generate a new migration, make sure that the model you are trying to migrate is imported in `addy/models/__init__.py`.

Then run `alembic revision --autogenerate -m "{migration message}"` . Check the contents that is generated in alembic/version, when it is good run `alembic upgrade head`.
