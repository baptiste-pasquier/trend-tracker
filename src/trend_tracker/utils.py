from __future__ import annotations

import logging
import os

import yaml


def load_config(config_path: str) -> dict:
    """Load yaml configuration file.

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
    """Load yaml file in environment variables.

    The yaml file should have the following format:
    ```
    CATEGORY:
        VARNAME: VARIABLE
        VARNAME2: VARIABLE2
    CATEGORY2:
        VARNAME3: VARIABLE3
    ```

    Parameters
    ----------
    config_path : str
        Path of the yaml configuration file
    logger : logging.Logger
        Logger
    """
    if os.path.isfile("secret_config.yml"):
        config = load_config(config_path)

        for category in config.keys():
            for name in config[category]:
                os.environ[f"{category}_{name}"] = config[category][name]
        if logger is not None:
            logger.info("Loading secret_config.yml in environment variables.")
    elif logger is not None:
        logger.warning(
            "File secret_config.yml not found, using default environment variables."
        )


def format_text_logging(
    string: str, pad: int | None = None, ljust: bool = False
) -> str:
    """Format text for safe logging.

    Parameters
    ----------
    string : str
         String to format
    pad : int | None, optional
        Maximum length of the string, by default None
    ljust : bool, optional
        Add spaces at the end of the string until length is pad

    Returns
    -------
    str
        Formatted string
    """
    string = string.encode("ascii", errors="ignore").decode()
    if pad is not None:
        if ljust:
            string = string.ljust(pad)
        string = string[:pad]
    return string
