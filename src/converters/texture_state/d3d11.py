from dataclasses import dataclass
from enum import Enum


class TextureAddressMode(Enum):
    WRAP = 1
    MIRROR = 2
    CLAMP = 3
    BORDER = 4
    MIRROR_ONCE = 5


class TextureFilterType(Enum):
    POINT = 0
    LINEAR = 1


class CompasrionFunction(Enum):
    NEVER = 1
    LESS = 2
    EQUAL = 3
    LESS_EQUAL = 4
    GREATER = 5
    NOT_EQUAL = 6
    GREATER_EQUAL = 7
    ALWAYS = 8


@dataclass
class SamplerState:
    address_mode_u: TextureAddressMode = None
    address_mode_v: TextureAddressMode = None
    address_mode_w: TextureAddressMode = None
    magnification_filter: TextureFilterType = None
    minification_filter: TextureFilterType = None
    mipmap_filter: TextureFilterType = None
    min_lod: float = None
    max_lod: float = None
    max_anisotropy: int = None
    mipmap_lod_bias: float = None
    comparsion_function: CompasrionFunction = None
    use_border_color: bool = None


@dataclass
class TextureState:
    sampler_state: SamplerState = None

    def __post_init__(self):
        self.sampler_state = SamplerState()
