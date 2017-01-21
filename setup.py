# This setup was made by following along with a youtube tutorial by sentdex:
# (https://www.youtube.com/watch?v=GSoOwSqTSrs)

from cx_Freeze import setup, Executable

setup(name="Date Copy Tool",
      version="1.0.0",
      description="Tool for copying dates to clipboard",
      executables = [Executable("date_copy_tool.py")])
