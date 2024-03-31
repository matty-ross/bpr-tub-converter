from dataclasses import dataclass
from enum import Enum


class TextureType(Enum):
    TEXTURE = 0
    CUBE_TEXTURE = 1
    VOLUME_TEXTURE = 2


class TextureFormat(Enum):
    UNKNOWN = 0
    A8R8G8B8 = 21
    DXT1 = int.from_bytes(b'DXT1', 'little')
    DXT5 = int.from_bytes(b'DXT5', 'little')


@dataclass
class Texture:
    format: TextureFormat = None
    width: int = None
    height: int = None
    depth: int = None
    mipmap_levels_count: int = None
    type: TextureType = None
