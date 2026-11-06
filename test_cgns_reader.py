# This file is part of D-EcoImpact
# Copyright (C) 2022-2025 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Test script for CGNS reader

This script tests the CGNS reader with example.cgns file
"""

import os
import sys
from pathlib import Path

script_dir = os.path.dirname(__file__)
sys.path.insert(0, script_dir)

from decoimpact.crosscutting.logging_logger import LoggingLogger
from decoimpact.data.entities.cgns_reader import CGNSReader


def test_cgns_reader():
    """Test CGNS reader with example file"""
    logger = LoggingLogger()

    INPUT_PATH = os.path.join(
        script_dir, "tests_acceptance/input_cgns_files/example.cgns"
    )
    cgns_file = Path(INPUT_PATH)

    if not cgns_file.exists():
        print(f"ERROR: CGNS file not found: {cgns_file}")
        return

    print(f"Testing CGNS reader with {cgns_file}")
    print("=" * 60)

    reader = CGNSReader(logger)

    variable_names = ["Pressure"]

    try:
        dataset = reader.read_file(
            cgns_file,
            variable_names,
        )
        print("SUCCESS: Dataset loaded successfully")
        print(f"Dataset structure:\n{dataset}")
        print(f"\nData variables: {list(dataset.data_vars)}")
        print(f"Coordinates: {list(dataset.coords)}")
    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    test_cgns_reader()
