import xarray as _xr

from decoimpact.business.entities.rule_based_model import RuleBasedModel
from decoimpact.business.entities.rules.multiply_rule import MultiplyRule
from decoimpact.business.entities.rules.layer_filter_rule import LayerFilterRule
from decoimpact.business.entities.rules.time_aggregation_rule import TimeAggregationRule
from decoimpact.business.entities.rules.step_function_rule import StepFunctionRule
from decoimpact.business.entities.rules.response_curve_rule import ResponseCurveRule
from decoimpact.business.entities.rules.combine_results_rule import CombineResultsRule
from decoimpact.business.entities.rules.formula_rule import FormulaRule
from decoimpact.data.api.time_operation_type import TimeOperationType
from decoimpact.business.entities.rules.multi_array_operation_type import MultiArrayOperationType
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

# read input dataset - Repeat "test_VKZM_simple_testcase.yaml"
inputPath = "data/ems_0003_map.nc"
inputDataset: _xr.Dataset = _xr.open_dataset(inputPath, mask_and_scale=True)

# create rules
#GET SEDIMENT FRACTIONS
rule1A = LayerFilterRule("Get sand layer", ["mesh2d_bodsed"], 1, "nSedTot", "sand1_kgm2")
rule1B = LayerFilterRule("Get mud1 layer", ["mesh2d_bodsed"], 2, "nSedTot", "mud1_kgm2")
rule1C = LayerFilterRule("Get mud2 layer", ["mesh2d_bodsed"], 3, "nSedTot", "mud2_kgm2")

# Determine ZES.1 SaltClass
rule2A = TimeAggregationRule("Mean salinity", ["mesh2d_sa1"],TimeOperationType.AVERAGE, "year","mean_salinity_PSU")
rule2B = StepFunctionRule("Mean salinity class", "mean_salinity_PSU", [-999.0, 0.5, 18.0, 999.0], [0.0, 1.0, 2.0, 2.0], "SaltClass")

# Determine ZES.1 SaltVarib
rule3A = TimeAggregationRule("Standard deviation salinity", ["mesh2d_sa1"],TimeOperationType.STDEV, "year","std_salinity_PSU")
rule3B = FormulaRule("formula_rule chloride", ["std_salinity_PSU","mean_salinity_PSU"], "std_salinity_PSU / mean_salinity_PSU", "salinity_variability")
rule3C = StepFunctionRule("Salinity variability class", "salinity_variability", [-999.0, 0.25, 999.0], [0.0, 1.0, 1.0], "SaltVarib")

# Determine ZES.1 HardSubCod
# MASK SHOULD BE PROVIDED IN DATA (1 or None) or data should be limited to mask beforehand

# Determine ZES.1 LitoralCod
# FUNCTIONALITY TO GIVE TIME DURATION NOT YET IMPLEMENTED
# rule4A = TimeAggregationRule("Low tide", ["mesh2d_s1"],TimeOperationType.MIN, 12.42 h (tide cycle) ,"year","low_water_mNAP")
rule4A = TimeAggregationRule("Low tide", ["mesh2d_s1"],TimeOperationType.MIN, "month","low_water_mNAP")
rule4B = TimeAggregationRule("Mean Low tide", ["low_water_mNAP"],TimeOperationType.AVERAGE, "year","mean_low_water_mNAP")
rule4C = FormulaRule("Mean Low tide minus 5 meters",["mean_low_water_mNAP"], "mean_low_water_mNAP - 5", "mean_low_water_minus_5_mNAP")
# Currently the FormulaRule does not allow operations between arrays of different axes.
#rule4D = FormulaRule("deep sublittoral ",["mesh2d_mor_bl","mean_low_water_minus_5_mNAP"], "mesh2d_mor_bl < mean_low_water_minus_5_mNAP", "deep_sublittoral")
rule4D1 = TimeAggregationRule("calculate bottom level", ["mesh2d_mor_bl"], TimeOperationType.AVERAGE, "year","mean_bottomlevel_mNAP")
rule4D2 = FormulaRule("deep sublittoral ",["mean_bottomlevel_mNAP","mean_low_water_minus_5_mNAP"], "mean_bottomlevel_mNAP < mean_low_water_minus_5_mNAP", "deep_sublittoral")
rule4E = StepFunctionRule("Dry land", "mesh2d_s1", [-999.0, 0.001, 999.0], [1.0, 1.0, 0.0], "dry_time")
rule4F = TimeAggregationRule("Exposure", ["dry_time"],TimeOperationType.AVERAGE, "year","exposure_time")
rule4G = StepFunctionRule("Littoral class minus sublittoral", "exposure_time", [0.0, 0.04, 0.25, 0.75, 0.85, 1.0], [0.0, 2.0, 3.0, 4.0, 5.0, 5.0], "LitoralCod_min_sublittoral")
rule4H = FormulaRule("Sublittoral ",["exposure_time"], "exposure_time <= 0.04", "sublittoral")
rule4I = CombineResultsRule("Sublittoral classes", ["sublittoral","deep_sublittoral"],MultiArrayOperationType.SUBTRACT,"sub_littoral_classes")
rule4J = CombineResultsRule("Littoral class", ["LitoralCod_min_sublittoral","sub_littoral_classes"],MultiArrayOperationType.ADD,"LitoralCod")

# Determine ZES.1 Hydrodynamics class
rule5A = TimeAggregationRule("max current velocity", ["mesh2d_ucmag"],TimeOperationType.MAX, "year","max_flowvelocity_ms")
rule5B = FormulaRule("Hydrodynamics class",["max_flowvelocity_ms"], "max_flowvelocity_ms >= 0.8", "DynamicCod")

# Determine ZES.1 sediment composition class
rule6A = CombineResultsRule("Mass of mud", ["mud1_kgm2","mud2_kgm2"],MultiArrayOperationType.ADD,"mud_kgm2")
rule6B = CombineResultsRule("Total mass of sediment", ["mud_kgm2","sand1_kgm2"],MultiArrayOperationType.ADD,"sediment_kgm2")
rule6C = FormulaRule("Fraction mud",["mud_kgm2","sediment_kgm2"], "mud_kgm2 / sediment_kgm2","mud_frac")
rule6D = StepFunctionRule("Sediment composition class", "mud_frac", [0.0, 0.25, 1.0], [2.0, 1.0, 1.0], "SedCode")

# create model
model = RuleBasedModel([inputDataset], [rule1A, rule1B, rule1C,\
                                        rule2A, rule2B,\
                                        rule3A, rule3B, rule3C,\
                                        rule4A, rule4B, rule4C, rule4D1, rule4D2, rule4E,\
                                        rule4F, rule4G, rule4H, rule4I,  rule4J,\
                                        rule5A, rule5B,\
                                        rule6A, rule6B, rule6C, rule6D
                                        ], name="my new model")

# run model
ModelRunner.run_model(model, logger)

# write output to netcdf
model.output_dataset.to_netcdf("data_out/RESTCOAST_python_output_file.nc", format="NETCDF4")