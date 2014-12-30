import user32
import win32con
import ctypes
import collections


class VirtualDesktopException(Exception):
    pass


class NoForegroundWindow(VirtualDesktopException):
    pass


class VirtualDesktop(object):
    def __init__(self):
        self.Windows = []
        self.RemovedWindows = []

    def RemoveForegroundWindow(self):
        ForegroundWindow = user32.GetForegroundWindow()
        if user32.IsWindowVisible(ForegroundWindow):
            self.RemovedWindows.append(ForegroundWindow)
            user32.ShowWindow(ForegroundWindow, win32con.SW_HIDE)
            return ForegroundWindow
        raise NoForegroundWindow("This Desktop is empty of windows.")

    def AddWindow(self, Window):
        self.Windows.append(Window)

    def Show(self):
        self.RemovedWindows = []
        for Window in self.Windows:
            user32.ShowWindow(Window, win32con.SW_SHOW)
        if len(self.Windows) > 0:
            user32.SetForegroundWindow(self.Windows[-1])

    def Hide(self):
        self.Windows = []

        def EnumWindowsProc(hWnd, lParam):
            if not hWnd: return True
            if not user32.IsWindowVisible(hWnd): return True

            # Get Window Title
            Length = user32.SendMessage(hWnd, win32con.WM_GETTEXTLENGTH, 0, 0)
            Buffer = ctypes.create_unicode_buffer(Length + 1)

            if not user32.SendMessage(hWnd, win32con.WM_GETTEXT, Length + 1, ctypes.byref(Buffer)):
                return True

            if Buffer.value != "Program Manager":
                if not (hWnd in self.RemovedWindows):
                    if hWnd == user32.GetForegroundWindow():
                        self.Windows.append(hWnd)
                    else:
                        self.Windows.insert(0, hWnd)
                    user32.ShowWindow(hWnd, win32con.SW_HIDE)

            return True

        user32.EnumWindows(EnumWindowsProc, 0)

    def __del__(self):
        self.ShowDesktop()


class DesktopManager(object):
    __Previous = 1
    __Next = -1

    def __init__(self, NumberOfDesktops=4):
        self.Desktops = collections.deque([VirtualDesktop() for x in xrange(NumberOfDesktops)])
        self.Index = collections.deque(range(NumberOfDesktops))

    def __Move(self, Direction):
        self.Desktops.rotate(Direction)
        self.Index.rotate(Direction)

    def __DisplayDesktop(self, Direction):
        self.Desktops[0].Hide()
        self.__Move(Direction)
        self.Desktops[0].Show()

    def __MoveWindowToDesktop(self, Direction, HideWindow=True):
        ForegroundWindow = self.Desktops[0].RemoveForegroundWindow()
        self.__Move(Direction)
        self.Desktops[0].AddWindow(ForegroundWindow)
        self.__Move(-Direction)

    def DisplayNextDesktop(self):
        self.__DisplayDesktop(self.__Next)

    def DisplayPreviousDesktop(self):
        self.__DisplayDesktop(self.__Previous)

    def MoveWindowToNextDesktop(self):
        self.__MoveWindowToDesktop(self.__Next)

    def MoveWindowToPreviousDesktop(self):
        self.__MoveWindowToDesktop(self.__Previous)

    def MoveWindowToNextDesktopAndDisplay(self):
        self.__MoveWindowToDesktop(self.__Next)
        self.__DisplayDesktop(self.__Next)

    def MoveWindowToPreviousDesktopAndDisplay(self):
        self.__MoveWindowToDesktop(self.__Previous)
        self.__DisplayDesktop(self.__Previous)

    def GetCurrentDesktopNumber(self):
        return self.Index[0]

    def ShowAllWindows(self):
        [Desktop.Show() for Desktop in self.Desktops]

