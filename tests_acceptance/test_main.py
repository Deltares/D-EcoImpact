# This file is part of D-EcoImpact
# Copyright (C) 2022-2024 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Run all acceptance tests available in the input_yaml_files folder
"""


import subprocess
import sys
from pathlib import Path

import pytest
import xarray as _xr

parent_path = Path(__file__).parent

input_yaml_files_path = parent_path / "input_yaml_files"
input_yaml_filenames = [file.name for file in input_yaml_files_path.glob("*.yaml")]
MAIN_SCRIPT_NAME = "main.py"
main_script_path = parent_path.parent / MAIN_SCRIPT_NAME
output_nc_files_path = parent_path / "output_nc_files"
# Create output folder if not already there
Path(output_nc_files_path).mkdir(exist_ok=True)
reference_files_path = parent_path / "reference_nc_files"


@pytest.mark.parametrize("input_filename", input_yaml_filenames)
def test_process_input(input_filename):
    """Execute acceptance test using a python subprocess
    using all input yaml files available

    Args:
        input_filename (str): name of input file
    """

    input_file_path = input_yaml_files_path / input_filename

    # Build the subprocess command
    command = [sys.executable, str(main_script_path), str(input_file_path)]

    # Run the script in a separate Python process
    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    stdout, stderr = process.communicate()

    # do not use stdout ;-)
    if MAIN_SCRIPT_NAME != "":
        print(stdout)

    # Check the exit code
    assert (
        process.returncode == 0
    ), f"Script {main_script_path} failed for {input_filename}\n{stderr}"

    # Load the generated and reference NetCDF files using xarray
    nc_filename = input_filename.replace(".yaml", ".nc")
    reference_filename = Path(output_nc_files_path, nc_filename)
    filenames_list = reference_filename.parent.glob(reference_filename.name)

    for filename in filenames_list:
        generated_nc = _xr.open_dataset(filename)
        reference_nc = _xr.open_dataset(reference_files_path / filename.name)

        # Compare the datasets if they have matching variables and coordinates
        assert generated_nc.equals(
            reference_nc
        ), f"Generated output does not match reference for {input_filename}"
