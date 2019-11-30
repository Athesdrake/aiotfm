# Client Documentation

## Client
>**Represents the client that connects to Transformice.**
>
>| Parameters | Type | Required | Description |
>| :-: | :-: | :-: | :-- |
>| `community` | `integer`| ✕ | The community the bot will connect to. Default is EN (0). 
>| `loop` | `eventLoop` | ✕ | The [`event loop`](https://docs.python.org/3/library/asyncio-eventloops.html) that will be used for asynchronous operations. If `None` is passed (which is default), the event loop that will be used will be ``asyncio.get_event_loop()``.


## Methods
### _coroutine_ received_data(self, data, connection)
>
>**Dispatches the received data.**
>
>| Parameters | Type | Description |
>| :-: | :-: | :-- |
>| **data** | `bytes` | The data recieved. 
>| **connection** | `aiotfm.connection.Connection` | The connection (name) that recieved the data. 

---

### _coroutine_ handle_packet(self, connection:Connection, packet:Packet)
>
>**Handles the known packets and dispatches events.
>The unhandled packets in this method should only be handled by subclasses.**
>
>| Parameters | Type | Required | Description |
>| :-: | :-: | :-: | :-
>| **connection** | `aiotfm.connection.Connection` | The connection that recieved the packet 
>| **packet** | [`Packet`](Packet.md) | The packet recieved
>
>**Returns**: `True` if the packet got handled, otherwise `False`.
>
>**Example:**
>```Python
>class SubClient(aiotfm.Client):
>	async def handle_packet(self, conn, packet):
>		tmp = packet.copy()
>		handled = await super().handle_packet(conn, packet)
>		packet = tmp
>
>		if not handled:
>			# Handle here the unhandled packets.
>			pass
>```

---

### _coroutine_ \_heartbeat_loop(self)
>**This sends a packet every ten seconds to stay connected to the game.**

---

### event(self, coro)
>**This is the decorator that registers an event.
>Learn more about events [here](Events.md).**

---

### wait_for(event, condition=None, timeout=None)
>**Waits for an event.**
>
>| Parameters | Type | Required | Description
>| :-: | :-: | :-: | :--
>| **event** | `string` | ✔ | The event name.
>| **condition** | `function` | ✕ | A predicate to check what to wait for. The arguments **must** meet the parameters of the event being waited for.
>| **timeout** | `int` | ✕ | The number of seconds to wait before `asyncio.TimeoutError` is raised.
>
>**Returns**: `asyncio.Future` that the user must await
>
>**Example:**
>```Python
>@client.event
>async def on_room_message(author, message):
>	if message=='id':
>		await client.sendCommand('profile '+author)
>		profile = await client.wait_for('on_profile', lambda p: p.username==author)
>		await client.sendRoomMessage('Your id: {}'.format(profile.id))
>```

---

### _coroutine_ \_run_event(self, coro, event_name, \*args, \*\*kwargs)
>**Runs an event and handles any errors found.**
>
>| Parameters | Type | Required | Description
>| :-: | :-: | :-: | :-- 
>| **coro** | `function` | ✔ | A coroutine function
>| **event_name** | `string` | ✔ | The name of the event
>| **\*args** | `*args` | ✔ | Arguments to be passed in the coroutine
>|**\*\*kwagrs** | `**kwargs` | ✔ | Keyword arguments to passed in the coroutine

---

### dispatch(self, event, \*args, \*\*kwargs)
>**Dispatches events**
>
>| Parameters | Type | Required | Description
>| :-: | :-: | :-: | :-- 
>| **event** | `string` | ✔ |The name of the event without `on_`
>| **\*args** | `*args` | ✔ |Arguments to be passed in the coroutine
>|**\*\*kwargs** | `**kwargs` | ✔ | Keyword arguments to passed in the coroutine

---

### _coroutine_ start(self, api_tfmid, api_token)
>**Connects the client to the game.**
>
>| Parameters | Type | Required | Description
>| :-: | :-: | :-: | :-- 
>| **api_tfm_id** | `int` or `string` | ✔ | Your Transformice ID.
>| **api_token** | `string` | ✔ | Your API token.

---

### _coroutine_ login(self, username, password, encrypted=True, room='1')
>**Log in the game.**
>
>| Parameters | Type | Required | Description
>| :-: | :-: | :-: | :--
>| **username** | `string` | ✔ | The client username.
>| **password** | `string` | ✔ | The client password.
>| **encrypted** | `boolean` | ✕ | Whether the password is already encrypted or not.
>| **room** | `string` | ✕ | The room where the client will log on to.

---

### run(self, api_tfmid, api_token, username, password, \*\*kwargs)
>**A blocking call that initializes the event loop for you.**
>
>**Doing this will also produce the same result:** 
>```Python
>@bot.event
>async def on_login_ready(*a):
>	await bot.login(username, password)
>
>loop = asyncio.get_event_loop()
>loop.create_task(bot.start(api_id, api_token))
>loop.run_forever()
>```

---

### _coroutine_ sendCP(self, code, data=b'')
>**Sends a packet to the community platform.**
>
>| Parameters | Type | Required | Description
>| :-: | :-: | :-: | :-- 
>| **code** | `integer` | ✔ | The community platform code
>| **data** | `Packet` or `bytes` | ✔ | The data to be sent

---

### _coroutine_ sendRoomMessage(self, message)
>**Send a message to the room.**
>
>| Parameters | Type | Required | Description
>| :-: | :-: | :-: | :-- 
>| **message** | `string` | ✔ | The message content

---

### _coroutine_ sendTribeMessage(self, message)
>**Send a message in the tribe chat.**
>
>| Parameters | Type | Required | Description
>| :-: | :-: | :-: | :-- 
>| **message** | `string` | ✔ | The message content

---

### _coroutine_ whisper(self, username, message)
>**Whispers a player.**
>
>| Parameters | Type | Required | Description
>| :-: | :-: | :-: |:--
>| **username** | `string` | ✔ | The player who will recieve the whisper
>| **message** | `string` | ✔ | The message to be whispered

---

### _coroutine_ getTribe(self, disconnected=True)
>**Gets the client's `Tribe` and returns it**
>
>| Parameters | Type | Required | Description
>| :-: | :-: | :-: | :--
>| **disconnected** | `boolean` | ✔ | If it should return the list of offline members.
>
>**Returns**: `Tribe` or ``None``.

---

### _coroutine_ playEmote(self, id, flag='be')
>**Plays an emote.**
>
>| Parameters | Type | Required | Description
>| :-: | :-: | :-: | :--
>| **id** | `integer` | ✔ | The emote id
>| **flag** | `string` | ✕ | The flag to be displayed.
>
>**NOTE: The emote id must be 10 in order to show a flag.**

---

### _coroutine_ sendSmiley(self, id)
>**Makes the client show an emoticon above it's head.**
>
>| Parameters | Type | Description
>| :-: | :-: | :--
>| **id** | `integer` | The emoticon id `(1 - 10)`

---

### _coroutine_ loadLua(self, lua_code)
>**Loads a lua code in the room.**
>
>| Parameters | Type | Description
>| :-: | :-: | :--
>| **lua_code** | `string` or `bytes` | The lua code to load.

---

### _coroutine_ sendCommand(self, command)
>**Sends a "/" command in the game.**
>
>| Parameters | Type | Description
>| :-: | :-: | :--
>| **command** | `string` | The command to send

---

### _coroutine_ enterTribe(self)
>**Joins the tribe house if the client is in a tribe.**

---

### _coroutine_ enterTribeHouse(self)
>**Alias for `enterTribe` function**

---

### _coroutine_ joinRoom(self, room_name)
>**Joins a room.
>The event 'on_joined_room' is dispatched when the client has successfully joined the room.**
>
>| Parameters | Type | Required | Description
>| :-: | :-: | :-: | :--
>| **room_name** | `string` | ✔ | The room name
>| **community** | `intger` | ✕ | The room community
>| **auto** | `boolean` | ✕ | Joins a random room

---

### _coroutine_ enterInvTribeHouse(self, author)
>**Join the tribe house after receiving an /inv from a player.**
>
>| Parameters | Type | Description
>| :-: | :-: | :--
>| **author** | `string` | The player who sent the invite

---

### _coroutine_ recruit(self, player)
>**Sends a tribe invite to a player.**
>
>| Parameters | Type | Required | Description
>| :-: | :-: | :-: | :--
>| **player** | `string` | ✔ | The player to be invited
