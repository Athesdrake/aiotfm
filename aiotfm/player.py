from .packet import Packet

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
			modeStats.append(packet.unpack('BLLB'))
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
	shamanCheeses `int` number of cheese personally gathered.
	firsts `int` number of cheese gathered first.
	gatheredCheeses `int` total number of gathered cheeses.
	bootcamps `int` number of bootcamp.
	modeStats `list` a list of tuples that represents the stats in different mode. (id, progress, progressLimit, imageId)
	"""
	def __init__(self, stats, modeStats):
		self.normalModeSaves = stats[0]
		self.hardModeSaves = stats[4]
		self.divineModeSaves = stats[6]
		self.shamanCheeses = stats[1]
		self.firsts = stats[2]
		self.gatheredCheeses = stats[3]
		self.bootcamps = stats[5]

		self.modeStats = modeStats # id, progress, progressLimit, imageId