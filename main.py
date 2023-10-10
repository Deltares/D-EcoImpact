# This file is part of D-EcoImpact
# Copyright (C) 2022-2023 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""Main script for running model using command-line"""


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
    input_path = Path(sys.argv[1])
    main(input_path)
