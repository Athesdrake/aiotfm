# Events Documentation

## on_raw_socket
>**This is triggered when a socket receives a packet.**
>
>|Parameters|Type|Description
>|:-:|:-:|-
>**connection** | [`Connection`](Connection.md) | The connection that has received the packet.
>**packet** | [`Packet`](Packet.md)| The packet.

---

## on_old_packet
>**This is triggered when a socket has received an old packet.**
>
>|Parameters|Type|Description
>|:-:|:-:|-
> **connection** | [`Connection`](Connection.md) | The connection that has received the packet.
> **oldCCC** | `tuple` | The packet identifiers.
> **data** | `list` | The packet data.

---

## on_joined_room
>**This is triggered when the [Client](Client.md) has successfully joined a room.**
>
>|Parameters|Type|Description
>|:-:|:-:|-
> **room_name** | `string` | The room name.
> **private** | `boolean`| Whether the room is private or not.

---

## on_room_message
>**This is triggered when the [Client](Client.md) has received a room message.**
>
>|Parameters|Type|Description
>|:-:|:-:|-
> **author** | `string` | The player sending the message.
> **content** | `string` | The message.

---

## on_profile
>**Triggered when the [Client](Client.md) recives a player's profile.**
>
>|Parameters|Type|Description
>|:-:|:-:|-
> **profile** | [`Profile`](Profile.md) | The player's profile.

---

## on_tribe_inv
>**This is triggered when the [Client](Client.md) is invited to a tribe house.**
>
>|Parameters|Type|Description
>|:-:|:-:|-
> **playerName** | `string` | The player who sent the invite.
> **tribe** | `string` | The tribe name.

---

## on_logged
>**This is triggered when the [Client](Client.md) successfully logs in.**
>
>|Parameters|Type|Description
>|:-:|:-:|-
> **player_id** | `integer` | The [Client](Client.md)'s id.
> **username** | `string` | The [Client](Client.md)'s username.
> **played_time** | `integer` | The total number of seconds the [Client](Client.md) has played.
> **community** | `integer` | The community id of the [Client](Client.md).
> **pid**| `integer` | The pid of the [Client](Client.md).

---

## on_login_ready
>**This is triggered when the [Client](Client.md) is ready to log in.**
>
>|Parameters|Type|Description
>|:-:|:-:|-
>**online_players** | `integer` | The number of players online.
>**community** | `string` | The [Client]'s community.
>**country** | `string` | The [Client]'s country.

---

## on_login_result
>**This triggers when the log-in procedure fails.**
>
>|Parameters|Type|Description
>|:-:|:-:|-
> |**result_id** | `integer` | The result id.
> |**result_message** | `string` | The result message.

---

## on_ping
>**This is triggered when the [Client](Client.md) sends a ping command.**
>
>|Parameters|Type|Description
>|:-:|:-:|-
>**id** | `integer` | The identifier of the ping.

---

## on_raw_cp
>**This is triggered when the [Client](Client.md) receives a community platform packet.**
>
>|Parameters|Type|Description
>|:-:|:-:|-
>**TC** | `integer` | The community platform packet identifiers.
>**packet** | [`Packet`](Packet.md) | The packet.

---

## on_tribe_message
>**This is triggered when a player sends a message in the tribe chat.**
>
>|Parameters|Type|Description
>|:-:|:-:|-
> **author** | `string` | The player's username.
> **content** | `string` | The message.

---

## on_whisper
>**This triggers when the [Client](Client.md) receives a whisper from another player.**
>
>|Parameters|Type|Description
>|:-:|:-:|-
> |**author**| `string` | The sender's username.
> | **commu** | `integer`| The senders's community.
> |**receiver**| `string` | The reciever's username.
> |**content** | `string` | The message.

---

## on_member_connected
>**This triggers when a tribe's member connects to Transformice.**
>
>|Parameters|Type|Description
>|:-:|:-:|-
>| **member** | `string` | The player's username.

---

## on_member_disconnected
>**This is triggered when a tribe's member disconnects.**
>
>|Parameters|Type|Description
>|:-:|:-:|-
>| **member** | `string` | The player's username.

---

## on_emoji
>**This is triggered when a player in the room shows an emoticon.**
>
>|Parameters|Type|Description
>|:-:|:-:|-
> **player** | [`Player`](Player.md) | The player's username.
> **emoji** | `integer` | The emoji id.
