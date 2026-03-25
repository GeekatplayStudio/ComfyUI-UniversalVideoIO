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
                "resize_mode": (["none", "fit", "stretch"],),
                "resize_width": ("INT", {"default": 0, "min": 0, "max": 8192}),
                "resize_height": ("INT", {"default": 0, "min": 0, "max": 8192}),
                "keep_aspect_ratio": ("BOOLEAN", {"default": True}),
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

    def _resize_nearest(self, frame, target_h, target_w):
        src_h, src_w = frame.shape[:2]
        if src_h == target_h and src_w == target_w:
            return frame
        y_idx = np.linspace(0, max(src_h - 1, 0), target_h).astype(np.int32)
        x_idx = np.linspace(0, max(src_w - 1, 0), target_w).astype(np.int32)
        return frame[y_idx][:, x_idx]

    def _resize_frame(self, frame, resize_mode, resize_width, resize_height, keep_aspect_ratio):
        if resize_mode == "none" or resize_width <= 0 or resize_height <= 0:
            return frame
        if resize_mode == "stretch" or not keep_aspect_ratio:
            return self._resize_nearest(frame, resize_height, resize_width)

        h, w = frame.shape[:2]
        scale = min(resize_width / max(w, 1), resize_height / max(h, 1))
        target_w = max(1, int(round(w * scale)))
        target_h = max(1, int(round(h * scale)))
        resized = self._resize_nearest(frame, target_h, target_w)
        canvas = np.zeros((resize_height, resize_width, frame.shape[2]), dtype=resized.dtype)
        y0 = (resize_height - target_h) // 2
        x0 = (resize_width - target_w) // 2
        canvas[y0 : y0 + target_h, x0 : x0 + target_w] = resized
        return canvas

    def load(
        self,
        path,
        start_frame=0,
        frame_limit=0,
        fps_override=0.0,
        resize_mode="none",
        resize_width=0,
        resize_height=0,
        keep_aspect_ratio=True,
        audio_detect_only=False,
    ):
        if not Path(path).exists():
            raise FileNotFoundError(f"Input video not found: {path}")

        probe = ffprobe_json(path)
        has_audio = any(s.get("codec_type") == "audio" for s in probe.get("streams", []))
        if audio_detect_only:
            empty = torch.zeros((1, 64, 64, 3), dtype=torch.float32)
            metadata = {
                "source": path,
                "fps": 0.0,
                "frame_count": 0,
                "width": 0,
                "height": 0,
                "audio_present": has_audio,
                "audio_detect_only": True,
            }
            audio_ref = path if has_audio else ""
            return empty, json.dumps(metadata), audio_ref, 0, 0, 0.0, 0

        reader = imageio.get_reader(path, format="ffmpeg")
        meta = reader.get_meta_data() or {}
        fps = float(fps_override) if fps_override and fps_override > 0 else float(meta.get("fps", 24.0))
        frames = []
        total = 0
        for i, frame in enumerate(reader):
            if i < start_frame:
                continue
            if frame_limit > 0 and total >= frame_limit:
                break
            frame = self._resize_frame(frame, resize_mode, resize_width, resize_height, keep_aspect_ratio)
            frames.append(frame)
            total += 1
        reader.close()

        if not frames:
            raise ValueError("No frames loaded. Check path/start_frame/frame_limit.")

        arr = np.stack(frames).astype(np.float32) / 255.0
        images = torch.from_numpy(arr)
        h, w = int(arr.shape[1]), int(arr.shape[2])

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
