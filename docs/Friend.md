# Friend's Documentation

## FriendList
**Represents a friend list.**

| Attributes | Type | Can be None | Description |
| :-: | :-: | :-: | :-- |
| soulmate | [`Friend`](Friend.md#Friend) | ✔ |  Your soulmate, if you have one. |
| friends | `list` | ✕ |  Your friends. |


### Methods
FriendList.**get\_friend**(_self, search_) <a id="FriendList.get_friend" href="#FriendList.get_friend">¶</a>
>
>Returns a friend from their name (or id) or None if not found.
>
>__Parameters:__
> * **search** - `str` or [`Player`](Player.md) or `int` search query
>
>__Returns:__ [`Friend`](Friend.md#Friend) or None

---

_coroutine_ FriendList.**remove**(_self, friend_) <a id="FriendList.remove" href="#FriendList.remove">¶</a>
>
>Remove a friend. If they're your soulmate, divorce them.
>
>__Parameters:__
> * **friend** - `str` or [`Player`](Player.md) or [`Friend`](Friend.md#Friend)

---

_coroutine_ FriendList.**add**(_self, name_) <a id="FriendList.add" href="#FriendList.add">¶</a>
>
>Add a friend.
>
>__Parameters:__
> * **name** - `str` or [`Player`](Player.md)
>
>__Returns:__ [`Friend`](Friend.md#Friend) or None

---

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
| hasAvatar | `bool` | ✕ |  True if the player has an avatar |
| game | [`Game`](Enums.md#Game) | ✕ |  What game the player is playing on |
| roomName | `str` | ✕ |  The player's room name, empty string if isAddedBack is False |
| lastConnection | [`Date`](#date) | ✕ |  The last connection of the player |

Friend.**remove**(_self_) <a id="Friend.remove" href="#Friend.remove">¶</a>
>
>Remove this friend. If they're your soulmate, divorce them.
---

