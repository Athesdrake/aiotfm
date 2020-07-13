# Events' Documentation

## on_raw_socket(_connection, packet_)
Called when a socket receives a packet. Does not interfere with [`handle_packet`](#Client.handle_packet).
>__Parameters:__
> * **connection** - [`Connection`](Connection.md) the connection that received the packet.
> * **packet** - [`Packet`](Packet.md) a copy of the packet.

---

## on_old_packet(_connection, oldCCC, data_)
Called when an old packet is received. Does not interfere with [`handle_old_packet`](#Client.handle_old_packet).
>__Parameters:__
> * **connection** - [`Connection`](Connection.md) the connection that received the packet.
> * **oldCCC** - `tuple` the packet identifiers on the old protocol.
> * **data** - `list` the packet data.

---

## on_joined_room(_room_)
Called when the client has joined a room.
>__Parameters:__
> * **room** - [`Room`](Room.md#Room) the room the client has entered.

---

## on_room_password(_room_)
Called when a password is required to enter a room
>__Parameters:__
> * **room** - [`Room`](Room.md#Room) the room the server is asking for a password.

---

## on_room_message(_message_)
Called when the client receives a message from the room.
>__Parameters:__
> * **message** - [`Message`](Message.md#Message) the message.

---

## on_server_message(_message, \*args_)
Called when the client receives a message from the server that needs to be translated.
>__Parameters:__
> * **message** - [`Translation`](Locale.md#Translation) the message translated with the current locale.
> * **\*args** - a list of string used as replacement inside the message.

---

## on_emote(_player, emote, flag_)
Called when a player plays an emote.
>__Parameters:__
> * **player** - [`Player`](Player.md) the player.
> * **emote** - `int` the emote's id.
> * **flag** - `str` the flag's id.

---

## on_emoji(_player, emoji_)
Called when a player is showing an emoji above its head.
>__Parameters:__
> * **player** - [`Player`](Player.md) the player.
> * **emoji** - `int` the emoji's id.

---

## on_player_won(_player, order, player_time_)
Called when a player get the cheese to the hole.
>__Parameters:__
> * **player** - [`Player`](Player.md) the player.
> * **order** - `int` the order of the player in the hole.
> * **player_time** - `float` player's time in the hole in seconds.

---

## on_profile(_profile_)
Called when the client receives the result of a /profile command.
>__Parameters:__
> * **profile** - [`Profile`](Player.md#Profile) the profile.

---

## on_shop(_shop_)
Called when the client receives the content of the shop.
>__Parameters:__
> * **shop** - [`Shop`](Shop.md#Shop) the shop.

---

## on_skills(_skills_)
Called when the client receives its skill tree.
>__Parameters:__
> * **skills** - `dict` the skills.

---

## on_tribe_inv(_author, tribe_)
Called when the client receives an invitation to a tribe. (/inv)
>__Parameters:__
> * **author** - `str` the player that invited you.
> * **tribe** - `str` the tribe.

---

## on_logged(_uid, username, played_time, community, pid_)
Called when the client successfully logged in.
>__Parameters:__
> * **uid** - `int` the client's unique id.
> * **username** - `str` the client's username.
> * **played_time** - `int` the total number of minutes the client has played.
> * **community** - [`Community`](Enums.md#Community) the community the client has connected to.
> * **pid** - `int` the client's player id.

---

## on_login_ready(_online_players, community, country_)
Called when the client can login through the game.
>__Parameters:__
> * **online_players** - `int` the number of player connected to the game.
> * **community** - [`Community`](Enums.md#Community) the community the server suggest.
> * **country** - `str` the country detected from your ip.

---

## on_login_result(_code, code, code_)
Called when the client failed logging.
>__Parameters:__
> * **code** - `int` the error code.
> * **code** - `str` error messages.
> * **code** - `str` error messages.

---

## on_ping()
Called when the client receives the ping response from the server.

---

## on_lua_log(_log_)
Called when the client receives lua logs from #Lua.
>__Parameters:__
> * **log** - `str` a log message.

---

## on_inventory_update(_inventory_)
Called when the client receives its inventory's content.
>__Parameters:__
> * **inventory** - [`Inventory`](Inventory.md#Inventory) the client's inventory.

---

## on_item_update(_item, previous_)
Called when the quantity of an item has been updated.
>__Parameters:__
> * **item** - [`InventoryItem`](Inventory.md#InventoryItem) the new item.
> * **previous** - [`InventoryItem`](Inventory.md#InventoryItem) the previous item.

---

## on_new_item(_item_)
Called when the client receives a new item in its inventory.
>__Parameters:__
> * **item** - [`InventoryItem`](Inventory.md#InventoryItem) the new item.

---

## on_trade_invite(_trade_)
Called when received an invitation to trade.
>__Parameters:__
> * **trade** - [`Trade`](Inventory.md#Trade) the trade object.

---

## on_trade_error(_trade, error_)
Called when an error occurred with a trade.
>__Parameters:__
> * **trade** - [`Trade`](Inventory.md#Trade) the trade that failed.
> * **error** - [`TradeError`](Enums.md#TradeError) the error.

---

## on_trade_start()
Called when a trade starts. You can access the trade object with `Client.trade`.

---

## on_trade_item_change(_trader, id, quantity, item_)
Called when an item has been added/removed from the current trade.
>__Parameters:__
> * **trader** - [`Player`](Player.md) the player that triggered the event.
> * **id** - `int` the item's id.
> * **quantity** - `int` the quantity added/removed. Can be negative.
> * **item** - [`InventoryItem`](Inventory.md#InventoryItem) the item after the change.

---

## on_trade_lock(_who, locked_)
Called when the trade got (un)locked.
>__Parameters:__
> * **who** - [`Player`](Player.md) the player that triggered the event.
> * **locked** - `bool` either the trade got locked or unlocked.

---

## on_raw_cp(_TC, packet_)
Called when the client receives a packet from the community platform.
>__Parameters:__
> * **TC** - `int` the packet's code.
> * **packet** - [`Packet`](Packet.md) the packet.

---

## on_ready()
Called when the client is successfully connected to the community platform.

---

## on_channel_joined_result(_result_)
Called when the client receives the result of joining a channel.
>__Parameters:__
> * **result** - `int` result code.

---

## on_channel_left_result(_result_)
Called when the client receives the result of leaving a channel.
>__Parameters:__
> * **result** - `int` result code.

---

## on_channel_who(_idSequence, players_)
Called when the client receives the result of the /who command in a channel.
>__Parameters:__
> * **idSequence** - `int` the reference to the packet that performed the request.
> * **players** - List[[`Player`](Player.md)] the list of players inside the channel.

---

## on_channel_joined(_channel_)
Called when the client joined a channel.
>__Parameters:__
> * **channel** - [`Channel`](Message.md#Channel) the channel.

---

## on_channel_closed(_name_)
Called when the client leaves a channel.
>__Parameters:__
> * **name** - `str` the channel's name.

---

## on_channel_message(_message_)
Called when the client receives a message from a channel.
>__Parameters:__
> * **message** - [`ChannelMessage`](Message.md#ChannelMessage) the message.

---

## on_tribe_message(_author, message_)
Called when the client receives a message from the tribe.
>__Parameters:__
> * **author** - `str` the message's author.
> * **message** - `str` the message's content.

---

## on_whisper(_message_)
Called when the client receives a whisper.
>__Parameters:__
> * **message** - [`Whisper`](Message.md#Whisper) the message.

---

## on_member_connected(_name_)
Called when a tribe member connected.
>__Parameters:__
> * **name** - `str` the member's name.

---

## on_member_disconnected(_name_)
Called when a tribe member disconnected.
>__Parameters:__
> * **name** - `str` the member's name.

---

## on_bulk_player_update(_before, players_)
Called when the client receives an update of all player in the room.
>__Parameters:__
> * **before** - Dict[[`Player`](Player.md)] the list of player before the update.
> * **players** - Dict[[`Player`](Player.md)] the list of player updated.

---

## on_player_join(_player_)
Called when a player joined the room.
>__Parameters:__
> * **player** - [`Player`](Player.md) the player.

---

## on_player_update(_before, player_)
Called when a player's data on the room has been updated.
>__Parameters:__
> * **before** - [`Player`](Player.md) the player before the update.
> * **player** - [`Player`](Player.md) the player updated.

---

## on_player_died(_player_)
Called when a player dies.
>__Parameters:__
> * **player** - [`Player`](Player.md) the player.

---

## on_player_remove(_player_)
Called when a player leaves the room.
>__Parameters:__
> * **player** - [`Player`](Player.md) the player.

---

## on_heartbeat(_time_)
Called at each heartbeat.
>__Parameters:__
> * **time** - `float` the time took to send the keep-alive packet.

---

## on_restart()
Notify when the client restarts.

---

## on_connection_made(_connection_)
Called when a connection has been successfully made with the server.
>__Parameters:__
> * **connection** - [`Connection`](#Connection) the connection that has been made.

---

## on_connection_error(_connection, exception_)
Called when a connection has been lost due to an error.
>__Parameters:__
> * **connection** - [`Connection`](#Connection) the connection that has been lost.
> * **exception** - `Exception` the error which occurred.

---

## on_trade_close(_trade, succed_)
Called when a trade is closed.
>__Parameters:__
> * **trade** - [`Trade`](Inventory.md#Trade) the trade object.
> * **succed** - `bool` whether or not the trade is successful.

---

