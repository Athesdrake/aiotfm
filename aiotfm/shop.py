from aiotfm.packet import Packet


class Shop:
	"""Represents the shop in game.

	Parameters
	----------
	packet: :class:`aiotfm.Packet`
		The packet where the shop content cill be read.

	Attributes
	----------
	cheese: :class:`int`
		The number of cheese the client has.
	fraise: :class:`int`
		The numberof fraise (strawberries) the client has.
	look: :class:`str`
		The client's look.
	owned_items: :class:`set`[:class:`aiotfm.shop.Item`]
		All items the client own.
	items: :class:`set`[:class:`aiotfm.shop.ShopItem`]
		All items present in the shop.
	full_outfits: :class:`set`[:class:`aiotfm.shop.Outfit`]
		Available fashion outfits you can buy.
	outfits: :class:`set`[:class:`aiotfm.shop.Outfit`]
		The client own outfits.
	owned_shaman_objects: :class:`set`[:class:`aiotfm.shop.OwnedShamanObject`]
		All shaman object the client own.
	shaman_objects: :class:`set`[:class:`aiotfm.shop.ShamanObject`]
		All shaman object available in the shop.
	"""
	def __init__(self, packet: Packet):
		self.cheese = packet.read32()
		self.fraise = packet.read32()
		self.look = packet.readUTF()

		self.owned_items = set(Item.from_packet(packet) for _ in range(packet.read32()))
		self.items = set(ShopItem.from_packet(packet) for _ in range(packet.read32()))

		self.full_outfits = set(Outfit.from_fashion(packet) for _ in range(packet.read8()))
		self.outfits = set(Outfit.from_packet(packet, i) for i in range(packet.read16()))

		self.owned_shaman_objects = set(
			OwnedShamanObject.from_packet(packet) for _ in range(packet.read16())
		)
		self.shaman_objects = set(ShamanObject.from_packet(packet) for _ in range(packet.read16()))

	def to_dict(self):
		"""Export the shop into a serializable dict.
		:return: :class:`dict`
		"""
		items = [item.to_dict() for item in sorted(self.items, key=lambda i: i.uid)]

		return {
			"cheese": self.cheese,
			"fraise": self.fraise,
			"look": self.look,
			"items": items
		}

	def cost(self, outfit):
		"""Compute and return the total price of an outfit.
		:param outfit: :class:`aiotfm.shop.Outfit`
		:return: :class:`tuple`[:class:`int`]
			(Total in cheese, total in fraise, cheese supplement of items you can't buy with fraise)
		"""
		cheese = 0
		fraise = 0
		fraise_sup = 0
		for item in outfit.items:
			if item.id == 0:
				continue
			item = self.getItem(item)
			cheese += item.cheese if item.cheese < 1000001 else 0
			if item.fraise == 0 and item.cheese < 1000001:
				fraise_sup += item.cheese
			else:
				fraise += item.fraise

		if outfit.fur != 1:
			fur = [i for i in self.items if i.id == outfit.fur and (21 <= i.category <= 22)][0]
			cheese += fur.cheese if fur.cheese < 1000001 else 0
			fraise += fur.fraise
			if fur.fraise == 0 and fur.cheese < 1000001:
				fraise_sup += fur.cheese

		return cheese, fraise, fraise_sup

	def getItem(self, item):
		"""Return the shop item with the same id.
		:param item: :class:`aiotfm.shop.Item` the item you want to price of.
		:return: :class:`aiotfm.shop.ShopItem` the item with the prices.
		"""
		for i in self.items:
			if i == item:
				return i
		return None

	def category(self, id_):
		"""Return the items from a category.
		:param id_: :class:`int` the category's id?
		:return: :class:`set`[:class:`aiotfm.shop.Item`] the items.
		"""
		return set(i for i in self.items if i.category == id_)


