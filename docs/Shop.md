# Shop's Documentation

## Shop
**Represents the shop in game.**

| Parameters | Type | Required | Description |
| :-: | :-: | :-: | :-- |
| packet | [`Packet`](Packet.md) | ✔ |  The packet where the shop content cill be read. |

| Attributes | Type | Can be None | Description |
| :-: | :-: | :-: | :-- |
| cheese | `int` | ✕ |  The number of cheese the client has. |
| fraise | `int` | ✕ |  The numberof fraise (strawberries) the client has. |
| look | `str` | ✕ |  The client's look. |
| owned_items | `set` | ✕ |  All items the client own. |
| items | `set` | ✕ |  All items present in the shop. |
| full_outfits | `set` | ✕ |  Available fashion outfits you can buy. |
| outfits | `set` | ✕ |  The client own outfits. |
| owned_shaman_objects | `set` | ✕ |  All shaman object the client own. |
| shaman_objects | `set` | ✕ |  All shaman object available in the shop. |


### Methods
Shop.**to\_dict**(_self_) <a id="Shop.to_dict" href="#Shop.to_dict">¶</a>
>
>Export the shop into a serializable dict.
---

Shop.**cost**(_self, outfit_) <a id="Shop.cost" href="#Shop.cost">¶</a>
>
>Compute and return the total price of an outfit.
>
>__Parameters:__
> * **outfit** - [`Outfit`](Shop.md#Outfit)

---

Shop.**getItem**(_self, item_) <a id="Shop.getItem" href="#Shop.getItem">¶</a>
>
>Return the shop item with the same id.
>
>__Parameters:__
> * **item** - [`Item`](Shop.md#Item) the item you want to price of.

---

Shop.**category**(_self, id__) <a id="Shop.category" href="#Shop.category">¶</a>
>
>Return the items from a category.
>
>__Parameters:__
> * **id_** - `int` the category's id?

---

## Item
**Represents an item from the shop.**

| Parameters | Type | Required | Description |
| :-: | :-: | :-: | :-- |
| category | `int` | ✔ |  The item's category. |
| id_ | `int` | ✔ |  The item's id. |
| colors | `int` | ✕ |  The item's colors. |

| Attributes | Type | Can be None | Description |
| :-: | :-: | :-: | :-- |
| category | `int` | ✕ |  The item's category. |
| id | `int` | ✕ |  The item's id. |
| uid | `int` | ✕ |  The item's unique id. |
| colors | `int` | ✕ |  The item's colors. |


### Methods
@*classmethod*<br>
Item.**from\_packet**(_cls, packet_) <a id="Item.from_packet" href="#Item.from_packet">¶</a>
>
>Reads an Item from a packet.
>
>__Parameters:__
> * **packet** - [`Packet`](Packet.md)

---

@*classmethod*<br>
Item.**parse**(_cls, cat, string_) <a id="Item.parse" href="#Item.parse">¶</a>
>
>Parse an Item from a string.
>
>__Parameters:__
> * **cat** - `int` the item's category.
> * **string** - `str` the item.

---

## ShopItem
**Represents an item from the shop with its specifications.**

| Parameters | Type | Required | Description |
| :-: | :-: | :-: | :-- |
| category | `int` | ✔ |  The item's category. |
| id_ | `int` | ✔ |  The item's id. |
| colors | `int` | ✔ |  The item's colors. |
| is_new | `bool` | ✔ |  True if it's a new item. |
| flag | `int` | ✔ |  Contains the item's metadata. |
| cheese | `int` | ✔ |  The item's price in cheese. |
| fraise | `int` | ✔ |  The item's price in fraise. |
| special | `int` | ✔ |  The item's special data. |

| Attributes | Type | Can be None | Description |
| :-: | :-: | :-: | :-- |
| category | `int` | ✕ |  The item's category. |
| id | `int` | ✕ |  The item's id. |
| uid | `int` | ✕ |  The item's unique id. |
| colors | `int` | ✕ |  The item's colors. |
| nbr_colors | `int` | ✕ |  The number of customizable colors the item has. |
| is_new | `bool` | ✕ |  True if it's a new item. |
| flag | `int` | ✕ |  Contains the item's metadata. |
| cheese | `int` | ✕ |  The item's price in cheese. |
| fraise | `int` | ✕ |  The item's price in fraise. |
| special | `int` | ✕ |  The item's special data. |


### Methods
ShopItem.**to\_dict**(_self_) <a id="ShopItem.to_dict" href="#ShopItem.to_dict">¶</a>
>
>Export the item into a serializable dict.
---

@*classmethod*<br>
ShopItem.**from\_packet**(_cls, packet_) <a id="ShopItem.from_packet" href="#ShopItem.from_packet">¶</a>
>
>Reads a ShopItem from a packet.
>
>__Parameters:__
> * **packet** - [`Packet`](Packet.md)

---

## Outfit
**Represents an outfit from the shop.**

| Parameters | Type | Required | Description |
| :-: | :-: | :-: | :-- |
| look | `str` | ✔ |  The outfit's look. |
| id_ | `int` | ✕ |  The outfit's id. |
| flag | `int` | ✔ |  Contains the outfit's metadata. |

| Attributes | Type | Can be None | Description |
| :-: | :-: | :-: | :-- |
| look | `str` | ✕ |  The outfit's look. |
| id | `int` | ✕ |  The outfit's id. |
| flag | `int` | ✕ |  Contains the outfit's metadata. |


### Methods
@*classmethod*<br>
Outfit.**from\_fashion**(_cls, packet_) <a id="Outfit.from_fashion" href="#Outfit.from_fashion">¶</a>
>
>Reads a fashion Outfit from a packet.
>
>__Parameters:__
> * **packet** - [`Packet`](Packet.md)

---

@*classmethod*<br>
Outfit.**from\_packet**(_cls, packet, id__) <a id="Outfit.from_packet" href="#Outfit.from_packet">¶</a>
>
>Reads an Outfit from a packet.
>
>__Parameters:__
> * **packet** - [`Packet`](Packet.md)

---

@*property*<br>
Outfit.**fur**(_self_) <a id="Outfit.fur" href="#Outfit.fur">¶</a>
>
>The fur's id of the outfit.
---

@*property*<br>
Outfit.**items**(_self_) <a id="Outfit.items" href="#Outfit.items">¶</a>
>
>The outfit's items.
---

@*property*<br>
Outfit.**head**(_self_) <a id="Outfit.head" href="#Outfit.head">¶</a>
>
>The outfit's head item.
---

@*property*<br>
Outfit.**eyes**(_self_) <a id="Outfit.eyes" href="#Outfit.eyes">¶</a>
>
>The outfit's eyes item.
---

@*property*<br>
Outfit.**ears**(_self_) <a id="Outfit.ears" href="#Outfit.ears">¶</a>
>
>The outfit's ears item.
---

@*property*<br>
Outfit.**mouth**(_self_) <a id="Outfit.mouth" href="#Outfit.mouth">¶</a>
>
>The outfit's mouth item.
---

@*property*<br>
Outfit.**neck**(_self_) <a id="Outfit.neck" href="#Outfit.neck">¶</a>
>
>The outfit's neck item.
---

@*property*<br>
Outfit.**hair**(_self_) <a id="Outfit.hair" href="#Outfit.hair">¶</a>
>
>The outfit's hair item.
---

@*property*<br>
Outfit.**tail**(_self_) <a id="Outfit.tail" href="#Outfit.tail">¶</a>
>
>The outfit's tail item.
---

@*property*<br>
Outfit.**lenses**(_self_) <a id="Outfit.lenses" href="#Outfit.lenses">¶</a>
>
>The outfit's lenses item.
---

@*property*<br>
Outfit.**hands**(_self_) <a id="Outfit.hands" href="#Outfit.hands">¶</a>
>
>The outfit's hands item.
---

## ShamanObject
**Represents shaman object from the shop.**

| Parameters | Type | Required | Description |
| :-: | :-: | :-: | :-- |
| id_ | `int` | ✔ |  The object's id. |
| colors | `int` | ✔ |  The number of customizable colors the object has. |
| is_new | `bool` | ✔ |  The object's metadata. |
| flag | `int` | ✔ |  Contains the object's metadata. |
| cheese | `int` | ✔ |  The obect's pricein cheese. |
| fraise | `int` | ✔ |  The obect's pricein fraise. |

| Attributes | Type | Can be None | Description |
| :-: | :-: | :-: | :-- |
| id | `int` | ✕ |  The object's id. |
| colors | `int` | ✕ |  The number of customizable colors the object has. |
| is_new | `bool` | ✕ |  The object's metadata. |
| flag | `int` | ✕ |  Contains the object's metadata. |
| cheese | `int` | ✕ |  The obect's pricein cheese. |
| fraise | `int` | ✕ |  The obect's pricein fraise. |

@*classmethod*<br>
ShamanObject.**from\_packet**(_cls, packet_) <a id="ShamanObject.from_packet" href="#ShamanObject.from_packet">¶</a>
>
>Reads a ShamanObject from a packet.
>
>__Parameters:__
> * **packet** - [`Packet`](Packet.md)

---

## OwnedShamanObject
**Represents shaman object that the client own.**

| Parameters | Type | Required | Description |
| :-: | :-: | :-: | :-- |
| id_ | `int` | ✔ |  The object's id. |
| equiped | `bool` | ✔ |  True if the client has the object equiped. |
| colors | `list` | ✔ |  The custom colors the object has. |

| Attributes | Type | Can be None | Description |
| :-: | :-: | :-: | :-- |
| id | `int` | ✕ |  The object's id. |
| equiped | `bool` | ✕ |  True if the client has the object equiped. |
| colors | `list` | ✕ |  The custom colors the object has. |

@*classmethod*<br>
OwnedShamanObject.**from\_packet**(_cls, packet_) <a id="OwnedShamanObject.from_packet" href="#OwnedShamanObject.from_packet">¶</a>
>
>Reads a OwnedShamanObject from a packet.
>
>__Parameters:__
> * **packet** - [`Packet`](Packet.md)

---

