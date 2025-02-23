import gc
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

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
                "Location": ("OOP_LOCATION", {"forceInput": True, "default": ""}),
                "Time": ("STRING", {"forceInput": True, "default": ""}),
                "Sky": ("STRING", {"forceInput": True, "default": ""})
            }
        }

    RETURN_TYPES = ("CONDITIONING", "STRING",)
    FUNCTION = "create_prompt"
    CATEGORY = "Object-Oriented Prompting"

    def _process_prompt(self, prompt):
        device="cuda"
        model_name = "Qwen/Qwen2.5-0.5B-Instruct"
        model = AutoModelForCausalLM.from_pretrained(
                model_name,
                device_map=device,
                torch_dtype="auto",
        )
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        system_prompt = (
            "Transform concepts into concise, high-detail Stable Diffusion XL prompts. "
            "Use vivid descriptors for *subject, style/medium, composition, lighting/colors, and key details* "
            "(e.g., 'ultra-realistic', 'cinematic lighting', 'vivid neon'). Structure as: "
            "`[Subject/action], [style/medium], [lighting/colors], [composition], [specific details], [technical terms]`."
        )
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ]
        text = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        model_inputs = tokenizer([text], return_tensors="pt").to(device)

        generated_ids = model.generate(
            **model_inputs,
            max_new_tokens=512
        )
        generated_ids = [
            output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]
        response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        return response

    def create_prompt(self, Clip, Style, View="", Person="", Location="", Time="", Sky=""):
        clip_skip = -3
        prompt_parts = []
        if Style: prompt_parts.append(f"Style({Style})")
        if View: prompt_parts.append(f"View({View})")
        if Person: prompt_parts.append(f"Person({Person})")
        if Location: prompt_parts.append(f"Location({Location})")
        if Time: prompt_parts.append(f"Time({Time})")
        if Sky: prompt_parts.append(f"Sky({Sky})")
        oop_prompt = ", ".join(prompt_parts)
        prompt = self._process_prompt(oop_prompt)

        # Force garbage collection
        gc.collect()
        torch.cuda.empty_cache()

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
