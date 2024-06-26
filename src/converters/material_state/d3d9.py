from dataclasses import dataclass
from enum import Enum


class Blend(Enum):
    ZERO = 1
    ONE = 2
    SRC_COLOR = 3
    INV_SRC_COLOR = 4
    SRC_ALPHA = 5
    INV_SRC_ALPHA = 6
    DEST_ALPHA = 7
    INV_DEST_ALPHA = 8
    DEST_COLOR = 9
    INV_DEST_COLOR = 10
    SRC_ALPHA_SAT = 11


class CullMode(Enum):
    NONE = 1
    CW = 2
    CCW = 3


@dataclass
class BlendState:
    source_blend: Blend = None
    destination_blend: Blend = None
    alpha_blend_enable: bool = None
    alpha_to_coverage_enable: bool = None


@dataclass
class DepthStencilState:
    z_write_enable: bool = None


@dataclass
class RasterizerState:
    cull_mode: CullMode = None


@dataclass
class MaterialState:
    blend_state: BlendState = None
    depth_stencil_state: DepthStencilState = None
    rasterizer_state: RasterizerState = None

    def __post_init__(self):
        self.blend_state = BlendState()
        self.depth_stencil_state = DepthStencilState()
        self.rasterizer_state = RasterizerState()