class Item:
	"""Represents an item from the shop.

	Parameters
	----------
	category: :class:`int`
		The item's category.
	id_: :class:`int`
		The item's id.
	colors: Optional[:class:`int`]
		The item's colors.

	Attributes
	----------
	category: :class:`int`
		The item's category.
	id: :class:`int`
		The item's id.
	uid: :class:`int`
		The item's unique id.
	colors: :class:`int`
		The item's colors.
	"""
	def __init__(self, category, id_, colors=None):
		self.category, self.id = int(category), int(id_)
		self.uid = self.category * 10000 + self.id

		self.colors = colors or []

	def __eq__(self, other):
		return self.category == other.category and self.id == other.id

	def __hash__(self):
		return self.uid

	@classmethod
	def from_packet(cls, packet: Packet):
		"""Reads an Item from a packet.
		:param packet: :class:`aiotfm.Packet`
		:return: :class:`aiotfm.shop.Item`
		"""
		nbr_colors = packet.read8()
		uid = packet.read32()
		cat = (uid - 10000) // 10000 if uid > 9999 else uid // 100

		if uid < 99:
			id_ = uid
		elif uid < 999:
			id_ = uid % (100 * cat)
		elif uid < 9999:
			id_ = uid % 100
		else:
			id_ = uid % 1000

		colors = []
		if nbr_colors > 0:
			colors = [packet.read32() for i in range(nbr_colors - 1)]

		return cls(cat, id_, colors)

	@classmethod
	def parse(cls, cat, string):
		"""Parse an Item from a string.
		:param cat: :class:`int` the item's category.
		:param string: :class:`str` the item.
		:return: :class:`aiotfm.shop.Item`
		"""
		string = string.split('_')
		id_ = int(string[0])
		if len(string) == 1:
			return cls(cat, id_)
		return cls(cat, id_, [int(color, 16) for color in string[1].split('+')])


class ShopItem(Item):
	"""Represents an item from the shop with its specifications.

	Parameters
	----------
	category: :class:`int`
		The item's category.
	id_: :class:`int`
		The item's id.
	colors: :class:`int`
		The item's colors.
	is_new: :class:`bool`
		True if it's a new item.
	flag: :class:`int`
		Contains the item's metadata.
	cheese: :class:`int`
		The item's price in cheese.
	fraise: :class:`int`
		The item's price in fraise.
	special: :class:`int`
		The item's special data.

	Attributes
	----------
	category: :class:`int`
		The item's category.
	id: :class:`int`
		The item's id.
	uid: :class:`int`
		The item's unique id.
	colors: :class:`int`
		The item's colors.
	nbr_colors: :class:`int`
		The number of customizable colors the item has.
	is_new: :class:`bool`
		True if it's a new item.
	flag: :class:`int`
		Contains the item's metadata.
	cheese: :class:`int`
		The item's price in cheese.
	fraise: :class:`int`
		The item's price in fraise.
	special: :class:`int`
		The item's special data.
	"""
	def __init__(self, category, id_, colors, is_new, flag, cheese, fraise, special):
		super().__init__(category, id_)

		self.nbr_colors = colors
		self.is_new = is_new
		self.flag = flag
		self.cheese = cheese
		self.fraise = fraise
		self.special = special
		if self.is_new:
			print(category, id_, colors, is_new, flag, cheese, fraise, special)

	def to_dict(self):
		"""Export the item into a serializable dict.
		:return: :class:`dict`
		"""
		data = {
			'category': self.category,
			'cheese': self.cheese,
			'colors': self.nbr_colors,
			'fraise': self.fraise,
			'id': self.id
		}
		if self.cheese == 1000001:
			data['purchasable'] = False
			data['cheese'] = 0
		if self.flag == 13:
			data['collector'] = self.flag == 13
		if self.is_new:
			data['new'] = self.is_new
		return data

	@classmethod
	def from_packet(cls, packet: Packet):
		"""Reads a ShopItem from a packet.
		:param packet: :class:`aiotfm.Packet`
		:return: :class:`aiotfm.shop.ShopItem`
		"""
		return cls(
			packet.read16(), packet.read16(), packet.read8(), packet.readBool(),
			packet.read8(), packet.read32(), packet.read32(), packet.read16()
		)


