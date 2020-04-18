from aiotfm.packet import Packet


class Player:
	"""Represents a player in game.

	Attributes
	----------
	username: :class:`str`
		The player's username.
	uid: :class:`int`
		The player's id. -1 if unknown
	pid: :class:`int`
		The player's pid. -1 if unknown
	look: :class:`str`
		The player's look. '' if unknown
	gender: :class:`int`
		The player's gender.
	title: :class:`int`
		The player's title id. 0 if unknown
	title_stars: :class:`int`
		The player's title's stars.
	hasCheese: :class:`bool`
		True if the player has the cheese.
	isDead: :class:`bool`
		True if the player is dead.
	isShaman: :class:`bool`
		True if the player is shaman.
	isVampire: :class:`bool`
		True if the player is vampire.
	score: :class:`int`
		The player's score.
	mouseColor: :class:`int`
		The color of the player's fur.
	nameColor: :class:`int`
		The color of the player's name.
	shamanColor: :class:`int`
		The color of the player's shaman's feather.
	facingRight: :class:`bool`
		True if the player is facing right.
	movingLeft: :class:`bool`
		True if the player is moving to the left.
	movingRight: :class:`bool`
		True if the player is moving to the right.
	x: :class:`int`
		The player's x position.
	y: :class:`int`
		The player's y position.
	vx: :class:`int`
		The player's horizontal speed.
	vy: :class:`int`
		The player's vertical speed.
	ducking: :class:`bool`
		True if the player is ducking (crouching).
	jumping: :class:`bool`
		True if the player is jumping.
	"""
	def __init__(self, username, uid=-1, pid=-1, **kwargs):
		self.gender = kwargs.get('gender', 0)
		self.look = kwargs.get('look', '')
		self.id = uid
		self.pid = pid
		self.title = kwargs.get('title', 0)
		self.title_stars = kwargs.get('title_stars', 0)
		self.username = username

		self.hasCheese = kwargs.get('hasCheese', False)
		self.isDead = kwargs.get('isDead', False)
		self.isShaman = kwargs.get('isShaman', False)
		self.isVampire = kwargs.get('isVampire', False)
		self.score = kwargs.get('score', 0)

		self.mouseColor = kwargs.get('mouseColor', 0)
		self.nameColor = kwargs.get('nameColor', -1)
		self.shamanColor = kwargs.get('shamanColor', 0)

		self.facingRight = True
		self.movingLeft = False
		self.movingRight = False

		self.x = 0
		self.y = 0
		self.vx = 0
		self.vy = 0
		self.ducking = False
		self.jumping = False

	@classmethod
	def from_packet(cls, packet: Packet):
		"""Reads a Player from a packet.
		:param packet: :class:`aiotfm.Packet` the packet.
		:return: :class:`aiotfm.Player` the player.
		"""
		name = packet.readUTF()
		pid = packet.read32()
		kwargs = {
			'isShaman': packet.readBool(),
			'isDead': packet.readBool(),
			'score': packet.read16(),
			'hasCheese': packet.readBool(),
			'title': packet.read16(),
			'title_stars': packet.read8() - 1,
			'gender': packet.read8(),
		}
		packet.readUTF() # ???

		look = packet.readUTF()
		packet.readBool() # rasterisation ? wth
		mouseColor = packet.read32()
		shamanColor = packet.read32()
		packet.read32() # ???
		color = packet.read32()
		nameColor = -1 if color == 0xFFFFFFFF else color

		kwargs.update({
			'look': look,
			'mouseColor': mouseColor,
			'shamanColor': shamanColor,
			'color': color,
			'nameColor': nameColor
		})

		return cls(name, pid=pid, **kwargs)

	def __str__(self):
		return self.username.capitalize().replace('#0000', '')

	def __eq__(self, other):
		if isinstance(other, str):
			return str(self) == other or self.username.lower() == other.lower()
		if -1 not in [self.id, other.id]:
			return self.id == other.id
		if -1 not in [self.pid, other.pid]:
			return self.pid == other.pid
		return self.username.lower() == other.username.lower()

	@property
	def isGuest(self):
		"""Return True if the player is a guest (Souris)"""
		return self.username.startswith('*')


class Profile:
	"""Represents a player's profile.

	Attributes
	----------
	username: `str`
		The player's username.
	uid: `int`
		The player's id.
	registration_date: `int`
		The registration timestamp of the player.
	privLevel: `int`
		The privilege level of the player.
	gender: `int`
		Player's gender.
	tribe: `str`
		Player's tribe. Can be `None`.
	soulmate: `str`
		Player's soulmate. Can be `None`.
	title: `int`
		The title above the player's head.
	titles: `set`
		The list of the unlocked titles.
	titles_stars: `dict`
		A dictionary where are stored the number of stars a title has.
	look: `str`
		The player's look.
	level: `int`
		The player's shaman level.
	badges: `dict`
		All badges unlocked by the player and their number.
	stats: `Stats`
		The player's stats.
	equippedOrb: `int`
		The equipped orb of the player.
	orbs: `set`
		The list of unlocked orbs.
	adventurePoints: `int`
		Number of adventure points the player has.
	"""
	def __init__(self, packet: Packet):
		self.username = packet.readUTF()
		self.id = packet.read32()

		self.registration_date = packet.read32()
		self.privLevel = packet.read8()
		self.gender = packet.read8()
		self.tribe = packet.readUTF() or None
		self.soulmate = packet.readUTF() or None
		stats = [packet.read32() for i in range(7)]
		self.title = packet.read16()

		self.titles = set()
		self.titles_stars = {}
		for _ in range(packet.read16()):
			title_id, stars = packet.read16(), packet.read8()
			self.titles.add(title_id)
			if stars > 1:
				self.titles_stars[title_id] = stars

		self.look = packet.readUTF()
		self.level = packet.read16()

		self.badges = {}
		for _ in range(round(packet.read16() / 2)):
			badge, quantity = packet.read16(), packet.read16()
			self.badges[badge] = quantity

		modeStats = []
		for _ in range(packet.read8()):
			modeStats.append((packet.read8(), packet.read32(), packet.read32(), packet.read8()))
		self.stats = Stats(stats, modeStats)

		self.equippedOrb = packet.read8()
		self.orbs = set()
		for _ in range(packet.read8()):
			self.orbs.add(packet.read8())

		self.adventurePoints = packet.read32()


class Stats:
	"""Represents the statistics of a player.

	Attributes
	----------
	normalModeSaves: `int`
		Number of shaman saves in normal mode.
	hardModeSaves: `int`
		Number of shaman saves in hard mode.
	divineModeSaves: `int`
		Number of shaman saves in divine mode.
	shamanCheese: `int`
		Number of cheese personally gathered.
	firsts: `int`
		Number of cheese gathered first.
	gatheredCheese: `int`
		Total number of gathered cheese.
	bootcamps: `int`
		Number of bootcamp.
	modeStats: `list`
		A list of tuples that represents the stats in different mode.
		(id, progress, progressLimit, imageId)
	"""
	def __init__(self, stats, modeStats):
		self.normalModeSaves = stats[0]
		self.hardModeSaves = stats[4]
		self.divineModeSaves = stats[6]
		self.shamanCheese = stats[1]
		self.firsts = stats[2]
		self.gatheredCheese = stats[3]
		self.bootcamps = stats[5]

		self.modeStats = modeStats # id, progress, progressLimit, imageId