import wx
import CalSudoku

LOCATION_X = 10
LOCATION_y = 10
WIDTH = 50
HEIGHT = 50
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 600


class SudoFrame(wx.Frame):
	def __init__(self, *args, **kw):
		super(SudoFrame, self).__init__(size=(WINDOW_WIDTH, WINDOW_HEIGHT),
										style=wx.DEFAULT_DIALOG_STYLE | wx.MINIMIZE_BOX, *args, **kw)
		self.sudo = ""
		self.sudoku = ""
		self.pnl = wx.Panel(self)
		self.input_list = []
		for j in range(9):
			for i in range(9):
				reset_x = i // 3 * 5
				reset_y = j // 3 * 5
				self.input_list.append(
					wx.TextCtrl(self.pnl, -1, pos=(LOCATION_X + WIDTH * i + reset_x, LOCATION_y + HEIGHT * j + reset_y),
								size=(WIDTH, HEIGHT), style=wx.TE_CENTER))
				font1 = wx.Font(30, wx.MODERN, wx.BOLD, wx.NORMAL, False, 'Calibri')
				self.input_list[-1].SetFont(font1)
				self.input_list[-1].SetMaxLength(1)
				self.input_list[-1].Bind(wx.EVT_TEXT, lambda evt, wh=self.input_list[-1]: self.validate(evt, wh))
		lines = [wx.StaticText(self.pnl, pos=(LOCATION_X, LOCATION_y + HEIGHT * 3), size=(460, 5)),
				 wx.StaticText(self.pnl, pos=(LOCATION_X, LOCATION_y + HEIGHT * 6 + 5), size=(460, 5)),
				 wx.StaticText(self.pnl, pos=(LOCATION_X + WIDTH * 3, LOCATION_y), size=(5, 460)),
				 wx.StaticText(self.pnl, pos=(LOCATION_X + WIDTH * 6 + 5, LOCATION_y), size=(5, 460))]
		for line in lines:
			line.SetBackgroundColour("rgb(0,0,0)")
		self.button1 = wx.Button(self.pnl, -1, label="计算", pos=(125, 500))
		self.button1.Bind(wx.EVT_BUTTON, self.calculate, self.button1)
		self.button2 = wx.Button(self.pnl, -1, label="清空", pos=(275, 500))
		self.button2.Bind(wx.EVT_BUTTON, self.clear, self.button2)

	def clear(self, event):
		for i in self.input_list:
			i.SetValue("")
			i.SetBackgroundColour("rgb(255,255,255)")

	# i.SetStyle(0,0,wx.TextAttr("red"))

	@staticmethod
	def validate(evt, wh):
		if wh.GetValue() == "":
			return
		if wh.GetValue() not in map(lambda x: str(x), range(1, 10)):  # ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
			wh.SetValue("")

	def calculate(self, event):
		self.sudo = ""
		for i in self.input_list:
			if i.GetValue() == "":
				self.sudo += '0'
				i.SetBackgroundColour("rgb(255,255,255)")
			else:
				self.sudo += i.GetValue()
				i.SetBackgroundColour("rgb(180,180,180")
				i.Refresh()
		# i.SetDefaultStyle(wx.TextAttr("rgb(255,0,0)"))
		# i.SetStyle(0,0,wx.TextAttr("red"))
		# print(self.sudo)
		self.sudoku = CalSudoku.Sudoku(self.sudo)
		# a=self.sudoku.cal_sudoku()
		n = 0
		for i in self.sudoku.answerArr[0]:
			for j in i:
				self.input_list[n].SetValue(str(j))
				n += 1
# print(a)


if __name__ == '__main__':
	my_window = wx.App()
	frm = SudoFrame(None, title="SudokuCalculate")
	frm.Show()

	my_window.MainLoop()

	pass
