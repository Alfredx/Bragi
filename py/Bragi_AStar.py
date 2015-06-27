#encoding: utf-8

class BgAStarMapFactory():
	def __init__(self):
		print('BgAStarMapFactory constructor')

class BgAStarPathFactory():
	def __init__(self):
		print('BgAStarPathFactory constructor')

class BgAStar():
	def __init__(self, BgAStarMap):
		print('BgAStar constructor')
		self.map = BgAStarMap 

	@classmethod
	def Heuristic(a, b):
		(x0, y0) = a
		(x1, y1) = b
		return abs(x1-x0) + abs(y1-y0)

	def Search(self, start, destination):
		return


	