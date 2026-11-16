# __init__.py
# V3 registration: the ComfyUI loader prefers comfy_entrypoint over NODE_CLASS_MAPPINGS,
# so the mappings are intentionally not defined here.
from comfy_api.latest import io, ComfyExtension
from typing_extensions import override

from .oop_node import OOPNode
from .oop_person_node import OOPPersonNode
from .oop_hair_node import OOPHairNode
from .oop_clothing_node import OOPClothingNode
from .oop_mouth_node import OOPMouthNode
from .oop_eyes_node import OOPEyesNode
from .oop_pose_node import OOPPoseNode
from .oop_style_node import OOPStyleNode
from .oop_view_node import OOPViewNode
from .oop_location_node import OOPLocationNode
from .oop_animal_node import OOPAnimalNode
from .oop_environment_node import OOPEnvironmentNode
from .oop_expression_node import OOPExpressionNode
from .oop_lighting_node import OOPLightingNode
from .oop_background_node import OOPBackgroundNode


class OOPExtension(ComfyExtension):
    @override
    async def get_node_list(self) -> list[type[io.ComfyNode]]:
        return [
            OOPNode,
            OOPPersonNode,
            OOPHairNode,
            OOPClothingNode,
            OOPMouthNode,
            OOPEyesNode,
            OOPPoseNode,
            OOPStyleNode,
            OOPViewNode,
            OOPLocationNode,
            OOPAnimalNode,
            OOPEnvironmentNode,
            OOPExpressionNode,
            OOPLightingNode,
            OOPBackgroundNode,
        ]


async def comfy_entrypoint() -> OOPExtension:
    return OOPExtension()
