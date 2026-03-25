import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from core.ffmpeg_probe import get_ffmpeg_path


def test_ffmpeg_path_resolves():
    assert get_ffmpeg_path()
