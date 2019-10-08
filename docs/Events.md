# Events

## on_raw_socket
Triggered when a socket has received a packet.

**Parameters**
- connection [`Connection`](Connection.md) The connection that has received the packet.
- packet [`Packet`](Packet.md) The packet.

## on_old_packet
Triggered when a socket has received a old packet.

**Parameters**
- connection [`Connection`](Connection.md) The connection that has received the packet.
- oldCCC `tuple` The packet identifiers.
- data `list` The packet data.

## on_joined_room
Triggered when the [Client] has successfully joined a room.

**Parameters**
- room_name `str` The room's name.
- private `bool` Whether the room is private or not.

## on_room_message
Triggered when the [Client] has received a room message.

**Parameters**
- author `str` The author of the message.
- content `str` The content of the message.

## on_profile
Triggered when the [Client] has received the profile of a player.

**Parameters**
- profile [`Profile`](Profile.md) The player's profile.

## on_tribe_inv
Triggered when a player invite the [Client] to its tribe house.

**Parameters**
- author `str` author's username.
- tribe `str` author's tribe name.

## on_logged
Triggered when the [Client] has successfully logged on.

**Parameters**
- player_id `int` The [Client]'s id.
- username `str` The [Client]'s username.
- played_time `int` The total number of seconds the [Client] has played.
- community `int` The community id of the [Client].
- pid `int` The pid of the [Client].

## on_login_ready
Triggered when the [Client] is ready to log in.

**Parameters**
- online_players `int` The number of players online.
- community `str` The [Client]'s community.
- country `str` The [Client]'s country.

## on_login_result
Triggered when log in failed.

**Parameters**
- result_id `int` The result id.
- result_message `str` The result message.

## on_ping
Triggered when the [Client] sent a ping command.

**Parameters**
- id `int` The identifier of the ping.

## on_raw_cp
Triggered when the [Client] received a community platform packet.

**Parameters**
- TC `int` The community platform packet identifiers.
- packet [`Packet`](Packet.md)

## on_tribe_message
Triggered when the [Client] has received a message in the tribe chat.

**Parameters**
- author `str` The message's author.
- content `str` the message's content.

## on_whisper
Triggered when the [Client] has received a whisper from another player.

**Parameters**
- author `str` The message's author.
- commu `int` The author's community.
- receiver `str` The message's receiver.
- content `str` The message's content.

## on_member_connected
Triggered when a tribe's member has connected.

**Parameters**
- member `str` The member username.

## on_member_disconnected
Triggered when a tribe's member has disconnected.

**Parameters**
- member `str` The member username.

## on_emoji
Triggered when a player in the room shows an emoji.

**Parameters**
- player [`Player`] The player who executed the emoji.
- emoji `int` The emoji id.

> References:
>
> \[`Client`]: Client.md
> \[`Player`]: Player.md
