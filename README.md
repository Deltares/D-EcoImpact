[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![TeamCity build status](https://dpcbuild.deltares.nl/app/rest/builds/buildType:id:DEcoImpact_UnitTests/statusIcon.svg)](https://dpcbuild.deltares.nl/viewType.html?buildTypeId=DEcoImpact_UnitTests)

# D-EcoImpact

A Python based kernel to perform spatial (environmental) impact assessment. Based on knowledge rules applied to model output and/or measurements.
The dependencies of the D-EcoImpact are declared, managed and installed with [Poetry](https://python-poetry.org/).

## Copyright
Copyright &copy; 2022-2023 Stichting Deltares and contributors

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU Lesser General Public License version 2.1 as
published by the Free Software Foundation.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Lesser General Public License for more details.

A copy of the GNU General Public License can be found at  
<https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md>  
and at  
<http://www.gnu.org/licenses/>

Contact:  software@deltares.nl  
Stichting Deltares  
P.O. Box 177  
2600 MH Delft, The Netherlands

All indications and logos of, and references to registered trademarks
of Stichting Deltares remain the property of Stichting Deltares. All
rights reserved.

## Prerequisites

- python 3.9 or higher
- poetry 1.3 or higher we recommend: ([installation instructions](https://python-poetry.org/docs/#installation))

If you prefer to install poetry with conda then we recommed to install poetry only to the base environment:

```sh
$ conda install -y -c conda-forge poetry
```

## Install

To install the dependencies of the project create a virtual environment either with `venv` or `conda`.\
Switch to this environment and use `poetry` to restore the package dependencies.

### Create environment

> Whereby **<env_name>** stands for your chosen environment name.
>
> The name can not contain any spaces or special characters.

#### Anaconda or Miniconda:

- Create `conda` environment
  ```sh
  $ conda create -y -c pip --name <env_name> python=3.11
  ```
- Activate `conda` environment
  ```sh
  $ conda activate <env_name>
  ```

### venv:

- Create `venv` virtual environment

  ```sh
  $ python -m venv <env_name>
  ```

- Activate `venv` environment
  ```
  $ .\env\Scripts\activate
  ```

(see
[Documentation](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment))

### Add dependencies

```sh
$ poetry install
```

## Run

Make sure you have a correct input file available in the main folder (eg. input_file.yaml) and use this as the first keyword argument when running the code through command line:

```sh
$ python main.py input_file.yaml
```

## Development

When adding a new dependency, do so using `poetry`

- Add a new dependency

  ```sh
  $ poetry add <package>
  ```

- Add a new dependency for development
  ```sh
  $ poetry add <package> --dev
  ```

### Versioning
-  The repository depends on automatic versioning throuhg github actions and the commit message.
- If the commit message starts with `Fix`, `fix`, `Bug`, or `bug` the patch version will be increased in the 
  pyproject.toml and a tag will be created.

## Documentation

There are mkdocs available for documentation on how to use this code.
For now these are available offline by running the command:

```
$ mkdocs serve
```

The pages will be served locally and available on one of you local ports. When executing this command in the INFO messages the location will be shown where the docs are available:

```
INFO     -  [10:44:34] Serving on http://127.0.0.1:8000/
```

In this case the docs are available on http://127.0.0.1:8000/ or http://localhost:8000:

## Add acceptance tests

To add an acceptance test:

- Create the [name].yaml file and store it in the tests_acceptance/input_yaml_files
- Put the [name].nc at the tests_acceptance/reference_nc_files folder. \* Note that the .nc file should have the same name as the .yaml file.
- To test if it is working correctly run: poetry run pytest tests_acceptance/test_main.py
