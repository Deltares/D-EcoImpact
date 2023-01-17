
![Python versions](https://img.shields.io/badge/Python-3.9-blue)

# D-EcoImpact

This is a short or long textual description of the project.

## Getting Started

The dependencies of the D-EcoImpact are declared, managed and installed with [Poetry](https://python-poetry.org/). 

Make sure to have Poetry and Python installations in your system. 

To install the dependencies of the project create a virtual environment either with pip or conda:

	
### CONDA:

- Create conda environment  
  ```sh
    $ conda create -y -c conda-forge --name <env_name> python=3.9 poetry
    ```
- Activate conda environment
  ```sh
    $ conda activate <env_name> 
    ```
- Install dependencies
  ```sh
    $ poetry install
    ```
- Add a new dependency for developement
  ```sh
    $ poetry add <package> --dev
    ```
- Add a new dependency 
  ```sh
    $ poetry add <package>
    ```
		


