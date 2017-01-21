# This setup was made by following along with youtube tutorials by sentdex:
# https://www.youtube.com/watch?v=GSoOwSqTSrs
# and
# https://www.youtube.com/watch?v=HosXxXE24hA

# I also had an error - KeyError: 'TCL_LIBRARY' which I found the fix for:
# http://stackoverflow.com/questions/34939356/python-pygame-exe-build-with-cx-freeze-tcl-library-error

from cx_Freeze import setup, Executable
import os

os.environ['TCL_LIBRARY'] = "C:\\Users\\Jerome\\AppData\\Local\\Programs" \
                            "\\Python\\Python35\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "C:\\Users\\Jerome\\AppData\\Local\\Programs" \
                           "\\Python\\Python35\\tcl\\tk8.6"

setup(name = "Date Copy Tool",
      options = {"build_exe": {"packages":["tkinter"]}},
      version = "1.0.0",
      description = "Tool for copying dates to clipboard",
      executables = [Executable("date_copy_tool.py")])
