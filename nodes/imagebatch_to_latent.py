class UV_ImageBatchToLatent:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "vae": ("VAE",),
                "tiled": ("BOOLEAN", {"default": False}),
                "tile_size": ("INT", {"default": 512, "min": 64, "max": 2048}),
            }
        }

    RETURN_TYPES = ("LATENT",)
    RETURN_NAMES = ("latent",)
    FUNCTION = "encode"
    CATEGORY = "UniversalVideoIO"

    def encode(self, images, vae, tiled=False, tile_size=512):
        if tiled and hasattr(vae, "encode_tiled"):
            latent = vae.encode_tiled(images[:, :, :, :3], tile_x=tile_size, tile_y=tile_size)
        else:
            latent = vae.encode(images[:, :, :, :3])
        if isinstance(latent, dict):
            return (latent,)
        return ({"samples": latent},)
