class AiotfmException(Exception):
	"""Base exception class for aiotfm"""


class LoginError(AiotfmException):
	"""Exception thrown when the login failed."""
	def __init__(self, code):
		self.code = code
		super().__init__('Login Failed ! Error code: {.code}.'.format(self))

class AlreadyConnected(LoginError):
	"""Exception thrown when the account provided is already connected."""
	pass

class IncorrectPassword(LoginError):
	"""Exception thrown when trying to connect with a wrong password."""
	pass


class InvalidEvent(AiotfmException):
	"""Exception thrown when you added an invalid event to the client.

	En event is valid only if its name begin by 'on_' and it is coroutine.
	"""
	pass


class ConnectionError(AiotfmException):
	"""Exception thrown when the Client can't connect to the server."""
	pass


class ConnectionClosed(AiotfmException):
	"""Exception thrown when one of the connection closes."""
	pass

class EndOfFile(ConnectionClosed):
	"""Exception thrown when a socket receive the End Of File signal."""
	pass


class InvalidSocketData(AiotfmException):
	"""Exception thrown when a socket receive an invalid data."""
	pass


class EndpointError(AiotfmException):
	"""Exception thrown when the endpoint sends an abnormal response."""
	pass

class InternalError(EndpointError):
	"""Exception thrown when the endpoint got an internal error."""
	pass

class MaintenanceError(EndpointError):
	"""Exception thrown when the endpoint thinks there is a maintenance."""
	pass


class InvalidLocale(AiotfmException):
	"""Exception thrown when you try to load an inexistent locale."""
	pass


class PacketError(AiotfmException):
	"""Exception thrown when a packet encounter a problem."""
	pass

class PacketTooLarge(PacketError):
	"""Exception thrown when a packet is too large to be exported."""
	pass

class XXTEAError(PacketError):
	"""Exception thrown when the XXTEA algorithm failed."""
	pass

class XXTEAInvalidPacket(XXTEAError):
	"""Exception thrown when you try to cipher an empty Packet."""
	pass

class XXTEAInvalidKeys(XXTEAError):
	"""Exception thrown when you try to cipher a packet with an invalid key."""
	pass


class CommunityPlatformError(AiotfmException):
	"""Exception thrown when the community platform send an error code."""
	def __init__(self, category, code):
		super().__init__('Internal error: {}-{}'.format(category, code))