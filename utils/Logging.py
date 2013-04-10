

class Logger(object):
	def __init__(self,logging=True):
		"""A simple logging tool.
		
		Args:
			logging - whether or not to print to stdout if you call Logger.log()
		
		"""
		self.logging = logging
		
	def log(self,string):
		"""Log to stdout if logging is enabled.
		
		Args:
			string - what to log to stdout
		
		"""
		if (self.logging):
			print string
			
	def shout(self,string):
		"""Shout to stdout if logging is enabled.
		
		Args:
			string - what to shout to stdout
		
		"""
		self.log("!!!"+string+"!!!")