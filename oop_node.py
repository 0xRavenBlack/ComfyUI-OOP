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
                "clip_skip": ("INT", {"default": 0, "min": -24, "max": 0, "step": 1,
                                      "tooltip": "Advanced. 0 keeps the layer the checkpoint loaded, which is already correct for SD1.5, SDXL, Flux, Flux2/Flux3, Krea2 and Ernie. A negative value re-encodes CLIP-style text encoders from that layer."})
            }
        }

    RETURN_TYPES = ("CONDITIONING", "STRING",)
    FUNCTION = "create_prompt"
    CATEGORY = "Object-Oriented Prompting"
    DESCRIPTION = "Assembles the connected OOP sections into one object-oriented prompt and encodes it with whatever text encoder the checkpoint provides, so it works for SDXL, SD1.5, Flux, Flux2, Flux3, Krea2, Ernie and any other model. Disconnecting a section drops its line."
    OUTPUT_TOOLTIPS = ("The positive conditioning for the KSampler.",
                       "The assembled prompt, for a text output node.")

    def create_prompt(self, Clip, Style="", View="", Person="", Animal="", Location="", Environment="", clip_skip=0):
        prompt_parts = []
        for label, section in (("Style", Style), ("Perspective", View), ("Person", Person),
                               ("Animal", Animal), ("Location", Location), ("Environment", Environment)):
            if section.strip():
                prompt_parts.append(f"{label}: {section}")
        prompt = "\n".join(prompt_parts)

        tokens = Clip.tokenize(prompt)
        # Only dual text encoders like SDXL's clip_g + clip_l need equal token-list
        # lengths; single-encoder tokenizers (Flux, Flux2/3, Krea2, Ernie, T5, …)
        # return their own layout and must be passed through untouched.
        if "l" in tokens and "g" in tokens and len(tokens["l"]) != len(tokens["g"]):
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
