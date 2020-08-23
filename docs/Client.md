# Client's Documentation

## Client
**Represents a client that connects to Transformice.
Two argument can be passed to the [`Client`](#Client).**

| Parameters | Type | Required | Description |
| :-: | :-: | :-: | :-- |
| community | `int` | ✕ |  Defines the community of the client. Defaults to 0 (EN community). |
| auto_restart | `bool` | ✕ |  Whether the client should automatically restart on error. Defaults to False. |
| bot_role | `bool` | ✕ |  Whether the has the game's special role bot or not. Avoids using the api endpoint and gives more stability. |
| loop | `event loop` | ✕ |  The [`event loop`](https://docs.python.org/3/library/asyncio-eventloops.html) to use for asynchronous operations. If ``None`` is passed (defaults), the event loop used will be ``asyncio.get_event_loop()``. |

| Attributes | Type | Can be None | Description |
| :-: | :-: | :-: | :-- |
| username | `str` | ✔ |  The bot's username received from the server. Might be None if the bot didn't log in yet. |
| room | [`Room`](Room.md#Room) | ✔ |  The bot's room. Might be None if the bot didn't log in yet or couldn't join any room yet. |
| trade | [`Trade`](Inventory.md#Trade) | ✔ |  The current trade that's going on (i.e: both traders accepted it). |
| trades | `list` | ✕ |  All the trades that the bot participates. Most of them might be invitations only. |
| inventory | [`Inventory`](Inventory.md#Inventory) | ✔ |  The bot's inventory. Might be None if the bot didn't log in yet or it didn't receive anything. |
| locale | [`Locale`](Locale.md#Locale) | ✕ |  The bot's locale (translations). |


### Methods
Client.**data\_received**(_self, data, connection_) <a id="Client.data_received" href="#Client.data_received">¶</a>
>
>Dispatches the received data.
>
>__Parameters:__
> * **data** - `bytes` the received data.
> * **connection** - [`Connection`](Connection.md) the connection that received

---

_coroutine_ Client.**handle\_packet**(_self, connection, packet_) <a id="Client.handle_packet" href="#Client.handle_packet">¶</a>
>
>Handles the known packets and dispatches events.
>Subclasses should handle only the unhandled packets from this method.
>
>__Example__:
>```Python
>class Bot(aiotfm.Client):
>	async def handle_packet(self, conn, packet):
>		handled = await super().handle_packet(conn, packet.copy())
>
>		if not handled:
>			# Handle here the unhandled packets.
>			pass
>```
>
>__Parameters:__
> * **connection** - [`Connection`](Connection.md) the connection that received
> * **packet** - [`Packet`](Packet.md) the packet.
>
>__Returns:__ True if the packet got handled, False otherwise.

---

_coroutine_ Client.**handle\_old\_packet**(_self, connection, oldCCC, data_) <a id="Client.handle_old_packet" href="#Client.handle_old_packet">¶</a>
>
>Handles the known packets from the old protocol and dispatches events.
>Subclasses should handle only the unhandled packets from this method.
>
>__Example__:
>```Python
>class Bot(aiotfm.Client):
>	async def handle_old_packet(self, conn, oldCCC, data):
>		handled = await super().handle_old_packet(conn, data.copy())
>
>		if not handled:
>			# Handle here the unhandled packets.
>			pass
>```
>
>__Parameters:__
> * **connection** - [`Connection`](Connection.md) the connection that received
> * **oldCCC** - `tuple` the packet identifiers on the old protocol.
> * **data** - `list` the packet data.
>
>__Returns:__ True if the packet got handled, False otherwise.

---

_coroutine_ Client.**\_heartbeat\_loop**(_self_) <a id="Client._heartbeat_loop" href="#Client._heartbeat_loop">¶</a>
>
>Send a packet every fifteen seconds to stay connected to the game.
---

Client.**get\_channel**(_self, name_) <a id="Client.get_channel" href="#Client.get_channel">¶</a>
>
>Returns a channel from it's name or None if not found.
>
>__Parameters:__
> * **name** - `str` the name of the channel.
>
>__Returns:__ [`ChannelMessage`](Message.md#ChannelMessage) or None

---

Client.**get\_trade**(_self, player_) <a id="Client.get_trade" href="#Client.get_trade">¶</a>
>
>Returns the pending/current trade with a player.
>
>__Parameters:__
> * **player** - [`Player`](Player.md) or `str` the player.
>
>__Returns:__ [`Trade`](Inventory.md#Trade) the trade with the player.

---

Client.**event**(_self, coro_) <a id="Client.event" href="#Client.event">¶</a>
>
>A decorator that registers an event.
>
>More about events [here](Events.md).
---

Client.**wait\_for**(_self, event, condition, timeout, stopPropagation_) <a id="Client.wait_for" href="#Client.wait_for">¶</a>
>
>Wait for an event.
>
>__Example__:
>```Python
>@client.event
>async def on_room_message(author, message):
>	if message == 'id':
>		await client.sendCommand('profile '+author)
>		profile = await client.wait_for('on_profile', lambda p: p.username == author)
>		await client.sendRoomMessage('Your id: {}'.format(profile.id))
>```
>
>__Parameters:__
> * **event** - `str` the event name.
> * **condition** - Optionnal[`function`] A predicate to check what to wait for.
> * **timeout** - Optionnal[`int`] the number of seconds before
>
>__Returns:__ [`asyncio.Future`](https://docs.python.org/3/library/asyncio-future.html#asyncio.Future)

---

_coroutine_ Client.**\_run\_event**(_self, coro, event_name, \*args, \*\*kwargs_) <a id="Client._run_event" href="#Client._run_event">¶</a>
>
>Runs an event and handle the error if any.
>
>__Parameters:__
> * **coro** - a coroutine function.
> * **event_name** - `str` the event's name.
> * **args** - arguments to pass to the coro.
> * **kwargs** - keyword arguments to pass to the coro.
>
>__Returns:__ `bool` whether the event ran successfully or not

---

Client.**dispatch**(_self, event, \*args, \*\*kwargs_) <a id="Client.dispatch" href="#Client.dispatch">¶</a>
>
>Dispatches events
>
>__Parameters:__
> * **event** - `str` event's name. (without 'on_')
> * **args** - arguments to pass to the coro.
> * **kwargs** - keyword arguments to pass to the coro.
>
>__Returns:__ [`Task`](https://docs.python.org/3/library/asyncio-task.html#asyncio.Task)

---

_coroutine_ Client.**on\_error**(_self, event, err, \*args, \*\*kwargs_) <a id="Client.on_error" href="#Client.on_error">¶</a>
>
>Default on_error event handler. Prints the traceback of the error.
---

_coroutine_ Client.**on\_connection\_error**(_self, conn, error_) <a id="Client.on_connection_error" href="#Client.on_connection_error">¶</a>
>
>Default on_connection_error event handler. Prints the error.
---

_coroutine_ Client.**on\_login\_result**(_self, code, \*args_) <a id="Client.on_login_result" href="#Client.on_login_result">¶</a>
>
>Default on_login_result handler. Raise an error and closes the connection.
---

_coroutine_ Client.**connect**(_self_) <a id="Client.connect" href="#Client.connect">¶</a>
>
>Creates a connection with the main server.
---

_coroutine_ Client.**sendHandshake**(_self_) <a id="Client.sendHandshake" href="#Client.sendHandshake">¶</a>
>
>Sends the handshake packet so the server recognizes this socket as a player.
---

_coroutine_ Client.**start**(_self, api_tfmid, api_token, keys_) <a id="Client.start" href="#Client.start">¶</a>
>
>Starts the client.
>
>__Parameters:__
> * **api_tfmid** - Optional[`int`] your Transformice id.
> * **api_token** - Optional[`str`] your token to access the API.

---

_coroutine_ Client.**restart\_soon**(_self, \*args, delay=5.0, \*\*kwargs_) <a id="Client.restart_soon" href="#Client.restart_soon">¶</a>
>
>Restarts the client in several seconds.
>
>__Parameters:__
> * **delay** - `int` the delay before restarting. Default is 5 seconds.
> * **args** - arguments to pass to the [`restart`](#Client.restart) method.
> * **kwargs** - keyword arguments to pass to the [`restart`](#Client.restart) method.

---

_coroutine_ Client.**restart**(_self, keys_) <a id="Client.restart" href="#Client.restart">¶</a>
>
>Restarts the client.
---

_coroutine_ Client.**login**(_self, username, password, encrypted, room_) <a id="Client.login" href="#Client.login">¶</a>
>
>Log in the game.
>
>__Parameters:__
> * **username** - `str` the client username.
> * **password** - `str` the client password.
> * **encrypted** - Optional[`bool`] whether the password is already encrypted or not.
> * **room** - Optional[`str`] the room where the client will be logged in.

---

Client.**run**(_self, api_tfmid, api_token, username, password, \*\*kwargs_) <a id="Client.run" href="#Client.run">¶</a>
>
>A blocking call that does the event loop initialization for you.
>
>__Equivalent to__:
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

Client.**close**(_self_) <a id="Client.close" href="#Client.close">¶</a>
>
>Closes the sockets.
---

_coroutine_ Client.**sendCP**(_self, code, data_) <a id="Client.sendCP" href="#Client.sendCP">¶</a>
>
>Send a packet to the community platform.
>
>__Parameters:__
> * **code** - `int` the community platform code.
> * **data** - [`Packet`](Packet.md) or `bytes` the data.

---

_coroutine_ Client.**sendRoomMessage**(_self, message_) <a id="Client.sendRoomMessage" href="#Client.sendRoomMessage">¶</a>
>
>Send a message to the room.
>
>__Parameters:__
> * **message** - `str` the content of the message.

---

_coroutine_ Client.**sendTribeMessage**(_self, message_) <a id="Client.sendTribeMessage" href="#Client.sendTribeMessage">¶</a>
>
>Send a message to the tribe.
>
>__Parameters:__
> * **message** - `str` the content of the message.

---

_coroutine_ Client.**sendChannelMessage**(_self, channel, message_) <a id="Client.sendChannelMessage" href="#Client.sendChannelMessage">¶</a>
>
>Send a message to a public channel.
>
>__Parameters:__
> * **channel** - `str` the channel's name.
> * **message** - `str` the content of the message.

---

_coroutine_ Client.**whisper**(_self, username, message, overflow_) <a id="Client.whisper" href="#Client.whisper">¶</a>
>
>Whisper to a player.
>
>__Parameters:__
> * **username** - `str` the player to whisper.
> * **message** - `str` the content of the whisper.
> * **overflow** - `bool` will send the complete message if True, splitted

---

_coroutine_ Client.**getFriendList**(_self_) <a id="Client.getFriendList" href="#Client.getFriendList">¶</a>
>
>Get the client's friend list>
>__Returns:__ List[[`Friend`](Friend.md)]  List of friends

---

_coroutine_ Client.**getTribe**(_self, disconnected_) <a id="Client.getTribe" href="#Client.getTribe">¶</a>
>
>Gets the client's [`Tribe`](Tribe.md) and return it
>
>__Parameters:__
> * **disconnected** - `bool` if True retrieves also the disconnected members.
>
>__Returns:__ [`Tribe`](Tribe.md) or ``None``.

---

_coroutine_ Client.**getRoomList**(_self, gamemode_) <a id="Client.getRoomList" href="#Client.getRoomList">¶</a>
>
>Get the room list
>
>__Parameters:__
> * **gamemode** - Optional[[`GameMode`](Enums.md#GameMode)] the room's gamemode.
>
>__Returns:__ [`RoomList`](Room.md#RoomList) the room list for the given gamemode

---

_coroutine_ Client.**playEmote**(_self, emote, flag_) <a id="Client.playEmote" href="#Client.playEmote">¶</a>
>
>Play an emote.
>
>__Parameters:__
> * **emote** - `int` the emote's id.
> * **flag** - Optional[`str`] the flag for the emote id 10. Defaults to 'be'.

---

_coroutine_ Client.**sendSmiley**(_self, smiley_) <a id="Client.sendSmiley" href="#Client.sendSmiley">¶</a>
>
>Makes the client showing a smiley above it's head.
>
>__Parameters:__
> * **smiley** - `int` the smiley's id. (from 0 to 9)

---

_coroutine_ Client.**loadLua**(_self, lua_code_) <a id="Client.loadLua" href="#Client.loadLua">¶</a>
>
>Load a lua code in the room.
>
>__Parameters:__
> * **lua_code** - `str` or `bytes` the lua code to send.

---

_coroutine_ Client.**sendCommand**(_self, command_) <a id="Client.sendCommand" href="#Client.sendCommand">¶</a>
>
>Send a command to the game.
>
>__Parameters:__
> * **command** - `str` the command to send.

---

_coroutine_ Client.**enterTribe**(_self_) <a id="Client.enterTribe" href="#Client.enterTribe">¶</a>
>
>Enter the tribe house
---

_coroutine_ Client.**enterTribeHouse**(_self_) <a id="Client.enterTribeHouse" href="#Client.enterTribeHouse">¶</a>
>
>Alias for [`enterTribe`](#Client.enterTribe)
---

_coroutine_ Client.**enterInvTribeHouse**(_self, author_) <a id="Client.enterInvTribeHouse" href="#Client.enterInvTribeHouse">¶</a>
>
>Join the tribe house of another player after receiving an /inv.
>
>__Parameters:__
> * **author** - `str` the author's username who sent the invitation.

---

_coroutine_ Client.**recruit**(_self, player_) <a id="Client.recruit" href="#Client.recruit">¶</a>
>
>Send a recruit request to a player.
>
>__Parameters:__
> * **player** - `str` the player's username you want to recruit.

---

_coroutine_ Client.**joinRoom**(_self, room_name, password, community, auto_) <a id="Client.joinRoom" href="#Client.joinRoom">¶</a>
>
>Join a room.
>The event 'on_joined_room' is dispatched when the client has successfully joined the room.
>
>__Parameters:__
> * **password** - `str` if given the client will ignore `community` and `auto` parameters
> * **room_name** - `str` the room's name.
> * **community** - Optional[`int`] the room's community.
> * **auto** - Optional[`bool`] joins a random room (I think).

---

_coroutine_ Client.**joinChannel**(_self, name, permanent_) <a id="Client.joinChannel" href="#Client.joinChannel">¶</a>
>
>Join a #channel.
>The event 'on_channel_joined' is dispatched when the client has successfully joined
>a channel.
>
>__Parameters:__
> * **name** - `str` the channel's name
> * **permanent** - Optional[`bool`] if True (default) the server will automatically

---

_coroutine_ Client.**leaveChannel**(_self, channel_) <a id="Client.leaveChannel" href="#Client.leaveChannel">¶</a>
>
>Leaves a #channel.
>
>__Parameters:__
> * **channel** - [`Channel`](Message.md#Channel) channel to leave.

---

_coroutine_ Client.**requestShopList**(_self_) <a id="Client.requestShopList" href="#Client.requestShopList">¶</a>
>
>Send a request to the server to get the shop list.
---

_coroutine_ Client.**startTrade**(_self, player_) <a id="Client.startTrade" href="#Client.startTrade">¶</a>
>
>Starts a trade with the given player.
>
>__Parameters:__
> * **player** - [`Player`](Player.md) the player to trade with.
>
>__Returns:__ [`Trade`](Inventory.md#Trade) the resulting trade

---

_coroutine_ Client.**requestInventory**(_self_) <a id="Client.requestInventory" href="#Client.requestInventory">¶</a>
>
>Send a request to the server to get the bot's inventory.
---

