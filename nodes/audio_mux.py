import subprocess

try:
    from ..core.ffmpeg_probe import get_ffmpeg_path
except Exception:  # pragma: no cover
    from core.ffmpeg_probe import get_ffmpeg_path


class UV_AudioMux:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "video_path": ("STRING", {"default": ""}),
                "audio_path": ("STRING", {"default": ""}),
                "output_path": ("STRING", {"default": "muxed_output.mp4"}),
                "overwrite": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("output_path",)
    FUNCTION = "mux"
    CATEGORY = "UniversalVideoIO"
    OUTPUT_NODE = True

    def mux(self, video_path, audio_path, output_path, overwrite=True):
        ffmpeg_path = get_ffmpeg_path()
        cmd = [
            ffmpeg_path,
            "-hide_banner",
            "-loglevel",
            "error",
            "-y" if overwrite else "-n",
            "-i",
            video_path,
            "-i",
            audio_path,
            "-map",
            "0:v:0",
            "-map",
            "1:a:0",
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-shortest",
            output_path,
        ]
        proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
        if proc.returncode != 0:
            raise RuntimeError(f"Audio mux failed: {proc.stderr.strip()}")
        return (output_path,)
