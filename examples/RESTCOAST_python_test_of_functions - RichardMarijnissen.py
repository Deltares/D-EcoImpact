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
# Determine adapted LitoralCod for Dollard in REST-COAST

rule4A1 = TimeAggregationRule("Compute mean ssc", ["mud1_kgm3"], TimeOperationType.AVERAGE, "year","mean_mud1_kgm3")
rule4A2 = TimeAggregationRule("Compute mean ssc", ["mud2_kgm3"], TimeOperationType.AVERAGE, "year","mean_mud2_kgm3")
rule4A3 = CombineResultsRule("Compute ssc of mud", ["mean_mud1_kgm3", "mean_mud2_kgm3"], MultiArrayOperationType.ADD, "mean_mud_kgm3")
# rule4A1 = CombineResultsRule("Compute ssc of mud", ["mud1_kgm3", "mud2_kgm3"], MultiArrayOperationType.ADD, "m_mud_kgm3")
# rule4A2 = TimeAggregationRule("Compute mean ssc", ["mud2_kgm3"], TimeOperationType.AVERAGE, "year","mean_mud2_kgm3")
rule4B1 = FormulaRule("Determine depth of photic zone", ["mean_mud_kgm3"], "4.605170185988091/(0.08 + 2.5e4 * mean_mud_kgm3)", "dpar1_m")
#rule4B2 = LayerFilterRule("Depth of photic zone without time", ["dpar1_m"], 2, "time_year", "dpar1_m_t0")
# # --> It would be more convenient to also be able to use constants across the script and have a log or ln() function e.g.
# #     SetConstant(Set background extinction coefficient (m-1 ), ["E0"], 0.08)
# #     SetConstant(Set mud extinction coefficient (kg m-3 ), ["Emud"], 2.5e4)
# #     rule4B = FormulaRule("Determine depth of photic zone", ["mud_kgm3", "E0", "Emud"], "-ln(0.01)/(E0 + Emud * mud_kgm3", "d_par1")
# # rule4C = FormulaRule("Determine level of photic zone", ["dpar1_m", "mesh2d_mesh2d_MLWN"], "mesh2d_mesh2d_MLWN - dpar1_m", "zpar1_mNAP")
# rule4C = CombineResultsRule("Determine level of photic zone", ["dpar1_m_t0", "mesh2d_mesh2d_MLWN"], MultiArrayOperationType.SUBTRACT, "zpar1_mNAP")
# rule4D1 = TimeAggregationRule("calculate bottom level", ["mesh2d_mor_bl"], TimeOperationType.AVERAGE, "year","mean_bottomlevel_mNAP")
# rule4D2 = FormulaRule("Deep sublittoral", ["mean_bottomlevel_mNAP", "zpar1_mNAP"], "mean_bottomlevel_mNAP < zpar1_mNAP", "deep_sublittoral")
rule4E = FormulaRule("Get exposure time", ["mesh2d_mesh2d_Inundation"], "1 - mesh2d_mesh2d_Inundation", "exposure_time")
rule4F = StepFunctionRule("Littoral class minus sublittoral", "exposure_time", [0.0, 0.04, 0.25, 0.40, 0.85, 1.0], [0.0, 2.0, 3.0, 4.0, 5.0, 5.0], "LitoralCod_min_sublittoral")
rule4G = FormulaRule("Sublittoral ",["exposure_time"], "exposure_time <= 0.04", "sublittoral")
# rule4H = CombineResultsRule("Sublittoral classes", ["sublittoral","deep_sublittoral"],MultiArrayOperationType.SUBTRACT,"sub_littoral_classes")
# rule4I = CombineResultsRule("Littoral class", ["LitoralCod_min_sublittoral","sub_littoral_classes"],MultiArrayOperationType.ADD,"LitoralCod")

# Determine ZES.1 Hydrodynamics class
rule5A = TimeAggregationRule("max current velocity", ["mesh2d_ucmag"],TimeOperationType.MAX, "year","max_flowvelocity_ms")
rule5B = FormulaRule("Hydrodynamics class",["max_flowvelocity_ms"], "max_flowvelocity_ms >= 0.8", "DynamicCod")

# Determine ZES.1 sediment composition class
rule6A1 = TimeAggregationRule("Compute the year average bed composition", ["mesh2d_mudfrac"], TimeOperationType.AVERAGE, "year","mean_mud_frac")
rule6A2 = StepFunctionRule("Sediment composition class 1 and 2", "mean_mud_frac", [0.0, 0.25, 1.0], [2.0, 1.0, 1.0], "SedCode1_2")
rule6B = TimeAggregationRule("Compute average bed shear stress", ["mesh2d_taub"], TimeOperationType.AVERAGE, "year","mean_taub")
rule6C = FormulaRule("Determine Sed Code 3", ["SedCode1_2", "mean_taub"], "(SedCode1_2 == 2.0) & (mean_taub > 0.18)", "SedCode3")
rule6D = CombineResultsRule("SedCode", ["SedCode1_2","SedCode3"],MultiArrayOperationType.ADD,"SedCode")

# Determine ZES.1 Salt Marsh class
rule7A = TimeAggregationRule("Determine max daily water depth", ["mesh2d_waterdepth"], TimeOperationType.MAX, "day","max_h_day")
rule7B = FormulaRule("Expected inundations per day", ["max_h_day"], "(max_h_day < 0.1) * 1.9138755980861246", "daily_inundations")
rule7C = TimeAggregationRule("Determine number of yearly inundations", ["daily_inundations"], TimeOperationType.SUM, "year","n_inundations")
rule7D = StepFunctionRule("Salt marsh inundation class", "n_inundations", [0.0, 5.0, 50.0, 150, 300, 9999999999999999], [4.0, 3.0, 2.0, 1.0, 0.0, 0.0], "SaltMarshC")

# create model
model = RuleBasedModel([inputDataset], [rule1A, rule1B,\
                                        rule2A, rule2B,\
                                        rule3A, rule3B, rule3C,\
                                        rule4A1, rule4A2, rule4A3, rule4B1,\
                                        #rule4C, rule4D1, rule4D2,
                                        rule4E,rule4F, rule4G,\
                                        #rule4H, rule4I,\
                                        rule5A, rule5B,\
                                        rule6A1, rule6A2, rule6B, rule6C, rule6D, \
                                        rule7A, rule7B, rule7C, rule7D \
                                        ], name="my new model")

# run model
ModelRunner.run_model(model, logger)

# write output to netcdf
model.output_dataset.to_netcdf("data_out/RESTCOAST_python_output_file2.nc", format="NETCDF4")