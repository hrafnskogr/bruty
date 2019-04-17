#!/usr/bin/python3
import itertools

class brutor(object):
	def __init__(self, string, c_min, c_max):
		self.seed = string
		self.low_bound = c_min
		self.high_bound = c_max
		self.generator = itertools.product(self.seed, repeat=self.low_bound)
		self.depleted = False
		self.infinite = True if c_max < 0 else False

	def reinit(self):
		self.low_bound += 1
		if((not self.infinite) and (self.low_bound > self.high_bound)):
			self.depleted = True
			return
		self.generator = itertools.product(self.seed, repeat=self.low_bound)

	def __next__(self):
		self.next()

	def next(self):
		try:
			return next(self.generator)
		except StopIteration:
			if(self.depleted):
				raise StopIteration("End of Brute-Force")
			else:
				self.reinit()
				return next(self.generator)
