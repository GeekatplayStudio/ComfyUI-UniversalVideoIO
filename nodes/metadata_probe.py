import json

try:
    from ..core.ffmpeg_probe import ffprobe_json
except Exception:  # pragma: no cover
    from core.ffmpeg_probe import ffprobe_json


class UV_MetadataProbe:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "path": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("metadata_json",)
    FUNCTION = "probe"
    CATEGORY = "UniversalVideoIO"

    def probe(self, path):
        raw = ffprobe_json(path)
        streams = raw.get("streams", [])
        v = next((s for s in streams if s.get("codec_type") == "video"), {})
        a = next((s for s in streams if s.get("codec_type") == "audio"), {})
        summary = {
            "container": raw.get("format", {}).get("format_name", ""),
            "codec": v.get("codec_name", ""),
            "fps": v.get("r_frame_rate", ""),
            "duration": raw.get("format", {}).get("duration", ""),
            "resolution": f"{v.get('width', 0)}x{v.get('height', 0)}",
            "audio_present": bool(a),
            "alpha_likely_present": "a" in str(v.get("pix_fmt", "")),
        }
        return (json.dumps(summary),)
