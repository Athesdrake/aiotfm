from aiotfm.errors import AiotfmException
from aiotfm.enums import GameMode


class Room:
	"""Represents the room that the bot currently is in.

	Attributes
	----------
	name: `str`
		The room's name. (i.e: en-1, *bad girls and so on)
	official: `bool`
		Whether the room is an official room or not. If official, it's name will be displayed in yellow.
	players: `list[:class:`aiotfm.Player`]`
		The list containing all the players of the room.
	"""
	def __init__(self, name, official=False):
		self.name = name
		self.official = official
		self.players = {}

	def __repr__(self):
		return "<Room name={} official={}>".format(self.name, self.official)

	@property
	def community(self):
		"""Returns the room's community."""
		if self.name.startswith('*'):
			return 'xx'
		return self.name.split('-', 1)[0]

	@property
	def is_tribe(self):
		"""Returns true if it's a tribe house."""
		return self.name.startswith('*\x03')

	@property
	def display_name(self):
		"""Return the display name of the room.
		It removes the \x03 char from the tribe house and the community from the public rooms."""
		if self.is_tribe:
			return self.name.replace('\x03', '')
		if self.name.startswith('*'):
			return self.name
		return self.name.split('-', 1)[1]

	def get_players(self, predicate, max_=None):
		"""Filters players from the room.

		:param predicate: A function that returns a boolean-like result to filter through
			the players.
		:param max_: Optional[:class:`int`] The maximum amount of players to return.
		:return: `Iterable` The filtered players."""
		return [p for p in self.players.values() if predicate(p)][:max_]

	def get_player(self, default=None, **kwargs):
		"""Gets one player in the room with an identifier.

		:param kwargs: Which identifier to use. Can be either name, username, id or pid.
		:return: :class:`aiotfm.Player` The player or None"""
		length = len(kwargs.keys())

		if length == 0:
			raise AiotfmException('You did not provide any identifier.')
		if length > 1:
			raise AiotfmException('You cannot filter one player with more than one identifier.')

		identifier, value = next(iter(kwargs.items()))

		if identifier in ('name', 'username'):
			def filter_(p):
				return p == value
		elif identifier == 'id':
			def filter_(p):
				return p.id == int(value)
		elif identifier == 'pid':
			return self.players.get(int(value), default)
		else:
			raise AiotfmException('Invalid filter.')

		for player in self.players.values():
			if filter_(player):
				return player
		return default


class RoomEntry:
	__slots__ = (
		'name', 'language', 'country', 'player_count', 'limit',
		'is_funcorp', 'is_pinned', 'command', 'args'
	)

	def __init__(
		self, name, language, country, player_count,
		limit=0, is_funcorp=False, is_pinned=False,
		command='', args=''
	):
		self.name = name
		self.language = language
		self.country = country
		self.player_count = player_count
		self.limit = limit
		self.is_funcorp = is_funcorp
		self.is_pinned = is_pinned
		self.command = command
		self.args = args

	def __repr__(self):
		return '<{} {}>'.format(
			self.__class__.__name__,
			' '.join('{}={!r}'.format(key, getattr(self, key)) for key in self.__slots__)
		)


class DropdownRoomEntry(RoomEntry):
	__slots__ = ('entries',)

	def __init__(self, entries, *args, **kwargs):
		super().__init__(*args, **kwargs, is_pinned=True)
		self.entries = entries


class RoomList:
	"""Represents the list of rooms in the server.

	Attributes
	----------
	gamemode: :class:`aiotfm.enums.GameMode`
		The list's gamemode.
	rooms: List[`RoomEntry`]
		The list of normal rooms.
	pinned_rooms: List[`RoomEntry`]
		The list of pinned(/module) rooms.
	gamemodes: List[:class:`aiotfm.enums.GameMode`]
		The list of gamemodes available.
	"""
	def __init__(self, gamemode, rooms, pinned_rooms, gamemodes):
		self.gamemode = gamemode
		self.rooms = rooms
		self.pinned_rooms = pinned_rooms
		self.gamemodes = gamemodes

	@classmethod
	def from_packet(cls, packet):
		gamemodes = [GameMode(packet.read8()) for _ in range(packet.read8())]
		gamemode = GameMode(packet.read8())
		rooms = []
		pinned = []

		while packet.pos < len(packet.buffer):
			is_pinned = packet.readBool()
			language = packet.readUTF()
			country = packet.readUTF()
			name = packet.readUTF()

			if is_pinned:
				player_count = packet.readUTF()
				command = packet.readUTF()
				args = packet.readUTF()

				if player_count.isdigit():
					player_count = int(player_count)

				if command == 'lm':
					entries = []
					room = DropdownRoomEntry(entries, name, language, country, player_count)

					for mode in args.split('&~'):
						if ',' not in mode:
							continue

						name, count = mode.split(',')
						entries.append(RoomEntry(
							name, room.language, room.country, int(count),
							command='mjj', args='m ' + name
						))

					pinned.append(room)
				else:
					pinned.append(RoomEntry(
						name, language, country, player_count,
						command=command, args=args, is_pinned=True
					))
			else:
				player_count = packet.read16()
				limit = packet.read8()
				is_funcorp = packet.readBool()

				rooms.append(RoomEntry(
					name, language, country, player_count,
					limit=limit, is_funcorp=is_funcorp
				))

		return cls(gamemode, rooms, pinned, gamemodes)
