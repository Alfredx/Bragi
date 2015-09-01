#encoding: utf-8
import sys
sys.path.append('..')
import game

class Character():
	def __init__(self, hostGame, x, y):
		self.hostGame = hostGame
		self.x = x
		self.y = y
		self.speed = 1
		self.color = '#FFD700'
	def Move(self, direction):
		if direction == game.DIRCT_UP:
			self.y -= 1
		elif direction == game.DIRCT_LEFT:
			self.x -= 1
		elif direction == game.DIRCT_RIGHT:
			self.x += 1
		elif direction == game.DIRCT_DOWN:
			self.y += 1

class Player(Character):
	def __init__(self, hostGame, x, y):
		Character.__init__(self,hostGame, x, y)
		self.color = '#00FFFF'

class GeneralNPC(Character):
	def __init__(self, hostGame, x, y):
		Character.__init__(self, hostGame, x, y)
		self.color = '#B03060'