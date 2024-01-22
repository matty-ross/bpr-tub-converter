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
    BLEND_FACTOR = 14
    INV_BLEND_FACTOR = 15
    SRC1_COLOR = 16
    INV_SRC1_COLOR = 17
    SRC1_ALPHA = 18
    INV_SRC1_ALPHA = 19


class BlendOperation(Enum):
    ADD = 1
    SUBTRACT = 2
    REV_SUBTRACT = 3
    MIN = 4
    MAX = 5


class ComparsionFunction(Enum):
    NEVER = 1
    LESS = 2
    EQUAL = 3
    LESS_EQUAL = 4
    GREATER = 5
    NOT_EQUAL = 6
    GREATER_EQUAL = 7
    ALWAYS = 8


class StencilOperation(Enum):
    KEEP = 1
    ZERO = 2
    REPLACE = 3
    INCR_SAT = 4
    DECR_SAT = 5
    INVERT = 6
    INCR = 7
    DECR = 8


class FillMode(Enum):
    WIREFRAME = 2
    SOLID = 3


class CullMode(Enum):
    NONE = 1
    FRONT = 2
    BACK = 3


@dataclass
class RenderTargetBlendState:
    blend_enable: bool = None
    source_blend: Blend = None
    destination_blend: Blend = None
    blend_oepration: BlendOperation = None
    source_blend_alpha: Blend = None
    destination_blend_alpha: Blend = None
    blend_operation_alpha: BlendOperation = None
    color_write_mask: int = None


@dataclass
class BlendState:
    render_target_blend_states: list[RenderTargetBlendState] = None
    blend_factor: tuple[float, float, float, float] = None
    alpha_to_coverage_enable: bool = None
    independent_blend_enable: bool = None


@dataclass
class DepthStencilState:
    depth_function: ComparsionFunction = None
    front_face_stencil_fail_operation: StencilOperation = None
    front_face_stencil_depth_fail_operation: StencilOperation = None
    front_face_stencil_pass_operation: StencilOperation = None
    front_face_stencil_function: ComparsionFunction = None
    back_face_stencil_fail_operation: StencilOperation = None
    back_face_stencil_depth_fail_operation: StencilOperation = None
    back_face_stencil_pass_operation: StencilOperation = None
    back_face_stencil_function: ComparsionFunction = None
    stencil_reference: int = None
    stencil_read_mask: int = None
    stencil_write_mask: int = None
    depth_enable: bool = None
    depth_write_enable: bool = None
    stencil_enable: bool = None


@dataclass
class RasterizerState:
    fill_mode: FillMode = None
    cull_mode: CullMode = None
    front_face: int = None
    depth_bias: int = None
    depth_bias_clamp: float = None
    slope_scaled_depth_bias: float = None
    depth_clip_enable: bool = None
    scissor_enable: bool = None
    multisample_enable: bool = None
    antialiased_line_enable: bool = None


@dataclass
class MaterialState:
    blend_state: BlendState
    depth_stencil_state: DepthStencilState
    rasterizer_state: RasterizerState
