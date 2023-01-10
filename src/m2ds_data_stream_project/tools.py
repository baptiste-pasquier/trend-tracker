import logging
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


def load_config_in_environment(config_path: str, logger: logging.Logger) -> None:
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
    logger : logging.Logger
        _description_
    """
    if os.path.isfile("secret_config.yml"):
        config = load_config(config_path)

        for category in config.keys():
            for name in config[category]:
                os.environ[f"{category}_{name}"] = config[category][name]
        logger.info("Loading secret_config.yml in environment variables.")
    else:
        logger.warning(
            "File secret_config.yml not found, using default environment variables."
        )


def format_text_logging(
    string: str, pad: int | None = None, ljust: bool = False
) -> str:
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
    string = ascii(string)
    if pad is not None:
        if ljust:
            string = string.ljust(pad)
        string = string[:pad]
    return string
