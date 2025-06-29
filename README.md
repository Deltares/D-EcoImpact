[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![TeamCity build status](https://dpcbuild.deltares.nl/app/rest/builds/buildType:id:DEcoImpact_UnitTests/statusIcon.svg)](https://dpcbuild.deltares.nl/viewType.html?buildTypeId=DEcoImpact_UnitTests)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=Deltares_D-EcoImpact&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=Deltares_D-EcoImpact)

# D-EcoImpact

A Python based kernel to perform spatial (environmental) impact assessment. Based on knowledge rules applied to model output and/or measurements.
The dependencies of the D-EcoImpact are declared, managed and installed with [Poetry](https://python-poetry.org/).

## Copyright
Copyright &copy; 2022-2025 Stichting Deltares

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU Affero General Public License version 3.0 as
published by the Free Software Foundation.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

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

### venv:

- Create `venv` virtual environment

  ```sh
  $ python -m venv <env_name>
  ```

- Activate `venv` environment
  ```
  $ .\env\Scripts\activate
  ```

#### conda:


<span style="color:orange">**⚠ WARNING: Due to licencing of Anaconda, it is recommended to use an alternative like [Miniforge](https://github.com/conda-forge/miniforge). This still uses the package manager conda and therefore the same commands can still be used. The same goes for [Miniconda](https://docs.anaconda.com/miniconda/) but you need to change the defaults channel to conda-forge ([instructions for changing the channel](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-channels.html))!**
</span>

- Create `conda` environment
  ```sh
  $ conda create -y -c pip --name <env_name> python=3.11
  ```
- Activate `conda` environment
  ```sh
  $ conda activate <env_name>
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
The version looks like this: major.minor.patch
- The repository depends on automatic versioning through github actions. For each commit, the patch version will be increased in the 
  pyproject.toml.
- The major and minor version will only be updated by a manual trigger through github actions (triggering the 'release.yaml') in which case a tag will be created.

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

In this case the docs are available on http://127.0.0.1:8000/ or http://localhost:8000

For each release a version of documentation is available at: 
[deltares.github.io/D-EcoImpact/](deltares.github.io/D-EcoImpact/)

## Add acceptance tests

To add an acceptance test:

- Create the [name].yaml file and store it in the tests_acceptance/input_yaml_files
- Put the [name].nc at the tests_acceptance/reference_nc_files folder. \* Note that the .nc file should have the same name as the .yaml file.
- To test if it is working correctly run: poetry run pytest tests_acceptance/test_main.py



## Docker image

### Build
To build the docker image, run the following command in the root of the project:

```sh

$ ./build-image.sh

```

### Pull

To pull the docker image from the docker hub, run the following command:

```sh 

$ docker pull ghcr.io/deltares/d-ecoimpact:latest

```

### Authentication with GitHub Container Registry
Before building your Docker image, ensure you're authenticated with GHCR to allow pulling private images. Use the 
docker login command with your GitHub username and a Personal Access Token (PAT) that has the appropriate scopes 
(read:packages at a minimum).

```bash
echo "YOUR_PERSONAL_ACCESS_TOKEN" | docker login ghcr.io -u YOUR_GITHUB_USERNAME --password-stdin
```

For pushing new images make sure that your token that has enough permissions and has  authorization for the Deltares orginization (sso).


## How to Cite
If you found D-Eco Impact useful for your study, please cite it as:

Weeber, M., Elzinga, H., Schoonveld, W., Van de Vries, C., Klapwijk, M., Mischa, I., Rodriguez Aguilera, D., Farrag, M., Ye, Q., Markus, A., Van Oorschot, M., Saager, P., & Icke, J. (2024). D-Eco Impact (v0.3.0). Zenodo. https://doi.org/10.5281/zenodo.10941913


