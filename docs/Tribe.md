# Tribe

Represent a tribe.

## Attributes

id `int` the tribe's id.
name `str` the tribe's name.
welcomeMessage `str` the tribe's welcome message.
mapcode `int` the tribehouse's mapcode.
members `list` the list of the [members](#member) in the tribe.
ranks `list` the list of the [ranks](#rank) in the tribe.

# Member

Represent a tribe's member.

## Attributes

tribe [`Tribe`](#tribe) the member's tribe.
id `int` the player's id of the member.
name `str` the username of the member.
gender `int` the member's gender.
lastConnection :class`Date` the last connection of the member.
rank_id `int` the rank's id of the member.
game_id `int` the game's id the player is playing.
room `str` the room where the player is.
rank [`Rank`](#rank) the member's rank.
online `bool` return True if the member is online.

# Rank

Represent a [tribe](#tribe)'s rank.

## Attributes

id `int` the rank's id.
name `str` the rank's name.
perm `int` the rank's permissions.

## Permissions

isLeader `bool`
canChangeGreetingMessage `bool`
canEditRanks `bool`
canChangeMembersRanks `bool`
canInvite `bool`
canExclude `bool`
canPlayMusic `bool`
canChangeTribeHouseMap `bool`
canLoadMap `bool`
canLoadLua `bool`
canManageForum `bool`