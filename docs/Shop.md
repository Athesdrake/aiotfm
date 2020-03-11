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
>
---

Shop.**cost**(_self, outfit_) <a id="Shop.cost" href="#Shop.cost">¶</a>
>
>
>
>__Parameters:__
> * **outfit** - [`Outfit`](Shop.md#Outfit)

---

Shop.**getItem**(_self, item_) <a id="Shop.getItem" href="#Shop.getItem">¶</a>
>
>
>
>__Parameters:__
> * **item** - [`Item`](Shop.md#Item) the item you want to price of.

---

Shop.**category**(_self, id__) <a id="Shop.category" href="#Shop.category">¶</a>
>
>
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
Item.**from\_packet**(_cls, packet_) <a id="Item.from_packet" href="#Item.from_packet">¶</a>
>
>
>
>__Parameters:__
> * **packet** - [`Packet`](Packet.md)

---

Item.**parse**(_cls, cat, string_) <a id="Item.parse" href="#Item.parse">¶</a>
>
>
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
>
---

ShopItem.**from\_packet**(_cls, packet_) <a id="ShopItem.from_packet" href="#ShopItem.from_packet">¶</a>
>
>
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
Outfit.**from\_fashion**(_cls, packet_) <a id="Outfit.from_fashion" href="#Outfit.from_fashion">¶</a>
>
>
>
>__Parameters:__
> * **packet** - [`Packet`](Packet.md)

---

Outfit.**from\_packet**(_cls, packet, id__) <a id="Outfit.from_packet" href="#Outfit.from_packet">¶</a>
>
>
>
>__Parameters:__
> * **packet** - [`Packet`](Packet.md)

---

Outfit.**fur**(_self_) <a id="Outfit.fur" href="#Outfit.fur">¶</a>
>
>
---

Outfit.**items**(_self_) <a id="Outfit.items" href="#Outfit.items">¶</a>
>
>
---

Outfit.**head**(_self_) <a id="Outfit.head" href="#Outfit.head">¶</a>
>
>
---

Outfit.**eyes**(_self_) <a id="Outfit.eyes" href="#Outfit.eyes">¶</a>
>
>
---

Outfit.**ears**(_self_) <a id="Outfit.ears" href="#Outfit.ears">¶</a>
>
>
---

Outfit.**mouth**(_self_) <a id="Outfit.mouth" href="#Outfit.mouth">¶</a>
>
>
---

Outfit.**neck**(_self_) <a id="Outfit.neck" href="#Outfit.neck">¶</a>
>
>
---

Outfit.**hair**(_self_) <a id="Outfit.hair" href="#Outfit.hair">¶</a>
>
>
---

Outfit.**tail**(_self_) <a id="Outfit.tail" href="#Outfit.tail">¶</a>
>
>
---

Outfit.**lenses**(_self_) <a id="Outfit.lenses" href="#Outfit.lenses">¶</a>
>
>
---

Outfit.**hands**(_self_) <a id="Outfit.hands" href="#Outfit.hands">¶</a>
>
>
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

ShamanObject.**from\_packet**(_cls, packet_) <a id="ShamanObject.from_packet" href="#ShamanObject.from_packet">¶</a>
>
>
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

OwnedShamanObject.**from\_packet**(_cls, packet_) <a id="OwnedShamanObject.from_packet" href="#OwnedShamanObject.from_packet">¶</a>
>
>
>
>__Parameters:__
> * **packet** - [`Packet`](Packet.md)

---

