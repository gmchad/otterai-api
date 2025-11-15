from otterai.otterai import OtterAI


def test_otterai_instantiation():
    otter = OtterAI()
    assert otter._userid is None
    assert otter._is_userid_invalid() is True
