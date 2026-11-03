# Installation
D-Eco Impact is a command-line operated model that requires Python and its dependencies. Install [Python 3.14](https://www.python.org/downloads/) and [uv 0.13.6 or higher](https://docs.astral.sh/uv/getting-started/installation/).

## Install with uv

1. Open a terminal and move to the D-Eco Impact source folder.
2. Run:
   ```sh
   uv sync
   ```

`uv sync` reads `uv.lock` and `pyproject.toml`, creates the project environment in `.venv` if it does not exist, and installs the required dependencies. You do not need to create or activate a virtual environment manually; `uv run` executes commands in the project environment.

To run D-Eco Impact with an input file:
```sh
uv run python main.py <your_input_file>.yaml
```

## Use with Visual Studio Code

1. Open the D-Eco Impact source folder in [Visual Studio Code](https://code.visualstudio.com/download).
2. Open a terminal in the source folder and run `uv sync` to create and populate `.venv`.
3. If you want VS Code to use this environment for features such as code completion, select `.venv` as the Python interpreter. In the Command Palette, choose **Python: Select Interpreter** and select the interpreter under `.venv`. There is no need to create another environment through VS Code.
4. Run the model from the terminal with:
   ```sh
   uv run python main.py <your_input_file>.yaml
   ```



## How to Cite
If you found D-Eco Impact useful for your study, please cite it as:

Weeber, M., Elzinga, H., Schoonveld, W., Van de Vries, C., Klapwijk, M., Mischa, I., Rodriguez Aguilera, D., Farrag, M., Ye, Q., Markus, A., Van Oorschot, M., Saager, P., & Icke, J. (2024). D-Eco Impact (v0.3.0). Zenodo. https://doi.org/10.5281/zenodo.10941913