import pytest

from otterai.exceptions import OtterAIException


def test_otterai_exception():
    with pytest.raises(OtterAIException) as exc_info:
        raise OtterAIException("Test error")
    assert str(exc_info.value) == "Test error"
