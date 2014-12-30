import preferences
import wx


class WindowPusher(wx.App):
    def OnInit(self):
        self.Preferences = preferences.Controller()
        self.SetTopWindow(self.Preferences.Window)
        return True


if __name__ == '__main__':
    WindowPusher(redirect=False).MainLoop()
