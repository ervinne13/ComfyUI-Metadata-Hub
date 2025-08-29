class ExifData:
    def __init__(self, seed, steps, cfg, sampler_name, scheduler, denoise,
                 prompt="", negative_prompt="", checkpoint=""):
        self.seed = seed
        self.steps = steps
        self.cfg = cfg
        self.sampler_name = sampler_name
        self.scheduler = scheduler
        self.denoise = denoise
        self.prompt = prompt
        self.negative_prompt = negative_prompt
        self.checkpoint = checkpoint