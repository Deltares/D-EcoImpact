"""Main script for running model using command-line"""


import sys
from pathlib import Path

from decoimpact.business.application import Application
from decoimpact.business.workflow.model_factory import ModelFactory
from decoimpact.crosscutting.i_logger import ILogger
from decoimpact.crosscutting.logger_factory import LoggerFactory
from decoimpact.data.entities.data_access_layer import DataAccessLayer, IDataAccessLayer


def main(input_path: str, output_path: Path):
    """Main function to run the application when running via command-line

    Args:
        input_path (str): path to the input file
        output_path (Path): path to the input file
    """

    # configure logger and data-access layer
    logger: ILogger = LoggerFactory.create_logger()
    da_layer: IDataAccessLayer = DataAccessLayer(logger)

    # CONVERT input_path TO PATHS! TO DO

    # create and run application
    application = Application(logger, da_layer, ModelFactory.create_model)
    application.run(input_path, output_path)


if __name__ == "__main__":
    # input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])
    main(sys.argv[1], output_path)
