from dataclasses import dataclass
from enum import Enum


class TextureType(Enum):
    TEXTURE = 0
    CUBE_TEXTURE = 1
    VOLUME_TEXTURE = 2


class Format(Enum):
    UNKNOWN = 0
    R8G8B8 = 20
    A8R8G8B8 = 21
    X8R8G8B8 = 22
    R5G6B5 = 23
    X1R5G5B5 = 24
    A1R5G5B5 = 25
    A4R4G4B4 = 26
    R3G3B2 = 27
    A8 = 28
    A8R3G3B2 = 29
    X4R4G4B4 = 30
    A2B10G10R10 = 31
    A8B8G8R8 = 32
    X8B8G8R8 = 33
    G16R16 = 34
    A2R10G10B10 = 35
    A16B16G16R16 = 36
    A8P8 = 40
    P8 = 41
    L8 = 50
    A8L8 = 51
    A4L4 = 52
    V8U8 = 60
    L6V5U5 = 61
    X8L8V8U8 = 62
    Q8W8V8U8 = 63
    V16U16 = 64
    A2W10V10U10 = 67
    UYVY = int.from_bytes(b'UYVY', 'little')
    R8G8_B8G8 = int.from_bytes(b'RGBG', 'little')
    YUY2 = int.from_bytes(b'YUY2', 'little')
    G8R8_G8B8 = int.from_bytes(b'GRGB', 'little')
    DXT1 = int.from_bytes(b'DXT1', 'little')
    DXT2 = int.from_bytes(b'DXT2', 'little')
    DXT3 = int.from_bytes(b'DXT3', 'little')
    DXT4 = int.from_bytes(b'DXT4', 'little')
    DXT5 = int.from_bytes(b'DXT5', 'little')
    D16_LOCKABLE = 70
    D32 = 71
    D15S1 = 73
    D24S8 = 75
    D24X8 = 77
    D24X4S4 = 79
    D16 = 80
    D32F_LOCKABLE = 82
    D24FS8 = 83
    D32_LOCKABLE = 84
    S8_LOCKABLE = 85
    L16 = 81
    VERTEXDATA = 100
    INDEX16 = 101
    INDEX32 = 102
    Q16W16V16U16 = 110
    MULTI2_ARGB8 = int.from_bytes(b'MET1', 'little')
    R16F = 111
    G16R16F = 112
    A16B16G16R16F = 113
    R32F = 114
    G32R32F = 115
    A32B32G32R32F = 116
    CxV8U8 = 117
    A1 = 118
    A2B10G10R10_XR_BIAS = 119
    BINARYBUFFER = 199


@dataclass
class Texture:
    data_offset: int = None
    format: Format = None
    width: int = None
    height: int = None
    depth: int = None
    mipmap_levels_count: int = None
    type: TextureType = None
    flags: int = None
