@echo "Run the tests"
python examples/python_test_of_functions.py
python main.py examples/test_DHYDRO_DELWAQ_Online.yaml
python main.py examples/test_DHYDRO_Maas.yaml
python main.py examples/test_DHYDRO_Maas_Potamogeton_testcase_fuzzylogic.yaml
python main.py examples/test_IMOD_Dommel.yaml
@echo next one is to be considered requested functionality (different time axes)
@echo 2023-05-31 10:51:46,661: ValueError: The arrays must have the same dimensions.
@echo python main.py examples/test_SFINCS_beira_flood.yaml
@echo 
python main.py examples/test_VKZM_Potamogeton_testcase_boundaries.yaml
python main.py examples/test_VKZM_Potamogeton_testcase_fuzzylogic.yaml
python main.py examples/test_VKZM_simple_testcase.yaml
python main.py examples/test_IRM_Doesburg_IJssel_rasters.yaml
python main.py examples/test_Westerschelde.yaml
python main.py examples/test1_default_independent_rules.yaml
python main.py examples/test2_variable_mapping.yaml
@echo next one is to be considered requested functionality  (error in yaml implementation, always variable mapping expected)
@echo AttributeError: 'str' object has no attribute 'keys'
@echo python main.py examples/test2b_variable_no_mapping.yaml
@echo
@echo next one is to be considered requested functionality  (error in yaml implementation, always variable mapping expected)
@echo 2023-05-31 10:53:25,352: ERROR    Mapping towards the following variables 'mesh2d_sa1, mesh2d_s1', will create duplicates with variables in the input datasets.
@echo 2023-05-31 10:53:25,352: ERROR    Model "Model 1" transition from ModelStatus.VALIDATING to ModelStatus.VALIDATED has failed.
@echo python main.py examples/test2c_variable_no_mapping.yaml
@echo 
python main.py examples/test3_layer_filter_layer22.yaml
python main.py examples/test3b_layer_filter_layer0.yaml
python main.py examples/test3c_layer_filter_layer1.yaml
@echo 
@echo next one is correct (expected error in model config,  not existing layer) WARNING could be clearer
@echo 2023-05-31 13:34:14,487: WARNING  Some rules can not be resolved: test name
@echo 2023-05-31 13:34:14,487: ERROR    Initialization failed.
@echo python main.py examples/test3d_layer_filter_not_existing_layer.yaml
@echo 
python main.py examples/test4_depending_rules_multiply.yaml
python main.py examples/test4b_depending_rules_multiply.yaml
python main.py examples/test5_depending_rules_multiply_layerfilter.yaml
python main.py examples/test6_combine_results_add.yaml
python main.py examples/test6b_combine_results_subtract.yaml
python main.py examples/test6c_combine_results_min.yaml
python main.py examples/test6d_combine_results_max.yaml
python main.py examples/test6e_combine_results_multiply.yaml
python main.py examples/test6f_combine_results_with_nans.yaml
python main.py examples/test7_time_aggregation_year.yaml
python main.py examples/test7b_time_aggregation_month.yaml
@echo next one is correct (expected error in model config, day is not implemented)
@echo 2023-05-31 10:54:04,909: ERROR    The provided time scale 'day' of rule 'test name' is not supported.
@echo Please select one of the following types: month,year
@echo python main.py examples/test7c_time_aggregation_day_not_existing_opp.yaml
@echo 
@echo next one is correct (expected error in model config, popcorn is not implemented)
@echo The provided time scale 'popcorn' of rule 'test name' is not supported.
@echo Please select one of the following types: month,year
@echo python main.py examples/test7d_time_aggregation_popcorn_not_existing_opp.yaml
@echo 
@echo next one is correct (expected error in model config,  time scale missing)
@echo AttributeError: Missing element time_scale
@echo python main.py examples/test7e_time_aggregation_default.yaml
@echo 
python main.py examples/test8_stepwise_classification_waterlevel.yaml
python main.py examples/test8b_stepwise_classification_salinity_limits.yaml
python main.py examples/test8c_stepwise_classification_salinity_categories.yaml
python main.py examples/test8d_stepwise_classification_waterlevel_lower_range.yaml
python main.py examples/test9_response_curve_waterlevel.yaml
@echo next one is correct (expected error in model config, data provided in wrong order)
@echo 2023-05-31 10:57:54,424: ERROR    The input values should be given in a sorted order.
@echo 2023-05-31 10:57:54,424: ERROR    Model "Model 1" transition from ModelStatus.VALIDATING to ModelStatus.VALIDATED has failed.
@echo python main.py examples/test9b_response_curve_waterlevel_wrong_order.yaml
@echo 
python main.py examples/test9c_response_curve_waterlevel_on_year.yaml
python main.py examples/test10_formula_based_comparison.yaml
python main.py examples/test10b_formula_based_arithmatic.yaml
python main.py examples/test10c_formula_based_ifelse.yaml
@echo next one is to be considered requested functionality (variable computations with missing/different time axes) 
@echo IndexError: too many indices for array: array is 1-dimensional, but 2 were indexed
@echo python main.py examples/test10d_formula_based_timeaxes_calculation.yaml
@echo 