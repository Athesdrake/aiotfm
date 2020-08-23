# Friend's Documentation

## Friend
**Represents a player in friend list, if you have one :feels:**

| Attributes | Type | Can be None | Description |
| :-: | :-: | :-: | :-- |
| id | `int` | ✕ |  The player's id |
| name | `str` | ✕ |  The player's username. |
| gender | `int` | ✕ |  The player's gender. |
| isSoulmate | `bool` | ✕ |  True if the player is your soulmate |
| isAddedBack | `bool` | ✕ |  True if the the player also added you to their friend list |
| isOnline | `bool` | ✕ |  True if the player is online |
| community | `int` | ✕ |  What community the player is on |
| roomName | `str` | ✕ |  The player's room name, empty string if isAddedBack is False |
| lastConnection | [`Date`](#date) | ✕ |  The last connection of the player |

@*staticmethod*<br>
Friend.**from\_packet**(_packet_) <a id="Friend.from_packet" href="#Friend.from_packet">¶</a>
>
>
---

