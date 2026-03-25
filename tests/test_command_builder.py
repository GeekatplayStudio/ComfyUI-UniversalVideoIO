import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from core.command_builder import build_video_command


def test_build_video_command_has_codec_and_output():
    cmd = build_video_command(
        ffmpeg_path="ffmpeg",
        input_pattern="/tmp/frame_%06d.png",
        output_path="out.mp4",
        fps=24,
        profile_name="youtube_h264",
        overwrite=True,
    )
    assert "-c:v" in cmd
    assert cmd[-1] == "out.mp4"


def test_build_video_command_advanced_overrides():
    cmd = build_video_command(
        ffmpeg_path="ffmpeg",
        input_pattern="/tmp/frame_%06d.png",
        output_path="out.mov",
        fps=30,
        profile_name="prores_422hq_master",
        overwrite=False,
        audio_path="/tmp/audio.wav",
        pix_fmt_override="yuv422p10le",
        quality_args_override="-qscale:v 7",
        color_range="tv",
        colorspace="bt709",
    )
    assert "-n" in cmd
    assert "-shortest" in cmd
    assert "yuv422p10le" in cmd
    assert "-qscale:v" in cmd
    assert "bt709" in cmd
