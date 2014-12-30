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
        self.window = []
        self.removed_windows = []

    def remove_foreground_window(self):
        foreground_window = user32.GetForegroundWindow()
        if user32.IsWindowVisible(foreground_window):
            self.removed_windows.append(foreground_window)
            user32.ShowWindow(foreground_window, win32con.SW_HIDE)
            return foreground_window
        raise NoForegroundWindow("This Desktop is empty of windows.")

    def add_window(self, window):
        self.window.append(window)

    def show(self):
        self.removed_windows = []
        for Window in self.window:
            user32.ShowWindow(Window, win32con.SW_SHOW)
        if len(self.window) > 0:
            user32.SetForegroundWindow(self.window[-1])

    def hide(self):
        self.window = []

        def enum_windows_proc(hWnd, lParam):
            if not hWnd: return True
            if not user32.IsWindowVisible(hWnd): return True

            # Get Window Title
            length = user32.SendMessage(hWnd, win32con.WM_GETTEXTLENGTH, 0, 0)
            buffer = ctypes.create_unicode_buffer(length + 1)

            if not user32.SendMessage(hWnd, win32con.WM_GETTEXT, length + 1, ctypes.byref(buffer)):
                return True

            if buffer.value != "Program Manager":
                if not (hWnd in self.removed_windows):
                    if hWnd == user32.GetForegroundWindow():
                        self.window.append(hWnd)
                    else:
                        self.window.insert(0, hWnd)
                    user32.ShowWindow(hWnd, win32con.SW_HIDE)

            return True

        user32.EnumWindows(enum_windows_proc, 0)

    def __del__(self):
        self.show()


class DesktopManager(object):
    __Previous = 1
    __Next = -1

    def __init__(self, desktop_count=4):
        self.Desktops = collections.deque([VirtualDesktop() for x in xrange(desktop_count)])
        self.Index = collections.deque(range(desktop_count))

    def _move(self, direction):
        self.Desktops.rotate(direction)
        self.Index.rotate(direction)

    def _display_desktop(self, direction):
        self.Desktops[0].hide()
        self._move(direction)
        self.Desktops[0].show()

    def _move_window_to(self, direction, HideWindow=True):
        foreground_window = self.Desktops[0].remove_foreground_window()
        self._move(direction)
        self.Desktops[0].add_window(foreground_window)
        self._move(-direction)

    def display_next(self):
        self._display_desktop(self.__Next)

    def display_previous(self):
        self._display_desktop(self.__Previous)

    def move_window_to_next_desktop(self):
        self._move_window_to(self.__Next)

    def move_window_to_previous_desktop(self):
        self._move_window_to(self.__Previous)

    def move_window_to_next_desktop_and_display(self):
        self._move_window_to(self.__Next)
        self._display_desktop(self.__Next)

    def move_window_to_previous_desktop_and_display(self):
        self._move_window_to(self.__Previous)
        self._display_desktop(self.__Previous)

    def get_current_desktop_number(self):
        return self.Index[0]

    def show_all_windows(self):
        [Desktop.show() for Desktop in self.Desktops]

