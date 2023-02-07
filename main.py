"""Main script for running model using command-line"""


import sys
from decoimpact.business.application import Application
from decoimpact.business.workflow.model_factory import ModelFactory
from decoimpact.crosscutting.i_logger import ILogger
from decoimpact.crosscutting.logger_factory import LoggerFactory
from decoimpact.data.entities.data_access_layer import DataAccessLayer, IDataAccessLayer


def main(input_path: str):
    """Main function to run the application when running via command-line

    Args:
        input_path (str): path to the input file
    """

    # configure logger and data-access layer
    logger: ILogger = LoggerFactory.create_logger()
    da_layer: IDataAccessLayer = DataAccessLayer(logger)

    # create and run application
    application = Application(logger, da_layer, ModelFactory.create_model)
    application.run(input_path)


if __name__ == "__main__":
    main(sys.argv[1])