class Outfit:
	"""Represents an outfit from the shop.

	Parameters
	----------
	look: :class:`str`
		The outfit's look.
	id_: Optional[:class:`int`]
		The outfit's id.
	flag: :class:`int`
		Contains the outfit's metadata.

	Attributes
	----------
	look: :class:`str`
		The outfit's look.
	id: :class:`int`
		The outfit's id.
	flag: :class:`int`
		Contains the outfit's metadata.

	"""
	def __init__(self, look, id_=-1, flag=-1):
		self.look = look
		self.id = id_
		self.flag = flag

	def __eq__(self, other):
		if isinstance(other, str):
			return self.look == other
		return self.look == other.look

	def __hash__(self):
		return hash(hash(self.look) + hash(self.id))

	@classmethod
	def from_fashion(cls, packet: Packet):
		"""Reads a fashion Outfit from a packet.
		:param packet: :class:`aiotfm.Packet`
		:return: :class:`aiotfm.shop.Outfit`
		"""
		id_ = packet.read16()
		look = packet.readUTF()
		flag = packet.read8()
		return cls(look, id_, flag)

	@classmethod
	def from_packet(cls, packet: Packet, id_):
		"""Reads an Outfit from a packet.
		:param packet: :class:`aiotfm.Packet`
		:return: :class:`aiotfm.shop.Outfit`
		"""
		return cls(packet.readUTF(), id_)

	@property
	def fur(self):
		"""The fur's id of the outfit."""
		return int(self.look.split(';')[0])

	@property
	def items(self):
		"""The outfit's items."""
		items = []
		for i, item in enumerate(self.look.split(';')[1].split(',')):
			items.append(Item.parse(i, item))
		return items

	@property
	def head(self):
		"""The outfit's head item."""
		return self.items[0]

	@property
	def eyes(self):
		"""The outfit's eyes item."""
		return self.items[1]

	@property
	def ears(self):
		"""The outfit's ears item."""
		return self.items[2]

	@property
	def mouth(self):
		"""The outfit's mouth item."""
		return self.items[3]

	@property
	def neck(self):
		"""The outfit's neck item."""
		return self.items[4]

	@property
	def hair(self):
		"""The outfit's hair item."""
		return self.items[5]

	@property
	def tail(self):
		"""The outfit's tail item."""
		return self.items[6]

	@property
	def lenses(self):
		"""The outfit's lenses item."""
		return self.items[7]

	@property
	def hands(self):
		"""The outfit's hands item."""
		return self.items[8]


class ShamanObject:
	"""Represents shaman object from the shop.

	Parameters
	----------
	id_: :class:`int`
		The object's id.
	colors: :class:`int`
		The number of customizable colors the object has.
	is_new: :class:`bool`
		The object's metadata.
	flag: :class:`int`
		Contains the object's metadata.
	cheese: :class:`int`
		The obect's pricein cheese.
	fraise: :class:`int`
		The obect's pricein fraise.

	Attributes
	----------
	id: :class:`int`
		The object's id.
	colors: :class:`int`
		The number of customizable colors the object has.
	is_new: :class:`bool`
		The object's metadata.
	flag: :class:`int`
		Contains the object's metadata.
	cheese: :class:`int`
		The obect's pricein cheese.
	fraise: :class:`int`
		The obect's pricein fraise.

	"""
	def __init__(self, id_, colors, is_new, flag, cheese, fraise):
		self.id = id_
		self.colors = colors
		self.is_new = is_new
		self.flag = flag
		self.cheese = cheese
		self.fraise = fraise

	def __eq__(self, other):
		return self.id == other.id

	def __hash__(self):
		return self.id

	@classmethod
	def from_packet(cls, packet: Packet):
		"""Reads a ShamanObject from a packet.
		:param packet: :class:`aiotfm.Packet`
		:return: :class:`aiotfm.shop.ShamanObject`
		"""
		return cls(
			packet.read32(), packet.read8(), packet.readBool(), packet.read8(),
			packet.read32(), packet.read16()
		)


class OwnedShamanObject:
	"""Represents shaman object that the client own.

	Parameters
	----------
	id_: :class:`int`
		The object's id.
	equiped: :class:`bool`
		True if the client has the object equiped.
	colors: :class:`list`[:class:`int`]
		The custom colors the object has.

	Attributes
	----------
	id: :class:`int`
		The object's id.
	equiped: :class:`bool`
		True if the client has the object equiped.
	colors: :class:`list`[:class:`int`]
		The custom colors the object has.

	"""
	def __init__(self, id_, equiped, colors):
		self.id = id_
		self.equiped = equiped
		self.colors = colors

	def __eq__(self, other):
		return self.id == other.id

	def __hash__(self):
		return self.id

	@classmethod
	def from_packet(cls, packet: Packet):
		"""Reads a OwnedShamanObject from a packet.
		:param packet: :class:`aiotfm.Packet`
		:return: :class:`aiotfm.shop.OwnedShamanObject`
		"""
		id_ = packet.read16()
		equiped = packet.readBool()
		colors = [packet.read32() for i in range(max(packet.read8() - 1, 0))]

		return cls(id_, equiped, colors)