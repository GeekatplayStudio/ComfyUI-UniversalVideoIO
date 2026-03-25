NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

try:
    from .core.ffmpeg_probe import ensure_ffmpeg_ready
    from .nodes.audio_mux import UV_AudioMux
    from .nodes.codec_preset import UV_CodecPreset
    from .nodes.imagebatch_to_latent import UV_ImageBatchToLatent
    from .nodes.load_video import UV_LoadVideo
    from .nodes.metadata_probe import UV_MetadataProbe
    from .nodes.save_master import UV_SaveMaster
    from .nodes.save_sequence import UV_SaveSequence
    from .nodes.save_video import UV_SaveVideo
    from .nodes.transcode_video import UV_TranscodeVideo

    NODE_CLASS_MAPPINGS = {
        "UV_AudioMux": UV_AudioMux,
        "UV_CodecPreset": UV_CodecPreset,
        "UV_LoadVideo": UV_LoadVideo,
        "UV_SaveVideo": UV_SaveVideo,
        "UV_SaveMaster": UV_SaveMaster,
        "UV_SaveSequence": UV_SaveSequence,
        "UV_ImageBatchToLatent": UV_ImageBatchToLatent,
        "UV_MetadataProbe": UV_MetadataProbe,
        "UV_TranscodeVideo": UV_TranscodeVideo,
    }

    NODE_DISPLAY_NAME_MAPPINGS = {
        "UV_AudioMux": "UV Audio Mux",
        "UV_CodecPreset": "UV Codec Preset",
        "UV_LoadVideo": "UV Load Video",
        "UV_SaveVideo": "UV Save Video",
        "UV_SaveMaster": "UV Save Master",
        "UV_SaveSequence": "UV Save Sequence",
        "UV_ImageBatchToLatent": "UV ImageBatch To Latent",
        "UV_MetadataProbe": "UV Metadata Probe",
        "UV_TranscodeVideo": "UV Transcode Video",
    }
    ensure_ffmpeg_ready()
except Exception:
    pass
