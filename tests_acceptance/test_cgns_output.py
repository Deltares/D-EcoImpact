# This file is part of D-EcoImpact
# Copyright (C) 2022-2025 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""End-to-end CGNS output through the normal YAML application workflow."""

from unittest.mock import Mock

import h5py
import numpy as np
import yaml

from decoimpact.business.application import Application
from decoimpact.business.workflow.model_builder import ModelBuilder
from decoimpact.crosscutting.i_logger import ILogger
from decoimpact.data.entities.cgns_reader import CGNSReader
from decoimpact.data.entities.data_access_layer import DataAccessLayer
from tests.data.entities.test_cgns_reader import _create_cgns_file


def test_partitioned_cgns_outputs_use_their_own_source_template(tmp_path):
    for index in (1, 2):
        source = tmp_path / f"input_{index}.cgns"
        _create_cgns_file(source, time_dependent=False)
        with h5py.File(source, "a") as cgns:
            cgns["Base/Zone/GridCoordinates/CoordinateX/ data"][:] *= index
            cgns["Base/Zone/Sol1/Pressure/ data"][:] *= index

    configuration = {
        "version": "0.0.0",
        "input-data": [
            {
                "dataset": {
                    "filename": str(tmp_path / "input_*.cgns"),
                    "variable_mapping": {"Pressure": "pressure"},
                },
            }
        ],
        "rules": [
            {
                "multiply_rule": {
                    "name": "Multiply pressure",
                    "description": "Scale the spatial snapshot",
                    "multipliers": [2.0],
                    "input_variable": "pressure",
                    "output_variable": "result",
                },
            }
        ],
        "output-data": {
            "filename": str(tmp_path / "output_*.cgns"),
            "save_only_variables": ["result"],
        },
    }
    input_yaml = tmp_path / "model.yaml"
    input_yaml.write_text(yaml.safe_dump(configuration), encoding="utf-8")
    logger = Mock(ILogger)
    data_layer = DataAccessLayer(logger)
    Application(logger, data_layer, ModelBuilder(data_layer, logger)).run(input_yaml)

    logger.log_error.assert_not_called()
    outputs = sorted(tmp_path.glob("output_*.cgns"))
    assert [path.name for path in outputs] == ["output_1.cgns", "output_2.cgns"]
    for index, output in enumerate(outputs, start=1):
        written = CGNSReader(logger).read_file(output)
        assert set(written.data_vars) == {"result"}
        np.testing.assert_array_equal(written["result"], np.array([2.0, 4.0]) * index)
        with h5py.File(output, "r") as cgns:
            np.testing.assert_array_equal(
                cgns["Base/Zone/GridCoordinates/CoordinateX/ data"],
                np.arange(4.0) * index,
            )
