#encoding: utf-8
import sys
import cPickle
import pprint
sys.path.append('..')
import Bragi_AStar as BgAStar


BLOCK_HEIGHT = 20

class terrain_pt(BgAStar.BgAStarNode):
	def __init__(self, bgmap, x=0.0, y=0.0, z=0.0):
		BgAStar.BgAStarNode.__init__(self, bgmap)
		self.x = x
		self.y = y
		self.z = z
		self.color = '#000000'
	def __str__(self):
		return '(%.2f,%.2f,%.2f)'%(self.x,self.y,self.z)

	def GetCoord(self):
		return (self.x, self.y)
	def GetCost(self, neighbor):
		return self.__DefaultGetCost(neighbor)

class terrain(BgAStar.BgAStarMap):
	def __init__(self, size):
		BgAStar.BgAStarMap.__init__(self)
		self.size = size
		self.data = None
		self.Build()
	def __str__(self):
		printStr = ''
		for j in range(self.size[1]):
			for i in range(self.size[0]):
				printStr += self.data[i][j].__str__()
				printStr += ' '
			printStr += '\n'
		return printStr
	def ConstructNodes(self, data = None):
		self.data = [[ terrain_pt(self,i,j,0) for j in range(self.size[1])] for i in range(self.size[0])]
		self.bgNodes = self.data
		return
	def ConstructNeighbors(self):
		for j in range(self.size[1]):
			for i in range(self.size[0]):
				if self.data[i][j].z >= BLOCK_HEIGHT:
					continue
				if j != self.size[1] - 1 and self.data[i][j+1].z < BLOCK_HEIGHT:
					self.data[i][j].neighbors.append(self.data[i][j+1])
				if j != 0 and self.data[i][j-1].z < BLOCK_HEIGHT:
					self.data[i][j].neighbors.append(self.data[i][j-1])
				if i != 0 and self.data[i-1][j].z < BLOCK_HEIGHT:
					self.data[i][j].neighbors.append(self.data[i-1][j])
				if i != self.size[0] - 1 and self.data[i+1][j].z < BLOCK_HEIGHT:
					self.data[i][j].neighbors.append(self.data[i+1][j])

		return
	def GetSize(self):
		return self.size
	def ExpandSize(self, size):
		if size[1] > self.size[1]:
			for i in range(self.size[0]):
				for j in range(size[1] - self.size[1]):
					self.data[i].append(terrain_pt(self,i,self.size[1]+j,0))
			self.size = (self.size[0],size[1])
		if size[0] > self.size[0]:
			for i in range(size[0] - self.size[0]):
				self.data.append([ terrain_pt(self,self.size[0]+i,j,0) for j in range(self.size[1])])
			self.size = (size[0], self.size[1])
	def CheckPointInTerrainSize(self, x, y):
		if x >= self.size[0] or x < 0:
			return False
		if y >= self.size[1] or y < 0:
			return False
		return True
	def CheckPointStandable(self, x, y):
		if not self.CheckPointInTerrainSize(x,y):
			return False
		if self.data[x][y].z >= BLOCK_HEIGHT:
			return False
		return True
	def GetPointZ(self, x, y):
		if not self.CheckPointInTerrainSize(x,y):
			return BLOCK_HEIGHT
		return self.data[x][y].z
	def SetPointZ(self, x, y, z):
		if not self.CheckPointInTerrainSize(x,y):
			return BLOCK_HEIGHT
		self.data[x][y].z = z
	def SetLineZ(self, x0, y0, x1, y1, z):
		if not self.CheckPointInTerrainSize(x0,y0):
			return BLOCK_HEIGHT
		if not self.CheckPointInTerrainSize(x1,y1):
			return BLOCK_HEIGHT
		steep = abs(y1-y0) > abs(x1-x0)
		if steep:
			x0, y0 = y0, x0
			x1, y1 = y1, x1
		if x0 > x1:
			x0, x1 = x1, x0
			y0, y1 = y1, y0
		deltax = x1 - x0
		deltay = abs(y1 - y0)
		error = deltax/2
		y = y0
		if y0<y1:
			ystep=1
		else:
			ystep=-1
		for x in xrange(x0,x1+1):
			if steep:
				self.data[y][x].z = z
			else:
				self.data[x][y].z = z
			error = error-deltay
			if error < 0:
				y += ystep
				error += deltax

def TerrainSaver(terrain, outputfilepath):
	try:
		with open(outputfilepath, 'wb') as output:
			cPickle.dump(terrain, output)
			print('terrain saved as '+outputfilepath)
	except Exception as e:
		print('TerrainSaver Error: '+str(e))
	return

def TerrainLoader(filepath):
	try:
		with open(filepath, 'rb') as pkl:
			terrain = cPickle.load(pkl)
			print('terrain loaded '+filepath)
			return terrain
	except Exception as e:
		print('TerrainLoader Error: '+str(e))
	return None