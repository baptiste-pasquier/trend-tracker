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
