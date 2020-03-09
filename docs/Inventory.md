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
InventoryItem.**image\_url**(_self_) <a id="InventoryItem.image_url" href="#InventoryItem.image_url">¶</a>
>
>
---

InventoryItem.**is\_currency**(_self_) <a id="InventoryItem.is_currency" href="#InventoryItem.is_currency">¶</a>
>
>
---

InventoryItem.**is\_equipped**(_self_) <a id="InventoryItem.is_equipped" href="#InventoryItem.is_equipped">¶</a>
>
>
---

InventoryItem.**from\_packet**(_cls, packet_) <a id="InventoryItem.from_packet" href="#InventoryItem.from_packet">¶</a>
>
>
>
>__Parameters:__
> * **packet** - [`Packet`](Packet.md) the packet.

---

_coroutine_ InventoryItem.**use**(_self_) <a id="InventoryItem.use" href="#InventoryItem.use">¶</a>
>
>
---

## Inventory
**Represents the client's inventory.**

| Attributes | Type | Can be None | Description |
| :-: | :-: | :-: | :-- |
| items | `dict` | ✕ |  A dict containing all the items. The key is an `int` and the value is an [`InventoryItem`](Inventory.md). |
| client | `Client` | ✕ |  The client that this inventory belongs to. |


### Methods
Inventory.**from\_packet**(_cls, packet_) <a id="Inventory.from_packet" href="#Inventory.from_packet">¶</a>
>
>
>
>__Parameters:__
> * **packet** - [`Packet`](Packet.md) the packet.

---

Inventory.**get**(_self, item_id_) <a id="Inventory.get" href="#Inventory.get">¶</a>
>
>
---

Inventory.**sort**(_self_) <a id="Inventory.sort" href="#Inventory.sort">¶</a>
>
>
---

## TradeContainer
**Represents the content of a Trade.**


### Methods
TradeContainer.**get**(_self, item_id, default_) <a id="TradeContainer.get" href="#TradeContainer.get">¶</a>
>
>
>
>__Parameters:__
> * **item_id** - `int` the item's id.
> * **default** - Optional[`int`] the default value if the item is not present.

---

TradeContainer.**getSlot**(_self, index_) <a id="TradeContainer.getSlot" href="#TradeContainer.getSlot">¶</a>
>
>
>
>__Parameters:__
> * **index** - `int` the index.

---

TradeContainer.**add**(_self, item_id, quantity_) <a id="TradeContainer.add" href="#TradeContainer.add">¶</a>
>
>
>
>__Parameters:__
> * **item_id** - `int` the item's id.
> * **quantity** - `int` the quantity to add. Can be negative.

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
Trade.**closed**(_self_) <a id="Trade.closed" href="#Trade.closed">¶</a>
>
>
---

Trade.**\_start**(_self_) <a id="Trade._start" href="#Trade._start">¶</a>
>
>
---

Trade.**\_close**(_self, succeed_) <a id="Trade._close" href="#Trade._close">¶</a>
>
>
---

_coroutine_ Trade.**cancel**(_self_) <a id="Trade.cancel" href="#Trade.cancel">¶</a>
>
>
---

_coroutine_ Trade.**accept**(_self_) <a id="Trade.accept" href="#Trade.accept">¶</a>
>
>
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
>
---

_coroutine_ Trade.**unlock**(_self_) <a id="Trade.unlock" href="#Trade.unlock">¶</a>
>
>
---

