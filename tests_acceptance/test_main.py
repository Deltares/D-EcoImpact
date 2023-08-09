"""
Tests for acceptance tests
"""


import subprocess
from pathlib import Path

import pytest
import xarray as _xr

input_files_path = Path(__file__).parent / "input_yaml_files"
input_filenames = [file.name for file in input_files_path.glob("*.yaml")]
main_script_path = (
    Path(__file__).parent.parent / "main.py"
)  # Adjust the path accordingly
reference_files_path = Path(__file__).parent / "reference_nc_files"


@pytest.mark.parametrize("input_filename", input_filenames)
def run_main_and_compare_output_nc_filet(input_filename):
    input_file_path = input_files_path / input_filename

    # Build the subprocess command
    command = ["python", str(main_script_path), str(input_file_path)]

    # Run the script in a separate Python process
    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    stdout, stderr = process.communicate()

    # Check the exit code
    assert (
        process.returncode == 0
    ), f"Script {main_script_path} failed for {input_filename}\n{stderr}"
