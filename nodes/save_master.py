try:
    from .save_video import UV_SaveVideo
except Exception:  # pragma: no cover
    from nodes.save_video import UV_SaveVideo


MASTER_PRESETS = {
    "Editorial Master — ProRes 422 HQ": "prores_422hq_master",
    "Alpha Master — ProRes 4444": "prores_4444_alpha",
    "Post Master — DNxHR HQ": "dnxhr_hq_master",
    "YouTube MP4": "youtube_h264",
}


class UV_SaveMaster:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "output_path": ("STRING", {"default": "master.mov"}),
                "preset": (list(MASTER_PRESETS.keys()),),
                "fps": ("FLOAT", {"default": 24.0, "min": 1.0, "max": 240.0}),
                "overwrite": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("saved_path",)
    FUNCTION = "save_master"
    CATEGORY = "UniversalVideoIO"
    OUTPUT_NODE = True

    def __init__(self):
        self._save_video = UV_SaveVideo()

    def save_master(self, images, output_path, preset, fps=24.0, overwrite=True):
        return self._save_video.save(images, output_path, MASTER_PRESETS[preset], fps, overwrite, "")
