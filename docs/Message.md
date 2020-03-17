# Message's Documentation

## Message
**Represents any message from the chat.
Convert an instance to string to get the representation in game of the message.**

| Attributes | Type | Can be None | Description |
| :-: | :-: | :-: | :-- |
| author | `Player` | ✕ |  The message's author. |
| community | `ChatCommunity` | ✕ |  The author's community. Note: the community isn't the author's language! |
| content | `str` | ✕ |  The actual content of the message. |

## Whisper
**Represents a whisper from the chat.
Inherit from [`Message`](Message.md#Message).**

| Attributes | Type | Can be None | Description |
| :-: | :-: | :-: | :-- |
| author | `Player` | ✕ |  The message's author. |
| receiver | `Player` | ✕ |  The message's addressee. |
| community | `ChatCommunity` | ✕ |  The author's community. Note: the community isn't the author's language! |
| content | `str` | ✕ |  The actual content of the message. |
| sent | `bool` | ✕ |  True if the author is the client. |

_coroutine_ Whisper.**reply**(_self, msg_) <a id="Whisper.reply" href="#Whisper.reply">¶</a>
>
>Reply to the author of the message. Shortcut to [`whisper`](#Client.whisper).
>
>__Parameters:__
> * **msg** - `str` the message.

---

## Channel
**Represents a channel (#chat) in the game.**

| Attributes | Type | Can be None | Description |
| :-: | :-: | :-: | :-- |
| name | `str` | ✕ |  The actual channel's name. |


### Methods
_coroutine_ Channel.**send**(_self, message_) <a id="Channel.send" href="#Channel.send">¶</a>
>
>Sends a message to the channel.
>
>__Parameters:__
> * **message** - `str` the content of the message

---

_coroutine_ Channel.**leave**(_self_) <a id="Channel.leave" href="#Channel.leave">¶</a>
>
>Leaves the channel.
---

_coroutine_ Channel.**who**(_self_) <a id="Channel.who" href="#Channel.who">¶</a>
>
>Sends the command /who to the channel and returns the list of players.
---

## ChannelMessage
**Represents a message from a [`Channel`](#Channel).**

| Attributes | Type | Can be None | Description |
| :-: | :-: | :-: | :-- |
| channel | `Channel` | ✕ |  The channel where the message is from. |
| author | `Player` | ✕ |  The message's author. |
| community | `ChatCommunity` | ✕ |  The author's community. Note: the community isn't the author's language! |
| content | `str` | ✕ |  The actual content of the message. |

_coroutine_ ChannelMessage.**reply**(_self, message_) <a id="ChannelMessage.reply" href="#ChannelMessage.reply">¶</a>
>
>Sends a message to the channel.
>
>__Parameters:__
> * **message** - `str` the content of the message

---

