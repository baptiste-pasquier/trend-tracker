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
