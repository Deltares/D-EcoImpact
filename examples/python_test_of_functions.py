import xarray as _xr

from decoimpact.business.entities.rule_based_model import RuleBasedModel
from decoimpact.business.entities.rules.multiply_rule import MultiplyRule
from decoimpact.business.entities.rules.layer_filter_rule import LayerFilterRule
from decoimpact.business.entities.rules.time_aggregation_rule import TimeAggregationRule
from decoimpact.business.entities.rules.step_function_rule import StepFunctionRule
from decoimpact.business.entities.rules.response_rule import ResponseRule
from decoimpact.data.api.time_operation_type import TimeOperationType
from decoimpact.business.workflow.model_runner import ModelRunner
from decoimpact.crosscutting.i_logger import ILogger
from decoimpact.crosscutting.logger_factory import LoggerFactory


class ScreenLogger(ILogger):
    """Logger implementation based on default logging library"""

    def __init__(self) -> None:
        super().__init__()

    def log_error(self, message: str) -> None:
        print("error:" + message)

    def log_warning(self, message: str) -> None:
        print("warning:" + message)

    def log_info(self, message: str) -> None:
        print("info:" + message)

    def log_debug(self, message: str) -> None:
        pass


# create an instance of a logger
logger: ILogger = ScreenLogger()

# read input dataset
inputPath = "data/FM-VZM_0000_map.nc"
inputDataset: _xr.Dataset = _xr.open_dataset(inputPath, mask_and_scale=True)

# create rules
rule1 = MultiplyRule("multiply rule", ["mesh2d_sa1"], [0.0018066, 1e5], "chloride")
rule2 = LayerFilterRule("layer filter rule", ["chloride"], 22, "chloride_top_layer")
rule3 = TimeAggregationRule("get average chloride level", ["chloride_top_layer"],TimeOperationType.AVERAGE, "year","chloride_top_layer_year")
rule4 = StepFunctionRule("step function rule", "chloride_top_layer_year", [-999.0, 0.0, 450.0, 999.0], [0.0, 1.0, 0.0, 0.0], "chloride_policy")
rule5 = ResponseRule("response rule", "chloride_top_layer_year", [-999.0, 0.0,0.0001, 300.0, 450.0, 600.0, 999.0], [0.0,0.0,1.0,0.8,0.4, 0.0, 0.0],"HSI_chloride")

# create model
model = RuleBasedModel([inputDataset], [rule1,rule2, rule3, rule4, rule5], name="my new model")

# run model
ModelRunner.run_model(model, logger)

# write output to netcdf
model.output_dataset.to_netcdf("data_out/test_python_output_file.nc", format="NETCDF4")