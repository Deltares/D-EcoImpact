import argparse
from pathlib import Path


def read_command_line_arguments():
    """Reads the command line arguments given to the tool

    Returns:
        Path: input yaml path
    """
    # Multiline description
    DESCRIPTION = """
    # D-EcoImpact

    # A Python based kernel to perform spatial (environmental) impact assessment. Based on knowledge rules applied to model output and/or measurements.
    # See the README.md for more details

    # Copyright (C) 2022-2023 Stichting Deltares
    # This program is free software distributed under the
    # GNU Affero General Public License version 3.0
    # A copy of the GNU Affero General Public License can be found at
    # https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
    """

    # Initialize parser with the multiline description
    parser = argparse.ArgumentParser(
        description=DESCRIPTION,
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
        exit()
    else:
        parser.print_help()
        exit()
    return input_path
