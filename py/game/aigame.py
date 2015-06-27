#encoding: utf-8
import terrain
import character
import sys
import threading
import timeit
sys.path.append('..')
import game
import Bragi
import Bragi_AStar as bgAStar

class AIGame(threading.Thread):
	def __init__(self, terrain_size):
		super(AIGame, self).__init__(name = 'AIGame')
		self.lock = threading.Lock()
		self.terrain = terrain.terrain(terrain_size)
		self.player = None
		self.npcs = []
		self.timeCounter = 0
		self.loopsCounter = 0
		self.loopPerSec = 0
		self.gamePaused = False
	def run(self):
		self.lock.acquire()
		self.timeCounter = timeit.default_timer()
		while not self.gamePaused:
			self.Loop()
		self.lock.release()
	def Loop(self):
		self.loopsCounter += 1
		elapsedTime = timeit.default_timer() - self.timeCounter
		if elapsedTime > 1.0:
			self.loopPerSec = self.loopsCounter
			self.loopsCounter = 0
			self.timeCounter += 1.0
			pass
	def ToggleGamePause(self):
		self.gamePaused = not self.gamePaused
		
	def ExpandTerrainSize(self, size):
		self.terrain.ExpandSize(size)
	def GetTerrainZ(self, x, y):
		return self.terrain.GetPointZ(x,y)
	def SaveTerrain(self, savepath):
		terrain.TerrainSaver(self.terrain, savepath)
	def LoadTerrain(self, loadpath):
		self.terrain = terrain.TerrainLoader(loadpath)
	def CheckBoundary(self, x, y):
		return self.terrain.CheckPointInTerrainSize(x,y)
	def AddPlayer(self, x, y):
		if not self.player is None:
			return False
		if not self.terrain.CheckPointStandable(x,y):
			return False
		self.player = character.Player(self, x, y)
		return True
	def AddNPC(self, x, y):
		if not self.terrain.CheckPointStandable(x,y):
			return False
		self.npcs.append(character.GeneralNPC(self,x,y))
		return True
	def GetCharacters(self):
		return self.npcs+[self.player]
	def MovePlayer(self, direction):
		oldxy = (self.player.x, self.player.y)
		self.player.Move(direction)
		if not self.terrain.CheckPointStandable(self.player.x, self.player.y):
			self.player.x, self.player.y = oldxy[0], oldxy[1]
	def MoveTo(self, x, y):
		return


if __name__ == '__main__':
	game = AIGame((3,3))
	print(game.terrain)
	game.ExpandTerrainSize((5,5))
	print(game.terrain)
	# terrain.TerrainSaver(game.terrain, 'terrain.pkl')
	# t = terrain.TerrainLoader('terrain.pkl')
	# if not t is None:
 		# pprint.pprint(t.data)