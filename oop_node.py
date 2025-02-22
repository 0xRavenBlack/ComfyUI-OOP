class OOPNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "optional": {
                "Style": ("OOP_STYLE", {"forceInput": True, "default": ""}),
                "Person": ("OOP_PERSON", {"forceInput": True, "default": ""}),
                "View": ("STRING", {"forceInput": True, "default": ""}),
                "Location": ("STRING", {"forceInput": True, "default": ""}),
                "Time": ("STRING", {"forceInput": True, "default": ""}),
                "Sky": ("STRING", {"forceInput": True, "default": ""})
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
