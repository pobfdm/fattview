##usage python freeze.py build

import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os","sys", "utils", "urllib","fpdf"], "excludes": ["tkinter"]}


exe1 = Executable(
    script = "fattview.py",
    targetName = "fattview.exe",
    icon = "icon.ico",
    base = "Win32GUI",
)

setup(  name = "fatview",
        version = "0.1",
        description = "Un semplice visualizzatore di fatture elettroniche.",
        options = {"build_exe": build_exe_options},
        executables = [exe1]
        )
