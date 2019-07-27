from aiotfm.utils import Date

IS_LEADER = 2
CAN_CHANGE_GREETING_MESSAGE = 4
CAN_EDIT_RANKS = 8
CAN_CHANGE_MEMBERS_RANKS = 16
CAN_INVITE = 32
CAN_EXCLUDE = 64
CAN_PLAY_MUSIC = 128
CAN_CHANGE_TRIBE_HOUSE_MAP = 256
CAN_LOAD_MAP = 512
CAN_LOAD_LUA = 512
CAN_MANAGE_FORUM = 1024

class Tribe:
	"""Represent a tribe.

	## Attributes

	id :class:`int` the tribe's id.
	name :class:`str` the tribe's name.
	welcomeMessage :class:`str` the tribe's welcome message.
	mapcode :class:`int` the tribehouse's mapcode.
	members :class:`list` the members' list of the tribe.
	ranks :class:`list` the ranks' list of the tribe.
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

class Member:
	"""Represent a tribe's member.

	## Attributes

	tribe :class:`Tribe` the member's tribe.
	id :class:`int` the player's id of the member.
	name :class:`str` the username of the member.
	gender :class:`int` the member's gender.
	lastConnection :class`Date` the last connection of the member.
	rank_id :class:`int` the rank's id of the member.
	game_id :class:`int` the game's id the player is playing.
	room :class:`str` the room where the player is.
	rank :class:`Rank` the member's rank.
	online :class:`bool` return True if the member is online.
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
		return self.game_id!=1

class Rank:
	"""Represent a tribe's rank.

	## Attributes

	id :class:`int` the rank's id.
	name :class:`str` the rank's name.
	perm :class:`int` the rank's permissions.

	## Permissions

	isLeader :class:`bool`
	canChangeGreetingMessage :class:`bool`
	canEditRanks :class:`bool`
	canChangeMembersRanks :class:`bool`
	canInvite :class:`bool`
	canExclude :class:`bool`
	canPlayMusic :class:`bool`
	canChangeTribeHouseMap :class:`bool`
	canLoadMap :class:`bool`
	canLoadLua :class:`bool`
	canManageForum :class:`bool`
	"""
	def __init__(self, id, name, perm):
		self.id = id
		self.name = name
		self.perm = perm

		self.isLeader = bool(perm&IS_LEADER)
		self.canChangeGreetingMessage = bool(perm&CAN_CHANGE_GREETING_MESSAGE)
		self.canEditRanks = bool(perm&CAN_EDIT_RANKS)
		self.canChangeMembersRanks = bool(perm&CAN_CHANGE_MEMBERS_RANKS)
		self.canInvite = bool(perm&CAN_INVITE)
		self.canExclude = bool(perm&CAN_EXCLUDE)
		self.canPlayMusic = bool(perm&CAN_PLAY_MUSIC)
		self.canChangeTribeHouseMap = bool(perm&CAN_CHANGE_TRIBE_HOUSE_MAP)
		self.canLoadMap = bool(perm&CAN_LOAD_MAP)
		self.canLoadLua = bool(perm&CAN_LOAD_LUA)
		self.canManageForum = bool(perm&CAN_MANAGE_FORUM)

	@classmethod
	def from_packet(cls, id, packet):
		return cls(id, packet.readUTF(), packet.read32())