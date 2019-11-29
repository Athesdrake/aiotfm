# Client Documentation

## Client
>**Represents the client that connects to Transformice.**
>
>| Parameters | Optional | Type | Description |
>| :-: | :-: | :-: | :-- |
>| `community` | ✔ | `integer`| The community the bot will connect to. Default is EN (0). 
>| `loop` | ✔ | `eventLoop` | The [`event loop`](https://docs.python.org/3/library/asyncio-eventloops.html) that will be used for asynchronous operations. If `None` is passed (which is default), the event loop that will be used will be ``asyncio.get_event_loop()``.


## Methods

### _coroutine_ received_data(self, data, connection)
This function is a *coroutine*.

Dispatches the received data.

* **data** `bytes` the received data.
* **connection** `aiotfm.connection.Connection` the connection that received the data.


### _coroutine_ handle_packet(self, connection:Connection, packet:Packet)
This function is a *coroutine*.

Handles the known packets and dispatches events.
Subclasses should handle only the unhandled packets from this method.

**Example:**
```Python
class SubClient(aiotfm.Client):
	async def handle_packet(self, conn, packet):
		tmp = packet.copy()
		handled = await super().handle_packet(conn, packet)
		packet = tmp

		if not handled:
			# Handle here the unhandled packets.
			pass
```

**Parameters**
* **connection** `aiotfm.connection.Connection` the connection that received the packet.
* **packet** [`Packet`](Packet.md) the packet.

**Returns**
True if the packet got handled, False otherwise.


### _coroutine_ \_heartbeat_loop(self)
This function is a *coroutine*.

Send a packet every ten seconds to stay connected to the game.

### event(self, coro)
A decorator that registers an event.
More about events [here](Events.md).


### wait_for(event, condition=None, timeout=None)
Wait for an event.

**Example:**
```Python
@client.event
async def on_room_message(author, message):
	if message=='id':
		await client.sendCommand('profile '+author)
		profile = await client.wait_for('on_profile', lambda p: p.username==author)
		await client.sendRoomMessage('Your id: {}'.format(profile.id))
```

**Parameters**
* **event** `str` the event name.
* **condition** Optionnal[`function`] A predicate to check what to wait for. The arguments must meet the parameters of the event being waited for.
* **timeout** Optionnal[`int`] the number of seconds before raise asyncio.TimeoutError
**Returns**
`asyncio.Future` a future that you must await.

### _coroutine_ \_run_event(self, coro, event_name, \*args, \*\*kwargs)
This function is a *coroutine*.

Runs an event and handles the error if any.

**Parameters**
* **coro** a coroutine function.
* **event_name** `str` the event's name.
* **args** arguments to pass to the coro.
* **kwargs** keyword arguments to pass to the coro.


### dispatch(self, event, \*args, \*\*kwargs)
Dispatches events

**Parameters**
* **event** `str` event's name. (without 'on_')
* **args** arguments to pass to the coro.
* **kwargs** keyword arguments to pass to the coro.


### _coroutine_ start(self, api_tfmid, api_token)
This function is a *coroutine*.

Connects the client to the game.

**Parameters**
* **api_tfmid** `int` or `str` your Transformice id.
* **api_token** `str` your token to access the API.


### _coroutine_ login(self, username, password, encrypted=True, room='1')
This function is a *coroutine*.

Log in the game.

**Parameters**
* **username** `str` the client username.
* **password** `str` the client password.
* **encrypted** Optional[`bool`] whether the password is already encrypted or not.
* **room** Optional[`str`] the room where the client will be logged in.


### run(self, api_tfmid, api_token, username, password, \*\*kwargs)
A blocking call that do the event loop initialization for you.

Equivalent to
```Python
@bot.event
async def on_login_ready(*a):
	await bot.login(username, password)

loop = asyncio.get_event_loop()
loop.create_task(bot.start(api_id, api_token))
loop.run_forever()
```


### _coroutine_ sendCP(self, code, data=b'')
This function is a *coroutine*.

Send a packet to the community platform.

**Parameters**
* **code** `int` the community platform code.
* **data** `Packet` or `bytes` the data.


### _coroutine_ sendRoomMessage(self, message)
This function is a *coroutine*.

Send a message to the room.

**Parameters**
* **message** `str` the content of the message.


### _coroutine_ sendTribeMessage(self, message)
This function is a *coroutine*.

Send a message to the tribe.

**Parameters**
* **message** `str` the content of the message.


### _coroutine_ whisper(self, username, message)
This function is a *coroutine*.

Whisper to a player.

**Parameters**
* **username** `str` the player to whisper.
* **message** `str` the content of the whisper.


### _coroutine_ getTribe(self, disconnected=True)
This function is a *coroutine*.

Gets the client's `Tribe` and return it

**Parameters**
* **disconnected** `bool` if True retrieves also the disconnected members.

**Returns**
`Tribe` or ``None``.


### _coroutine_ sendPrivateMessage(self, username, message)
This function is a *coroutine*.

Deprecated alias for `Client.whisper`.

**Parameters**
* **username** `str` the player to whisper.
* **message** `str` the content of the whisper.


### _coroutine_ playEmote(self, id, flag='be')
This function is a *coroutine*.

Play an emote.

**Parameters**
* **id** `int` the emote's id.
* **flag** Optional[`str`] the flag for the emote id 10. Defaults to 'be'.


### _coroutine_ sendSmiley(self, id)
This function is a *coroutine*.

Makes the client showing a smiley above it's head.

**Parameters**
* **id** `int` the smiley's id. (from 0 to 10)


### _coroutine_ loadLua(self, lua_code)
This function is a *coroutine*.

Load a lua code in the room.

**Parameters**
* **lua_code** `str` or `bytes` the lua code to send.


### _coroutine_ sendCommand(self, command)
This function is a *coroutine*.

Send a command to the game.

**Parameters**
* **command** `str` the command to send.


### _coroutine_ enterTribe(self)
This function is a *coroutine*.

Enter the tribe house


### _coroutine_ enterTribeHouse(self)
This function is a *coroutine*.

Alias for `#enterTribe`


### _coroutine_ joinRoom(self, room_name)
This function is a *coroutine*.

Join a room.
The event 'on_joined_room' is dispatched when the client has successfully joined the room.

**Parameters**
* **room_name** `str` the room's name.
* **community** Optional[`int`] the room's community.
* **auto** Optional[`bool`] joins a random room (I think).


### _coroutine_ enterInvTribeHouse(self, author)
This function is a *coroutine*.

Join the tribe house of another player after receiving an /inv.

**Parameters**
* **author** `str` the author's username who sent the invitation.


### _coroutine_ recruit(self, player)
This function is a *coroutine*.

Send a recruit request to a player.

**Parameters**
* **player** `str` the player's username you want to recruit.
