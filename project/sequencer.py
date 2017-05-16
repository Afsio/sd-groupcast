'''
Arnau Montanes
Christian Zanger
01/05/2017 version 0.1
'''

class Sequencer(object):
	_tell = []
	_ask = ["timestamp"]

	def __init__(self):
		self.seq = -1

	def timestamp(self):
		self.seq += 1
		return self.seq
