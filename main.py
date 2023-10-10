# This file is part of D-EcoImpact
# Copyright (C) 2022-2023 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""Main script for running model using command-line"""


import argparse
import sys
from pathlib import Path

from decoimpact.business.application import Application
from decoimpact.business.workflow.model_builder import ModelBuilder
from decoimpact.crosscutting.i_logger import ILogger
from decoimpact.crosscutting.logger_factory import LoggerFactory
from decoimpact.data.entities.data_access_layer import DataAccessLayer, IDataAccessLayer


def main(path: Path):
    """Main function to run the application when running via command-line

    Args:
        input_path (Path): path to the input file
    """

    # configure logger and data-access layer
    logger: ILogger = LoggerFactory.create_logger()
    da_layer: IDataAccessLayer = DataAccessLayer(logger)
    model_builder = ModelBuilder(da_layer, logger)

    # create and run application
    application = Application(logger, da_layer, model_builder)
    application.run(path)


if __name__ == "__main__":

    # Multiline description
    description = """
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
        description=description,
        formatter_class=argparse.RawTextHelpFormatter,
    )

    # Adding optional argument
    parser.add_argument("-i", "--input_file", help="Input yaml file")
    parser.add_argument(
        "input_file_positional",
        nargs="?",
        help="Input yaml file",
    )
    parser.add_argument("-v", "--version", action="store_true", help="Show version")

    # Read arguments from command line
    args = parser.parse_args()

    if args.input_file:
        input_path = Path(args.input_file)
    elif args.input_file_positional:
        input_path = Path(args.input_file_positional)
    elif args.version:
        print("VERSION")
        exit()
    else:
        parser.print_help()
        exit()

    main(input_path)
