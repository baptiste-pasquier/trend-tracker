from pathlib import Path

import pytest

from trend_tracker.utils import format_text_logging, load_config


@pytest.fixture
def config_path(tmp_path):
    target_output = Path(tmp_path, "config.yml")
    with open(target_output, "w") as f:
        f.write(
            """
        # Comment
        parameter1: 12
        parameter2 : 1.2

        block:
            parameter3: "string"
            parameter4: ["1", 2]
        """
        )
        # write stuff here
    return target_output


def test_load_config(config_path):
    config = load_config(config_path)

    assert config["parameter1"] == 12
    assert config["parameter2"] == 1.2
    assert config["block"]["parameter3"] == "string"
    assert config["block"]["parameter4"] == ["1", 2]


def test_format_text_logging():
    string = format_text_logging("hello")
    assert string == "hello"

    string = format_text_logging("hello_bye", pad=5)
    assert string == "hello"

    string = format_text_logging("hello", pad=10)
    assert string == "hello"

    string = format_text_logging("hello", pad=10, ljust=False)
    assert string == "hello"

    string = format_text_logging("hello", pad=10, ljust=True)
    assert string == "hello     "
