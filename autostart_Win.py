# script to add your exe to startup without showing it in the startup menu in settings

# pip install pywin32 winshell

import os
import winshell
from win32com.client import Dispatch

# Path to your executable
exe_path = r"C:\path\to\your\executable.exe"

# Path to the shortcut
shortcut_path = os.path.join(winshell.startup(), "YourApp.lnk")
# The shortcut is already copied to the startup folder in the code above. The winshell.startup() function returns the path to the startup folder.
#you can rename YourApp.lnk in you want to specify a different name for the shortcut file.

# Create the shortcut
shell = Dispatch('WScript.Shell')
shortcut = shell.CreateShortCut(shortcut_path)
shortcut.Targetpath = exe_path
shortcut.WindowStyle = 7  # 7 means hidden window
shortcut.save()