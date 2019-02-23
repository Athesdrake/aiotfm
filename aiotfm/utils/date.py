from datetime import datetime

class Date(datetime):
	@classmethod
	def fromtimestamp(cls, timestamp, **kw):
		return super().fromtimestamp(timestamp*60, **kw)

	def timestamp(self):
		return round(super().timestamp()/60)
