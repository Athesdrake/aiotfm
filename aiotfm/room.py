class Room:
	"""Represents the room that the bot currently is in.

	Attributes
	----------
	name: `str`
		The room's name. (i.e: en-1, *bad girls and so on)
	private: `bool`
		Whether the room is public or private.
	players: `list[aiotfm.player.Player]`
		The list containing all the players of the room.
	"""
	def __init__(self, name, private=True):
		self.name = name
		self.private = private
		self.players = []

	def __repr__(self):
		return "<Room name={} private={}>".format(self.name, self.private)

	def get_player(self, max=None, gate="and", **kwargs):
		"""Gets a player from the room.

		:param max: Optional[:class:`int`] The maximum amout of players to return. If this is one it will return the player instead of a list.
		:param gate: Optional[:class:`str`] The gate to compare values given to kwargs. Can be either 'and' or 'or'.
		:param kwargs: Applied filters. You set a :class:`Player` attribute and its value and the function will use them as filters.
		:return: Union[:class:`list`[:class:`tuple`], :class:`tuple`] The filtered players. Each tuple is an index-player pair."""
		players = []
		quantity = 0

		for index, player in enumerate(self.players):
			if max is not None:
				if quantity >= max:
					break

			if gate == "and":
				append = True
				for key, value in kwargs.items():
					if getattr(player, key) != value:
						append = False
						break

			elif gate == "or":
				append = False
				for key, value in kwargs.items():
					if getattr(player, key) == value:
						append = True
						break

			if append:
				players.append((index, player))
				quantity += 1

		if max == 1:
			if quantity == 1:
				return players[0]
			return None
		return players