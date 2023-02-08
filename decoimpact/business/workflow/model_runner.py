"""
Module for ModelRunner class

Classes:
    ModelRunner

"""

from typing import Any, Callable

from decoimpact.business.entities.i_model import IModel, ModelStatus
from decoimpact.crosscutting.i_logger import ILogger


class ModelRunner:
    """Runner for models"""

    @staticmethod
    def run_model(model: IModel, logger: ILogger) -> bool:
        """Runs the provided model

        Args:
            model (IModel): model to run
        """

        logger.log_info(f'Validating model "{model.name}"')
        ModelRunner._change_state(
            model.validate, model, logger, ModelStatus.VALIDATING, ModelStatus.VALIDATED
        )

        if model.status == ModelStatus.FAILED:
            logger.log_error(f'Validation of model "{model.name}" failed')
            return False

        logger.log_info(f'Initializing model "{model.name}"')
        ModelRunner._change_state(
            model.initialize,
            model,
            logger,
            ModelStatus.INITIALIZING,
            ModelStatus.INITIALIZED,
        )

        if model.status == ModelStatus.FAILED:
            logger.log_error(f'Initialization of model "{model.name}" failed')
            return False

        logger.log_info(f'Executing model "{model.name}"')
        ModelRunner._change_state(
            model.execute, model, logger, ModelStatus.EXECUTING, ModelStatus.EXECUTED
        )

        if model.status == ModelStatus.FAILED:
            logger.log_error(f'Execution of model "{model.name}" failed')
            return False

        logger.log_info(f'Finalizing model "{model.name}"')
        ModelRunner._change_state(
            model.finalize, model, logger, ModelStatus.FINALIZING, ModelStatus.FINALIZED
        )

        if model.status == ModelStatus.FAILED:
            logger.log_error(f'Finalization of model "{model.name}" failed')
            return False

        logger.log_info(f'Model "{model.name}" has successfully finished running')
        return True

    @staticmethod
    def _change_state(
        action: Callable[[], Any],
        model: IModel,
        logger: ILogger,
        pre_status: ModelStatus,
        post_status: ModelStatus,
    ):

        model.status = pre_status

        try:
            return_value = action()

            if isinstance(return_value, bool) and return_value is False:
                model.status = ModelStatus.FAILED
            else:
                model.status = post_status

        except RuntimeError:
            model.status = ModelStatus.FAILED
