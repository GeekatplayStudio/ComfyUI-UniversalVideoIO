PROFILES = {
    "youtube_h264": {
        "container": "mp4",
        "vcodec": "libx264",
        "pix_fmt": "yuv420p",
        "quality_args": ["-crf", "18", "-preset", "slow"],
    },
    "hevc_hq": {
        "container": "mp4",
        "vcodec": "libx265",
        "pix_fmt": "yuv420p10le",
        "quality_args": ["-crf", "20", "-preset", "slow"],
    },
    "av1_web": {
        "container": "mkv",
        "vcodec": "libsvtav1",
        "pix_fmt": "yuv420p",
        "quality_args": ["-crf", "28", "-preset", "6"],
    },
    "vp9_webm": {
        "container": "webm",
        "vcodec": "libvpx-vp9",
        "pix_fmt": "yuv420p",
        "quality_args": ["-crf", "30", "-b:v", "0"],
    },
    "prores_422hq_master": {
        "container": "mov",
        "vcodec": "prores_ks",
        "pix_fmt": "yuv422p10le",
        "quality_args": ["-profile:v", "3"],
    },
    "prores_4444_alpha": {
        "container": "mov",
        "vcodec": "prores_ks",
        "pix_fmt": "yuva444p10le",
        "quality_args": ["-profile:v", "4"],
    },
    "dnxhr_hq_master": {
        "container": "mov",
        "vcodec": "dnxhd",
        "pix_fmt": "yuv422p",
        "quality_args": ["-profile:v", "dnxhr_hq"],
    },
    "dnxhr_hqx_master": {
        "container": "mov",
        "vcodec": "dnxhd",
        "pix_fmt": "yuv422p10le",
        "quality_args": ["-profile:v", "dnxhr_hqx"],
    },
}


def list_profiles():
    return sorted(PROFILES.keys())


def get_profile(name):
    if name not in PROFILES:
        raise ValueError(f"Unknown encoder profile: {name}")
    return PROFILES[name]
