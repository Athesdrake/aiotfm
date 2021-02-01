from typing import List

import aiotfm
from aiotfm.enums import ChatCommunity
from aiotfm.packet import Packet
from aiotfm.player import Player


class Message:
	"""Represents any message from the chat.
	Convert an instance to string to get the representation in game of the message.

	Attributes
	----------
	author: :class:`aiotfm.Player`
		The message's author.
	content: `str`
		The actual content of the message.
	"""
	def __init__(self, author: Player, content: str, client: 'aiotfm.Client'):
		self.author: Player = author
		self.content: str = content
		self._client: aiotfm.Client = client

	def __str__(self):
		return '[{0.author}] {0.content}'.format(self)

	def __repr__(self):
		return '<{.__class__.__name__} {}>'.format(self, ' '.join(
			'='.join((k, repr(v)[:32])) for k, v in vars(self).items()
			if not k.startswith('_')
		))


class Whisper(Message):
	"""Represents a whisper from the chat.
	Inherit from :class:`Message`.

	Attributes
	----------
	author: :class:`aiotfm.Player`
		The message's author.
	receiver: :class:`aiotfm.Player`
		The message's addressee.
	community: :class:`aiotfm.enums.ChatCommunity`
		The author's community. Note: the community isn't the author's language!
	content: `str`
		The actual content of the message.
	sent: `bool`
		True if the author is the client.
	"""
	def __init__(self, author: Player, community: ChatCommunity, receiver: Player, content: str, client: 'aiotfm.Client'):
		super().__init__(author, content, client)
		self.receiver: Player = receiver
		self.community: ChatCommunity = ChatCommunity(community)
		self.sent: bool = self.author == client.username

	def __str__(self):
		direction = '<' if self.sent else '>'
		author = self.receiver if self.sent else self.author
		commu = '' if self.sent else '[{}] '.format(self.community.name)
		return f'{direction} {commu}[{author}] {self.content}'

	async def reply(self, msg: str):
		"""|coro|
		Reply to the author of the message. Shortcut to :meth:`aiotfm.Client.whisper`.
		:param msg: :class:`str` the message."""
		await self._client.whisper(self.author, msg)


class Channel:
	"""Represents a channel (#chat) in the game.

	Attributes
	----------
	name: `str`
		The actual channel's name.
	"""
	def __init__(self, name: str, client: 'aiotfm.Client'):
		self.name: str = name
		self._client: aiotfm.Client = client

	def __repr__(self):
		return '<Channel name={.name}>'.format(self)

	def __eq__(self, other):
		if isinstance(other, str):
			return self.name == other
		return self.name == other.name

	async def send(self, message: str):
		"""|coro|
		Sends a message to the channel.

		:param message: :class:`str` the content of the message"""
		await self._client.sendChannelMessage(self, message)

	async def leave(self):
		"""|coro|
		Leaves the channel."""
		await self._client.leaveChannel(self)

	async def who(self) -> List[Player]:
		"""|coro|
		Sends the command /who to the channel and returns the list of players.

		:throws: :class:`asyncio.TimeoutError`
		:return: List[:class:`aiotfm.Player`]"""
		def check(idseq, players):
			return idseq == idSequence

		idSequence = await self._client.sendCP(58, Packet().writeString(self.name))
		_, players = await self._client.wait_for('on_channel_who', check, timeout=3)
		return players


class ChannelMessage(Message):
	"""Represents a message from a :class:`Channel`.

	Attributes
	----------
	channel: `Channel`
		The channel where the message is from.
	author: :class:`aiotfm.Player`
		The message's author.
	community: :class:`aiotfm.enums.ChatCommunity`
		The author's community. Note: the community isn't the author's language!
	content: `str`
		The actual content of the message."""
	def __init__(self, author: Player, community: ChatCommunity, content: str, channel: Channel):
		super().__init__(author, content, channel._client)
		self.channel: Channel = channel
		self.community: ChatCommunity = ChatCommunity(community)

	async def reply(self, message: str):
		"""|coro|
		Sends a message to the channel.

		:param message: :class:`str` the content of the message"""
		await self.channel.send(message)

	def __str__(self):
		return '(#{0.channel.name}) [{0.community.value}] [{0.author}] {0.content}'.format(self)
