import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from core.ffmpeg_probe import get_ffmpeg_path


def test_ffmpeg_path_resolves():
    assert get_ffmpeg_path()


def test_ffmpeg_ready_payload_shape():
    from core.ffmpeg_probe import ensure_ffmpeg_ready

    payload = ensure_ffmpeg_ready()
    assert "ffmpeg_path" in payload
    assert "encoders" in payload
