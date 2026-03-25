import subprocess
from pathlib import Path

try:
    from ..core.ffmpeg_probe import get_ffmpeg_path
except Exception:  # pragma: no cover
    from core.ffmpeg_probe import get_ffmpeg_path


class UV_TranscodeVideo:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_path": ("STRING", {"default": ""}),
                "output_path": ("STRING", {"default": "transcoded_output.mp4"}),
                "video_codec": (["copy", "libx264", "libx265", "libvpx-vp9", "libsvtav1"],),
                "audio_codec": (["copy", "aac", "libopus"],),
                "overwrite": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("output_path",)
    FUNCTION = "transcode"
    CATEGORY = "UniversalVideoIO"
    OUTPUT_NODE = True

    def transcode(self, input_path, output_path, video_codec="copy", audio_codec="copy", overwrite=True):
        if not Path(input_path).exists():
            raise FileNotFoundError(f"input_path not found: {input_path}")
        if not output_path:
            raise ValueError("output_path is required")
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        ffmpeg_path = get_ffmpeg_path()
        cmd = [
            ffmpeg_path,
            "-hide_banner",
            "-loglevel",
            "error",
            "-y" if overwrite else "-n",
            "-i",
            input_path,
            "-c:v",
            video_codec,
            "-c:a",
            audio_codec,
            output_path,
        ]
        proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
        if proc.returncode != 0:
            raise RuntimeError(f"Transcode failed: {proc.stderr.strip()}")
        return (output_path,)
