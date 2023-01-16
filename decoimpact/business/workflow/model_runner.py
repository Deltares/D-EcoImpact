"""
Module for ModelRunner class

Classes:
    ModelRunner

"""

from decoimpact.business.entities.model_base import ModelBase, ModelStatus
from decoimpact.crosscutting.logger_factory import Logger


class ModelRunner:
    """Runner for models"""

    @staticmethod
    def run_model(model: ModelBase, logger: Logger) -> bool:
        """Runs the provided model

        Args:
            model (ModelBase): model to run
        """

        logger.log_info(f"Validating model \"{model.name}\"")
        ModelRunner._change_state(
            model.validate,
            model,
            ModelStatus.VALIDATING,
            ModelStatus.VALIDATED
            )

        if model.status == ModelStatus.FAILED:
            logger.log_error(f"Validation of model \"{model.name}\" failed")
            return False

        logger.log_info(f"Initializing model \"{model.name}\"")
        ModelRunner._change_state(
            model.initialize,
            model,
            ModelStatus.INITIALIZING,
            ModelStatus.INITIALIZED
            )

        if model.status == ModelStatus.FAILED:
            logger.log_error(f"Initialization of model \"{model.name}\" failed")
            return False

        logger.log_info(f"Executing model \"{model.name}\"")
        ModelRunner._change_state(
            model.execute,
            model,
            ModelStatus.EXECUTING,
            ModelStatus.EXECUTED
            )

        if model.status == ModelStatus.FAILED:
            logger.log_error(f"Execution of model \"{model.name}\" failed")
            return False

        logger.log_info(f"Finalizing model \"{model.name}\"")
        ModelRunner._change_state(
            model.finalize,
            model,
            ModelStatus.FINALIZING,
            ModelStatus.FINALIZED
            )

        if model.status == ModelStatus.FAILED:
            logger.log_error(f"Finalization of model \"{model.name}\" failed")
            return False

        logger.log_info(f"Model \"{model.name}\" has successfully finished running")
        return True

    @staticmethod
    def _change_state(
            action,
            model: ModelBase,
            pre_status: ModelStatus,
            post_status: ModelStatus
            ):

        model.status = pre_status

        try:
            action()
            model.status = post_status
        except Exception:
            model.status = ModelStatus.FAILED
