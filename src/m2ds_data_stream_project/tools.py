import os

import yaml


def load_config(config_path: str) -> dict:
    """Function to load yaml configuration file

    Parameters
    ----------
    config_path : str
        Path of the yaml configuration file

    Returns
    -------
    dict
        Configuration file as a Python dictionnary
    """

    with open(config_path) as file:
        config = yaml.safe_load(file)

    return config


def load_config_in_environment(config_path: str) -> None:
    """Function to load yaml file in environment variables.

    The yaml file should have the following format:
    ```
    CATEGORY:
        VARNAME: VARIABLE
    ```

    Parameters
    ----------
    config_path : str
        Path of the yaml configuration file
    """

    config = load_config(config_path)

    for category in config.keys():
        for name in config[category]:
            os.environ[f"{category}_{name}"] = config[category][name]


def log_text(string: str, pad) -> str:
    """_summary_

    Parameters
    ----------
    string : str
        _description_

    Returns
    -------
    str
        _description_
    """
    string = string.replace("\n", " ")
    string = string.ljust(pad)[:pad]
    return string
