# This file is part of D-EcoImpact
# Copyright (C) 2022-2024 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Module for command line utils
"""
import argparse
import sys
from pathlib import Path

from decoimpact.business.utils.version_utils import read_version_number

# Multiline description
PROGRAM_DESCRIPTION = """
# D-EcoImpact

# A Python based kernel to perform spatial ecological impact assessment.
# Based on knowledge rules applied to model output and/or measurements.

# For more details see the README.md found at
# https://github.com/Deltares/D-EcoImpact/blob/main/README.md

# Copyright (C) 2022-2024 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""


def read_command_line_arguments():
    """Reads the command line arguments given to the tool

    Returns:
        Path: input yaml path
    """

    # Initialize parser with the multiline description
    parser = argparse.ArgumentParser(
        description=PROGRAM_DESCRIPTION,
        formatter_class=argparse.RawTextHelpFormatter,
    )

    # Adding optional argument
    parser.add_argument(
        "input_file",
        nargs="?",
        help="Input yaml file",
    )
    parser.add_argument("-v", "--version", action="store_true", help="Show version")

    # Read arguments from command line
    args = parser.parse_args()

    if args.input_file:
        input_path = Path(args.input_file)
    elif args.version:
        version = read_version_number()
        print("D-EcoImpact version:", version)
        sys.exit()
    else:
        print("\nNo inputfile given. Exiting. \n")
        parser.print_help()
        sys.exit()
    return input_path
