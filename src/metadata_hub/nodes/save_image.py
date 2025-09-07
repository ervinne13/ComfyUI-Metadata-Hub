
import os
import time
import torch
import numpy as np
from PIL import Image, PngImagePlugin
from metadata_hub.dao.exif_data import ExifData

class SaveImage:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "exifdata": ("EXIFDATA",),
                "prefix": ("STRING", {"default": "output"}),
                "output_dir": ("STRING", {"default": "./output"})
            }
        }

    RETURN_TYPES = ()
    RETURN_NAMES = ()
    FUNCTION = "save_image"
    CATEGORY = "image"
    OUTPUT_NODE = True

    def save_image(self, image, exifdata, prefix, output_dir):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Convert torch.Tensor to numpy and handle extra dimensions
        if isinstance(image, torch.Tensor):
            image = image.cpu().numpy()

        if np.issubdtype(image.dtype, np.floating):
            image = np.squeeze(image)
            image = (image * 255).clip(0, 255).astype(np.uint8)
        else:
            # Only squeeze if shape is (H, W, 1) to avoid removing important dimensions
            if image.ndim == 3 and image.shape[2] == 1:
                image = image[:, :, 0]

        # If image has more than 3 dims, try to get the last 3 as (H, W, C)
            image = image.reshape(image.shape[-3], image.shape[-2], image.shape[-1])
        image = Image.fromarray(image)

        # Exif metadata
        meta = PngImagePlugin.PngInfo()
        meta.add_text("cfg", str(exifdata.cfg))
        meta.add_text("seed", str(exifdata.seed))
        meta.add_text("steps", str(exifdata.steps))
        meta.add_text("sampler_name", exifdata.sampler_name)
        meta.add_text("scheduler", exifdata.scheduler)
        meta.add_text("denoise", str(exifdata.denoise))
        if exifdata.prompt:
            meta.add_text("prompt", exifdata.prompt)
        if exifdata.negative_prompt:
            meta.add_text("negative_prompt", exifdata.negative_prompt)
        if exifdata.checkpoint:
            meta.add_text("checkpoint", exifdata.checkpoint)

        # Filename with timestamp + seed
        filename = f"{prefix}_{int(time.time())}_{exifdata.seed}.png"
        out_path = os.path.join(output_dir, filename)

        image.save(out_path, pnginfo=meta)
        return {}
