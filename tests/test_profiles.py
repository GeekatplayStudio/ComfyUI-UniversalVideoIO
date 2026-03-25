import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from core.encoder_profiles import get_profile, list_profiles


def test_profiles_include_expected_keys():
    profiles = list_profiles()
    assert "youtube_h264" in profiles
    p = get_profile("prores_422hq_master")
    assert p["container"] == "mov"
