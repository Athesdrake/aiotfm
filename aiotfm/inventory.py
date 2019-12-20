import asyncio

from functools import cmp_to_key

from aiotfm.packet import Packet
from aiotfm.player import Player
from aiotfm.utils import TradeState
from aiotfm.errors import TradeOnWrongState

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

	def __eq__(self, other):
		return self.id == other.id

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

	def __getitem__(self, index):
		if not isinstance(index, int):
			raise TypeError("Index must be int, not {}".format(type(index)))
		return self.items[index]

	def __setitem__(self, index, value):
		if not isinstance(index, int):
			raise TypeError("Index must be int, not {}".format(type(index)))
		self.items[index] = value

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
		return self.items.get(id, InventoryItem(id))

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


class TradeContainer:
	def __init__(self, trade):
		self.trade = trade
		self._content = []

	def get(self, id, default=0):
		for item in self._content:
			if item.id == id:
				return item.quantity
		return default

	def getSlot(self, index):
		return self._content[index]

	def add(self, id, quantity):
		for item in self._content:
			if item.id == id:
				item.quantity += quantity
				if item.quantity == 0:
					self._content.remove(item)
				break
		else:
			self._content.append(InventoryItem(id, quantity=quantity))


class Trade:
	"""Represents a trade that the bot is participating (not started, in progress or ended).

	Attributes
	----------
	client: :class:`aiotfm.Client`
		The reference to the client involved in the trade.
	trader: `str`
		The player the client is trading with.
	locked: List[`bool`]
		A list of two `bool` describing the locked state of each party.
	imports: :class:`aiotfm.inventory.TradeContainer`
		The container of the items you will receive if the trade succeed.
	exports: :class:`aiotfm.inventory.TradeContainer`
		The container of the items you will give if the trade succeed.
	state: :class:`aiotfm.utils.TradeState`
		The current state of the trade.
			ON_INVITE: an invitation has been received from/sent to the other party.
			ACCEPTING: the client accepted and is waiting for the other party to be ready.
			TRADING:   the only state of the trade where you are able to add items.
			CANCELLED: the trade has been cancelled by one of the parties.
			SUCCESS:   the trade finished successfully."""
	def __init__(self, client, trader):
		self.client = client
		self.trader = trader
		self.locked = [False, False] # 0: client, 1: trader

		self.imports = TradeContainer(self)
		self.exports = TradeContainer(self)

		self.state = TradeState.ON_INVITE
		self.pid = -1

		if isinstance(trader, Player):
			if self.trader.isGuest:
				raise TypeError("You can not trade with a guest.")
			if self.trader == self.client.username:
				raise TypeError("You can not trade with yourself.")
			if self.trader.pid == 0:
				raise TypeError("You can not trade with a player having the same IP.")
			self.trader = self.trader.username
			self.pid = trader.pid
		elif isinstance(trader, str):
			if '#' not in trader:
				raise TypeError("The player tag is needed to begin a trade.")
			if trader.startswith('*'):
				raise TypeError("You can not trade with a guest.")
		else:
			raise TypeError(f"Trade excepted 'Player' or 'str' type, got '{type(trader)}")

	def __repr__(self):
		return "<Trade state={} locked=[client:{}, trader:{}] trader={} pid={}>".format(TradeState[self.state], *self.locked, self.trader, self.pid)

	def __eq__(self, other):
		if self.pid == -1 or other.pid == -1:
			return self.trader.lower() == other.trader.lower()
		return self.pid == other.pid

	@property
	def closed(self):
		"""Returns True if the trade is closed."""
		return self.state in (TradeState.SUCCESS, TradeState.CANCELLED)

	def _start(self, pid):
		self.state = TradeState.TRADING
		self.client.trade = self
		self.pid = pid

	def _close(self, succeed=False):
		self.state = TradeState.SUCCESS if succeed else TradeState.CANCELLED
		if self.client.trades.pop(self.pid, None) is None:
			self.client.pending_trades.remove(self)

		self.client.dispatch('trade_close', self, succeed)

	async def cancel(self):
		"""|coro|
		Cancels the trade."""
		if self.state != TradeState.TRADING:
			raise TradeOnWrongState('cancel', TradeState[self.state])

		await self.client.main.send(Packet.new(31, 6).writeString(self.trader).write8(2))

	async def accept(self):
		"""|coro|
		Accepts the trade."""
		if self.state != TradeState.ON_INVITE:
			raise TradeOnWrongState('accept', TradeState[self.state])

		self.state = TradeState.ACCEPTING
		await self.client.main.send(Packet.new(31, 5).writeString(self.trader))

	async def addItem(self, id, quantity):
		"""|coro|
		Adds an item to the trade.

		:param id: :class:`int` The item id.
		:param quantity: :class:`int` The quantity of item to add."""
		if self.state != TradeState.TRADING:
			raise TradeOnWrongState('addItem', TradeState[self.state])

		quantity = min(max(quantity, 0), 200)
		packet = Packet.new(31, 8).write16(id).writeBool(True).buffer

		ten = packet + b'\x01'
		for i in range(quantity//10):
			await self.client.main.send(Packet(ten))
			await asyncio.sleep(.05)

		unit = packet + b'\x00'
		for i in range(quantity%10):
			await self.client.main.send(Packet(unit))
			await asyncio.sleep(.05)

	async def removeItem(self, id, quantity):
		"""|coro|
		Removes an item from the trade.

		:param id: :class:`int` The item id.
		:param quantity: :class:`int` The quantity of item to remove."""
		if self.state != TradeState.TRADING:
			raise TradeOnWrongState('removeItem', TradeState[self.state])

		quantity = min(max(quantity, 0), 200)
		packet = Packet.new(31, 8).write16(id).writeBool(False).buffer

		ten = packet + b'\x01'
		for i in range(quantity//10):
			await self.client.main.send(Packet(ten))
			await asyncio.sleep(.05)

		unit = packet + b'\x00'
		for i in range(quantity%10):
			await self.client.main.send(Packet(unit))
			await asyncio.sleep(.05)

	async def lock(self):
		"""|coro|
		Locks (confirms) the trade."""
		if self.state != TradeState.TRADING:
			raise TradeOnWrongState('lock', TradeState[self.state])
		if self.locked[0]:
			raise TypeError("Can not lock a trade that is already locked by the client.")

		await self.client.main.send(Packet.new(31, 9).writeBool(True))

	async def unlock(self):
		"""|coro|
		Unlocks (cancels the confirmation) the trade."""
		if self.state != TradeState.TRADING:
			raise TradeOnWrongState('lock', TradeState[self.state])
		if not self.locked[0]:
			raise TypeError("Can not unlock a trade that is not locked by the client.")

		await self.client.main.send(Packet.new(31, 9).writeBool(False))
