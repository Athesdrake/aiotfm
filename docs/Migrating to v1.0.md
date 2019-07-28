The v1.0 version of aiotfm comes with a lot of changes.
The documentation of all new methods and objects will come shortly.

# Messages
All event related to messages are now called with the appropriate object.

E.g.
```Python
@bot.event
async def on_whisper(message):
	if message.author=='AtHeSdRaKe': # True !
		if message.content=='stop':
			await message.reply('Shutting down ...') # Shortcut for
			# await bot.whisper(message.author, 'Shutting down ...')
			bot.close()
```

Check `message.py` for more.