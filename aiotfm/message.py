from aiotfm.enums import chatCommu
from aiotfm.packet import Packet

class Message:
	"""Represents any message from the chat.
	Convert an instance to string to get the representation in game of the message.

	Attributes
	----------
	author: `aiotfm.Player`
		The message's author.
	community: `aiotfm.enum.chatCommu`
		The author's community. Note: the community isn't the author's language!
	content: `str`
		The actual content of the message.
	"""
	def __init__(self, author, content, community, client):
		self.author = author
		self.community = chatCommu[community]
		self.content = content
		self._client = client

	def __str__(self):
		return '[{0.author}] {0.content}'.format(self)

	def __repr__(self):
		text = ' '.join('{}={}'.format(k,repr(v)[:32]) for k,v in vars(self).items() if not k.startswith('_'))
		return '<{.__class__.__name__} {}>'.format(self, text)

class Whisper(Message):
	"""Represents a whisper from the chat.
	Inherit from :class:`aiotfm.message.Message`.

	Attributes
	----------
	author: `aiotfm.Player`
		The message's author.
	receiver: `aiotfm.Player`
		The message's addressee.
	community: `aiotfm.enum.chatCommu`
		The author's community. Note: the community isn't the author's language!
	content: `str`
		The actual content of the message.
	sent: `bool`
		True if the author is the client.
	"""
	def __init__(self, author, community, receiver, content, client):
		super().__init__(author, content, community, client)
		self.receiver = receiver

		self.sent = self.author==client.username

	def __str__(self):
		direction = '<' if self.sent else '>'
		author = self.receiver if self.sent else self.author
		commu = '' if self.sent else '[{}] '.format(self.community)
		return f'{direction} {commu}[{author}] {self.content}'

	async def reply(self, msg):
		return await self._client.whisper(self.author, msg)

class Channel:
	"""Represents a channel (#chat) in the game.

	Attributes
	----------
	name: `str`
		The actual channel's name.
	"""
	def __init__(self, name, client):
		self.name = name
		self._client = client

	def __repr__(self):
		return '<Channel name={.name}>'.format(self)

	def __eq__(self, other):
		if isinstance(other, str):
			return self.name==other
		return self.name==other.name

	async def send(self, message):
		"""|coro|
		Sends a message to the channel.

		:param message: :class:`str` the content of the message"""
		await self._client.sendChannelMessage(self, message)

	async def leave(self):
		"""|coro|
		Leaves the channel."""
		await self._client.leaveChannel(self)

	async def who(self):
		"""|coro|
		Sends the command /who to the channel and returns the list of players.

		:throws: `asyncio.TimeoutError`
		:return: List[`aiotfm.Player`]"""
		def check(idseq, players):
			return idseq==idSequence

		idSequence = await self._client.sendCP(58, Packet().writeString(self.name))
		_, players = await self._client.wait_for('on_channel_who', check, timeout=3)
		return players

class ChannelMessage(Message):
	"""Represent a message from a :class:`Channel`.

	Attributes
	----------
	channel: `Channel`
		The channel where the message is from.
	author: `aiotfm.Player`
		The message's author.
	community: `aiotfm.enum.chatCommu`
		The author's community. Note: the community isn't the author's language!
	content: `str`
		The actual content of the message."""
	def __init__(self, author, community, content, channel):
		super().__init__(author, content, community, channel._client)
		self.channel = channel

	async def reply(self, message):
		"""|coro|
		Sends a message to the channel.

		:param message: :class:`str` the content of the message"""
		await self.channel.send(message)

	def __str__(self):
		return '{0.channel.name} [{0.community}] [{0.author}] {0.content}'.format(self)