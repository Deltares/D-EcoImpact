# This file is part of D-EcoImpact
# Copyright (C) 2022-2023 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""Main script for creating executable based on Python source files"""


from pathlib import Path

import PyInstaller.__main__  # pylint: disable=import-error, no-name-in-module

# MDK: thess warnings are disabled on purpose. Using PyInstaller.__main__
# comes directly from the documentation of PyInstaller.

HERE = Path(__file__).parent.absolute()
PATH_TO_MAIN = str(HERE / "main.py")


def install():
    """Function to create self-contained executable out of python files.
    Function can be called from command line using a poetry function.
    Contains settings for pyinstaller."""

    # MDK: this warning is disabled on purpose. Using PyInstaller.__main__
    # comes directly from the documentation of PyInstaller.

    # pylint: disable=maybe-no-member
    PyInstaller.__main__.run(
        [
            PATH_TO_MAIN,
            "--name=decoimpact",
            "--onefile",
            "--console",
            # other pyinstaller options...
        ]
    )
