from typing import List, Optional, Set, Tuple, Union

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
		self.cheese: int = packet.read32()
		self.fraise: int = packet.read32()
		self.look: str = packet.readUTF()

		self.owned_items: Set[Item] = set(Item.from_packet(packet) for _ in range(packet.read32()))
		self.items: Set[ShopItem] = set(ShopItem.from_packet(packet) for _ in range(packet.read32()))

		self.full_outfits: Set[Outfit] = set(Outfit.from_fashion(packet) for _ in range(packet.read8()))
		self.outfits: Set[Outfit] = set(Outfit.from_packet(packet, i) for i in range(packet.read16()))

		self.owned_shaman_objects: Set[OwnedShamanObject] = set(
			OwnedShamanObject.from_packet(packet) for _ in range(packet.read16())
		)
		self.shaman_objects: Set[ShamanObject] = set(ShamanObject.from_packet(packet) for _ in range(packet.read16()))

	def to_dict(self) -> dict:
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

	def cost(self, outfit: 'Outfit') -> Tuple[int, int, int]:
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
			if item is None:
				continue

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

	def getItem(self, item: 'Item') -> Optional['ShopItem']:
		"""Return the shop item with the same id.
		:param item: :class:`aiotfm.shop.Item` the item you want to price of.
		:return: :class:`aiotfm.shop.ShopItem` the item with the prices.
		"""
		for i in self.items:
			if i == item:
				return i
		return None

	def category(self, id_: int) -> Set['ShopItem']:
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
	def __init__(self, category: int, id_: int, colors: Optional[List[int]] = None):
		self.category: int = int(category)
		self.id: int = int(id_)
		self.uid: int = self.category * 10000 + self.id

		self.colors: List[int] = colors or []

	def __eq__(self, other: object):
		if isinstance(other, Item):
			return self.category == other.category and self.id == other.id
		return NotImplemented

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
	def parse(cls, cat: int, string: Union[List[str], str]) -> 'Item':
		"""Parse an Item from a string.
		:param cat: :class:`int` the item's category.
		:param string: :class:`str` the item.
		:return: :class:`aiotfm.shop.Item`
		"""
		if isinstance(string, str):
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
	flags: :class:`int`
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
	flags: :class:`int`
		Contains the item's metadata.
	cheese: :class:`int`
		The item's price in cheese.
	fraise: :class:`int`
		The item's price in fraise.
	special: :class:`int`
		The item's special data.
	"""
	def __init__(
		self, category: int, id_: int, colors: int, is_new: bool,
		flags: int, cheese: int, fraise: int, special: int
	):
		super().__init__(category, id_)

		self.nbr_colors: int = colors
		self.is_new: bool = is_new
		self.flags: int = flags
		self.cheese: int = cheese
		self.fraise: int = fraise
		self.special: int = special

	def to_dict(self) -> dict:
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
		if self.flags == 13:
			data['collector'] = self.flags == 13
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
			packet.read8(), packet.read32(), packet.read32(), packet.read32() if packet.readBool() else 0
		)


class Outfit:
	"""Represents an outfit from the shop.

	Parameters
	----------
	look: :class:`str`
		The outfit's look.
	id_: Optional[:class:`int`]
		The outfit's id.
	flags: :class:`int`
		Contains the outfit's metadata.

	Attributes
	----------
	look: :class:`str`
		The outfit's look.
	id: :class:`int`
		The outfit's id.
	flags: :class:`int`
		Contains the outfit's metadata.

	"""
	def __init__(self, look: str, id_: int = -1, flags: int = -1):
		self.look: str = look
		self.id: int = id_
		self.flags: int = flags

	def __eq__(self, other: object):
		if isinstance(other, str):
			return self.look == other
		if isinstance(other, Outfit):
			return self.look == other.look
		return NotImplemented

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
		flags = packet.read8()
		return cls(look, id_, flags)

	@classmethod
	def from_packet(cls, packet: Packet, id_):
		"""Reads an Outfit from a packet.
		:param packet: :class:`aiotfm.Packet`
		:return: :class:`aiotfm.shop.Outfit`
		"""
		return cls(packet.readUTF(), id_)

	@property
	def fur(self) -> int:
		"""The fur's id of the outfit."""
		return int(self.look.split(';')[0])

	@property
	def items(self) -> List[Item]:
		"""The outfit's items."""
		items = []
		for i, item in enumerate(self.look.split(';')[1].split(',')):
			items.append(Item.parse(i, item))
		return items

	@property
	def head(self) -> Item:
		"""The outfit's head item."""
		return self.items[0]

	@property
	def eyes(self) -> Item:
		"""The outfit's eyes item."""
		return self.items[1]

	@property
	def ears(self) -> Item:
		"""The outfit's ears item."""
		return self.items[2]

	@property
	def mouth(self) -> Item:
		"""The outfit's mouth item."""
		return self.items[3]

	@property
	def neck(self) -> Item:
		"""The outfit's neck item."""
		return self.items[4]

	@property
	def hair(self) -> Item:
		"""The outfit's hair item."""
		return self.items[5]

	@property
	def tail(self) -> Item:
		"""The outfit's tail item."""
		return self.items[6]

	@property
	def lenses(self) -> Item:
		"""The outfit's lenses item."""
		return self.items[7]

	@property
	def hands(self) -> Item:
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
	flags: :class:`int`
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
	flags: :class:`int`
		Contains the object's metadata.
	cheese: :class:`int`
		The obect's pricein cheese.
	fraise: :class:`int`
		The obect's pricein fraise.

	"""
	def __init__(self, id_: int, colors: int, is_new: bool, flags: int, cheese: int, fraise: int):
		self.id: int = id_
		self.colors: int = colors
		self.is_new: bool = is_new
		self.flags: int = flags
		self.cheese: int = cheese
		self.fraise: int = fraise

	def __eq__(self, other: object):
		if isinstance(other, ShamanObject):
			return self.id == other.id
		return NotImplemented

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
	def __init__(self, id_: int, equiped: bool, colors: List[int]):
		self.id: int = id_
		self.equiped: bool = equiped
		self.colors: List[int] = colors

	def __eq__(self, other: object):
		if isinstance(other, OwnedShamanObject):
			return self.id == other.id
		return NotImplemented

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
