class OOPNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Clip": ("CLIP", ),
                "Style": ("OOP_STYLE", {"forceInput": True, "default": ""}),
            },
            "optional": {
                "Person": ("OOP_PERSON", {"forceInput": True, "default": ""}),
                "View": ("STRING", {"forceInput": True, "default": ""}),
                "Location": ("STRING", {"forceInput": True, "default": ""}),
                "Time": ("STRING", {"forceInput": True, "default": ""}),
                "Sky": ("STRING", {"forceInput": True, "default": ""})
            }
        }

    RETURN_TYPES = ("CONDITIONING", "STRING",)
    FUNCTION = "create_prompt"
    CATEGORY = "Object-Oriented Prompting"

    def create_prompt(self, Clip, Style, Person="", View="", Location="", Time="", Sky=""):
        clip_skip = -2
        prompt=""
        if Style:
            prompt+=f"Style({Style})"
        if Person != "":
            prompt+=f" ,Person({Person})"
        if View != "":
            prompt+=f" ,View({View})"
        if Location != "":
            prompt+=f" ,Location({Location})"
        if Time != "":
            prompt+=f" ,Location({Time})"
        if Sky != "":
            prompt+=f" ,Location({Sky})"

        Clip.clip_layer(clip_skip)

        tokenized_text = prompt.replace(" ", "")
        # Tokenize with compatibility
        try:
            # Try modern SDLongClipModel syntax
            tokens = Clip.tokenize(tokenized_text, truncate=False)
        except TypeError:
            # Fallback for standard CLIP
            tokens = Clip.tokenize(tokenized_text)

         # Encode text using CLIP
        cond, pooled = Clip.encode_from_tokens(tokens, return_pooled=True)
        # Format conditioning output
        conditioning = [[
                    cond, {
                        "pooled_output": pooled,
                        "clip_skip": clip_skip,
                        "token_normalization": "mean",
                        "original_size": (1024, 1024),
                        "crop_coords": (0, 0),
                    }
                ]]
        return (conditioning, prompt,)

NODE_CLASS_MAPPINGS = {
    "OOPNode": OOPNode
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "OOPNode": "OOP Node 💫"
}
