from pathlib import Path

import imageio
import numpy as np

try:
    from ..core.validation import ensure_image_batch
except Exception:  # pragma: no cover
    from core.validation import ensure_image_batch


class UV_SaveSequence:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "output_dir": ("STRING", {"default": "frames"}),
                "format": (["png", "jpg", "exr"],),
                "name_template": ("STRING", {"default": "frame_[counter]"}),
                "padding": ("INT", {"default": 6, "min": 1, "max": 10}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("output_dir",)
    FUNCTION = "save_sequence"
    CATEGORY = "UniversalVideoIO"
    OUTPUT_NODE = True

    def save_sequence(self, images, output_dir, format="png", name_template="frame_[counter]", padding=6):
        images = ensure_image_batch(images)
        data = images.detach().cpu().numpy()
        if format.lower() == "exr":
            data = np.clip(data.astype(np.float32), 0.0, 1.0)
        else:
            data = np.clip(data * 255.0, 0, 255).astype(np.uint8)

        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)
        for i, frame in enumerate(data):
            counter = str(i).zfill(padding)
            name = name_template.replace("[counter]", counter)
            imageio.imwrite(out / f"{name}.{format}", frame)
        return (str(out),)
