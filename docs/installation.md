# Installation 
D-Eco Impact is a command line operated model. To use D-Eco Impact (currently) an installation of Python and the used libraries is required. This is best achieved by installing D-Eco Impact in a virtual environment.


## Conda or Visual Studio Code
Conda is a package and environment manager that can be used to install the poetry package and other packages needed to run D-Eco Impact. 

- [Miniforge](https://github.com/conda-forge/miniforge)
- [Miniconda](https://docs.conda.io/en/main/miniconda.html)
- [Visual Studio code](https://code.visualstudio.com/download)

## Installation of D-Eco Impact with conda (use Miniforge or Miniconda)

Note: when using miniconda, make sure to update the defaults channel to conda-forge ([instructions for changing the channel](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-channels.html))!

1.	Open a commandline tool (eg. cmd or powershell):
  ```sh
  $ conda create -y -c pip --name <env_name> python=3.11
  ```

2.	Activate the newly created environment
  ```sh
  $ conda activate <env_name>
  ```

3.	Move to the folder where you have placed the D-Eco Impact source code
You can use cd ../ and cd <folder_name> to move to the location or use windows explorer and type “cmd” + enter in the path bar.

4.	To install the required libraries Poetry is used. 
Use poetry 1.3 or higher: ([installation instructions](https://python-poetry.org/docs/#installation))
If you prefer to install poetry with conda then we recommed to install poetry only to the base environment.

Activate base environment:
```sh
$ conda activate base
```
Install poetry using pip:
```sh
$ pip install poetry
```
Activate your created environment:
```sh
$ conda activate <env_name>
```

5. Poetry makes use of the poetry.lock and pyproject.toml (present in the D-Eco Impact folder) to find these required libraries.
Execute the following command:
  ```
  poetry install
  ```
NB. If errors occur while installing the libraries, this might have to do with your administrative rights. Either start the cmd prompt “As administrator” or discuss this with your IT support.

6.	Now D-Eco Impact is ready to use. You can test this by executing one of the input yaml files.
To execute use the following in the command prompt while your environment is active:
  ```
  python main.py <your_input_file>.yaml
  ```

## Installation D-Eco impact with Visual Studio Code and venv

1.	Install [Python version 3.11.2] (https://www.python.org/downloads/)
2.	Open Visual Studio Code.
3.	Press CRTL + Shift + P and type “Python: Create Environment” followed by enter, select “Venv”.
4.	Place the environment in the D-Eco Impact folder.
5.	Press CTRL + Shift + P and type “Python: Select interpreter” and select the newly created environment.
6.	In the terminal in Visual Studio Code execute the following command:
  ```
  pip install poetry
  ```
7.	In the terminal in Visual Studio Code execute the following command:
poetry install
6.	Now D-Eco Impact is setup for use. You can test this by executing one of the input yaml files.
To execute use the following in the command prompt while your environment is active:
  ```
  python main.py <your_input_file>.yaml
  ```



## How to Cite
If you found D-Eco Impact useful for your study, please cite it as:

Weeber, M., Elzinga, H., Schoonveld, W., Van de Vries, C., Klapwijk, M., Mischa, I., Rodriguez Aguilera, D., Farrag, M., Ye, Q., Markus, A., Van Oorschot, M., Saager, P., & Icke, J. (2024). D-Eco Impact (v0.3.0). Zenodo. https://doi.org/10.5281/zenodo.10941913