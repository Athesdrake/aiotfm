# aiotfm

aiotfm is an asynchronous Client implementation of [Transformice](https://www.transformice.com/) that allows developers to make bots easily.
It uses an API endpoint to get the keys needed to connect to the game. To get access to this API you must ask *Tocutoeltuco* (preferably via discord: Tocutoeltuco#0018) by explaining your project.
aiotfm is based on [TransFromage](https://github.com/Tocutoeltuco/transfromage) which use threads instead of coroutines.

If you prefer Lua over Python then checkout the [Lua version](https://github.com/Lautenschlager-id/Transfromage) made by [@Lautenschlager-id](https://github.com/Lautenschlager-id)

## Advantages

- 3 times faster than TransFromage
- Compatible with discord.py
- Faster

### Speed

TransFromage takes around 13 seconds to be connected to the community platform while aiotfm takes less than 4 seconds.
Those results can vary depending on your computer and your internet connection.

## Installation

You can install aiotfm using pip:
`pip install aiotfm`

You can also clone this repository and install it manually:
```sh
git clone https://github.com/Athesdrake/aiotfm
cd aiotfm
python3 -m pip install .
```

### Requirements

aiotfm require python 3.5.3 or higher and [aiohttp](https://github.com/aio-libs/aiohttp).

### Update

To update aiotfm, use the following command:
`pip install -U aiotfm`

## Example

```Python
import aiotfm

bot = aiotfm.Client()

@bot.event
def on_ready():
	print('Connected to the community platform.')

bot.run("api_tfmid", "api_token", "username", "password", encrypted=False, room="start_room")
```

[A more complete example.](https://github.com/Athesdrake/aiotfm/blob/master/example_bot.py)

## Documentation

You can find the documentation of aiotfm [here](https://github.com/Athesdrake/aiotfm/tree/master/docs).

## About

You can have more information about TransFromage in this [thread](https://atelier801.com/topic?f=5&t=917024).