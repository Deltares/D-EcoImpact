"""
Main script for running model using command-line
"""


from decoimpact.business.workflow.model_factory import ModelFactory
from decoimpact.business.workflow.model_runner import ModelRunner
from decoimpact.crosscutting.logger_factory import LoggerFactory


def main():
    """Main function to execute when running via command-line"""
    logger = LoggerFactory.create_logger()
    model = ModelFactory.create_rule_based_model(logger)

    ModelRunner.run_model(model, logger)


if __name__ == "__main__":
    main()
