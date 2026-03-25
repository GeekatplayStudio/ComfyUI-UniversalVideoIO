from .encoder_profiles import get_profile


def build_sequence_pattern(folder, ext="png"):
    return f"{folder.rstrip('/')}/frame_%06d.{ext}"


def build_video_command(
    ffmpeg_path,
    input_pattern,
    output_path,
    fps,
    profile_name,
    overwrite=True,
    audio_path=None,
    pix_fmt_override="auto",
    quality_args_override="",
    color_range="auto",
    colorspace="auto",
):
    profile = get_profile(profile_name)
    cmd = [ffmpeg_path, "-hide_banner", "-loglevel", "error"]
    cmd.append("-y" if overwrite else "-n")
    cmd += ["-framerate", str(fps), "-i", input_pattern]
    if audio_path:
        cmd += ["-i", audio_path, "-shortest"]
    pix_fmt = profile["pix_fmt"] if pix_fmt_override == "auto" else pix_fmt_override
    quality_args = profile["quality_args"]
    if quality_args_override.strip():
        quality_args = quality_args_override.strip().split()
    cmd += [
        "-c:v",
        profile["vcodec"],
        "-pix_fmt",
        pix_fmt,
        *quality_args,
    ]
    if color_range != "auto":
        cmd += ["-color_range", color_range]
    if colorspace != "auto":
        cmd += ["-colorspace", colorspace]
    cmd += [output_path]
    return cmd
