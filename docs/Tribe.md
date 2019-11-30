# Tribe Documentation

## Tribe 
>**This section represents the tribe.** 
>
>**Attributes:**
>
>| Attribute | Type | Description 
>| :-: | :-: | :--
>| **id** | `integer` | The tribe's id
>| **name** | `string`| The tribe name.
>| **welcomeMessage** | `string` | the tribe's greeting message.
>| **mapcode** | `integer` | the tribehouse's mapcode.
>| **members** | `list` | The list of the [members](#member) in the tribe.
>| **ranks** | `list` | The list of the [ranks](#rank) in the tribe.

---

## Member
>**This section represents the tribe member(s).**
>
>**Attributes:**
>
>| Attribute | Type | Description 
>| :-: | :-: | :--
>| **tribe** | [`Tribe`](#tribe) | The member's tribe.
>| **id** | `integer` | The player's unique id.
>| **name** | `string` | Player name.
>| **gender** | `integer` | Player's gender.
>| **lastConnection** | `Date` | The date the player was last seen.
>| **rank_id** | `integer` | The id of the member's rank.
>| **game_id** | `integer` | The game id the player is (currently) playing (if online).
>| **room** | `string` | The room where the player currently is (if online).
>| **rank** | [`Rank`](#rank) | The member's rank.
>| **online** | `boolean`| Returns `True` if the player is currently online.

## Rank
>**This section represents the ranks in the [tribe](#tribe).**
>
> **Attributes:**
>
>| Attribute | Type | Description 
>| :-: | :-: | :--
>| **id** | `integer` | The rank id.
>| **name** | `string` | The rank name.
>| **perm** | `int` | The rank permissions.
>
>**Permissions:**
>
>|Permission|Type
>|:-:|:-:
>|**isLeader** | `boolean`
>|**canChangeGreetingMessage** | `boolean`
>|**canEditRanks** | `boolean`
>|**canChangeMembersRanks** | `boolean`
>|**canInvite** | `boolean`
>|**canExclude** | `boolean`
>|**canPlayMusic** | `boolean`
>|**canChangeTribeHouseMap** | `boolean`
>|**canLoadMap** | `boolean`
>|**canLoadLua** | `boolean`
>**canManageForum**| `boolean`
