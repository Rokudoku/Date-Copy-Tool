# This setup was made by following along with youtube tutorials by sentdex:
# https://www.youtube.com/watch?v=GSoOwSqTSrs
# and
# https://www.youtube.com/watch?v=HosXxXE24hA

from cx_Freeze import setup, Executable

setup(name = "Date Copy Tool",
      options = {"build_exe": {"packages":["tkinter"]}}
      version = "1.0.0",
      description = "Tool for copying dates to clipboard",
      executables = [Executable("date_copy_tool.py")])
