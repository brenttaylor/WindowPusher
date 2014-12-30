from ctypes import windll, byref, create_unicode_buffer, WINFUNCTYPE, c_int
import win32con
import win32gui


def SendMessage(hWnd, Msg, wParam, lParam):
    return windll.user32.SendMessageW(hWnd, Msg, wParam, lParam)


def IsWindowVisible(hWnd):
    return windll.user32.IsWindowVisible(hWnd)


def EnumWindows(lpEnumFunc, lParam):
    EnumWindowsProc = WINFUNCTYPE(c_int, c_int, c_int)
    windll.user32.EnumWindows(EnumWindowsProc(lpEnumFunc), lParam)


def RegisterHotKey(hWnd, evt_id, modifier, key):
    return windll.user32.RegisterHotKey(hWnd, evt_id, modifier, key)


def UnregisterHotKey(hWnd, evt_id):
    windll.user32.UnregisterHotKey(hWnd, evt_id)


def ShowWindow(hWnd, nCmdShow):
    windll.user32.ShowWindow(hWnd, nCmdShow)


def GetForegroundWindow():
    return windll.user32.GetForegroundWindow()


def GetWindowThreadProcessId(hWnd):
    processID = None
    windll.user32.GetWindowThreadProcessId(hWnd, processID)
    return processID


def SetActiveWindow(hWnd):
    return windll.user32.SetActiveWindow(hWnd)


def SetForegroundWindow(hWnd):
    return windll.user32.SetForegroundWindow(hWnd)


def GetForegroundWindow():
    return windll.user32.GetForegroundWindow()
