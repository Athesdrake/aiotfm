# Player's Documentation

## Player
**Represents a player in game.**

| Attributes | Type | Can be None | Description |
| :-: | :-: | :-: | :-- |
| username | `str` | ✕ |  The player's username. |
| uid | `int` | ✕ |  The player's id. -1 if unknown |
| pid | `int` | ✕ |  The player's pid. -1 if unknown |
| look | `str` | ✕ |  The player's look. '' if unknown |
| gender | `int` | ✕ |  The player's gender. |
| title | `int` | ✕ |  The player's title id. 0 if unknown |
| title_stars | `int` | ✕ |  The player's title's stars. |
| hasCheese | `bool` | ✕ |  True if the player has the cheese. |
| isDead | `bool` | ✕ |  True if the player is dead. |
| isShaman | `bool` | ✕ |  True if the player is shaman. |
| isVampire | `bool` | ✕ |  True if the player is vampire. |
| score | `int` | ✕ |  The player's score. |
| mouseColor | `int` | ✕ |  The color of the player's fur. |
| nameColor | `int` | ✕ |  The color of the player's name. |
| shamanColor | `int` | ✕ |  The color of the player's shaman's feather. |
| facingRight | `bool` | ✕ |  True if the player is facing right. |
| movingLeft | `bool` | ✕ |  True if the player is moving to the left. |
| movingRight | `bool` | ✕ |  True if the player is moving to the right. |
| x | `int` | ✕ |  The player's x position. |
| y | `int` | ✕ |  The player's y position. |
| vx | `int` | ✕ |  The player's horizontal speed. |
| vy | `int` | ✕ |  The player's vertical speed. |
| ducking | `bool` | ✕ |  True if the player is ducking (crouching). |
| jumping | `bool` | ✕ |  True if the player is jumping. |


### Methods
Player.**from\_packet**(_cls, packet_) <a id="Player.from_packet" href="#Player.from_packet">¶</a>
>
>
>
>__Parameters:__
> * **packet** - [`Packet`](Packet.md) the packet.

---

Player.**isGuest**(_self_) <a id="Player.isGuest" href="#Player.isGuest">¶</a>
>
>
---

## Profile
**Represents a player's profile.**

## Stats
**Represents the statistics of a player.**

