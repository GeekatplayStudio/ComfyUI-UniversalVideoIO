try:
    from .save_video import UV_SaveVideo
    from .save_sequence import UV_SaveSequence
except Exception:  # pragma: no cover
    from nodes.save_video import UV_SaveVideo
    from nodes.save_sequence import UV_SaveSequence


MASTER_PRESETS = {
    "Editorial Master — ProRes 422 HQ": "prores_422hq_master",
    "Alpha Master — ProRes 4444": "prores_4444_alpha",
    "Post Master — DNxHR HQ": "dnxhr_hq_master",
    "Post Master — DNxHR HQX": "dnxhr_hqx_master",
    "Archive Frames — PNG Sequence": "png_sequence",
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
        self._save_sequence = UV_SaveSequence()

    def save_master(self, images, output_path, preset, fps=24.0, overwrite=True):
        if MASTER_PRESETS[preset] == "png_sequence":
            return self._save_sequence.save_sequence(images, output_path, "png", "frame_[counter]", 6)
        return self._save_video.save(
            images=images,
            output_path=output_path,
            profile=MASTER_PRESETS[preset],
            fps=fps,
            quality_mode="preset",
            overwrite=overwrite,
            audio_mode="none",
            pix_fmt="auto",
            color_range="auto",
            colorspace="auto",
            audio_path="",
            advanced_quality_args="",
        )
