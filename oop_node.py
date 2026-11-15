class OOPNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Clip": ("CLIP", ),
            },
            "optional": {
                "Style": ("OOP_STYLE", {"forceInput": True, "default": ""}),
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
    DESCRIPTION = "Assembles the connected OOP sections into one object-oriented prompt and encodes it with the checkpoint's CLIP into SDXL conditioning (clip_l + clip_g). Disconnecting a section drops its line."
    OUTPUT_TOOLTIPS = ("The positive conditioning for the KSampler.",
                       "The assembled prompt, for a text output node.")

    def create_prompt(self, Clip, Style="", View="", Person="", Animal="", Location="", Environment="", clip_skip=-2):
        prompt_parts = []
        for label, section in (("Style", Style), ("Perspective", View), ("Person", Person),
                               ("Animal", Animal), ("Location", Location), ("Environment", Environment)):
            if section.strip():
                prompt_parts.append(f"{label}: {section}")
        prompt = "\n".join(prompt_parts)

        tokens = Clip.tokenize(prompt)
        if "g" not in tokens:
            raise RuntimeError("OOPNode builds SDXL conditioning (clip_g + clip_l); use CLIP Text Encode with single text-encoder checkpoints")
        if len(tokens["l"]) != len(tokens["g"]):
            empty = Clip.tokenize("")
            while len(tokens["l"]) < len(tokens["g"]):
                tokens["l"] += empty["l"]
            while len(tokens["l"]) > len(tokens["g"]):
                tokens["g"] += empty["g"]

        return (self.encode_with_clip_skip(Clip, tokens, clip_skip), prompt)

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
