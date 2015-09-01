#encoding: utf-8
import abc
import Bragi_utils as bgutils

class BgAStarNode():
	__metaclass__ = abc.ABCMeta
	def __init__(self, astarMap):
		self.parentMap = None
		assert(astarMap!= None)
		self.parentMap = astarMap
		self.bgID = astarMap.GenerateNodeID()
		self.neighbors = []

	@abc.abstractmethod
	def GetCoord(self):
		"""Should be implemented in your code"""
		return

	@abc.abstractmethod
	def GetCost(self, neighbor):
		"""Should be implemented in your code"""
		return

	def __DefaultGetCost(self, neighbor):
		cost = None
		for n in self.neighbors:
			if neighbor == n:
				cost = BgAStar.Heuristic(self.GetCoord(), n.GetCoord())
				break
		assert(cost != None)
		return cost

class BgAStarMap():
	__metaclass__ = abc.ABCMeta
	def __init__(self):
		self.__generateNodeID = -1
		self.bgNodes = None

	def Build(self):
		self.ConstructNodes()
		self.ConstructNeighbors()

	@abc.abstractmethod
	def ConstructNodes(self, data = None):
		"""Should be implemented in your code"""
		return
	@abc.abstractmethod
	def ConstructNeighbors(self):
		"""Should be implemented in your code"""
		return

	def GenerateNodeID(self):
		self.__generateNodeID += 1
		return self.__generateNodeID

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
		openList = bgutils.PriorityQueue()
		openList.put(start.bgID, 0)
		cost_so_far = {}
		closeList = {}
		cost_so_far[start.bgID] = 0
		closeList[start.bgID] = None

		while not openList.empty():
			current = openList.get()
			if current == destination:
				break

			for next in current.neighbors:
				new_cost = cost_so_far[current.bgID] + current.GetCost(next)
				if next.bgID not in cost_so_far or new_cost < cost_so_far[next.bgID]:
					cost_so_far[next.bgID] = new_cost
					priority = new_cost + Heuristic(destination.GetCoord(), next.GetCoord())
					openList.put(next, priority)
					closeList[next.bgID] = current
		print(closeList, cost_so_far)
		return	closeList, cost_so_far


	