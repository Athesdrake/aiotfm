import asyncio
from functools import cmp_to_key
from typing import List, Optional, Union

import aiotfm
from aiotfm.enums import TradeState
from aiotfm.errors import TradeOnWrongState
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
	def __init__(self, item_id: int, **kwargs):
		self.id: int = item_id
		self.quantity: int = kwargs.get("quantity", 0)
		self.inventory: Optional[Inventory] = kwargs.get("inventory", None)

		self.can_use: bool = kwargs.get("can_use", True)
		self.category: int = kwargs.get("category", 0)
		self.img_id: str = kwargs.get("img_id", str(self.id))
		self.is_event: bool = kwargs.get("is_event", False)
		self.slot: int = kwargs.get("slot", 0)

	def __repr__(self):
		return f"<InventoryItem id={self.id} quantity={self.quantity}>"

	def __eq__(self, other: object):
		if isinstance(other, InventoryItem):
			return self.id == other.id
		return NotImplemented

	@property
	def image_url(self) -> str:
		"""The image's url of the item."""
		return f'https://www.transformice.com/images/x_transformice/x_inventaire/{self.img_id}.jpg'

	@property
	def is_currency(self) -> bool:
		"""Return True if the item is a currency."""
		return self.id in (800, 801, 2253, 2254, 2257, 2260, 2261)

	@property
	def is_equipped(self) -> bool:
		"""Return True if the item is equipped"""
		return self.slot > 0

	@classmethod
	def from_packet(cls, packet: Packet):
		"""Read an item from a packet.
		:param packet: :class:`aiotfm.Packet` the packet.
		:return: :class:`aiotfm.inventory.InventoryItem` the item.
		"""
		item_id = packet.read16()
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

		# if equipped, this is the slot (1, 2, 3); otherwise this is 0
		kwargs['slot'] = packet.read8()
		return cls(item_id, **kwargs)

	async def use(self):
		"""|coro|
		Uses this item."""
		if self.inventory is None or self.inventory.client is None:
			message = "InventoryItem doesn't have the inventory variable or Inventory doesn't \
				have the client variable."
			raise TypeError(message)
		await self.inventory.client.main.send(Packet.new(31, 3).write16(self.id))


class Inventory:
	"""Represents the client's inventory.

	Attributes
	----------
	items: `dict`
		A dict containing all the items. The key is an :class:`int` and the value is
		an :class:`aiotfm.inventory.InventoryItem`.
	client: `aiotfm.client.Client`
		The client that this inventory belongs to.
	"""
	def __init__(self, client: 'aiotfm.Client' = None, items: dict = None):
		self.items: dict = items or {}
		self.client: aiotfm.Client = client

		for item in self:
			item.inventory = self

	def __repr__(self):
		return f"<Inventory client={self.client!r}>"

	def __iter__(self):
		return iter(self.items.values())

	def __getitem__(self, index: int):
		if not isinstance(index, int):
			raise TypeError(f"Index must be int, not {type(index)}")
		return self.items[index]

	def __setitem__(self, index: int, value: InventoryItem):
		if not isinstance(index, int):
			raise TypeError(f"Index must be int, not {type(index)}")
		self.items[index] = value

	@classmethod
	def from_packet(cls, packet: Packet):
		"""Read the inventory from a packet.
		:param packet: :class:`aiotfm.Packet` the packet.
		:return: :class:`aiotfm.inventory.Inventory` the inventory.
		"""
		items = {}

		for item in range(packet.read16()):
			item = InventoryItem.from_packet(packet)
			items[item.id] = item

		return cls(items=items)

	def get(self, item_id: int) -> InventoryItem:
		"""Gets an item from this :class:`aiotfm.inventory.Inventory`.
		Shorthand for :class:`aiotfm.inventory.Inventory`.items.get"""
		return self.items.get(item_id, InventoryItem(item_id))

	def getEquipped(self) -> List[InventoryItem]:
		"""Return all equipped items. Items are sorted.
		:return: List[:class:`aiotfm.inventory.InventoryItem`]
		"""
		return sorted((i for i in self.items.values() if i.is_equipped), key=lambda i: i.slot)

	def sort(self) -> List[InventoryItem]:
		"""Sort the inventory the same way the client does.
		:return: List[:class:`aiotfm.inventory.InventoryItem`]
		"""
		def cmp(a, b):
			if (a.is_currency or b.is_currency) and not (a.is_currency and b.is_currency):
				return -1 if a.is_currency else 1 # Currency are always on the top
			if (a.is_event or b.is_event) and not (a.is_event and b.is_event):
				return -1 if a.is_event else 1 # Event items comes always after the currency
			if a.category != b.category:
				return b.category - a.category # Higher means first
			return a.id - b.id # Lastly the items are sorted by their ids

		return sorted(iter(self), key=cmp_to_key(cmp))


