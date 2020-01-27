from aiotfm.packet import Packet

class Shop:
	def __init__(self, packet:Packet):
		self.cheese = packet.read32()
		self.fraise = packet.read32()
		self.look = packet.readUTF()

		self.owned_items = set(Item.from_packet(packet) for i in range(packet.read32()))
		self.items = set(ShopItem.from_packet(packet) for i in range(packet.read32()))

		self.full_outfits = set(Outfit.from_fashion(packet) for i in range(packet.read8()))
		self.outfits = set(Outfit.from_packet(packet, i) for i in range(packet.read16()))

		self.owned_shaman_objects = set(OwnedShamanObject.from_packet(packet) for i in range(packet.read16()))
		self.shaman_objects = set(ShamanObject.from_packet(packet) for i in range(packet.read16()))

	def to_dict(self):
		items = [item.to_dict() for item in sorted(self.items, key=lambda i: i.uid)]

		return {
			"cheese": self.cheese,
			"fraise": self.fraise,
			"look": self.look,
			"items": items
		}

	def cost(self, outfit):
		cheese = 0
		fraise = 0
		fraise_sup = 0
		for item in outfit.items:
			if item.id==0:
				continue
			item = self.getItem(item)
			cheese += item.cheese if item.cheese<1000001 else 0
			if item.fraise==0:
				fraise_sup += item.cheese if item.cheese<1000001 else 0
			else:
				fraise += item.fraise

		if outfit.fur!=1:
			fur = [i for i in self.items if i.id==outfit.fur and (i.category==21 or i.category==22)][0]
			cheese += fur.cheese if fur.cheese<1000001 else 0
			fraise += fur.fraise
			if fur.fraise==0:
				fraise_sup += fur.cheese if fur.cheese<1000001 else 0

		return cheese, fraise, fraise_sup

	def getItem(self, item):
		for i in self.items:
			if i==item:
				return i
		return None

	def category(self, id):
		return set(i for i in self.items if i.category==id)

class Item:
	def __init__(self, category, id, colors=None):
		self.category, self.id = int(category), int(id)
		self.uid = self.category*10000+self.id

		self.colors = colors or []

	def __eq__(self, other):
		return self.category==other.category and self.id==other.id

	def __hash__(self):
		return self.uid

	@classmethod
	def from_packet(cls, packet:Packet):
		nbr_colors = packet.read8()
		uid = packet.read32()
		cat = (uid-10000)//10000 if uid>9999 else uid//100
		id = uid%1000 if uid>9999 else uid%100 if uid>999 else uid%(100*cat) if uid>99 else uid
		colors = []
		if nbr_colors>0:
			colors = [packet.read32() for i in range(nbr_colors-1)]

		return cls(cat, id, colors)

	@classmethod
	def parse(cls, cat, string):
		string = string.split('_')
		id = int(string[0])
		if len(string)==1:
			return cls(cat, id)
		return cls(cat, id, [int(color, 16) for color in string[1].split('+')])

class ShopItem(Item):
	def __init__(self, category, id, colors, is_new, flag, cheese, fraise, special):
		super().__init__(category, id)

		self.nbr_colors = colors
		self.is_new = is_new
		self.flag = flag
		self.cheese = cheese
		self.fraise = fraise
		self.special = special
		if self.is_new:
			print(category, id, colors, is_new, flag, cheese, fraise, special)

	def to_dict(self):
		data = {
			'category': self.category,
			'cheese': self.cheese,
			'colors': self.nbr_colors,
			'fraise': self.fraise,
			'id': self.id
		}
		if self.cheese==1000001:
			data['purchasable'] = False
			data['cheese'] = 0
		if self.flag==13:
			data['collector'] = self.flag==13
		if self.is_new:
			data['new'] = self.is_new
		return data

	@classmethod
	def from_packet(cls, packet:Packet):
		return cls(
			packet.read16(), packet.read16(), packet.read8(), packet.readBool(),
			packet.read8(), packet.read32(), packet.read32(), packet.read16()
		)

class Outfit:
	def __init__(self, look, id=-1, flag=-1):
		self.look = look
		self.id = id
		self.flag = flag

	def __eq__(self, other):
		if isinstance(other, str):
			return self.look==other
		return self.look==other.look

	def __hash__(self):
		return hash(hash(self.look)+hash(self.id))

	@classmethod
	def from_fashion(cls, packet:Packet):
		id = packet.read16()
		look = packet.readUTF()
		flag = packet.read8()
		return cls(look, id, flag)

	@classmethod
	def from_packet(cls, packet:Packet, id):
		return cls(packet.readUTF(), id)

	@property
	def fur(self):
		return int(self.look.split(';')[0])

	@property
	def items(self):
		items = []
		for i, item in enumerate(self.look.split(';')[1].split(',')):
			items.append(Item.parse(i, item))
		return items

	@property
	def head(self):
		return self.items[0]

	@property
	def eyes(self):
		return self.items[1]

	@property
	def ears(self):
		return self.items[2]

	@property
	def mouth(self):
		return self.items[3]

	@property
	def neck(self):
		return self.items[4]

	@property
	def hair(self):
		return self.items[5]

	@property
	def tail(self):
		return self.items[6]

	@property
	def lenses(self):
		return self.items[7]

	@property
	def hands(self):
		return self.items[8]

class ShamanObject:
	def __init__(self, id, colors, is_new, flag, cheese, fraise):
		self.id = id
		self.colors = colors
		self.is_new = is_new
		self.flag = flag
		self.cheese = cheese
		self.fraise = fraise

	def __eq__(self, other):
		return self.id==other.id

	def __hash__(self):
		return self.id

	@classmethod
	def from_packet(cls, packet:Packet):
		return cls(
			packet.read32(), packet.read8(), packet.readBool(), packet.read8(),
			packet.read32(), packet.read16()
		)

class OwnedShamanObject(ShamanObject):
	def __init__(self, id, equiped, colors):
		self.id = id
		self.equiped = equiped
		self.colors = colors

	@classmethod
	def from_packet(cls, packet:Packet):
		id = packet.read16()
		equiped = packet.readBool()

		nbr_colors = packet.read8()
		colors = []
		if nbr_colors>0:
			colors = [packet.read32() for i in range(nbr_colors-1)]

		return cls(id, equiped, colors)