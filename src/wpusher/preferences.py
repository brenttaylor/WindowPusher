import wx
import vdesk
import win32con
import sys
import movementindicator


class Model(object):
    def __init__(self):
        pass

    def shortcut_data(self):
        def generate_shortcut(Modifiers, Key, Function):
            return {
                "Modifiers": Modifiers,
                "Key": Key,
                "Function": Function
            }

        return (
            generate_shortcut(
                win32con.MOD_ALT | win32con.MOD_WIN,
                win32con.VK_RIGHT,
                lambda Controller: Controller.display_next()
            ),
            generate_shortcut(
                win32con.MOD_ALT | win32con.MOD_WIN,
                win32con.VK_LEFT,
                lambda Controller: Controller.display_previous()
            ),
            generate_shortcut(
                win32con.MOD_CONTROL | win32con.MOD_WIN,
                win32con.VK_RIGHT,
                lambda Controller: Controller.move_window_to_next_desktop_and_display()
            ),
            generate_shortcut(
                win32con.MOD_CONTROL | win32con.MOD_WIN,
                win32con.VK_LEFT,
                lambda Controller: Controller.move_window_to_previous_desktop_and_display()
            )
        )


class Controller(object):
    def __init__(self):
        self.EventIDs = []
        self.DesktopManager = vdesk.DesktopManager()
        self.Model = Model()
        self.Window = Window(self)
        self.TaskBarIcon = TaskBarIcon(self.Window, self)
        self.register_hot_keys(self.Model.shortcut_data())
        self.MIController = movementindicator.Controller()

    def register_hot_keys(self, Hotkeys):
        def register_hotkey(Hotkey):
            ID = wx.NewId()
            self.Window.RegisterHotKey(ID, Hotkey["Modifiers"], Hotkey["Key"])
            self.Window.Bind(wx.EVT_HOTKEY, lambda Event: Hotkey["Function"](self),
                             id=ID)
            self.EventIDs.append(ID)

        [register_hotkey(Hotkey) for Hotkey in Hotkeys]

    def unregister_hotkeys(self):
        for ID in self.EventIDs:
            self.Window.UnregisterHotKey(ID)
        self.EventIDs = []

    def display_next_desktop(self):
        self.DesktopManager.display_next()
        self.MIController.next()

    def display_previous_desktop(self):
        self.DesktopManager.display_previous()
        self.MIController.previous()

    def move_window_to_next_desktop_and_display(self):
        try:
            self.DesktopManager.move_window_to_next_desktop_and_display()
            self.MIController.next()
        except vdesk.NoForegroundWindow:
            pass

    def move_window_to_previous_desktop_and_display(self):
        try:
            self.DesktopManager.move_window_to_previous_desktop_and_display()
            self.MIController.previous()
        except vdesk.NoForegroundWindow:
            pass

    def close(self):
        self.Window.Hide()

    def exit(self):
        self.unregister_hotkeys()
        self.DesktopManager.show_all_windows()
        self.TaskBarIcon.RemoveIcon()
        sys.exit(1)

    def icon_dbl_click(self):
        if self.Window.IsIconized():
            self.Window.Iconize(False)
        if not self.Window.IsShown():
            self.Window.Show(True)
            self.Window.Raise()


class TaskBarIcon(wx.TaskBarIcon):
    def __init__(self, Parent, Controller):
        wx.TaskBarIcon.__init__(self)

        def create_child_widgets():
            self.Icon = wx.EmptyIcon()
            self.ParentFrame = Parent
            self.Controller = Controller
            self.Menu = wx.Menu()

        def configure():
            self.EventIDs = {
                "NextDesktop": wx.NewId(),
                "PreviousDesktop": wx.NewId(),
                "Exit": wx.NewId(),
                "LaunchPreferences": wx.NewId(),
                "LaunchMenu": wx.NewId()
            }

            def load_bitmap():
                image = wx.Image("Resources/icon.bmp", wx.BITMAP_TYPE_ANY)
                image.SetMaskColour(255, 0, 255)
                return wx.BitmapFromImage(image)

            self.Icon.CopyFromBitmap(load_bitmap())
            self.SetIcon(self.Icon, "WindowPusher")

            self.Menu.Append(self.EventIDs["NextDesktop"], "Display Next Desktop")
            self.Menu.Append(self.EventIDs["PreviousDesktop"], "Display Previous Desktop")
            self.Menu.AppendSeparator()
            self.Menu.Append(self.EventIDs["Exit"], "Exit")

        def bind_events():
            self.Bind(wx.EVT_TASKBAR_LEFT_DCLICK,
                      lambda event: self.Controller.icon_dbl_click())
            self.Bind(wx.EVT_TASKBAR_RIGHT_UP,
                      lambda event: self.PopupMenu(self.Menu))
            self.Bind(wx.EVT_MENU,
                      lambda event: self.Controller.exit(),
                      id=self.EventIDs["Exit"])
            self.Bind(wx.EVT_MENU,
                      lambda event: self.Controller.display_next(),
                      id=self.EventIDs["NextDesktop"])
            self.Bind(wx.EVT_MENU,
                      lambda event: self.Controller.display_previous(),
                      id=self.EventIDs["PreviousDesktop"])

        create_child_widgets()
        configure()
        bind_events()


