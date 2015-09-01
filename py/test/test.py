#encoding: utf-8
import wx
import sys
sys.path.append('..')
import ui.main_ui as MainUI

if __name__ == '__main__':
	app = wx.App()
	mainUI = MainUI.MainUI(None, 'BragiTest', (800,600))
	mainUI.Show()
	app.MainLoop()