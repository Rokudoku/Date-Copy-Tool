# This setup was made by following along with youtube tutorials by sentdex:
# https://www.youtube.com/watch?v=GSoOwSqTSrs
# and
# https://www.youtube.com/watch?v=HosXxXE24hA

### NOTE: ONLY WORKS WITH PYTHON3.4 (tried 3.5 and 3.6)
### created build by opening the location in cmd and typing
### "python34 setup.py build" (after making a python34.exe and setting a PATH
### to the folder)

import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(name = "Date-Copy-Tool",
      options = {"build_exe": {"packages":["tkinter"]}},
      version = "1.0.0",
      description = "Tool for copying dates to clipboard",
      executables = [Executable("date_copy_tool.py", base=base)])


# First attempt resolted in KeyError: 'TCL_Library'.
# The attempted bugfix to force the paths to point to my tcl and tk folders
# resulted in >1600 file large build folder...
