# Profile

Represents a player's profile.

## Attributes

username `str` the player's username.
id `int` the player's id.
registration_date `int` the registration timestamp of the player.
privLevel `int` the privilege level of the player.
gender `int` player's gender.
tribe `str` player's tribe. Can be `None`.
soulmate `str` player's soulmate. Can be `None`.
title `int` the title above the player's head.
titles `set` the list of the unlocked titles.
titles_stars `dict` a dictionary where are stored the number of stars a title has.
look `str` the player's look.
level `int` the player's shaman level.
badges `dict` all badges unlocked by the player and their number.
stats [`Stats`](#stats) the player's stats.
equippedOrb `int` the equipped orb of the player.
orbs `set` the list of unlocked orbs.
adventurePoints `int` number of adventure points the player has.

# Stats

Represents the statistics of a player.

## Attributes

normalModeSaves `int` number of shaman saves in normal mode.
hardModeSaves `int`  number of shaman saves in hard mode.
divineModeSaves `int` number of shaman saves in divine mode.
shamanCheeses `int` number of cheese personally gathered.
firsts `int` number of cheese gathered first.
gatheredCheeses `int` total number of gathered cheeses.
bootcamps `int` number of bootcamp.
modeStats `list` a list of tuples that represents the stats in different mode. (id, progress, progressLimit, imageId)