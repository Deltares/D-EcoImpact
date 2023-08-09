"""
Tests for acceptance tests
"""

import pathlib
import runpy
import sys

import pytest

input_files = pathlib.Path(__file__, "..", "data").resolve().glob("*.yaml")
script = pathlib.Path(__file__, "..", "main.py")


# @pytest.mark.parametrize("input_file", input_files)
# def test_script_execution(script, input_file):
#     sys.argv = ["", input_file]
#     runpy.run_path(script)


# def pytest_collect_yaml_file(parent, path):
#     p = pathlib.Path(str(path))
#     if p.suffix == ".yaml" and p.parent.name == "data":
#         return Script(path, parent)


# class Script(pytest.File):
#     def collect(self):
#         yield ScriptItem(self.name, self)


# class ScriptItem(pytest.Item):
#     def runtest(self):
#         runpy.run_path(self.fspath)

#     def repr_failure(self, excinfo):
#         excinfo.traceback = excinfo.traceback.cut(path=self.fspath)
#         return super().repr_failure(excinfo)


# def test_running_application():
#     """Test running application for test file"""

#     # Arrange
#     logger = Mock(ILogger)
#     data_layer = Mock(IDataAccessLayer)
#     model: IModel = Mock(IModel)
#     model_builder = Mock(IModelBuilder)

#     model.name = "Test model"
#     model_builder.build_model.return_value = model

#     application = Application(logger, data_layer, model_builder)

#     # Act
#     application.run("Test.yaml")

#     # Assert
#     expected_message = 'Model "Test model" has successfully finished running'
#     logger.log_info.assert_called_with(expected_message)

#     model.validate.assert_called()
#     model.initialize.assert_called()
#     model.execute.assert_called()
#     model.finalize.assert_called()
#     # assert
