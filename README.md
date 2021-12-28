# aiotfm

aiotfm is an asynchronous Client implementation of [Transformice](https://www.transformice.com/) that allows developers to make bots easily.
It uses an API endpoint to get the keys needed to connect to the game.
aiotfm is based on [TransFromage](https://github.com/Tocutoeltuco/transfromage) which use threads instead of coroutines.

If you prefer Lua over Python then checkout the [Lua version](https://github.com/Lautenschlager-id/Transfromage) made by [@Lautenschlager-id](https://github.com/Lautenschlager-id)

Join the **_[Fifty Shades of Lua](https://discord.gg/qmdryEB)_** [discord](https://discordapp.com/) server to discuss about this API and to receive special support.

## Keys Endpoint

This API depends on an [endpoint](https://api.tocu.tk/get_transformice_keys.php) that gives you access to the Transformice encryption keys.

To use it you will need a token which you can get by [applying through this form](https://forms.gle/N6Et1hLGQ9hmg95F6). See below to know the names of Transfromage managers who handle the token system.
- **[Tocutoeltuco](https://github.com/Tocutoeltuco)** @discord=> `Tocu#0018` <sub>`212634414021214209`</sub>;
- **[Blank3495](https://github.com/Blank3495)** @discord=> `󠂪󠂪 󠂪󠂪 󠂪󠂪󠂪󠂪 󠂪󠂪 󠂪󠂪󠂪󠂪 󠂪󠂪 󠂪󠂪#8737` <sub>`436703225140346881`</sub>;
- **[Bolodefchoco](https://github.com/Lautenschlager-id)** @discord=> `Lautenschlager#2555` <sub>`285878295759814656`</sub>.

## Advantages

- 3 times faster than TransFromage
- Compatible with discord.py
- Faster
- Asynchronous

### Speed

TransFromage takes around 13 seconds to be connected to the community platform while aiotfm takes less than 4 seconds.
Those results can vary depending on your computer and your internet connection.

## Installation

You can install aiotfm using pip:
`pip install aiotfm`

To have a more up to date package, you have to clone this repository and install it manually:
```sh
git clone https://github.com/Athesdrake/aiotfm
cd aiotfm
python3 -m pip install .
```

### Requirements

aiotfm require python 3.7 or higher and [aiohttp](https://github.com/aio-libs/aiohttp).

### Python 3.6

Python 3.6 support is not guaranteed since [v1.4.3](https://github.com/Athesdrake/aiotfm/releases/tag/v1.4.3) as Python 3.6 has reached EOF.

#### Python 3.5

You can still use aiotfm with Python 3.5.3 or higher by cloning the repository and remove the sugar syntax of Python 3.6.
These changes are the typed variables and fstrings.
Due to a major update in the asynchronous stuff of Python 3.5.3, aiotfm is not compatible with the previous versions of Python.

### Update

To update aiotfm, use the following command:
`pip install -U aiotfm`

## Example

```Python
import aiotfm

bot = aiotfm.Client()


@bot.event
async def on_ready():
	print('Connected to the community platform.')

bot.run("api_tfmid", "api_token", "username", "password", encrypted=False, room="start_room")
```

[A more complete example.](https://github.com/Athesdrake/aiotfm/blob/master/example_bot.py)

## Documentation

You can find the documentation of aiotfm [here](https://github.com/Athesdrake/aiotfm/tree/master/docs).

## About

You can have more information about TransFromage in this [thread](https://atelier801.com/topic?f=5&t=917024).