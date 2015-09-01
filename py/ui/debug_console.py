#encoding: utf-8

import wx

class DebugConsole(wx.Frame):
	def __init__(self, parent, title, host):
		super(DebugConsole, self).__init__(parent, title=title, size=(400,300))
		self.size = (400,300)
		self.host = host
		self.panel = wx.Panel(self, wx.ID_ANY, pos=(0,0), size = self.size)

		self.consoleLogText = wx.TextCtrl(self.panel, wx.ID_ANY, pos=(0,0), size = (self.size[0],self.size[1]-80), style=wx.TE_MULTILINE|wx.TE_READONLY)
		self.consoleLogText.SetEditable(False)
		self.consoleLogText.SetValue('>')
		self.consoleInput = wx.TextCtrl(self.panel, wx.ID_ANY, pos = (0, self.size[1]-75), size = (self.size[0], 40), style=wx.TE_PROCESS_ENTER|wx.TE_MULTILINE)

		self.consoleInput.Bind(wx.EVT_KEY_DOWN, self.ConsoleInputKeyDown)
		self.consoleInput.SetFocus()
		# self.panel.Bind(wx.EVT_PAINT, self.OnPaint)

	def ConsoleInputKeyDown(self, event):
		keycode = event.GetKeyCode()
		if keycode == wx.WXK_RETURN or keycode == wx.WXK_NUMPAD_ENTER:
			new_text = self.consoleInput.GetValue()
			self.host.InputDebugCommand(new_text.decode('utf-8'))
			old_st = self.consoleLogText.GetValue()
			self.consoleLogText.SetValue(old_st+'\n>'+new_text)
			self.consoleInput.SetValue('')
			if (new_text == 'clr'):
				self.consoleLogText.SetValue('>')
		else:
			event.Skip(True)