import subprocess
from pathlib import Path

import imageio
import numpy as np

try:
    from ..core.command_builder import build_sequence_pattern, build_video_command
    from ..core.encoder_profiles import list_profiles
    from ..core.ffmpeg_probe import get_ffmpeg_path
    from ..core.tempfiles import make_temp_dir
    from ..core.validation import ensure_image_batch
except Exception:  # pragma: no cover
    from core.command_builder import build_sequence_pattern, build_video_command
    from core.encoder_profiles import list_profiles
    from core.ffmpeg_probe import get_ffmpeg_path
    from core.tempfiles import make_temp_dir
    from core.validation import ensure_image_batch


class UV_SaveVideo:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "output_path": ("STRING", {"default": "output.mp4"}),
                "profile": (list_profiles(),),
                "fps": ("FLOAT", {"default": 24.0, "min": 1.0, "max": 240.0}),
                "quality_mode": (["preset", "advanced"],),
                "overwrite": ("BOOLEAN", {"default": True}),
                "audio_mode": (["none", "mux"],),
                "pix_fmt": (["auto", "yuv420p", "yuv420p10le", "yuv422p10le", "yuva444p10le"],),
                "color_range": (["auto", "tv", "pc"],),
                "colorspace": (["auto", "bt709", "bt2020nc", "smpte170m"],),
            },
            "optional": {
                "audio_path": ("STRING", {"default": ""}),
                "advanced_quality_args": ("STRING", {"default": ""}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("saved_path",)
    FUNCTION = "save"
    CATEGORY = "UniversalVideoIO"
    OUTPUT_NODE = True

    def save(
        self,
        images,
        output_path,
        profile,
        fps=24.0,
        quality_mode="preset",
        overwrite=True,
        audio_mode="none",
        pix_fmt="auto",
        color_range="auto",
        colorspace="auto",
        audio_path="",
        advanced_quality_args="",
    ):
        images = ensure_image_batch(images)
        if not output_path:
            raise ValueError("output_path is required")
        if audio_mode == "mux" and not audio_path:
            raise ValueError("audio_path is required when audio_mode is 'mux'")
        if audio_mode == "mux" and audio_path and not Path(audio_path).exists():
            raise FileNotFoundError(f"audio_path not found: {audio_path}")

        data = images.detach().cpu().numpy()
        data = np.clip(data * 255.0, 0, 255).astype(np.uint8)

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        temp_dir = make_temp_dir()
        for i, frame in enumerate(data):
            imageio.imwrite(temp_dir / f"frame_{i:06d}.png", frame)

        ffmpeg_path = get_ffmpeg_path()
        cmd = build_video_command(
            ffmpeg_path=ffmpeg_path,
            input_pattern=build_sequence_pattern(str(temp_dir), "png"),
            output_path=output_path,
            fps=fps,
            profile_name=profile,
            overwrite=overwrite,
            audio_path=(audio_path or None) if audio_mode == "mux" else None,
            pix_fmt_override=pix_fmt,
            quality_args_override=advanced_quality_args if quality_mode == "advanced" else "",
            color_range=color_range,
            colorspace=colorspace,
        )
        proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
        if proc.returncode != 0:
            raise RuntimeError(f"FFmpeg export failed: {proc.stderr.strip()}")
        return (output_path,)
