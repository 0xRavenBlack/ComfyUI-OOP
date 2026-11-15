import gc

class OOPNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Clip": ("CLIP", ),
                "Style": ("OOP_STYLE", {"forceInput": True, "default": ""}),
            },
            "optional": {
                "View": ("OOP_VIEW", {"forceInput": True, "default": ""}),
                "Person": ("OOP_PERSON", {"forceInput": True, "default": ""}),
                "Animal": ("OOP_ANIMAL", {"forceInput": True, "default": ""}),
                "Location": ("OOP_LOCATION", {"forceInput": True, "default": ""}),
                "Environment": ("OOP_ENVIRONMENT", {"forceInput": True, "default": ""}),
                # 0 = keep the layer the checkpoint loaded; negative = encode from that layer
                "clip_skip": ("INT", {"default": -2, "min": -24, "max": 0, "step": 1,
                                      "tooltip": "CLIP layer to encode at. 0 keeps the checkpoint's own layer; -2 is already SDXL's default."})
            }
        }

    RETURN_TYPES = ("CONDITIONING", "STRING",)
    FUNCTION = "create_prompt"
    CATEGORY = "Object-Oriented Prompting"

    def create_prompt(self, Clip, Style, View="", Person="", Animal="", Location="", Environment="", clip_skip=-2):
        prompt_parts = []
        if Style: prompt_parts.append(f"Style: {Style}")
        if View: prompt_parts.append(f"Perspective: {View}")
        if Person: prompt_parts.append(f"Person: {Person}")
        if Animal: prompt_parts.append(f"Animal: {Animal}")
        if Location: prompt_parts.append(f"Location: {Location}")
        if Environment: prompt_parts.append(f"Environment: {Environment}")
        prompt = "\n".join(prompt_parts)

        # Force garbage collection
        gc.collect()

        # Tokenize and process G/L prompts
        tokens = Clip.tokenize(prompt)
        if "g" not in tokens:
            raise RuntimeError("OOPNode builds SDXL conditioning (clip_g + clip_l); use CLIP Text Encode with single text-encoder checkpoints")
        tokens["l"] = Clip.tokenize(prompt)["l"]
        if len(tokens["l"]) != len(tokens["g"]):
            empty = Clip.tokenize("")
            while len(tokens["l"]) < len(tokens["g"]):
                tokens["l"] += empty["l"]
            while len(tokens["l"]) > len(tokens["g"]):
                tokens["g"] += empty["g"]
        # Encode tokens exactly as ComfyUI's own SDXL encoder does, so the
        # conditioning carries only what the sampler reads (pooled output, plus
        # any clip-schedule/hook data) instead of invented, hard-coded metadata.
        conditioning = self.encode_with_clip_skip(Clip, tokens, clip_skip)

        return (conditioning, prompt)

    def encode_with_clip_skip(self, Clip, tokens, clip_skip):
        if not clip_skip:
            return Clip.encode_from_tokens_scheduled(tokens)

        # clip_layer() stores layer_idx on the CLIP wrapper the whole graph shares,
        # and every later encode re-applies it, so the skip is set only around this
        # encode and the graph's previous value is put back afterwards.
        previous_layer_idx = getattr(Clip, "layer_idx", None)
        try:
            Clip.clip_layer(clip_skip)
            return Clip.encode_from_tokens_scheduled(tokens)
        finally:
            Clip.layer_idx = previous_layer_idx

NODE_CLASS_MAPPINGS = {
    "OOPNode": OOPNode
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "OOPNode": "OOP Node 💫"
}
