#encoding: utf-8

import sys
import wx
import os
import debug_console as dbgconsole
sys.path.append('..')
import Bragi
import game
import game.aigame as MyGame
import game.terrain as terrain

class MainUI(wx.Frame):
	def __init__(self, parent, title, size):
		super(MainUI, self).__init__(parent, title=title, size=size)
		self.size = size

		self.drawPanel = wx.Panel(self, wx.ID_ANY, pos=(0,0), size=self.size)

		self.Bind(wx.EVT_CHAR_HOOK, self.OnKeyHook)
		self.drawPanel.Bind(wx.EVT_SIZE, self.OnWindowSizeChanged)
		self.drawPanel.Bind(wx.EVT_PAINT, self.OnPaint)
		self.drawPanel.Bind(wx.EVT_MOTION, self.OnMouseMove)
		self.Bind(wx.EVT_CLOSE, self.OnClose)

		self.drawPanel.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
		self.drawPanel.SetBackgroundColour(wx.BLACK)
		self.drawPanel.SetForegroundColour(wx.WHITE)

		self.cmdList = {}
		self.needRepaint = True
		self.needPrintDebugInfo = False
		self.needDrawGrid = True
		self.gridGapSize = 20
		self.gridRows = self.size[1]/self.gridGapSize
		self.gridColumns = self.size[0]/self.gridGapSize
		self.mousePosition = (0,0)
		self.mouseGridPosition = (0,0)
		self.game = None
		# debug
		self.dbgConsole = dbgconsole.DebugConsole(None, 'Bragi Test Console', self)
		self.ToggleDebugInfo()
		self.BuildCmdList()

		self.CreateGame()

		self.Centre()

	def OnKeyHook(self, event):
		keycode = event.GetKeyCode()
		if keycode == wx.WXK_F1:
			self.ToggleDebugInfo()
		elif keycode == wx.WXK_F2:
			self.ToggleDrawGrid()
		elif keycode == wx.WXK_UP:
			self.game.MovePlayer(game.DIRCT_UP)
		elif keycode == wx.WXK_LEFT:
			self.game.MovePlayer(game.DIRCT_LEFT)
		elif keycode == wx.WXK_RIGHT:
			self.game.MovePlayer(game.DIRCT_RIGHT)
		elif keycode == wx.WXK_DOWN:
			self.game.MovePlayer(game.DIRCT_DOWN)
	def OnMouseMove(self, event):
		self.mousePosition = event.GetPosition()
		self.mouseGridPosition = (self.mousePosition[0]/self.gridGapSize,self.mousePosition[1]/self.gridGapSize)

	def OnWindowSizeChanged(self, event):
		event.Skip()
		size = self.GetSize()
		self.size = size
		self.drawPanel.SetSize(size)
		self.drawPanel.Refresh()
		self.gridRows = self.size[1]/self.gridGapSize
		self.gridColumns = self.size[0]/self.gridGapSize
		self.game.ExpandTerrainSize((self.gridColumns, self.gridRows))

	def OnPaint(self, event):
		if self.needRepaint:
			dc = wx.AutoBufferedPaintDC(self.drawPanel)
			self.RePaint(dc)
		else:
			event.Skip()
	def OnClose(self, event):
		app = wx.GetApp()
		if hasattr(app, 'stdioWin') and app.stdioWin:
			app.stdioWin.close()
			app.RestoreStdio()
		self.Destroy()
		os._exit(0)

	def RePaint(self, dc):
		dc.Clear()
		dc.SetBrush(wx.Brush(wx.BLACK))
		dc.SetBackground(wx.Brush(wx.BLACK))
		dc.DrawRectangle(0,0,self.size[0],self.size[1])
		dc.SetBrush(wx.Brush(wx.WHITE))
		if self.needDrawGrid:
			self.DrawGrid(dc)
		self.PaintGameObjects(dc)
		if self.needPrintDebugInfo:
			self.PrintDebufInfo(dc)
		self.drawPanel.Refresh()
	def ToggleDebugInfo(self):
		self.needPrintDebugInfo = not self.needPrintDebugInfo
		if hasattr(self, 'dbgConsole') and self.dbgConsole:
			self.dbgConsole.Show(self.needPrintDebugInfo)
	def PrintDebufInfo(self, dc):
		brush = dc.GetBrush()
		dc.SetTextForeground(wx.WHITE)
		currentHeight = 5
		charHeight = dc.GetCharHeight()
		dc.DrawText('Panel Size: (%d, %d)'%(self.size[0],self.size[1]),5,currentHeight)
		currentHeight += charHeight
		dc.DrawText('Max Terrain Size: ' + str(self.game.terrain.GetSize()),5,currentHeight)
		currentHeight += charHeight
		dc.DrawText('Mouse Grid Position: '+str(self.mouseGridPosition),5,currentHeight)
		currentHeight += charHeight
		dc.DrawText('lps: '+str(self.game.loopPerSec),5,currentHeight)
		
	def ToggleDrawGrid(self):
		self.needDrawGrid = not self.needDrawGrid
	def DrawGrid(self,dc):
		horizontal_lines = [(i*self.gridGapSize, 0, i*self.gridGapSize, self.size[1]) for i in range(self.gridColumns)]
		vertical_lines = [(0, i*self.gridGapSize, self.size[0], i*self.gridGapSize) for i in range(self.gridRows)]
		dc.SetPen(wx.Pen('#696969',1))
		dc.DrawLineList(vertical_lines+horizontal_lines)
		return
	def PaintGameObjects(self, dc):
		self.PaintTerrain(dc)
		self.PaintCharacters(dc)
	def PaintTerrain(self,dc):
		for x in range(self.gridColumns):
			for y in range(self.gridRows):
				z = self.game.GetTerrainZ(x,y)
				if z >= terrain.BLOCK_HEIGHT:
					dc.SetBrush(wx.Brush('#B22222'))
					dc.DrawRectangle(x*self.gridGapSize, y*self.gridGapSize, self.gridGapSize+1, self.gridGapSize+1)
	def PaintCharacters(self,dc):
		characters = self.game.GetCharacters()
		for chara in characters:
			dc.SetBrush(wx.Brush(chara.color))
			dc.DrawRectangle(chara.x*self.gridGapSize, chara.y*self.gridGapSize, self.gridGapSize+1, self.gridGapSize+1)

	def BuildCmdList(self):
		def func_help(self, params):
			for cmd in self.cmdList:
				print(cmd)
		def func_saveterrain(self, params):
			self.game.SaveTerrain(params[1])
		def func_loadterrain(self, param):
			self.game.LoadTerrain(params[1])
		def func_line(self, params):
			self.game.terrain.SetLineZ(int(params[1]),int(params[2]),int(params[3]),int(params[4]),int(params[5]))
		def func_point(self, params):
			self.game.terrain.SetPointZ(int(params[1]),int(params[2]),int(params[3]))
		def func_moveto(self, params):
			self.game.MovePlayerTo(int(params[1]),int(params[2]))
		self.cmdList['help'] = func_help
		self.cmdList['saveterrain'] = func_saveterrain
		self.cmdList['loadterrain'] = func_loadterrain
		self.cmdList['line'] = func_line
		self.cmdList['point'] = func_point
		self.cmdList['moveto'] = func_moveto

	def InputDebugCommand(self, cmds):
		print('console >'+cmds)
		try:
			cmds = cmds.lower().split(' ')
			cmd = cmds[0]
			if not cmd in self.cmdList:
				print('no cmd %s found'%(cmd))
				return
			self.cmdList[cmd](self,cmds)
		except Exception as e:
			print('cmd <%s> error: %s'%(cmd,str(e)))

	def CreateGame(self):
		self.game = MyGame.AIGame((self.gridColumns, self.gridRows))
		# self.game.LoadTerrain('../game/assets/tt.bgt')
		self.game.AddPlayer(6,9)
		self.game.AddNPC(22,18)
		self.GameStart()
	def GameStart(self):
		self.game.start()
	def GamePause(self):
		self.game.ToggleGamePause(self)

if __name__ == '__main__':
	app = wx.App()
	mainUI = MainUI(None, 'BragiTest', (800,600))
	mainUI.Show()
	app.MainLoop()
