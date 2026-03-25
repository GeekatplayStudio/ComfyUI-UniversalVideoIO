def ensure_image_batch(images):
    if images is None:
        raise ValueError("IMAGE batch is required")
    if not hasattr(images, "shape") or len(images.shape) != 4:
        raise ValueError("Expected IMAGE batch tensor with shape [B, H, W, C]")
    if images.shape[-1] not in (3, 4):
        raise ValueError("Expected RGB or RGBA channels")
    return images
