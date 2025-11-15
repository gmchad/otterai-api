from otterai.otterai import OtterAI


def test_otterai_instantiation():
    otter = OtterAI()
    assert otter._userid is None
    assert otter._is_userid_invalid() is True


def test_is_userid_invalid_true():
    otter = OtterAI()
    assert otter._is_userid_invalid() is True


def test_otterai_valid_userid():
    otter = OtterAI()
    otter._userid = "validid"
    assert otter._is_userid_invalid() is False


def test_stop_speech():
    otter = OtterAI()
    otter.stop_speech()
