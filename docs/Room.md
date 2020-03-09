# Room's Documentation

## Room
**Represents the room that the bot currently is in.**

| Attributes | Type | Can be None | Description |
| :-: | :-: | :-: | :-- |
| name | `str` | ✕ |  The room's name. (i.e: en-1, *bad girls and so on) |
| private | `bool` | ✕ |  Whether the room is public or private. |
| players | `Player]` | ✕ |  The list containing all the players of the room. |


### Methods
Room.**community**(_self_) <a id="Room.community" href="#Room.community">¶</a>
>
>
---

Room.**is\_tribe**(_self_) <a id="Room.is_tribe" href="#Room.is_tribe">¶</a>
>
>
---

Room.**display\_name**(_self_) <a id="Room.display_name" href="#Room.display_name">¶</a>
>
>
---

Room.**get\_players**(_self, predicate, max__) <a id="Room.get_players" href="#Room.get_players">¶</a>
>
>Filters players from the room.
>
>__Parameters:__
> * **predicate** - A function that returns a boolean-like result to filter through
> * **max_** - Optional[`int`] The maximum amount of players to return.

---

Room.**get\_player**(_self, default, \*\*kwargs_) <a id="Room.get_player" href="#Room.get_player">¶</a>
>
>Gets one player in the room with an identifier.
>
>__Parameters:__
> * **kwargs** - Which identifier to use. Can be either name, username, id or pid.

---

