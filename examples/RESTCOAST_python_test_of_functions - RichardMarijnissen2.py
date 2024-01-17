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
inputPath = r"preprocessing/ems_deco_prep.nc"
inputDataset: _xr.Dataset = _xr.open_dataset(inputPath, mask_and_scale=True)

# create rules
#GET SEDIMENT FRACTIONS
rule1A = LayerFilterRule("Get ssc mud1 layer", ["mesh2d_sedfrac_concentration"], 2, "nSedSus", "mud1_kgm3")
rule1B = LayerFilterRule("Get ssc mud2 layer", ["mesh2d_sedfrac_concentration"], 3, "nSedSus", "mud2_kgm3")

#COMPUTE TIDAL PARAMETERS
rule1C = CustomTimeAxis("A new time axis for semidiurnal tidal statistics", 12.42, "hours", "tidal_cycle") # format CustomTimeAxis([Description], [duration], [unit], [name])
rule1D = CustomTimeAxis("A new time axis for spring-neap tidal statistics", 29.531, "days", "spring_neap_cycle") # format CustomTimeAxis([Description], [duration], [unit], [name])
rule1E = TimeAggregationRule("High tide", ["mesh2d_s1"], TimeOperationType.MAX, "tidal_cycle", "high_tide_mNAP")
rule1F = TimeAggregationRule("Low tide",  ["mesh2d_s1"], TimeOperationType.MIN, "tidal_cycle", "low_tide_mNAP")
rule1G = TimeAggregationRule("High water spring", ["high_tide_mNAP"], TimeOperationType.MAX, "spring_neap_cycle", "high_water_spring_mNAP")
rule1H = TimeAggregationRule("High water neap", ["high_tide_mNAP"], TimeOperationType.MIN, "spring_neap_cycle", "high_water_neap_mNAP")
rule1I = TimeAggregationRule("Low water spring", ["low_tide_mNAP"], TimeOperationType.MIN, "spring_neap_cycle", "low_water_spring_mNAP")
rule1J = TimeAggregationRule("Low water neap", ["low_tide_mNAP"], TimeOperationType.MAX, "spring_neap_cycle", "low_water_neap_mNAP")
rule1K = TimeAggregationRule("Mean high water", ["high_tide_mNAP"], TimeOperationType.AVERAGE, "year", "MHW_mNAP")
rule1L = TimeAggregationRule("Mean low water",  ["low_tide_mNAP"], TimeOperationType.AVERAGE, "year", "MLW_mNAP")
rule1M = TimeAggregationRule("Mean high water spring", ["high_water_spring_mNAP"], TimeOperationType.AVERAGE, "year", "MHWS_mNAP")
rule1N = TimeAggregationRule("Mean high water neap",  ["high_water_neap_mNAP"], TimeOperationType.AVERAGE, "year", "MHWN_mNAP")
rule1O = TimeAggregationRule("Mean low water spring", ["low_water_spring_mNAP"], TimeOperationType.AVERAGE, "year", "MLWS_mNAP")
rule1P = TimeAggregationRule("Mean low water neap",  ["low_water_neap_mNAP"], TimeOperationType.AVERAGE, "year", "MLWN_mNAP")

#COMPUTE INUNDATION PARAMETERS
rule1Q = StepFunctionRule("Dry land", "mesh2d_waterdepth", [-999.0, 0.001, 999.0], [1.0, 0.0, 0.0], "dry_time")
rule1R = FormulaRule("Flooded", ["dry_time"], "1 - dry_time", "flooded")
rule1S = TimeAggregationRule("Exposure", ["dry_time"],TimeOperationType.AVERAGE, "year", "exposure_frac")
rule1T = FormulaRule("Inundation", ["exposure_time"], "1 - exposure_time", "inundation_frac")

rule1U = DerrivativeRule("Flood Drying Events", ["flooded"], NumericalDerrivative.FORWARD, "dE_dt")
rule1V = FormulaRule("Flood Events", ["dE_dt"], "dE_dt > 0", "dE_dt_greater_0")
rule1W = TimeAggregationRule("Number of flood events", ["dE_dt_greater_0"], TimeOperationType.SUM, "year", "nFloods_year")

