from datetime import datetime

class Date(datetime):
	@classmethod
	def fromtimestamp(cls, timestamp):
		return cls(*super().fromtimestamp(timestamp*60).timetuple()[:6])

	def timestamp(self):
		return round(super().timestamp()/60)
