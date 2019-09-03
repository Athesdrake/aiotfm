from functools import cmp_to_key

from aiotfm.packet import Packet
from aiotfm.player import Player

class InventoryItem:
	"""Represents an inventory item.

	Attributes
	----------
	id: `int`
		The item id.
	quantity: `int`
		The quantity of the item.
	inventory: Optional[`aiotfm.inventory.Inventory`]
		The inventory class. Might be None.
	can_use: `bool`
		True if you can use this item.
	category: `int`
		Define the category's item. Used by the sorting algorithm.
	img_id: `str`
		Id used to get the item's image.
	is_event: `bool`
		True if it's an item from an event.
	slot: `int`
		Define the equipped slot with this item. If slot is 0 then the item is not equipped.
	"""
	def __init__(self, id, **kwargs):
		self.id = id
		self.quantity = kwargs.get("quantity", 0)
		self.inventory = kwargs.get("inventory", None)

		self.can_use = kwargs.get("can_use", True)
		self.category = kwargs.get("category", 0)
		self.img_id = kwargs.get("img_id", str(self.id))
		self.is_event = kwargs.get("is_event", False)
		self.slot = kwargs.get("slot", 0)

	def __repr__(self):
		return "<InventoryItem id={} quantity={}>".format(self.id, self.quantity)

	@property
	def image_url(self):
		return 'https://www.transformice.com/images/x_transformice/x_inventaire/{.img_id}.jpg'.format(self)

	@property
	def is_currency(self):
		return self.id in (800, 801, 2253, 2254, 2257, 2260, 2261)

	@property
	def is_equipped(self):
		return self.slot>0

	@classmethod
	def from_packet(cls, packet):
		id = packet.read16()
		kwargs = {
			'quantity': packet.read8(),
			'category': packet.read8(),
			'is_event': packet.readBool(),
			'can_use': packet.readBool()
		}
		packet.readBool() # similar to `can_use`
		packet.readBool() # similar to `can_use`
		packet.readBool()
		packet.readBool()
		if packet.readBool():
			kwargs['img_id'] = packet.readUTF()
		kwargs['slot'] = packet.read8() # if equipped, this is the slot (1, 2, 3); otherwise this is 0
		return cls(id, **kwargs)

	async def use(self):
		"""|coro|
		Uses this item."""
		if self.inventory is None or self.inventory.client is None:
			raise TypeError("InventoryItem doesn't have the inventory variable or Inventory doesn't have the client variable.")
		await self.inventory.client.main.send(Packet.new(31, 3).write16(self.id))

class Inventory:
	"""Represents the bot's inventory.

	Attributes
	----------
	items: `dict`
		A dict containing all the items. The key is an :class:`int` and the value is an :class:`aiotfm.inventory.InventoryItem`.
	client: `aiotfm.client.Client`
		The bot that this inventory belongs to.
	"""
	def __init__(self, client=None, items=None):
		self.items = items or {}
		self.client = client

		for item in self:
			item.inventory = self

	def __repr__(self):
		return "<Inventory client={!r}>".format(self.client)

	def __iter__(self):
		return iter(self.items.values())

	@classmethod
	def from_packet(cls, packet):
		items = {}

		for item in range(packet.read16()):
			item = InventoryItem.from_packet(packet)
			items[item.id] = item

		return cls(items=items)

	def get(self, id):
		"""Gets an item from this :class:`aiotfm.inventory.Inventory`.
		Shorthand for :class:`aiotfm.inventory.Inventory`.items.get"""
		return self.items.get(id)

	def sort(self):
		"""Sort the inventory the same way the client does.
		:return: :class:`list`
		"""
		def cmp(a, b):
			if (a.is_currency or b.is_currency) and not (a.is_currency and b.is_currency):
				return -1 if a.is_currency else 1 # Currency are always on the top
			if (a.is_event or b.is_event) and not (a.is_event and b.is_event):
				return -1 if a.is_event else 1 # Event items comes always after the currency
			if a.category!=b.category:
				return b.category - a.category # Higher means first
			return a.id - b.id # Lastly the items are sorted by their ids

		return sorted(iter(self), key=cmp_to_key(cmp))

