@echo **Run small D-Eco Impact examples**
@echo  * NB. Make sure that you run this batch script with
@echo  *     examples within your D-Eco Impact environment (e.g. conda, venv).
@echo  *     See README.md on how to setup and activate this environment.
@echo:
@echo  ** Example - Run D-Eco Impact with configuration yaml (standard):
python main.py examples/input_yaml_files/test1_default_independent_rules.yaml
@echo: 
@echo  ** Example - Run D-Eco Impact directly from Python script (experimental):
python examples/python_test_of_functions.py
@echo: 
@echo  * For other D-Eco Impact configuration examples and tests of functionality
@echo  *     see 'tests_acceptance/input_yaml_files/..' .
@echo: 
@echo  * Note that D-Eco Impact is also available as executable and as docker container. 
@echo  *     Contact us for requesting these versions.
@echo  *     Go to : https://www.deltares.nl/en/software-and-data/products/d-eco-impact 
pause