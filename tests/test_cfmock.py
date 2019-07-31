"""Test commandline"""
import pytest


@pytest.mark.parametrize('response_data', ['./test.json'])
def test_return_mock_successfully(response_data):
    """
    Tests success response mock
    :param response_data: json file
    :return: json response data from endpoint-test
    """
    pass