class GeneralTab(wx.Panel):
    def __init__(self, parent, controller):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.Controller = controller

        def create_child_widgets():
            self.RootSizer = wx.BoxSizer(wx.VERTICAL)
            self.stNumDesktops = wx.StaticText(self, wx.ID_ANY,
                                               label="Number of Desktops?")
            self.scNumDesktops = wx.SpinCtrl(self, wx.ID_ANY, size=(40, -1))

            self.sbDesktopIndicator = wx.CheckBox(self, wx.ID_ANY,
                                                  "Show Desktop Indicator?")

            self.stDesktopIndicatorDelay = wx.StaticText(self, wx.ID_ANY,
                                                         label="Desktop Indicator Delay?")
            self.slDesktopIndicatorDelay = wx.Slider(self, wx.ID_ANY, 1, 0, 30,
                                                     wx.DefaultPosition, (250, -1), wx.SL_HORIZONTAL)

            self.sbStartWithWindows = wx.CheckBox(self, wx.ID_ANY,
                                                  "Start with Windows?")
            self.btnKeyboardShortcuts = wx.Button(self, wx.ID_ANY,
                                                  "Keyboard Shortcuts", (50, 130))

        def configure():
            def horizontal_sizer(Widgets):
                sizer = wx.BoxSizer(wx.HORIZONTAL)
                for Widget in Widgets:
                    sizer.Add(Widget, 0, wx.ALL, 5)
                return sizer

            self.scNumDesktops.SetRange(1, 4)
            self.scNumDesktops.SetValue(4)

            sizerNumDesktops = horizontal_sizer((self.stNumDesktops, self.scNumDesktops))
            sizerDesktopIndicatorDelay = horizontal_sizer(
                (self.stDesktopIndicatorDelay,
                 self.slDesktopIndicatorDelay)
            )

            self.RootSizer.Add(sizerNumDesktops, 0, wx.LEFT)
            self.RootSizer.Add(self.sbStartWithWindows, 0, wx.LEFT)
            self.RootSizer.AddSpacer(5)
            self.RootSizer.Add(self.sbDesktopIndicator, 0, wx.LEFT)
            self.RootSizer.Add(sizerDesktopIndicatorDelay, 0, wx.LEFT)
            self.RootSizer.AddSpacer(10)
            self.RootSizer.Add(self.btnKeyboardShortcuts, 0, wx.LEFT)
            self.SetSizer(self.RootSizer)

        def bind_events():
            pass

        create_child_widgets()
        configure()
        bind_events()


class PreferencesNotebook(wx.Notebook):
    def __init__(self, Parent, Controller):
        wx.Notebook.__init__(self, Parent, id=wx.ID_ANY, style=wx.BK_DEFAULT)
        self.Controller = Controller

        def create_child_widgets():
            self.General = GeneralTab(self, Controller)

        def configure():
            self.AddPage(self.General, "General")

        def bind_events():
            pass

        create_child_widgets()
        configure()
        bind_events()


class Window(wx.Frame):
    def __init__(self, Controller):
        wx.Frame.__init__(self, None, -1, "WindowPusher", (100, 100), (300, 300),
                          style=wx.CLOSE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.FRAME_TOOL_WINDOW)
        self.Controller = Controller
        self.EventIDs = []

        def create_child_widgets():
            self.Panel = wx.Panel(self, wx.ID_ANY)
            self.RootSizer = wx.BoxSizer(wx.VERTICAL)
            self.Notebook = PreferencesNotebook(self.Panel, Controller)
            self.btnClose = wx.Button(self.Panel, wx.ID_ANY, "Close", (50, 130))
            self.btnApply = wx.Button(self.Panel, wx.ID_ANY, "Apply", (50, 130))

        def configure():
            self.Controller = Controller
            self.EventIDs = []

            ButtonSizer = wx.BoxSizer(wx.HORIZONTAL)
            ButtonSizer.Add(self.btnClose, 0, wx.ALL, 5)
            ButtonSizer.Add(self.btnApply, 0, wx.ALL, 5)

            self.RootSizer.Add(self.Notebook, 1, wx.EXPAND | wx.ALL, 5)
            self.RootSizer.Add(ButtonSizer, 0, wx.ALIGN_BOTTOM | wx.ALIGN_RIGHT, 5)
            self.Panel.SetSizer(self.RootSizer)
            self.Panel.Layout()

        # self.Layout()

        def bind_events():
            self.Bind(wx.EVT_CLOSE, lambda Event: self.Controller.close())
            self.btnClose.Bind(wx.EVT_BUTTON, lambda Event: self.Controller.close())
            self.btnApply.Bind(wx.EVT_BUTTON, lambda Event: self.Controller.close())

        create_child_widgets()
        configure()
        bind_events()
