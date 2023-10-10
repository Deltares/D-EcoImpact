# This file is part of D-EcoImpact
# Copyright (C) 2022-2023 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""Main script for creating executable based on Python source files"""


from pathlib import Path

import PyInstaller.__main__

HERE = Path(__file__).parent.absolute()
PATH_TO_MAIN = str(HERE / ".." / "main.py")


def install():
    PyInstaller.__main__.run(
        [
            PATH_TO_MAIN,
            "--onefile",
            "--windowed",
            "-ndecoimpact"
            # other pyinstaller options...
        ]
    )
