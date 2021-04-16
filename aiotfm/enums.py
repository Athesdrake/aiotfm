from enum import IntEnum


class ChatCommunity(IntEnum):
	"""Enumerates the different chat's communities."""
	int = -1
	en = 1
	fr = 2
	ru = 3
	br = 4
	es = 5
	cn = 6
	tr = 7
	vk = 8
	pl = 9
	hu = 10
	nl = 11
	ro = 12
	id = 13
	de = 14
	e2 = 15
	ar = 16
	ph = 17
	lt = 18
	jp = 19
	fi = 21
	cz = 22
	hr = 23
	bg = 25
	lv = 26
	he = 27
	it = 28
	pt = 31

	@classmethod
	def _missing_(cls, value):
		return cls.int


class Community(IntEnum):
	"""Enumerates the different game's communities."""
	en = 0
	int = 0
	xx = 0
	fr = 1
	ru = 2
	br = 3
	es = 4
	cn = 5
	tr = 6
	vk = 7
	pl = 8
	hu = 9
	nl = 10
	ro = 11
	id = 12
	de = 13
	e2 = 14
	ar = 15
	ph = 16
	lt = 17
	jp = 18
	fi = 20
	cz = 21
	hr = 23
	bg = 24
	lv = 25
	he = 26
	it = 27
	et = 29
	pt = 31

	@classmethod
	def _missing_(cls, value):
		return cls.int


class TradeState(IntEnum):
	"""Enumerates the different states a trade can have."""
	ON_INVITE = 0
	ACCEPTING = 1
	TRADING = 2
	CANCELLED = 3
	SUCCESS = 4


class TradeError(IntEnum):
	"""Enumerates the different error codes the server could send."""
	ALREADY_TRADING = 0
	INVITE_DECLINED = 1
	CANCELLED = 2
	SAME_ROOM = 3
	SUCCEED = 4
	SHAMAN = 5
	NOT_CONNECTED = 6
	INTERNAL = 7


class Permissions(IntEnum):
	"""Enumerates the different tribe's rank's permissions."""
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


class GameMode(IntEnum):
	"""Enumerates the different room gamemodes"""
	NORMAL = 1
	BOOTCAMP = 2
	VANILLA = 3
	SURVIVOR = 8
	RACING = 9
	DEFILANTE = 10
	MUSIC = 11
	SHAMAN = 13
	VILLAGE = 16
	MODULES = 18
	MADCHESS = 20
	CELOUSCO = 22
	RANKED = 31
	DUEL = 33
	ARENA = 34
	DOMINATION = 42


class Game(IntEnum):
	"""Enumerates the different Atelier801 games."""
	INVALID = 0

	TRANSFORMICE = 4
	FORTORESSE = 6
	BOUBOUM = 7
	NEKODANCER = 15
	DEADMAZE = 17

	@classmethod
	def _missing_(cls, value):
		return cls.INVALID
