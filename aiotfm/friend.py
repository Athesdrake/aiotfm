from aiotfm.utils import Date
from aiotfm.enums import Game


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

	def __init__(self, packet, isSoulmate=False):
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

	@staticmethod
	def from_packet(packet):
		friends = []

		soulmate = Friend(packet, True)
		if soulmate.id != 0:
			friends.append(soulmate)

		for i in range(packet.read16()):
			friends.append(Friend(packet))

		return friends
