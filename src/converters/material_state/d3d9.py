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
    BOTH_SRC_ALPHA = 12
    BOTH_INV_SRC_ALPHA = 13
    BLEND_FACTOR = 14
    INV_BLEND_FACTOR = 15
    SRC_COLOR_2 = 16
    INV_SRC_COLOR_2 = 17


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


class ZBufferType(Enum):
    FALSE = 0
    TRUE = 1
    USE_W = 2


class FillMode(Enum):
    POINT = 1
    WIREFRAME = 2
    SOLID = 3


class CullMode(Enum):
    NONE = 1
    CW = 2
    CCW = 3


@dataclass
class BlendState:
    source_blend: Blend = None
    blend_oepration: BlendOperation = None
    destination_blend: Blend = None
    source_blend_alpha: Blend = None
    blend_operation_alpha: BlendOperation = None
    destination_blend_alpha: Blend = None
    color_write_enable: tuple[int, int, int, int] = None
    blend_factor: tuple[float, float, float, float] = None
    alpha_blend_enable: bool = None
    separate_alpha_blend_enable: bool = None
    alpha_test_enable: bool = None
    alpha_function: ComparsionFunction = None
    alpha_reference: int = None
    alpha_to_coverage_enable: bool = None


@dataclass
class DepthStencilState:
    z_function: ComparsionFunction = None
    stencil_fail_operation: StencilOperation = None
    stencil_z_fail_operation: StencilOperation = None
    stencil_pass_operation: StencilOperation = None
    stencil_function: ComparsionFunction = None
    ccw_stencil_fail_operation: StencilOperation = None
    ccw_stencil_z_fail_operation: StencilOperation = None
    ccw_stencil_pass_operation: StencilOperation = None
    ccw_stencil_function: ComparsionFunction = None
    stencil_reference: int = None
    stencil_mask: int = None
    stencil_write_mask: int = None
    z_enable: ZBufferType = None
    z_write_enable: bool = None
    stencil_enable: bool = None
    two_sided_stencil_mode_enable: bool = None


@dataclass
class RasterizerState:
    fill_mode: FillMode = None
    cull_mode: CullMode = None
    depth_bias: float = None
    slope_scale_depth_bias: float = None
    multisample_mask: int = None
    scissor_test_enable: bool = None
    multisample_antialias_enable: bool = None
    srgb_write_enable: bool = None
    antialiased_line_enable: bool = None


@dataclass
class MaterialState:
    blend_state: BlendState
    depth_stencil_state: DepthStencilState
    rasterizer_state: RasterizerState
