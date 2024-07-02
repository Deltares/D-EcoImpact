# This file is part of D-EcoImpact
# Copyright (C) 2022-2024 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Tests for ModelRunner class
"""

from unittest.mock import Mock
import pytest
from decoimpact.business.entities.i_model import ModelStatus
from decoimpact.business.workflow.model_runner import ModelRunner


def test_run_model_with_valid_model_should_pass_all_model_stages():
    """Test a valid model goes through all the ModelStatus states
    (except for Failed state) during a run"""

    # Arrange
    model = Mock()
    logger = Mock()

    # Act
    success = ModelRunner.run_model(model, logger)

    # Assert
    assert success
    assert model.status == ModelStatus.FINALIZED


def test_run_model_with_invalid_model_should_fail():
    """Test that model runner puts an invalid model (a model that
    fails the validate method) into the Failed model state during run_model"""

    # Arrange
    logger = Mock()
    model = Mock()

    model.validate.return_value = False

    # Act
    success = ModelRunner.run_model(model, logger)

    # Assert
    assert success is False
    assert model.status == ModelStatus.FAILED


@pytest.mark.parametrize(
    "method",
    [
        "initialize",
        "execute",
        "finalize",
    ],
)
def test_run_model_with_model_throwing_exception_should_fail(method: str):
    """Test that model runner puts the model into the Failed state
    if an error occurred during the execution of the provided method"""

    # Arrange
    logger = Mock()
    model = Mock()

    method = getattr(model, method)
    method.side_effect = RuntimeError()

    model.validate.return_value = True

    # Act
    success = ModelRunner.run_model(model, logger)

    # Assert
    assert success is False
    assert model.status == ModelStatus.FAILED
