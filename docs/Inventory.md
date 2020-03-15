# Inventory's Documentation

## InventoryItem
**Represents an inventory item.**

| Attributes | Type | Can be None | Description |
| :-: | :-: | :-: | :-- |
| id | `int` | ✕ |  The item id. |
| quantity | `int` | ✕ |  The quantity of the item. |
| inventory | `Optional[` | ✕ |  The inventory class. Might be None. |
| can_use | `bool` | ✕ |  True if you can use this item. |
| category | `int` | ✕ |  Define the category's item. Used by the sorting algorithm. |
| img_id | `str` | ✕ |  Id used to get the item's image. |
| is_event | `bool` | ✕ |  True if it's an item from an event. |
| slot | `int` | ✕ |  Define the equipped slot with this item. If slot is 0 then the item is not equipped. |


### Methods
@*property*<br>
InventoryItem.**image\_url**(_self_) <a id="InventoryItem.image_url" href="#InventoryItem.image_url">¶</a>
>
>The image's url of the item.
---

@*property*<br>
InventoryItem.**is\_currency**(_self_) <a id="InventoryItem.is_currency" href="#InventoryItem.is_currency">¶</a>
>
>Return True if the item is a currency.
---

@*property*<br>
InventoryItem.**is\_equipped**(_self_) <a id="InventoryItem.is_equipped" href="#InventoryItem.is_equipped">¶</a>
>
>Return True if the item is equipped
---

@*classmethod*<br>
InventoryItem.**from\_packet**(_cls, packet_) <a id="InventoryItem.from_packet" href="#InventoryItem.from_packet">¶</a>
>
>Read an item from a packet.
>:param packet: :class:`aiotfm.Packet` the packet.
>:return: :class:`aiotfm.inventory.InventoryItem` the item.
---

_coroutine_ InventoryItem.**use**(_self_) <a id="InventoryItem.use" href="#InventoryItem.use">¶</a>
>
>Uses this item.
---

## Inventory
**Represents the client's inventory.**

| Attributes | Type | Can be None | Description |
| :-: | :-: | :-: | :-- |
| items | `dict` | ✕ |  A dict containing all the items. The key is an `int` and the value is an [`InventoryItem`](Inventory.md#InventoryItem). |
| client | `Client` | ✕ |  The client that this inventory belongs to. |


### Methods
@*classmethod*<br>
Inventory.**from\_packet**(_cls, packet_) <a id="Inventory.from_packet" href="#Inventory.from_packet">¶</a>
>
>Read the inventory from a packet.
>:param packet: :class:`aiotfm.Packet` the packet.
>:return: :class:`aiotfm.inventory.Inventory` the inventory.
---

Inventory.**get**(_self, item_id_) <a id="Inventory.get" href="#Inventory.get">¶</a>
>
>Gets an item from this :class:`aiotfm.inventory.Inventory`.
>Shorthand for :class:`aiotfm.inventory.Inventory`.items.get
---

Inventory.**sort**(_self_) <a id="Inventory.sort" href="#Inventory.sort">¶</a>
>
>Sort the inventory the same way the client does.
>:return: :class:`list`
---

## TradeContainer
**Represents the content of a Trade.**


### Methods
TradeContainer.**get**(_self, item_id, default_) <a id="TradeContainer.get" href="#TradeContainer.get">¶</a>
>
>Returns the quantity of an item inside the TradeContainer.
>:param item_id: :class:`int` the item's id.
>:param default: Optional[:class:`int`] the default value if the item is not present.
>:return: :class:`int` the quantity of the item.
---

TradeContainer.**getSlot**(_self, index_) <a id="TradeContainer.getSlot" href="#TradeContainer.getSlot">¶</a>
>
>Returns the item inside a certain slot.
>:param index: :class:`int` the index.
>:return: :class:`aiotfm.inventory.InventoryItem` the item.
---

TradeContainer.**add**(_self, item_id, quantity_) <a id="TradeContainer.add" href="#TradeContainer.add">¶</a>
>
>Add a quantity of an item inside the container.
>:param item_id: :class:`int` the item's id.
>:param quantity: :class:`int` the quantity to add. Can be negative.
---

## Trade
**Represents a trade that the client is participating (not started, in progress or ended).**

| Attributes | Type | Can be None | Description |
| :-: | :-: | :-: | :-- |
| client | [`Client`](Client.md) | ✕ |  The reference to the client involved in the trade. |
| trader | `str` | ✕ |  The player the client is trading with. |
| locked | `List[` | ✕ |  A list of two `bool` describing the locked state of each party. |
| imports | [`TradeContainer`](Inventory.md) | ✕ |  The container of the items you will receive if the trade succeed. |
| exports | [`TradeContainer`](Inventory.md) | ✕ |  The container of the items you will give if the trade succeed. |
| state | [`TradeState`](Utils.md) | ✕ |  The current state of the trade. ON_INVITE: an invitation has been received from/sent to the other party. ACCEPTING: the client accepted and is waiting for the other party to be ready. TRADING: the only state of the trade where you are able to add items. CANCELLED: the trade has been cancelled by one of the parties. SUCCESS: the trade finished successfully. |


### Methods
@*property*<br>
Trade.**closed**(_self_) <a id="Trade.closed" href="#Trade.closed">¶</a>
>
>Returns True if the trade is closed.
---

Trade.**\_start**(_self_) <a id="Trade._start" href="#Trade._start">¶</a>
>
>Set the state of the trade as TRADING.
---

Trade.**\_close**(_self, succeed_) <a id="Trade._close" href="#Trade._close">¶</a>
>
>Closes the trade.
---

_coroutine_ Trade.**cancel**(_self_) <a id="Trade.cancel" href="#Trade.cancel">¶</a>
>
>Cancels the trade.
---

_coroutine_ Trade.**accept**(_self_) <a id="Trade.accept" href="#Trade.accept">¶</a>
>
>Accepts the trade.
---

_coroutine_ Trade.**addItem**(_self, item_id, quantity_) <a id="Trade.addItem" href="#Trade.addItem">¶</a>
>
>Adds an item to the trade.
>
>__Parameters:__
> * **item_id** - `int` The item id.
> * **quantity** - `int` The quantity of item to add.

---

_coroutine_ Trade.**removeItem**(_self, item_id, quantity_) <a id="Trade.removeItem" href="#Trade.removeItem">¶</a>
>
>Removes an item from the trade.
>
>__Parameters:__
> * **item_id** - `int` The item id.
> * **quantity** - `int` The quantity of item to remove.

---

_coroutine_ Trade.**lock**(_self_) <a id="Trade.lock" href="#Trade.lock">¶</a>
>
>Locks (confirms) the trade.
---

_coroutine_ Trade.**unlock**(_self_) <a id="Trade.unlock" href="#Trade.unlock">¶</a>
>
>Unlocks (cancels the confirmation) the trade.
---

