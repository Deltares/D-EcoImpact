
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
		

### Using pip directly
Note: This installs the packages system wide, without the use of python environments.

Windows PowerShell:
- Install poetry
  ```powershell
    $ pip3 install poetry
    ```
- Install dependencies
  ```powershell
    $ poetry install
```

Linux:
- Install poetry
  ```sh
    $ pip3 install poetry
    ```
- Install dependencies
  ```sh
    $ poetry install
```
    
### Remarks on use of poetry on Windows

The poetry is not compatible with the python installation from the Microsoft Store. Instead, it is recommended to install python from https://www.python.org/downloads/.