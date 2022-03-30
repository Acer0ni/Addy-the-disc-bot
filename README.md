### Meet Addy

I started this project as an exercise to get more familiar with Python, and it has become an ongoing source of inspiration and exploration.

# Commands

## Count

### **!count**

Replies with the amount of times this command has been run since last restart.

## 99

### **!99**

Replies with a random brooklyn 99 quote.

## Coin

### **!coin {coin symbol}**

Returns the price of the looked up coins.

Supported coins: eth,btc,matic,sol,dot

## Uptime

### **!uptime**

Responds with how long the bot has been online.

## High Scores Lookup

### **!hs {username}**

Returns with the stats of the specified player in Runescape 3.

## Bestiary Lookup

### **!beast {monster name}**

Returns with the information on the requested monster.

## Create

### **!create {video url}**

Creates a room for you and your friends on Watch2Gether with the specified video.

## Play

### **!play {video url}**

Plays the specified video immediately in your personal room. If you do not have one, it creates one for you

## Add

### **!add {video url} {title}**

Adds the video to your room's queue. If you do not have a room, it creates a room for you with the specified video.

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
