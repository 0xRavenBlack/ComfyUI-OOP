from comfy_api.latest import io
from .oop_shared import OOP_STYLE, OOP_VIEW, OOP_PERSON, OOP_ANIMAL, OOP_LOCATION, OOP_ENVIRONMENT, OOP_LIGHTING, OOP_BACKGROUND


class OOPNode(io.ComfyNode):
    @classmethod
    def define_schema(cls):
        return io.Schema(
            node_id="OOPNode",
            display_name="OOP Node 💫",
            category="Object-Oriented Prompting",
            description="Assembles the connected OOP sections into one object-oriented prompt and encodes it with whatever text encoder the checkpoint provides, so it works for SDXL, SD1.5, Flux, Flux2, Flux3, Krea2, Ernie and any other model. Disconnecting a section drops its line.",
            inputs=[
                io.Clip.Input("Clip"),
                OOP_STYLE.Input("Style", optional=True),
                OOP_VIEW.Input("View", optional=True),
                OOP_PERSON.Input("Person", optional=True),
                OOP_ANIMAL.Input("Animal", optional=True),
                OOP_LOCATION.Input("Location", optional=True),
                OOP_ENVIRONMENT.Input("Environment", optional=True),
                OOP_LIGHTING.Input("Lighting", optional=True),
                OOP_BACKGROUND.Input("Background", optional=True),
                # 0 = keep the layer the checkpoint loaded; negative = encode from that layer
                io.Int.Input("clip_skip", default=0, min=-24, max=0, step=1,
                             tooltip="Advanced. 0 keeps the layer the checkpoint loaded, which is already correct for SD1.5, SDXL, Flux, Flux2/Flux3, Krea2 and Ernie. A negative value re-encodes CLIP-style text encoders from that layer."),
            ],
            outputs=[
                io.Conditioning.Output("conditioning", tooltip="The positive conditioning for the KSampler."),
                io.String.Output("prompt", tooltip="The assembled prompt, for a text output node."),
            ],
        )

    @classmethod
    def execute(cls, Clip, Style=None, View=None, Person=None, Animal=None, Location=None, Environment=None, Lighting=None, Background=None, clip_skip=0) -> io.NodeOutput:
        prompt_parts = []
        for label, section in (("Style", Style), ("Perspective", View), ("Person", Person),
                               ("Animal", Animal), ("Location", Location), ("Environment", Environment),
                               ("Lighting", Lighting), ("Background", Background)):
            if section and section.strip():
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

        return io.NodeOutput(cls.encode_with_clip_skip(Clip, tokens, clip_skip), prompt)

    @classmethod
    def encode_with_clip_skip(cls, Clip, tokens, clip_skip):
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
