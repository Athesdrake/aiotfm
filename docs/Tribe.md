# Tribe's Documentation

## Tribe
**Represents a tribe.**

| Attributes | Type | Can be None | Description |
| :-: | :-: | :-: | :-- |
| id | `int` | ✕ |  The tribe's id. |
| name | `str` | ✕ |  The tribe's name. |
| welcomeMessage | `str` | ✕ |  The tribe's welcome message. |
| mapcode | `int` | ✕ |  The tribehouse's mapcode. |
| members | `list` | ✕ |  The members' list of the tribe. |
| ranks | `list` | ✕ |  The ranks' list of the tribe. |

## Member
**Represents a tribe's member.**

| Attributes | Type | Can be None | Description |
| :-: | :-: | :-: | :-- |
| tribe | [`Tribe`](#tribe) | ✕ |  The member's tribe. |
| id | `int` | ✕ |  The player's id of the member. |
| name | `str` | ✕ |  The username of the member. |
| gender | `int` | ✕ |  The member's gender. |
| lastConnection | `:class` | ✕ |  The last connection of the member. |
| rank_id | `int` | ✕ |  The rank's id of the member. |
| game_id | `int` | ✕ |  The game's id the player is playing. |
| room | `str` | ✕ |  The room where the player is. |
| rank | [`Rank`](#rank) | ✕ |  The member's rank. |
| online | `bool` | ✕ |  True if the member is online. |


### Methods
@*property*<br>
Member.**rank**(_self_) <a id="Member.rank" href="#Member.rank">¶</a>
>
>return the :class:`Rank` of the member.
---

@*property*<br>
Member.**online**(_self_) <a id="Member.online" href="#Member.online">¶</a>
>
>return True if the member is online.
---

## Rank
**Represents a tribe's rank.**

| Attributes | Type | Can be None | Description |
| :-: | :-: | :-: | :-- |
| id | `int` | ✕ |  The rank's id. |
| name | `str` | ✕ |  The rank's name. |
| perm | `int` | ✕ |  The rank's permissions. |


### Methods
@*property*<br>
Rank.**isLeader**(_self_) <a id="Rank.isLeader" href="#Rank.isLeader">¶</a>
>
>True if it's the tribe's leader's rank.
---

@*property*<br>
Rank.**canChangeGreetingMessage**(_self_) <a id="Rank.canChangeGreetingMessage" href="#Rank.canChangeGreetingMessage">¶</a>
>
>True if it has the permission to change the greeting message.
---

@*property*<br>
Rank.**canEditRanks**(_self_) <a id="Rank.canEditRanks" href="#Rank.canEditRanks">¶</a>
>
>True if it has the permission to edit ranks.
---

@*property*<br>
Rank.**canChangeMembersRanks**(_self_) <a id="Rank.canChangeMembersRanks" href="#Rank.canChangeMembersRanks">¶</a>
>
>True if it has the permission to change members' rank.
---

@*property*<br>
Rank.**canInvite**(_self_) <a id="Rank.canInvite" href="#Rank.canInvite">¶</a>
>
>True if it has the permission to invite someone to the tribe.
---

@*property*<br>
Rank.**canExclude**(_self_) <a id="Rank.canExclude" href="#Rank.canExclude">¶</a>
>
>True if it has the permission to exclude someone of the tribe.
---

@*property*<br>
Rank.**canPlayMusic**(_self_) <a id="Rank.canPlayMusic" href="#Rank.canPlayMusic">¶</a>
>
>True if it has the permission to play music inside the tribe's house.
---

@*property*<br>
Rank.**canChangeTribeHouseMap**(_self_) <a id="Rank.canChangeTribeHouseMap" href="#Rank.canChangeTribeHouseMap">¶</a>
>
>True if it has the permission to change the tribe's house's map.
---

@*property*<br>
Rank.**canLoadMap**(_self_) <a id="Rank.canLoadMap" href="#Rank.canLoadMap">¶</a>
>
>True if it has the permission to load maps inside the tribe's house.
---

@*property*<br>
Rank.**canLoadLua**(_self_) <a id="Rank.canLoadLua" href="#Rank.canLoadLua">¶</a>
>
>True if it has the permission to load Lua inside the tribe's house.
---

@*property*<br>
Rank.**canManageForum**(_self_) <a id="Rank.canManageForum" href="#Rank.canManageForum">¶</a>
>
>True if it has the permission to mange the tribe's forum.
---

@*classmethod*<br>
Rank.**from\_packet**(_cls, id_, packet_) <a id="Rank.from_packet" href="#Rank.from_packet">¶</a>
>
>Reads a Tribe from a packet.
>
>__Parameters:__
> * **id** - `int` the tribe's id.
> * **packet** - [`Packet`](Packet.md)

---

