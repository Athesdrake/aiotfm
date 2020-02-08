from datetime import datetime


class Date(datetime):
	"""Represents the date format of the game.

	Inherit from datetime.datetime class.
	"""
	@classmethod
	def fromtimestamp(cls, t, tz=None):
		"""Return a date from a timestamp
		:param t: :class:`int` the timestamp.
		:param tz: Optional[:class:`datetime.timezone`] a time zone to pass to the super method.
		:return: :class:`aiotfm.utils.Date` the date.
		"""
		return cls(*super().fromtimestamp(t * 60, tz).timetuple()[:6])

	def timestamp(self):
		"""Convert the date into the timestamp format used by the game.
		:return: :class:`int` the timestamp.
		"""
		return round(super().timestamp() / 60)
