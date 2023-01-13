"""
Module for ModelRunner class

Classes:
    ModelRunner

"""

from decoimpact.business.entities.model_base import ModelBase, ModelStatus


class ModelRunner:
    """Runner for models"""

    @staticmethod
    def run_model(model: ModelBase, logger: Logger) -> bool:
        """Runs the provided model

        Args:
            model (ModelBase): model to run
        """

        ModelRunner._change_state(
            model.validate,
            model,
            ModelStatus.VALIDATING,
            ModelStatus.VALIDATED
            )

        if model.status == ModelStatus.FAILED:
            return False

        ModelRunner._change_state(
            model.initialize,
            model,
            ModelStatus.INITIALIZING,
            ModelStatus.INITIALIZED
            )

        if model.status == ModelStatus.FAILED:
            return False

        ModelRunner._change_state(
            model.execute,
            model,
            ModelStatus.EXECUTING,
            ModelStatus.EXECUTED
            )

        if model.status == ModelStatus.FAILED:
            return False

        ModelRunner._change_state(
            model.finalize,
            model,
            ModelStatus.FINALIZING,
            ModelStatus.FINALIZED
            )

        return model.status == ModelStatus.FAILED

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
