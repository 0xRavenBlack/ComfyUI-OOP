class OOPNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "optional": {
                "style": ("OOP_STYLE", {"forceInput": True, "default": ""}),
                "person": ("OOP_PERSON", {"forceInput": True, "default": ""}),
                "view": ("STRING", {"forceInput": True, "default": ""}),
                "location": ("STRING", {"forceInput": True, "default": ""}),
                "time": ("STRING", {"forceInput": True, "default": ""}),
                "sky": ("STRING", {"forceInput": True, "default": ""})
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "create_prompt"
    CATEGORY = "Object-Oriented Prompting"

    def create_prompt(self, **kwargs):
        prompt_parts = []
        for key, value in kwargs.items():
            if value.strip():
                prompt_parts.append(f"{key}({value.strip()})")

        # Combine all object definitions with commas
        prompt = ", ".join(prompt_parts)
        return (prompt,)

NODE_CLASS_MAPPINGS = {
    "OOPNode": OOPNode
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "OOPNode": "OOP Node 💫"
}
