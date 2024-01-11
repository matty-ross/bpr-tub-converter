from dataclasses import dataclass
from enum import Enum


class TextureAddressMode(Enum):
    WRAP = 1
    MIRROR = 2
    CLAMP = 3
    BORDER = 4
    MIRROR_ONCE = 5


class TextureFilterType(Enum):
    NONE = 0
    POINT = 1
    LINEAR = 2
    ANISOTROPIC = 3
    PYRAMIDAL_QUAD = 6
    GAUSSIAN_QUAD = 7
    CONVOLUTION_MONO = 8


@dataclass
class SamplerState:
    address_mode_u: TextureAddressMode = None
    address_mode_v: TextureAddressMode = None
    address_mode_w: TextureAddressMode = None
    magnification_filter: TextureFilterType = None
    minification_filter: TextureFilterType = None
    mipmap_filter: TextureFilterType = None
    max_mipmap_level: int = None
    max_anisotropy: int = None
    mipmap_lod_bias: float = None
    border_color: int = None


@dataclass
class TextureState:
    sampler_state: SamplerState
