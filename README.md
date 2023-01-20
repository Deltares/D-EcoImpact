[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![TeamCity build status](https://dpcbuild.deltares.nl/app/rest/builds/buildType:id:DEcoImpact_UnitTests/statusIcon.svg)](https://dpcbuild.deltares.nl/viewType.html?buildTypeId=DEcoImpact_UnitTests)

# D-EcoImpact

A Python based kernel to perform spatial (environmental) impact assessment. Based on knowledge rules applied to model output and/or measurements.
The dependencies of the D-EcoImpact are declared, managed and installed with [Poetry](https://python-poetry.org/).

## Prerequisites

- python 3.9 or higher
- poetry 1.3 or higher ([installation instructions](https://python-poetry.org/docs/#installation))

## Install
To install the dependencies of the project create a virtual environment either with `venv` or `conda`.\
Switch to this environment and use `poetry` to restore the package dependencies.

### Create environment

#### Anaconda:

- Create `conda` environment
  ```sh
  $ conda create -y -c conda-forge --name <env_name> poetry
  ```
- Activate `conda` environment
  ```sh
  $ conda activate <env_name>
  ```

### venv:

- Create `venv` virtual environment
  ```sh
  $ py -m venv <env_name>
  ```

- Activate `venv` environment
  ```
  $ .\env\Scripts\activate
  ```

(see
    [Documentation](
    https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment))

### Add dependencies

```sh
$ poetry install
```


## Run

  ```sh
  $ py main.py
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
