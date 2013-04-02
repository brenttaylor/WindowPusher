import wx

class Model(object):
	def __init__(self):
		pass
	def GetDelay(self):
		return 100

class Controller(object):
	def __init__(self):
		self.Model = Model()
		self.NextWindow = Window(self, "Resources/moveRight.png")
		self.PreviousWindow = Window(self, "Resources/moveLeft.png")
	def Next(self):
		self.NextWindow.Start(self.Model.GetDelay())
	def Previous(self):
		self.PreviousWindow.Start(self.Model.GetDelay())

#As a reminder, del DelayTimer on close to avoid memory leak
class Window(wx.Frame):
	def __init__(self, Controller, FrameShape):
		wx.Frame.__init__(self, None, -1, "WindowPusher", (1,1),
				style = wx.FRAME_SHAPED | wx.SIMPLE_BORDER |
				wx.FRAME_NO_TASKBAR | wx.STAY_ON_TOP)
		self.Controller = Controller
		
		def CreateChildWidgets():
			def CreateBitmap():
				bmp = wx.Image(FrameShape, wx.BITMAP_TYPE_PNG)
				bmp.ConvertAlphaToMask()
				return bmp.ConvertToBitmap()
			self.FrameShape = CreateBitmap()
			self.DC = wx.ClientDC(self)
			self.DelayTimer = wx.Timer(self)

		def Configure():
			def SetFrameShape():
				self.SetClientSize((self.FrameShape.GetWidth(),
					self.FrameShape.GetHeight()))
				self.DC.DrawBitmap(self.FrameShape, 0, 0, True)
				self.SetShape(wx.RegionFromBitmap(self.FrameShape))

			def MoveWindow():
				ScreenRect = wx.Display().GetGeometry()
				self.Move(((ScreenRect.GetWidth()/2)-(self.FrameShape.GetWidth()/2),
					(ScreenRect.GetHeight()/2)-(self.FrameShape.GetHeight()/2)))

			SetFrameShape()
			MoveWindow()
			self.SetTransparent(220)
			
		def BindEvents():
			self.Bind(wx.EVT_PAINT,
					lambda evt: wx.PaintDC(self).DrawBitmap(self.FrameShape,
						0, 0, True))
			self.Bind(wx.EVT_WINDOW_CREATE,
					lambda event=None: self.SetShape(wx.RegionFromBitmap(self.FrameShape)))
			self.Bind(wx.EVT_TIMER, self.DelayEvent, self.DelayTimer)
		CreateChildWidgets()
		Configure()
		BindEvents()
	def DelayEvent(self, Evt):
		self.DelayTimer.Stop()
		self.Show(False)
	def Start(self, Delay):
		self.Show(True)
		self.DelayTimer.Start(Delay)
