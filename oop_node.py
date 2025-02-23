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
                "Location": ("STRING", {"forceInput": True, "default": ""}),
                "Time": ("STRING", {"forceInput": True, "default": ""}),
                "Sky": ("STRING", {"forceInput": True, "default": ""})
            }
        }

    RETURN_TYPES = ("CONDITIONING", "STRING",)
    FUNCTION = "create_prompt"
    CATEGORY = "Object-Oriented Prompting"

    def create_prompt(self, Clip, Style, View="", Person="", Location="", Time="", Sky=""):
        clip_skip = -3
        prompt_parts = []
        if Style: prompt_parts.append(f"Style({Style})")
        if View: prompt_parts.append(f"View({View})")
        if Person: prompt_parts.append(f"Person({Person})")
        if Location: prompt_parts.append(f"Location({Location})")
        if Time: prompt_parts.append(f"Time({Time})")
        if Sky: prompt_parts.append(f"Sky({Sky})")
        prompt = ", ".join(prompt_parts)

        # Apply CLIP skip
        Clip.clip_layer(clip_skip)
        # Tokenize and process G/L prompts
        tokens = Clip.tokenize(prompt)
        tokens["l"] = Clip.tokenize(prompt)["l"]
        if len(tokens["l"]) != len(tokens["g"]):
            empty = Clip.tokenize("")
            while len(tokens["l"]) < len(tokens["g"]):
                tokens["l"] += empty["l"]
            while len(tokens["l"]) > len(tokens["g"]):
                tokens["g"] += empty["g"]
        # Encode tokens
        cond, pooled = Clip.encode_from_tokens(tokens, return_pooled=True)

        return ([[
            cond,
                {
                "pooled_output": pooled,
                "clip_skip": clip_skip,
                "original_size": (1024, 1024),
                 "crop_coords": (0, 0),
                "target_size": (1024, 1024)
                 }
             ]], prompt)

NODE_CLASS_MAPPINGS = {
    "OOPNode": OOPNode
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "OOPNode": "OOP Node 💫"
}
