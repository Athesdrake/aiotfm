from aiotfm.enums import TradeState


class AiotfmException(Exception):
	"""Base exception class for aiotfm"""


class LoginError(AiotfmException):
	"""Exception thrown when the login failed."""
	def __init__(self, code: int):
		self.code = code
		super().__init__('Login Failed ! Error code: {.code}.'.format(self))


class AlreadyConnected(LoginError):
	"""Exception thrown when the account provided is already connected."""
	def __init__(self):
		super().__init__(1)


class IncorrectPassword(LoginError):
	"""Exception thrown when trying to connect with a wrong password."""
	def __init__(self):
		super().__init__(2)


class InvalidEvent(AiotfmException):
	"""Exception thrown when you added an invalid event to the client.

	An event is valid only if its name begin by 'on_' and it is coroutine.
	"""


class ServerUnreachable(AiotfmException):
	"""Exception thrown when the Client can't connect to the server."""


class ConnectionClosed(AiotfmException):
	"""Exception thrown when one of the connection closes."""


class InvalidSocketData(AiotfmException):
	"""Exception thrown when a socket receive an invalid data."""


class EndpointError(AiotfmException):
	"""Exception thrown when the endpoint sends an abnormal response."""


class InternalError(EndpointError):
	"""Exception thrown when the endpoint got an internal error."""


class MaintenanceError(EndpointError):
	"""Exception thrown when the endpoint thinks there is a maintenance."""


class InvalidLocale(AiotfmException):
	"""Exception thrown when you try to load an inexistent locale."""


class PacketError(AiotfmException):
	"""Exception thrown when a packet encounter a problem."""


class PacketTooLarge(PacketError):
	"""Exception thrown when a packet is too large to be exported."""


class XXTEAError(PacketError):
	"""Exception thrown when the XXTEA algorithm failed."""


class XXTEAInvalidPacket(XXTEAError):
	"""Exception thrown when you try to cipher an empty Packet."""


class XXTEAInvalidKeys(XXTEAError):
	"""Exception thrown when you try to cipher a packet with an invalid key."""


class CommunityPlatformError(AiotfmException):
	"""Exception thrown when the community platform send an error code."""
	def __init__(self, category: int, code: int):
		super().__init__('Internal error: {}-{}'.format(category, code))
		self.category = category
		self.code = code


class TradeOnWrongState(AiotfmException):
	"""Exception thrown when the client try an impossible action on trade due to its state."""
	def __init__(self, action: str, state: TradeState):
		super().__init__(f'Can not {action} when the trade is {state}.')
		self.action: str = action
		self.state: TradeState = state


class InvalidAccountError(AiotfmException):
	"""Exception thrown when a server action does not find a user."""
	def __init__(self, player: str):
		super().__init__(f'The account {player} does not exist.')
		self.player: str = player


class FriendLimitError(AiotfmException):
	"""Exception thrown when your friend list is full."""
	def __init__(self):
		super().__init__('You can\'t add more friends.')


class CantFriendPlayerError(AiotfmException):
	"""Exception thrown when the server does not let you friend a player."""
	def __init__(self, player: str):
		super().__init__(f'You can\'t friend the player {player}')
		self.player: str = player