# Background detecting number of inundations with derrivative:
# Suppose the inundation variable is
# E          = [0 0 0   1 1 1 1  1   0 0 0   1] then the change (or derivative) is calculated with the forward scheme (x_{i+1] - x_{i}) / dt. Assuming dt =1 you get:
# dE/dt      = [0 0 0.5 0 0 0 0 -0.5 0 0 0.5 0]
# By scanning which entries are  positive and which are negative you get the timesteps during which flooding or drying occurred.
# (dE/dt > 0) = [0 0 1 0 0 0 0 0 0 0 1 0] ; # flooding
# (dE/dt < 0) = [0 0 0 0 0 0 0 1 0 0 0 0] l # drying
# With a sum in the time aggregation rule the  number of flood events is detected:
# SUM(dE/dt > 0) = 2
# With a sum in the time aggregation rule the  number of dry events is detected:
# SUM(dE/dt < 0) = 1

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
rule4A = StepFunctionRule("Littoral class minus sublittoral", "exposure_time", [0.0, 0.04, 0.25, 0.40, 0.85, 1.0], [0.0, 1.0, 2.0, 3.0, 4.0, 5.0], "LitoralCod_min_sublittoral")
rule4B = TimeAggregationRule("calculate bottom level", ["mesh2d_mor_bl"], TimeOperationType.AVERAGE, "year","mean_bottomlevel_mNAP")
rule4C = FormulaRule("Shallow sublittoral",["mean_bottomlevel_mNAP","MLWS_mNAP"], "mean_bottomlevel_mNAP < (MLWS_mNAP - 5.0)", "shallow_sublittoral")
rule4D = CombineResultsRule("Littoral class", ["LitoralCod_min_sublittoral", "shallow_sublittoral"],MultiArrayOperationType.ADD,"LitoralCod")

# Determine ZES.1 Hydrodynamics class
rule5A = TimeAggregationRule("max current velocity", ["mesh2d_ucmag"],TimeOperationType.MAX, "year","max_flowvelocity_ms")
rule5B = FormulaRule("Hydrodynamics class",["max_flowvelocity_ms"], "max_flowvelocity_ms >= 0.8", "DynamicCod")

# Determine ZES.1 sediment composition class
rule6A = TimeAggregationRule("Compute the year average bed composition", ["mesh2d_mudfrac"], TimeOperationType.AVERAGE, "year","mean_mud_frac")
rule6B = StepFunctionRule("Sediment composition class 1 and 2", "mean_mud_frac", [0.0, 0.25, 1.0], [2.0, 1.0, 1.0], "SedCode1_2")
rule6C = TimeAggregationRule("Compute average bed shear stress", ["mesh2d_taub"], TimeOperationType.AVERAGE, "year","mean_taub")
rule6D = FormulaRule("Determine Sed Code 3", ["SedCode1_2", "mean_taub"], "(SedCode1_2 == 2.0) & (mean_taub > 0.18)", "SedCode3")
rule6E = CombineResultsRule("SedCode", ["SedCode1_2", "SedCode3"], MultiArrayOperationType.ADD,"SedCode")

# Determine ZES.1 Salt Marsh class
rule7A = StepFunctionRule("Salt marsh inundation class", "nFloods_year", [0.0, 5.0, 50.0, 150, 300, 9999999999999999], [4.0, 3.0, 2.0, 1.0, 0.0, 0.0], "SaltMarshC_min1")
rule7B = FormulaRule("Add no vegetation category", ["SaltMarshC_min1", "MHWN_mNAP", "mean_bottomlevel_mNAP"], "SaltMarshC_min1 + (MHWN_mNAP < mean_bottomlevel_mNAP)", "SaltMarshC")

# Classify EUNIS Ecotopes with ZES.1 classes
rule8  = ClassificationRule("EUNIS_ecotopes",
                            [[    "output", "LitoralCod", "SedCode", "SaltClass", "SaltMarshC"],
                             [     "MC521",          "0",       "-",         "-",          "-"],
                             [     "MB523",          "1",       "-",         "2",          "-"],
                             [     "MB524",          "1",       "-",        "<2",          "-"],
                             [      "MB52",         ">1",   "0 | 2",         "-",          "-"],
                             [     "MB621",         ">1",       "1",         "2",          "-"],
                             [     "MB622",         ">1",       "1",        "<2",          "-"],
                             [     "MA321",         ">1",       "1",         "2",          "-"],
                             [     "MA322",         ">1",       "1",        "<2",          "-"],
                             [     "MA225",      "2 | 3",   "1 | 2",         "-",          "1"],
                             [     "MA224",      "3 | 4",   "1 | 2",         "-",          "2"],
                             [     "MA223",      "4 | 5",   "1 | 2",         "-",          "3"],
                             [     "MA222",          "6",   "1 | 2",         "-",          "4"],
                             [      "MA22",          "6",       "-",         "-",          "5"]],
                             ["LitoralCod", "SedCode", "SaltClass", "SaltMarshC"],
                            "EUNIS"
                            )
# create model
model = RuleBasedModel([inputDataset], [rule1A, rule1B,\
                                        rule2A, rule2B,\
                                        rule3A, rule3B, rule3C,\
                                        rule4A1, rule4A2, rule4A3, rule4B1,\
                                        rule4C, rule4D1, rule4D2,
                                        rule4E,rule4F, rule4G,\
                                        rule4H, rule4I,\
                                        rule5A, rule5B,\
                                        rule6A1, rule6A2, rule6B, rule6C, rule6D, \
                                        rule7A, rule7B, rule7C, rule7D \
                                        ], name="my new model")

# run model
ModelRunner.run_model(model, logger)

# write output to netcdf
model.output_dataset.to_netcdf("data_out/RESTCOAST_python_output_file2.nc", format="NETCDF4")