import os
import time
import torch, numpy as np
from PIL import Image, PngImagePlugin
from comfy.samplers import SAMPLER_NAMES, SCHEDULER_NAMES

class ExifData:
    def __init__(self, seed, steps, cfg, sampler_name, scheduler, denoise):
        self.seed = seed
        self.steps = steps
        self.cfg = cfg
        self.sampler_name = sampler_name
        self.scheduler = scheduler
        self.denoise = denoise

class MetadataHub:
    @classmethod
    def INPUT_TYPES(cls):
        sampler_default = "dpmpp_2m_sde_gpu" if "dpmpp_2m_sde_gpu" in SAMPLER_NAMES else SAMPLER_NAMES[0]
        scheduler_default = "karras" if "karras" in SCHEDULER_NAMES else SCHEDULER_NAMES[0]

        return {
            "required": {
                "seed": ("INT", {"default": 1234567890}),
                "steps": ("INT", {"default": 20}),
                "cfg": ("FLOAT", {"default": 7.0}),
                "sampler_name": (SAMPLER_NAMES, {"default": sampler_default}),
                "scheduler": (SCHEDULER_NAMES, {"default": scheduler_default}),
                "denoise": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
            }
        }

    RETURN_TYPES = (
        "EXIFDATA",  # for your Save node
        "INT",       # seed
        "INT",       # steps
        "FLOAT",     # cfg
        SAMPLER_NAMES,   # sampler_name (dropdown type, not string)
        SCHEDULER_NAMES, # scheduler (dropdown type, not string)
        "FLOAT",     # denoise
    )
    RETURN_NAMES = (
        "exifdata",
        "seed",
        "steps",
        "cfg",
        "sampler_name",
        "scheduler",
        "denoise"
    )

    FUNCTION = "make_config"
    CATEGORY = "config"

    def make_config(self, seed, steps, cfg, sampler_name, scheduler, denoise):
        exif = ExifData(seed, steps, cfg, sampler_name, scheduler, denoise)
        return (exif, seed, steps, cfg, sampler_name, scheduler, denoise)

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

        if isinstance(image, torch.Tensor):
            image = image.squeeze(0).cpu().numpy()
            image = (image * 255).clip(0, 255).astype(np.uint8)
            image = Image.fromarray(image)

        # Exif
        meta = PngImagePlugin.PngInfo()
        meta.add_text("cfg", str(exifdata.cfg))
        meta.add_text("seed", str(exifdata.seed))
        meta.add_text("steps", str(exifdata.steps))
        meta.add_text("sampler_name", exifdata.sampler_name)
        meta.add_text("scheduler", exifdata.scheduler)
        meta.add_text("denoise", str(exifdata.denoise))

        filename = f"{prefix}_{int(time.time())}_{exifdata.seed}.png"
        out_path = os.path.join(output_dir, filename)

        image.save(out_path, pnginfo=meta)
        return {}

CUSTOM_TYPE_CLASSES = {
    "EXIFDATA": ExifData,
}

NODE_CLASS_MAPPINGS = {
    "Metadata Hub": MetadataHub,
    "Save Image With Metadata": SaveImage,
}