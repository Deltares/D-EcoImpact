# This file is part of D-EcoImpact
# Copyright (C) 2022-2023  Stichting Deltares
# This program is free software distributed under the GNU
# Lesser General Public License version 2.1
# A copy of the GNUGeneral Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""Main script for creating executable based on Python source files"""


import PyInstaller.__main__
from pathlib import Path

HERE = Path(__file__).parent.absolute()
path_to_main = str(HERE / ".." / "main.py")

def install():
    PyInstaller.__main__.run([
        path_to_main,
        '--onefile',
        '--windowed',
        # other pyinstaller options... 
    ])