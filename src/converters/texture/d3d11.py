from dataclasses import dataclass
from enum import Enum


class TextureType(Enum):
    TEXTURE_1D = 6
    TEXTURE_2D = 7
    TEXTURE_3D = 8
    CUBE_TEXTURE = 9


class TextureFormat(Enum):
    UNKNOWN = 0
    R8G8B8A8_UNORM = 28
    BC1_UNORM = 71
    BC3_UNORM = 77


@dataclass
class Texture:
    type: TextureType = None
    format: TextureFormat = None
    width: int = None
    height: int = None
    depth: int = None
    count: int = None
    mipmap_levels_count: int = None
