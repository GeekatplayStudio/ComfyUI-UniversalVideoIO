# ComfyUI Universal Video IO

Minimal ComfyUI custom node pack for video import/export with FFmpeg profiles and sequence output.

## Nodes
- UV_LoadVideo
- UV_SaveVideo
- UV_SaveMaster
- UV_SaveSequence
- UV_MetadataProbe
- UV_ImageBatchToLatent
- UV_CodecPreset
- UV_AudioMux

## Install
1. Clone into `ComfyUI/custom_nodes/ComfyUI-UniversalVideoIO`
2. Install deps: `pip install -r requirements.txt`
3. Restart ComfyUI

## Notes
- FFmpeg is resolved from system PATH first, then `imageio-ffmpeg`.
- V1 supports pixel-video workflows and IMAGE->LATENT bridging.
- Relative import fallbacks are included for ComfyUI custom-node loading contexts.
