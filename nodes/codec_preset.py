class UV_CodecPreset:
    PRESET_MAP = {
        "YouTube MP4": "youtube_h264",
        "High Quality HEVC": "hevc_hq",
        "AV1 Web": "av1_web",
        "VP9 WebM": "vp9_webm",
        "ProRes 422 HQ Master": "prores_422hq_master",
        "ProRes 4444 Alpha Master": "prores_4444_alpha",
        "DNxHR Master": "dnxhr_hq_master",
    }

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"preset": (list(cls.PRESET_MAP.keys()),)}}

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("profile",)
    FUNCTION = "select"
    CATEGORY = "UniversalVideoIO"

    def select(self, preset):
        return (self.PRESET_MAP[preset],)
