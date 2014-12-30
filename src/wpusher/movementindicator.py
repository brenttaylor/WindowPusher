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

    def next(self):
        self.NextWindow.start(self.Model.GetDelay())

    def previous(self):
        self.PreviousWindow.start(self.Model.GetDelay())


# As a reminder, del DelayTimer on close to avoid memory leak
class Window(wx.Frame):
    def __init__(self, Controller, FrameShape):
        wx.Frame.__init__(self, None, -1, "WindowPusher", (1, 1),
                          style=wx.FRAME_SHAPED | wx.SIMPLE_BORDER |
                                wx.FRAME_NO_TASKBAR | wx.STAY_ON_TOP)
        self.Controller = Controller

        def create_child_widgets():
            def CreateBitmap():
                bmp = wx.Image(FrameShape, wx.BITMAP_TYPE_PNG)
                bmp.ConvertAlphaToMask()
                return bmp.ConvertToBitmap()

            self.FrameShape = CreateBitmap()
            self.DC = wx.ClientDC(self)
            self.DelayTimer = wx.Timer(self)

        def configure():
            def set_frame_shape():
                self.SetClientSize((self.FrameShape.GetWidth(),
                                    self.FrameShape.GetHeight()))
                self.DC.DrawBitmap(self.FrameShape, 0, 0, True)
                self.SetShape(wx.RegionFromBitmap(self.FrameShape))

            def move_window():
                ScreenRect = wx.Display().GetGeometry()
                self.Move(((ScreenRect.GetWidth() / 2) - (self.FrameShape.GetWidth() / 2),
                           (ScreenRect.GetHeight() / 2) - (self.FrameShape.GetHeight() / 2)))

            set_frame_shape()
            move_window()
            self.SetTransparent(220)

        def bind_events():
            self.Bind(wx.EVT_PAINT,
                      lambda evt: wx.PaintDC(self).DrawBitmap(self.FrameShape,
                                                              0, 0, True))
            self.Bind(wx.EVT_WINDOW_CREATE,
                      lambda event=None: self.SetShape(wx.RegionFromBitmap(self.FrameShape)))
            self.Bind(wx.EVT_TIMER, self.delay_event, self.DelayTimer)

        create_child_widgets()
        configure()
        bind_events()

    def delay_event(self, Evt):
        self.DelayTimer.Stop()
        self.Show(False)

    def start(self, Delay):
        self.Show(True)
        self.DelayTimer.start(Delay)
