import os

import pytest
from dotenv import load_dotenv

from otterai.otterai import OtterAI, OtterAIException
from tests.helpers import dump_json_response

load_dotenv()


@pytest.fixture
def logged_in_otter():
    username = os.getenv("OTTERAI_USERNAME")
    password = os.getenv("OTTERAI_PASSWORD")
    otter = OtterAI()
    otter.login(username, password)
    return otter


def test_dump_json_dummy():
    dummy_response = {"foo": "bar", "baz": [1, 2, 3]}
    dump_json_response(dummy_response, "dummy.json")


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


def test_login(logged_in_otter):
    assert logged_in_otter._userid is not None


def test_get_user(logged_in_otter):
    username = os.getenv("OTTERAI_USERNAME")
    response = logged_in_otter.get_user()
    assert response["data"]["user"]["email"] == username


def test_get_speakers(logged_in_otter):
    response = logged_in_otter.get_speakers()
    assert response["status"] == 200


def test_get_speeches(logged_in_otter):
    response = logged_in_otter.get_speeches()
    assert response["status"] == 200


def test_get_speakers_invalid_userid():
    otter = OtterAI()
    with pytest.raises(OtterAIException, match="userid is invalid"):
        otter.get_speakers()


def test_get_speeches_invalid_userid():
    otter = OtterAI()
    with pytest.raises(OtterAIException, match="userid is invalid"):
        otter.get_speeches()


def test_get_speech_invalid_userid():
    otter = OtterAI()
    with pytest.raises(OtterAIException, match="userid is invalid"):
        otter.get_speech("dummyid")


def test_upload_speech_invalid_userid():
    otter = OtterAI()
    with pytest.raises(OtterAIException, match="userid is invalid"):
        otter.upload_speech("dummy.mp4")


def test_download_speech_invalid_userid():
    otter = OtterAI()
    with pytest.raises(OtterAIException, match="userid is invalid"):
        otter.download_speech("dummyid")


def test_move_to_trash_bin_invalid_userid():
    otter = OtterAI()
    with pytest.raises(OtterAIException, match="userid is invalid"):
        otter.move_to_trash_bin("dummyid")


def test_create_speaker_invalid_userid():
    otter = OtterAI()
    with pytest.raises(OtterAIException, match="userid is invalid"):
        otter.create_speaker("dummy_speaker")


def test_list_groups_invalid_userid():
    otter = OtterAI()
    with pytest.raises(OtterAIException, match="userid is invalid"):
        otter.list_groups()


def test_get_folders_invalid_userid():
    otter = OtterAI()
    with pytest.raises(OtterAIException, match="userid is invalid"):
        otter.get_folders()


def test_stop_speech():
    otter = OtterAI()
    otter.stop_speech()
