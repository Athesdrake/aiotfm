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
@*classmethod*<br>
Player.**from\_packet**(_cls, packet_) <a id="Player.from_packet" href="#Player.from_packet">¶</a>
>
>Reads a Player from a packet.
>
>__Parameters:__
> * **packet** - [`Packet`](Packet.md) the packet.
>
>__Returns:__ [`Player`](Player.md#Player) the player.

---

@*property*<br>
Player.**isGuest**(_self_) <a id="Player.isGuest" href="#Player.isGuest">¶</a>
>
>Return True if the player is a guest (Souris)
---

## Profile
**Represents a player's profile.**

| Attributes | Type | Can be None | Description |
| :-: | :-: | :-: | :-- |
| username | `str` | ✕ |  The player's username. |
| uid | `int` | ✕ |  The player's id. |
| registration_date | `int` | ✕ |  The registration timestamp of the player. |
| privLevel | `int` | ✕ |  The privilege level of the player. |
| gender | `int` | ✕ |  Player's gender. |
| tribe | `str` | ✕ |  Player's tribe. Can be `None`. |
| soulmate | `str` | ✕ |  Player's soulmate. Can be `None`. |
| title | `int` | ✕ |  The title above the player's head. |
| titles | `set` | ✕ |  The list of the unlocked titles. |
| titles_stars | `dict` | ✕ |  A dictionary where are stored the number of stars a title has. |
| look | `str` | ✕ |  The player's look. |
| level | `int` | ✕ |  The player's shaman level. |
| badges | `dict` | ✕ |  All badges unlocked by the player and their number. |
| stats | `Stats` | ✕ |  The player's stats. |
| equippedOrb | `int` | ✕ |  The equipped orb of the player. |
| orbs | `set` | ✕ |  The list of unlocked orbs. |
| adventurePoints | `int` | ✕ |  Number of adventure points the player has. |

## Stats
**Represents the statistics of a player.**

| Attributes | Type | Can be None | Description |
| :-: | :-: | :-: | :-- |
| normalModeSaves | `int` | ✕ |  Number of shaman saves in normal mode. |
| hardModeSaves | `int` | ✕ |  Number of shaman saves in hard mode. |
| divineModeSaves | `int` | ✕ |  Number of shaman saves in divine mode. |
| shamanCheese | `int` | ✕ |  Number of cheese personally gathered. |
| firsts | `int` | ✕ |  Number of cheese gathered first. |
| gatheredCheese | `int` | ✕ |  Total number of gathered cheese. |
| bootcamps | `int` | ✕ |  Number of bootcamp. |
| modeStats | `list` | ✕ |  A list of tuples that represents the stats in different mode. (id, progress, progressLimit, imageId) |