class TradeContainer:
	"""Represents the content of a Trade."""
	def __init__(self, trade: 'Trade'):
		self.trade: Trade = trade
		self._content: List[InventoryItem] = []

	def __iter__(self):
		return iter(self._content)

	def get(self, item_id: int, default: int = 0) -> int:
		"""Returns the quantity of an item inside the TradeContainer.
		:param item_id: :class:`int` the item's id.
		:param default: Optional[:class:`int`] the default value if the item is not present.
		:return: :class:`int` the quantity of the item.
		"""
		for item in self._content:
			if item.id == item_id:
				return item.quantity

		return default

	def getSlot(self, index: int) -> InventoryItem:
		"""Returns the item inside a certain slot.
		:param index: :class:`int` the index.
		:return: :class:`aiotfm.inventory.InventoryItem` the item.
		"""
		return self._content[index]

	def add(self, item_id: int, quantity: int):
		"""Add a quantity of an item inside the container.
		:param item_id: :class:`int` the item's id.
		:param quantity: :class:`int` the quantity to add. Can be negative.
		"""
		for item in self._content:
			if item.id == item_id:
				item.quantity += quantity
				if item.quantity == 0:
					self._content.remove(item)
				break
		else:
			self._content.append(InventoryItem(item_id, quantity=quantity))


