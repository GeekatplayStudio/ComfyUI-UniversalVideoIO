# ComfyUI-UniversalVideoIO

Dedicated ComfyUI custom node pack for production-ready video import/export with FFmpeg profiles, mastering presets, sequence output, and image-batch-to-latent workflows.

Maintained by **Geekatplay Studio**.

## Nodes
- UV_LoadVideo
- UV_SaveVideo
- UV_SaveMaster
- UV_SaveSequence
- UV_MetadataProbe
- UV_ImageBatchToLatent
- UV_CodecPreset
- UV_AudioMux
- UV_TranscodeVideo

## Install (Git Clone)
1. Clone into `ComfyUI/custom_nodes/ComfyUI-UniversalVideoIO`
2. Install deps: `pip install -r requirements.txt`
3. Restart ComfyUI

## Install (ComfyUI-Manager / Registry)
- Ensure `[tool.comfy]` in `pyproject.toml` has your real `PublisherId`.
- Publish with Comfy Registry flow (`comfy node publish`).
- Then install/update from ComfyUI-Manager in one click.

## V1 Coverage
- Pixel video import: `UV_LoadVideo` (frames + metadata + audio presence token)
- Video export: `UV_SaveVideo` (preset or advanced quality args)
- Mastering export presets: `UV_SaveMaster`
- Sequence export: `UV_SaveSequence` (PNG/JPG/EXR)
- Latent bridge: `UV_ImageBatchToLatent` (regular or tiled VAE encode)
- Metadata probe: `UV_MetadataProbe`
- Profile selector: `UV_CodecPreset`
- Audio mux: `UV_AudioMux`
- Transcode utility: `UV_TranscodeVideo`

## Notes
- FFmpeg is resolved from system PATH first, then `imageio-ffmpeg`.
- V1 supports pixel-video workflows and IMAGE->LATENT bridging.
- Direct model-native latent video bridges are deferred to model-family-specific V2 nodes.
- Relative import fallbacks are included for ComfyUI custom-node loading contexts.
