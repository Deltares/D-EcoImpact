"""
Tests for acceptance tests
"""


import runpy
import sys
from pathlib import Path

import pytest

input_files_path = Path(__file__).parent / "input_yaml_files"
input_filenames = [file.name for file in input_files_path.glob("*.yaml")]
main_script_name = "main.py"


@pytest.mark.parametrize("input_filename", input_filenames)
def test_process_input(input_filename):
    input_file_path = input_files_path / input_filename

    # Set up command line arguments for the script
    sys.argv = ["", input_file_path]
    print("QQ", sys.argv)
    print("QQ", sys.argv)
    # Run the script within the same Python process
    result = runpy.run_path(main_script_name)

    assert result is not None, f"Script {main_script_name} failed for {input_filename}"
