import json
import shutil
import subprocess


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
