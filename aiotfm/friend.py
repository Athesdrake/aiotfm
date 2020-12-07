from aiotfm.utils import Date
from aiotfm.enums import Game
from aiotfm.packet import Packet
from aiotfm.player import Player
from aiotfm.errors import CommunityPlatformError, InvalidAccountError, \
	FriendLimitError, CantFriendPlayerError


class FriendList:
	"""Represents a friend list.

	Attributes
	----------
	soulmate: Optional[:class:`aiotfm.friend.Friend`]
		Your soulmate, if you have one.
	friends: :class:`list`
		Your friends.
	"""
	def __init__(self, client, packet):
		self.friends = []
		self.soulmate = None

		soulmate = Friend(self, packet, True)
		if soulmate.id != 0:
			self.soulmate = soulmate
			self.friends.append(soulmate)

		for i in range(packet.read16()):
			self.friends.append(Friend(self, packet))

		self._client = client

	def get_friend(self, search):
		"""Returns a friend from their name (or id) or None if not found.
		:param search: :class:`str` or :class:`aiotfm.Player` or :class:`int` search query
		:return: :class:`aiotfm.friend.Friend` or None
		"""
		if isinstance(search, int): # Search by id
			for f in self.friends:
				if search == f.id:
					return f

		else:
			if isinstance(search, Player):
				search = search.username
			search = search.lower()

			for f in self.friends:
				if search == f.name:
					return f

	async def remove(self, friend):
		"""|coro|
		Remove a friend. If they're your soulmate, divorce them.
		:param friend: :class:`str` or :class:`aiotfm.Player` or :class:`aiotfm.friend.Friend`
		"""
		if not isinstance(friend, Friend):
			friend = self.get_friend(friend)

			if friend is None:
				return

		sid = self._client.cp_fingerprint + 1

		if friend.isSoulmate:
			await self._client.sendCP(26, Packet())
			result, error = 27, 36
		else:
			await self._client.sendCP(20, Packet().writeString(friend.name.lower()))
			result, error = 21, 30

		def is_deletion(tc, packet):
			return tc == result and packet.read32() == sid

		tc, packet = await self._client.wait_for('on_raw_cp', is_deletion, timeout=5)
		result = packet.read8()

		if result != 1:
			raise CommunityPlatformError(error, result)

		if friend not in self.friends:
			return

		if friend == self.soulmate:
			self.soulmate = None
		self.friends.remove(friend)

	async def add(self, name):
		"""|coro|
		Add a friend.
		:param name: :class:`str` or :class:`aiotfm.Player`
		:return: :class:`aiotfm.friend.Friend` or None
		"""
		if isinstance(name, Player):
			name = name.username

		friend = self.get_friend(name)
		if friend is not None:
			return friend

		sid = self._client.cp_fingerprint + 1
		await self._client.sendCP(18, Packet().writeString(name))

		def is_addition(tc, packet):
			return tc == 19 and packet.read32() == sid

		tc, packet = await self._client.wait_for('on_raw_cp', is_addition, timeout=5)
		result = packet.read8()

		if result == 12:
			raise InvalidAccountError(name)

		elif result == 7:
			raise FriendLimitError()

		elif result == 4 or result == 15:
			raise CantFriendPlayerError(name)

		elif result != 1:
			raise CommunityPlatformError(28, result)

		return self.get_friend(name)


class Friend:
	"""Represents a player in friend list, if you have one :feels:

	Attributes
	----------
	id: :class:`int`
		The player's id
	name: :class:`str`
		The player's username.
	gender: :class:`int`
		The player's gender.
	isSoulmate: :class:`bool`
		True if the player is your soulmate
	isAddedBack: :class:`bool`
		True if the the player also added you to their friend list
	isOnline: :class:`bool`
		True if the player is online
	hasAvatar: :class:`bool`
		True if the player has an avatar
	game: :class:`aiotfm.enums.Game`
		What game the player is playing on
	roomName: :class:`str`
		The player's room name, empty string if isAddedBack is False
	lastConnection: :class:`Date`
		The last connection of the player
	"""

	def __init__(self, flist, packet, isSoulmate=False):
		self.hasAvatar = packet.read32() != 0
		self.name = packet.readUTF()
		self.gender = packet.read8()
		self.id = packet.read32()
		self.isSoulmate = isSoulmate
		self.isAddedBack = packet.readBool()
		self.isConnected = packet.readBool()
		self.game = Game(packet.read32())
		self.roomName = packet.readUTF()
		self.lastConnection = Date.fromtimestamp(packet.read32())

		self._flist = flist

	def remove(self):
		"""|coro|
		Remove this friend. If they're your soulmate, divorce them.
		"""
		return self._flist.remove(self)
