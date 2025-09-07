
from metadata_hub.dao.exif_data import ExifData
from comfy.samplers import SAMPLER_NAMES, SCHEDULER_NAMES

class MetadataHub:
    @classmethod
    def INPUT_TYPES(cls):
        sampler_default = "dpmpp_2m_sde_gpu" if "dpmpp_2m_sde_gpu" in SAMPLER_NAMES else SAMPLER_NAMES[0]
        scheduler_default = "karras" if "karras" in SCHEDULER_NAMES else SCHEDULER_NAMES[0]

        # TODO: Reattempt checkpoint later

        return {
            "required": {
                "seed": ("INT", {"default": 1234567890}),
                "steps": ("INT", {"default": 20}),
                "cfg": ("FLOAT", {"default": 7.0}),
                "sampler_name": (SAMPLER_NAMES, {"default": sampler_default}),
                "scheduler": (SCHEDULER_NAMES, {"default": scheduler_default}),
                "denoise": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "prompt": ("STRING", {"multiline": True, "default": ""}),
                "negative_prompt": ("STRING", {"multiline": True, "default": ""})
            }
        }

    RETURN_TYPES = (
        "EXIFDATA",      # for Save node
        "INT",           # seed
        "INT",           # steps
        "FLOAT",         # cfg
        SAMPLER_NAMES,   # sampler_name
        SCHEDULER_NAMES, # scheduler
        "FLOAT",         # denoise
        "STRING",        # prompt
        "STRING",        # negative_prompt
    )
    RETURN_NAMES = (
        "exifdata",
        "seed",
        "steps",
        "cfg",
        "sampler_name",
        "scheduler",
        "denoise",
        "prompt", 
        "negative_prompt"
    )

    FUNCTION = "make_config"
    CATEGORY = "config"

    def make_config(self, seed, steps, cfg, sampler_name, scheduler, denoise, prompt, negative_prompt):
        exif = ExifData(seed, steps, cfg, sampler_name, scheduler, denoise, prompt, negative_prompt)
        return (exif, seed, steps, cfg, sampler_name, scheduler, denoise, prompt, negative_prompt)