class Trade:
	"""Represents a trade that the bot is participating (not started, in progress or ended).

	Attributes
	----------
	traders: `list`
		The users that are participating on the trade. One of them is an instance of :class:`aiotfm.client.Client` and the other one of :class:`aiotfm.player.Player`.
		The first item is always who invited to trade.
	locked_me: `bool`
		Whether the bot has locked (confirmed) the trade.
	locked_other: `bool`
		Whether the other trader (not the bot itself) has locked (confirmed) the trade.
	items_me: `dict`
		A dict containing all the items that the bot offers. It is a dict where the key is the item id and the value is the quantity.
	items_other: `dict`
		A dict containing all the items that the other trader offers. It is a dict where the key is the item id and the value is the quantity.
	on_invite: `bool`
		Whether the trade is still on the invite screen.
	accepted: `bool`
		Whether the trade has been accepted (started).
	alive: `bool`
		Whether the trade didn't end yet (even if it is on the invite screen).
	canceled: `bool`
		Whether the trade was canceled by the bot."""
	def __init__(self, host, destiny):
		self.traders = [host, destiny]
		self.locked_me = False
		self.locked_other = False

		self.items_me = {}
		self.items_other = {}

		self.on_invite = False
		self.accepted = False
		self.alive = False
		self.canceled = False

		self._starter = None
		self._client, self._other = None, None
		for trader in self.traders:
			if isinstance(trader, Player): # If we import client.py it will be an infinite import!
				if self._client is None:
					self._other_index = 0
				else:
					self._other_index = 1
				self._other = trader
			else:
				self._client = trader

		if self._client is None:
			raise TypeError("Either host or destiny trader must be an instance of Client.")
		if self._other is None:
			raise TypeError("Either host or destiny trader must be an instance of Player.")

		self._update_player(self._other)

	def __repr__(self):
		return "<Trade on_invite={} accepted={} alive={} canceled={} locked_me={} locked_other={} traders={}>".format(
			self.on_invite, self.accepted, self.alive, self.canceled, self.locked_me, self.locked_other, self.traders
		)

	def _update_player(self, player):
		self.traders[self._other_index] = self._other = player
		if player.trade != self:
			player.trade = self

	def _close(self):
		self.alive = False
		if self._client.trade == self:
			self._client.trade = None
		if self._other.trade == self:
			self._other.trade = None
		if self in self._client.trades:
			self._client.trades.remove(self)

	async def cancel(self):
		"""|coro|
		Cancels the trade."""
		if not self.alive:
			raise TypeError("Can not cancel a dead trade.")
		self._close()
		self.canceled = True
		await self._client.main.send(Packet.new(31, 6).writeString(self._other.username).write8(2))
		self._client.dispatch('trade_close', self)

	async def accept(self):
		"""|coro|
		Accepts the trade."""
		if not self.alive:
			raise TypeError("Can not accept a dead trade.")
		if not self.on_invite:
			raise TypeError("Can not accept a trade when it is not on the invite state.")
		if self.accepted:
			raise TypeError("Can not accept an already accepted trade.")
		self.accepted = True
		await self._client.main.send(Packet.new(31, 5).writeString(self._other.username))

	async def addItem(self, id, ten=False):
		"""|coro|
		Adds an item to the trade.

		:param id: :class:`int` The item id.
		:param ten: Optional[:class:`bool`] Whether to add ten items or only one."""
		if not self.alive:
			raise TypeError("Can not add items to a dead trade.")
		if self.on_invite:
			raise TypeError("Can not add items to a trade when it is on the invite state.")
		await self._client.main.send(Packet.new(31, 8).write16(id).writeBool(True).writeBool(ten))

	async def removeItem(self, id, ten=False):
		"""|coro|
		Removes an item from the trade.

		:param id: :class:`int` The item id.
		:param ten: Optional[:class:`bool`] Whether to remove ten items or only one."""
		if not self.alive:
			raise TypeError("Can not remove items from a dead trade.")
		if self.on_invite:
			raise TypeError("Can not remove items from a trade when it is on the invite state.")
		await self._client.main.send(Packet.new(31, 8).write16(id).writeBool(False).writeBool(ten))

	async def lock(self):
		"""|coro|
		Locks (confirms) the trade."""
		if not self.alive:
			raise TypeError("Can not lock a dead trade.")
		if self.on_invite:
			raise TypeError("Can not lock a trade when it is on the invite state.")
		if self.locked_me:
			raise TypeError("Can not lock a trade that is already locked by me.")
		self.locked_me = True
		await self._client.main.send(Packet.new(31, 9).writeBool(True))

	async def unlock(self):
		"""|coro|
		Unlocks (cancels the confirmation) the trade."""
		if not self.alive:
			raise TypeError("Can not lock a dead trade.")
		if self.on_invite:
			raise TypeError("Can not lock a trade when it is on the invite state.")
		if not self.locked_me:
			raise TypeError("Can not lock a trade that is already unlocked by me.")
		self.locked_me = False
		await self._client.main.send(Packet.new(31, 9).writeBool(False))