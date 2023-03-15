from unittest.mock import patch

import climetlab as cml
import pytest

from climetlab_wekeo_source import WekeoAPIKeyPrompt


def test_invalid_json():
    with pytest.raises(AssertionError):
        cml.load_source("wekeo", 0)


def test_incomplete_json():
    with pytest.raises(AssertionError):
        cml.load_source("wekeo", {})


@patch.object(WekeoAPIKeyPrompt, "check", return_value=None)
def test_valid_arguments(api_check):
    cml.load_source("wekeo", {"datasetId": "dummy"})
    api_check.assert_called()
