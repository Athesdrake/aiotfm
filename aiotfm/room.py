from typing import Any, Callable, List, Optional, Union

from aiotfm.enums import GameMode
from aiotfm.errors import AiotfmException
from aiotfm.packet import Packet
from aiotfm.player import Player


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
	def __init__(self, name: str, official: bool = False):
		self.name: str = name
		self.official: bool = official
		self.players: dict = {}

	def __repr__(self):
		return "<Room name={} official={}>".format(self.name, self.official)

	@property
	def community(self) -> str:
		"""Returns the room's community."""
		if self.name.startswith('*'):
			return 'xx'
		return self.name.split('-', 1)[0]

	@property
	def is_tribe(self) -> bool:
		"""Returns true if it's a tribe house."""
		return self.name.startswith('*\x03')

	@property
	def display_name(self) -> str:
		r"""Return the display name of the room.
		It removes the \x03 char from the tribe house and the community from the public rooms."""
		if self.is_tribe:
			return self.name.replace('\x03', '')
		if self.name.startswith('*'):
			return self.name
		return self.name.split('-', 1)[1]

	def get_players(self, predicate: Callable, max_: Optional[int] = None) -> List[Player]:
		"""Filters players from the room.

		:param predicate: A function that returns a boolean-like result to filter through
			the players.
		:param max_: Optional[:class:`int`] The maximum amount of players to return.
		:return: `Iterable` The filtered players."""
		return [p for p in self.players.values() if predicate(p)][:max_]

	def get_player(self, default: Optional[Any] = None, **kwargs) -> Union[Player, Any]:
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
		'is_funcorp', 'is_pinned', 'command', 'args', 'is_modified',
		'shaman_skills', 'consumables', 'adventure', 'collision',
		'aie', 'map_duration', 'mice_mass', 'map_rotation'
	)

	def __init__(
		self, name: str, language: str, country: str, player_count: int,
		limit: int = 0, is_funcorp: bool = False, is_pinned: bool = False,
		command: str = '', args: str = '', is_modified: bool = False, shaman_skills: bool = True,
		consumables: bool = True, adventure: bool = True, collision: bool = False, aie: bool = False,
		map_duration: int = 100, mice_mass: int = 100, map_rotation: list = []
	):
		self.name: str = name
		self.language: str = language
		self.country: str = country
		self.player_count: int = player_count
		self.limit: int = limit
		self.is_funcorp: bool = is_funcorp
		self.is_pinned: bool = is_pinned
		self.command: str = command
		self.args: str = args
		self.is_modified: bool = is_modified
		self.shaman_skills: bool = shaman_skills
		self.consumables: bool = consumables
		self.adventure: bool = adventure
		self.collision: bool = collision
		self.aie: bool = aie
		self.map_duration: int = map_duration
		self.mice_mass: int = mice_mass
		self.map_rotation: list = map_rotation

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
	def __init__(
		self, gamemode: GameMode, rooms: List[RoomEntry],
		pinned_rooms: List[RoomEntry], gamemodes: List[GameMode]
	):
		self.gamemode: GameMode = gamemode
		self.rooms: List[RoomEntry] = rooms
		self.pinned_rooms: List[RoomEntry] = pinned_rooms
		self.gamemodes: List[GameMode] = gamemodes

	@classmethod
	def from_packet(cls, packet: Packet):
		gamemodes = [GameMode(packet.read8()) for _ in range(packet.read8())]
		gamemode = GameMode(packet.read8())
		rooms: List[RoomEntry] = []
		pinned: List[RoomEntry] = []

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
					entries: List[RoomEntry] = []
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
				is_modified = packet.readBool()

				kwargs = {
					"limit": limit,
					"is_funcorp": is_funcorp,
				}

				# Read the modified properties
				if is_modified:
					shaman_skills = not packet.readBool()
					consumables = not packet.readBool()
					adventure = not packet.readBool()
					collision = packet.readBool()
					aie = packet.readBool()
					map_duration = packet.read8()
					mice_mass = packet.read32()
					map_rotation = []

					for i in range(0, packet.read8()):
						map_rotation.append(packet.read8())

					# Append the room's specific properties
					kwargs.update({
						"is_modified": is_modified,
						"shaman_skills": shaman_skills,
						"consumables": consumables,
						"adventure": adventure,
						"collision": collision,
						"aie": aie,
						"map_duration": map_duration,
						"mice_mass": mice_mass,
						"map_rotation": map_rotation
					})

				rooms.append(RoomEntry(
					name, language, country, player_count,
					**kwargs
				))

		return cls(gamemode, rooms, pinned, gamemodes)
