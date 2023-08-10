"""
Tests for acceptance tests
"""


import subprocess
import sys
from pathlib import Path

import pytest
import xarray as _xr

input_yaml_files_path = Path(__file__).parent / "input_yaml_files"
input_yaml_filenames = [file.name for file in input_yaml_files_path.glob("*.yaml")]
MAIN_SCRIPT_NAME = "main.py"
main_script_path = Path(__file__).parent.parent / MAIN_SCRIPT_NAME
output_nc_files_path = Path(__file__).parent / "output_nc_files"
reference_files_path = Path(__file__).parent / "reference_nc_files"


@pytest.mark.parametrize("input_filename", input_yaml_filenames)
def test_process_input(input_filename):
    """Execute acceptance test using a python subprocess
    using all input yaml files available"""
    input_file_path = input_yaml_files_path / input_filename

    # Build the subprocess command
    command = [sys.executable, str(main_script_path), str(input_file_path)]

    # Run the script in a separate Python process
    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate()

    # do not use stdout ;-)
    if 1 == 0:
        print(stdout)

    # Check the exit code
    assert (
        process.returncode == 0
    ), f"Script {main_script_path} failed for {input_filename}\n{stderr}"

    # Load the generated and reference NetCDF files using xarray
    generated_nc = _xr.open_dataset(
        output_nc_files_path / input_filename.replace(".yaml", ".nc")
    )
    reference_nc = _xr.open_dataset(
        reference_files_path / input_filename.replace(".yaml", ".nc")
    )

    # Compare the datasets
    assert generated_nc.identical(
        reference_nc
    ), f"Generated output does not match reference for {input_filename}"
