# Profile Documentation

## Profile
>**This represents a player's profile.**
>
>**Attributes:**
>
>|Attribute|Type|Description
>|:-:|:-:|:--
>|**username**| `string` | The player's username.
>|**id** | `integer` | The player's id.
>|**registration_date**| `integer`| The registration timestamp of the player.
>|**privLevel**| `integer`| The privilege level of the player.
>|**gender**| `integer`| The player's gender.
>|**tribe**| `string` | The player's tribe. Can be `None`.
>|**soulmate**| `string`| Name of the player's soulmate. Can be `None`.
>|**title**| `integer` | Player's current title.
>|**titles**| `set` | The list of the unlocked titles.
>|**titles_stars**| `dict` | A dictionary where the number of stars the player's title has is stored.
>|**look**| `string` | The player's look.
>|**level** | `integer` | The player's shaman level.
>|**badges** | `dict` | All the badges unlocked by the player with their numbers.
>|**stats** | [`stats`](#stats) | The player's staistics.
>|**equippedOrb** | `integer` | The orb currently equipped by the player.
>|**orbs** | `set` | The list of orbs the player currently has.
>|**adventurePoints** | `integer` | Player's adventure points.

---

##Stats
>**Represents the statistics of a player.**
>
>**Attributes:**
>
>|Attribute|Type|Description
>|:-:|:-:|:--
>|**normalModeSaves**|`integer`| Number of saves in normal mode.
>|**hardModeSaves** | `integer` |  Number of  saves in hard mode.
>|**divineModeSaves** | `integer`| Number of  saves in divine mode.
>|**shamanCheeses**| `integer`| Number of cheese gathered as a shaman.
>|**firsts** | `integer` | Number of cheese gathered first.
>|**gatheredCheeses**| `integer` | Total amount of gathered cheese.
>|**bootcamps**| `integer` | Number of bootcamp maps completed.
>|**modeStats**| `list` | A list of tuples that represents the statistics in a different mode. (id, progress, progressLimit, imageId)
