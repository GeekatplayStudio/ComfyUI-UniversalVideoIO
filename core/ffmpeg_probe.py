import json
import shutil
import subprocess
import tempfile
from pathlib import Path


_CACHE_PATH = Path(tempfile.gettempdir()) / "uvio_ffmpeg_probe_cache.json"


def get_ffmpeg_path(prefer_system=True):
    if prefer_system:
        found = shutil.which("ffmpeg")
        if found:
            return found
    try:
        import imageio_ffmpeg

        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception as exc:
        raise RuntimeError("FFmpeg binary not found. Install ffmpeg or imageio-ffmpeg.") from exc


def ffmpeg_codec_probe(ffmpeg_path=None):
    ffmpeg_path = ffmpeg_path or get_ffmpeg_path()
    proc = subprocess.run([ffmpeg_path, "-hide_banner", "-codecs"], capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        return {"error": proc.stderr.strip() or "ffmpeg codec probe failed", "encoders": {}}
    txt = proc.stdout.lower()
    return {
        "encoders": {
            "libx264": "libx264" in txt,
            "libx265": "libx265" in txt,
            "libsvtav1": "libsvtav1" in txt,
            "libvpx-vp9": "libvpx-vp9" in txt,
            "prores_ks": "prores_ks" in txt,
            "dnxhd": "dnxhd" in txt,
        }
    }


def ensure_ffmpeg_ready():
    if _CACHE_PATH.exists():
        try:
            return json.loads(_CACHE_PATH.read_text())
        except Exception:
            pass
    ffmpeg_path = get_ffmpeg_path()
    codecs = ffmpeg_codec_probe(ffmpeg_path)
    payload = {"ffmpeg_path": ffmpeg_path, **codecs}
    try:
        _CACHE_PATH.write_text(json.dumps(payload))
    except Exception:
        pass
    return payload


def _ffprobe_path(ffmpeg_path):
    folder = ffmpeg_path.rsplit("/", 1)[0] if "/" in ffmpeg_path else ""
    candidate = f"{folder}/ffprobe" if folder else "ffprobe"
    return candidate if shutil.which(candidate) else "ffprobe"


def ffprobe_json(path, ffmpeg_path=None):
    ffmpeg_path = ffmpeg_path or get_ffmpeg_path()
    ffprobe = _ffprobe_path(ffmpeg_path)
    cmd = [
        ffprobe,
        "-v",
        "error",
        "-print_format",
        "json",
        "-show_streams",
        "-show_format",
        path,
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        return {"error": proc.stderr.strip() or "ffprobe failed"}
    return json.loads(proc.stdout or "{}")
