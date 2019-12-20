from aiotfm.packet import Packet

class Player:
	def __init__(self, username, id=-1, pid=-1, **kwargs):
		self.gender = kwargs.get('gender', 0)
		self.look = kwargs.get('look', '')
		self.id = id
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
	def from_packet(cls, packet:Packet):
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
			return str(self)==other or self.username.lower()==other.lower()
		if -1 not in [self.id, other.id]:
			return self.id==other.id
		if -1 not in [self.pid, other.pid]:
			return self.pid==other.pid
		return self.username.lower()==other.username.lower()

	@property
	def isGuest(self):
		return self.username.startswith('*')

class Profile:
	"""Represents a player's profile.

	## Attributes

	username `str` the player's username.
	id `int` the player's id.
	registration_date `int` the registration timestamp of the player.
	privLevel `int` the privilege level of the player.
	gender `int` player's gender.
	tribe `str` player's tribe. Can be `None`.
	soulmate `str` player's soulmate. Can be `None`.
	title `int` the title above the player's head.
	titles `set` the list of the unlocked titles.
	titles_stars `dict` a dictionary where are stored the number of stars a title has.
	look `str` the player's look.
	level `int` the player's shaman level.
	badges `dict` all badges unlocked by the player and their number.
	stats [`Stats`](#stats) the player's stats.
	equippedOrb `int` the equipped orb of the player.
	orbs `set` the list of unlocked orbs.
	adventurePoints `int` number of adventure points the player has.
	"""
	def __init__(self, packet:Packet):
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
		for i in range(packet.read16()):
			title_id, stars = packet.read16(), packet.read8()
			self.titles.add(title_id)
			if stars>1:
				self.titles_stars[title_id] = stars

		self.look = packet.readUTF()
		self.level = packet.read16()

		self.badges = {}
		for i in range(round(packet.read16()/2)):
			id, quantity = packet.read16(), packet.read16()
			self.badges[id] = quantity

		modeStats = []
		for i in range(packet.read8()):
			modeStats.append((packet.read8(), packet.read32(), packet.read32(), packet.read8()))
		self.stats = Stats(stats, modeStats)

		self.equippedOrb = packet.read8()
		self.orbs = set()
		for i in range(packet.read8()):
			self.orbs.add(packet.read8())

		self.adventurePoints = packet.read32()

class Stats:
	"""Represents the statistics of a player.

	## Attributes

	normalModeSaves `int` number of shaman saves in normal mode.
	hardModeSaves `int`  number of shaman saves in hard mode.
	divineModeSaves `int` number of shaman saves in divine mode.
	shamanCheese `int` number of cheese personally gathered.
	firsts `int` number of cheese gathered first.
	gatheredCheese `int` total number of gathered cheese.
	bootcamps `int` number of bootcamp.
	modeStats `list` a list of tuples that represents the stats in different mode. (id, progress, progressLimit, imageId)
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