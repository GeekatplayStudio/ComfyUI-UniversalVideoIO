import json
from pathlib import Path

import imageio
import numpy as np
import torch

try:
    from ..core.ffmpeg_probe import ffprobe_json
except Exception:  # pragma: no cover
    from core.ffmpeg_probe import ffprobe_json


class UV_LoadVideo:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "path": ("STRING", {"default": ""}),
                "start_frame": ("INT", {"default": 0, "min": 0, "max": 1000000}),
                "frame_limit": ("INT", {"default": 0, "min": 0, "max": 1000000}),
                "fps_override": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 1000.0}),
                "audio_detect_only": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("IMAGE", "STRING", "STRING", "INT", "INT", "FLOAT", "INT")
    RETURN_NAMES = (
        "images",
        "metadata_json",
        "audio_ref",
        "width",
        "height",
        "fps",
        "frame_count",
    )
    FUNCTION = "load"
    CATEGORY = "UniversalVideoIO"

    def load(self, path, start_frame=0, frame_limit=0, fps_override=0.0, audio_detect_only=False):
        if not Path(path).exists():
            raise FileNotFoundError(f"Input video not found: {path}")

        reader = imageio.get_reader(path)
        meta = reader.get_meta_data() or {}
        fps = float(fps_override) if fps_override and fps_override > 0 else float(meta.get("fps", 24.0))
        frames = []
        total = 0
        for i, frame in enumerate(reader):
            if i < start_frame:
                continue
            if frame_limit > 0 and total >= frame_limit:
                break
            frames.append(frame)
            total += 1
        reader.close()

        if not frames:
            raise ValueError("No frames loaded. Check path/start_frame/frame_limit.")

        arr = np.stack(frames).astype(np.float32) / 255.0
        images = torch.from_numpy(arr)
        h, w = int(arr.shape[1]), int(arr.shape[2])

        probe = ffprobe_json(path)
        has_audio = any(s.get("codec_type") == "audio" for s in probe.get("streams", []))
        metadata = {
            "source": path,
            "fps": fps,
            "frame_count": int(arr.shape[0]),
            "width": w,
            "height": h,
            "audio_present": has_audio,
            "audio_detect_only": bool(audio_detect_only),
        }
        audio_ref = path if has_audio else ""
        return images, json.dumps(metadata), audio_ref, w, h, fps, int(arr.shape[0])
