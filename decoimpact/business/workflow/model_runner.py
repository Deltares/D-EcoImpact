# This file is part of D-EcoImpact
# Copyright (C) 2022-2025 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
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

        success = True

        success = ModelRunner._change_state(
            model.validate, model, logger, ModelStatus.VALIDATING, ModelStatus.VALIDATED
        )
        success = success and ModelRunner._change_state(
            model.initialize,
            model,
            logger,
            ModelStatus.INITIALIZING,
            ModelStatus.INITIALIZED,
        )
        success = success and ModelRunner._change_state(
            model.execute, model, logger, ModelStatus.EXECUTING, ModelStatus.EXECUTED
        )
        success = success and ModelRunner._change_state(
            model.finalize, model, logger, ModelStatus.FINALIZING, ModelStatus.FINALIZED
        )

        if success:
            part_str = ""
            if model.partition:
                part_str = f" (Partition: {model.partition})"
            logger.log_info(
                f'Model "{model.name}{part_str}" has successfully finished running'
            )

        return success

    @staticmethod
    def _change_state(
        action: Callable[[ILogger], Any],
        model: IModel,
        log: ILogger,
        pre_status: ModelStatus,
        post_status: ModelStatus,
    ) -> bool:

        part_str = ""
        if model.partition:
            part_str = f" (Partition: {model.partition})"

        log.log_info(f'Model "{model.name}{part_str}" -> {str(pre_status)}')
        model.status = pre_status

        success = ModelRunner._change_state_core(action, log)

        if success:
            model.status = post_status
            message = f'Model "{model.name}{part_str}" -> {str(post_status)}'
            log.log_info(message)
            return True

        model.status = ModelStatus.FAILED
        message = (
            f'Model "{model.name}{part_str}" transition from '
            f"{str(pre_status)} to {str(post_status)} has failed."
        )

        log.log_error(message)

        return False

    @staticmethod
    def _change_state_core(action: Callable[[ILogger], Any], logger: ILogger) -> bool:

        try:
            return_value = action(logger)

            if isinstance(return_value, bool) and return_value is False:
                return False

            return True

        except RuntimeError:
            return False
