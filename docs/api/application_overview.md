# Application overview

The application is setup using a layered architecture (see [link](architecture.md)).
To create the application you will need to create these three components: logger, data-access layer and model builder (see [main.py](https://github.com/Deltares/D-EcoImpact/blob/main/main.py)).

```python
    # configure logger and data-access layer
    logger: ILogger = LoggerFactory.create_logger()
    da_layer: IDataAccessLayer = DataAccessLayer(logger)
    model_builder = ModelBuilder(da_layer, logger)

    # create and run application
    application = Application(logger, da_layer, model_builder)
    application.run(path)
```

The logger provides logging functionality to the application, like reporting errors, warnings, user information and debug messages and is created using a factory pattern.
The DataAccessLayer gives the application access to the file system and allows for parsing of input and output.
The modelbuilder uses the builder pattern to create a model from a IModelData data object (created by the data-access layer).

## Running the application

After constructing the application, the application should be ready to run.
During the running of the application the following steps are executed.

![Application execution](../assets/images/Application_run.svg)

The application starts by reading the `ModelData` object from the input files via the `IDataAccessLayer`.
This gets passed to the `IModelBuilder`to convert the `ModelData` into a `IModel` that can be run.
The static `ModelRunner` will then be called to run the created `IModel` and do the real computation.

## Model run

When the `ModelRunner` `run_model` command is executed, the following steps are performed (using `RuleBasedModel` and `ICellBasedRule` as an example).

![Model execution](../assets/images/Model_run.svg)

The `ModelRunner` starts by validating the model (`RuleBasedModel` in this example).
The `RuleBasedModel` delegates the validation of the set of rules that it is composed with, calling the validate on every rule (`ICellBasedRule` in this example).
After the model is successfully validated, the initialize of the model is called. In case of the `RuleBasedModel`, this creates an instance of the `RuleProcessor` and initializes it.

The `ModelRunner` continues by calling the `execute` method on the `RuleBasedModel` that in turn calls `process_rules` on the `RuleBasedProcessor`.
This method loops over all the specified rules and executes the rules based on their type. So for example, with the `ICellBasedRule` the `RuleBasedProcessor` will loop over all the cells and call the `ICellBasedRule` execute method for every cell.

When the model execute has successfully finished with the execute step, the `finalize` method will be called on the model to clean up all resources.

## Class diagram

![Overview class diagram](../assets/images/Overview.svg)