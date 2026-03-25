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
):
    profile = get_profile(profile_name)
    cmd = [ffmpeg_path, "-hide_banner", "-loglevel", "error"]
    cmd.append("-y" if overwrite else "-n")
    cmd += ["-framerate", str(fps), "-i", input_pattern]
    if audio_path:
        cmd += ["-i", audio_path, "-shortest"]
    cmd += [
        "-c:v",
        profile["vcodec"],
        "-pix_fmt",
        profile["pix_fmt"],
        *profile["quality_args"],
        output_path,
    ]
    return cmd