class Trade:
	"""Represents a trade that the client is participating (not started, in progress or ended).

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
	state: :class:`aiotfm.enums.TradeState`
		The current state of the trade.
			ON_INVITE: an invitation has been received from/sent to the other party.
			ACCEPTING: the client accepted and is waiting for the other party to be ready.
			TRADING:   the only state of the trade where you are able to add items.
			CANCELLED: the trade has been cancelled by one of the parties.
			SUCCESS:   the trade finished successfully."""
	def __init__(self, client: 'aiotfm.Client', trader: Union[Player, str]):
		self.client: aiotfm.Client = client
		self.trader: str = trader
		self.locked: List[bool] = [False, False] # 0: trader, 1: client

		self.imports: TradeContainer = TradeContainer(self)
		self.exports: TradeContainer = TradeContainer(self)

		self.state: TradeState = TradeState.ON_INVITE
		self.pid: int = -1

		if isinstance(trader, str):
			trader = client.room.get_player(name=trader)
			if trader is None:
				TypeError(f"Can not find the player '{self.trader}' in the room.")

		if isinstance(trader, Player):
			if self.trader.isGuest:
				raise TypeError("You can not trade with a guest.")
			if self.trader == self.client.username:
				raise TypeError("You can not trade with yourself.")
			if self.trader.pid == 0:
				raise TypeError("You can not trade with a player having the same IP.")
			self.trader = self.trader.username
			self.pid = trader.pid
		else:
			raise TypeError(f"Trade expected 'Player' or 'str' type, got '{type(trader)}")

	def __repr__(self):
		return "<Trade state={} locked=[trader:{}, client:{}] trader={} pid={}>".format(
			self.state.name, *self.locked, self.trader, self.pid)

	def __eq__(self, other: object):
		if isinstance(other, Trade):
			if self.pid == -1 or other.pid == -1:
				return self.trader.lower() == other.trader.lower()
			return self.pid == other.pid
		return NotImplemented

	@property
	def closed(self) -> bool:
		"""Returns True if the trade is closed."""
		return self.state in (TradeState.SUCCESS, TradeState.CANCELLED)

	def _start(self):
		"""Set the state of the trade as TRADING."""
		self.state = TradeState.TRADING

	def _close(self, succeed: bool = False):
		"""Closes the trade."""
		self.state = TradeState.SUCCESS if succeed else TradeState.CANCELLED
		if self.client.trade == self:
			self.client.trade = None

		# :desc: Called when a trade is closed.
		# :param trade: :class:`aiotfm.inventory.Trade` the trade object.
		# :param succed: :class:`bool` whether or not the trade is successful.
		self.client.trades.pop(self.pid, None)
		self.client.dispatch('trade_close', self, succeed)

	async def cancel(self):
		"""|coro|
		Cancels the trade."""
		if self.state != TradeState.TRADING:
			raise TradeOnWrongState('cancel', self.state)

		await self.client.main.send(Packet.new(31, 6).writeString(self.trader).write8(2))

	async def accept(self):
		"""|coro|
		Accepts the trade."""
		if self.state != TradeState.ON_INVITE:
			raise TradeOnWrongState('accept', self.state)

		self.state = TradeState.ACCEPTING
		await self.client.main.send(Packet.new(31, 5).writeString(self.trader))

	async def addItem(self, item_id: int, quantity: int):
		"""|coro|
		Adds an item to the trade.

		:param item_id: :class:`int` The item id.
		:param quantity: :class:`int` The quantity of item to add."""
		if self.state != TradeState.TRADING:
			raise TradeOnWrongState('addItem', self.state)

		quantity = min(max(quantity, 0), 200)
		packet = Packet.new(31, 8).write16(item_id).writeBool(True).buffer

		ten = packet + b'\x01'
		for i in range(quantity // 10):
			await self.client.main.send(Packet(ten))
			await asyncio.sleep(.05)

		unit = packet + b'\x00'
		for i in range(quantity % 10):
			await self.client.main.send(Packet(unit))
			await asyncio.sleep(.05)

	async def removeItem(self, item_id: int, quantity: int):
		"""|coro|
		Removes an item from the trade.

		:param item_id: :class:`int` The item id.
		:param quantity: :class:`int` The quantity of item to remove."""
		if self.state != TradeState.TRADING:
			raise TradeOnWrongState('removeItem', self.state)

		quantity = min(max(quantity, 0), 200)
		packet = Packet.new(31, 8).write16(item_id).writeBool(False).buffer

		ten = packet + b'\x01'
		for i in range(quantity // 10):
			await self.client.main.send(Packet(ten))
			await asyncio.sleep(.05)

		unit = packet + b'\x00'
		for i in range(quantity % 10):
			await self.client.main.send(Packet(unit))
			await asyncio.sleep(.05)

	async def lock(self):
		"""|coro|
		Locks (confirms) the trade."""
		if self.state != TradeState.TRADING:
			raise TradeOnWrongState('lock', self.state)
		if self.locked[1]:
			raise TypeError("Can not lock a trade that is already locked by the client.")

		await self.client.main.send(Packet.new(31, 9).writeBool(True))

	async def unlock(self):
		"""|coro|
		Unlocks (cancels the confirmation) the trade."""
		if self.state != TradeState.TRADING:
			raise TradeOnWrongState('lock', self.state)
		if not self.locked[1]:
			raise TypeError("Can not unlock a trade that is not locked by the client.")

		await self.client.main.send(Packet.new(31, 9).writeBool(False))
