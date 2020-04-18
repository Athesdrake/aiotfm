from aiotfm.utils import Date
from aiotfm.enums import Permissions


class Tribe:
	"""Represents a tribe.

	Attributes
	----------
	id: :class:`int`
		The tribe's id.
	name: :class:`str`
		The tribe's name.
	welcomeMessage: :class:`str`
		The tribe's welcome message.
	mapcode: :class:`int`
		The tribehouse's mapcode.
	members: :class:`list`
		The members' list of the tribe.
	ranks: :class:`list`
		The ranks' list of the tribe.
	"""
	def __init__(self, packet):
		self.id = packet.read32()
		self.name = packet.readUTF()
		self.welcomeMessage = packet.readUTF()
		self.mapcode = packet.read32()
		self.members = []
		self.ranks = []

		for i in range(packet.read16()):
			self.members.append(Member(self, packet))

		for i in range(packet.read16()):
			self.ranks.append(Rank.from_packet(i, packet))

	def get_member(self, name):
		"""Returns a member from it's name or None if not found.
		:param name: :class:`str` or :class:`aiotfm.Player` the name of the member.
		:return: :class:`aiotfm.tribe.Member` or None
		"""
		for m in self.members:
			if name == m.name:
				return m


class Member:
	"""Represents a tribe's member.

	Attributes
	----------
	tribe: :class:`Tribe`
		The member's tribe.
	id: :class:`int`
		The player's id of the member.
	name: :class:`str`
		The username of the member.
	gender: :class:`int`
		The member's gender.
	lastConnection: :class`Date`
		The last connection of the member.
	rank_id: :class:`int`
		The rank's id of the member.
	game_id: :class:`int`
		The game's id the player is playing.
	room: :class:`str`
		The room where the player is.
	rank: :class:`Rank`
		The member's rank.
	online: :class:`bool`
		True if the member is online.
	"""
	def __init__(self, tribe, packet):
		self.tribe = tribe
		self.id = packet.read32()
		self.name = packet.readUTF()
		self.gender = packet.read8()
		packet.read32() # id
		self.lastConnection = Date.fromtimestamp(packet.read32())
		self.rank_id = packet.read8()
		self.game_id = packet.read32()
		self.room = packet.readUTF()

	@property
	def rank(self):
		"""return the :class:`Rank` of the member."""
		return self.tribe.ranks[self.rank_id]

	@property
	def online(self):
		"""return True if the member is online."""
		return self.game_id != 1


class Rank:
	"""Represents a tribe's rank.

	Attributes
	----------
	id: :class:`int`
		The rank's id.
	name: :class:`str`
		The rank's name.
	perm: :class:`int`
		The rank's permissions.
	"""
	def __init__(self, id_, name, perm):
		self.id = id_
		self.name = name
		self.perm = perm

	@property
	def isLeader(self):
		"""True if it's the tribe's leader's rank."""
		return bool(self.perm & Permissions.IS_LEADER)

	@property
	def canChangeGreetingMessage(self):
		"""True if it has the permission to change the greeting message."""
		return bool(self.perm & Permissions.CAN_CHANGE_GREETING_MESSAGE)

	@property
	def canEditRanks(self):
		"""True if it has the permission to edit ranks."""
		return bool(self.perm & Permissions.CAN_EDIT_RANKS)

	@property
	def canChangeMembersRanks(self):
		"""True if it has the permission to change members' rank."""
		return bool(self.perm & Permissions.CAN_CHANGE_MEMBERS_RANKS)

	@property
	def canInvite(self):
		"""True if it has the permission to invite someone to the tribe."""
		return bool(self.perm & Permissions.CAN_INVITE)

	@property
	def canExclude(self):
		"""True if it has the permission to exclude someone of the tribe."""
		return bool(self.perm & Permissions.CAN_EXCLUDE)

	@property
	def canPlayMusic(self):
		"""True if it has the permission to play music inside the tribe's house."""
		return bool(self.perm & Permissions.CAN_PLAY_MUSIC)

	@property
	def canChangeTribeHouseMap(self):
		"""True if it has the permission to change the tribe's house's map."""
		return bool(self.perm & Permissions.CAN_CHANGE_TRIBE_HOUSE_MAP)

	@property
	def canLoadMap(self):
		"""True if it has the permission to load maps inside the tribe's house."""
		return bool(self.perm & Permissions.CAN_LOAD_MAP)

	@property
	def canLoadLua(self):
		"""True if it has the permission to load Lua inside the tribe's house."""
		return bool(self.perm & Permissions.CAN_LOAD_LUA)

	@property
	def canManageForum(self):
		"""True if it has the permission to mange the tribe's forum."""
		return bool(self.perm & Permissions.CAN_MANAGE_FORUM)

	@classmethod
	def from_packet(cls, id_, packet):
		"""Reads a Tribe from a packet.
		:param id: :class:`int` the tribe's id.
		:param packet: :class:`aiotfm.Packet`"""
		return cls(id_, packet.readUTF(), packet.read32())