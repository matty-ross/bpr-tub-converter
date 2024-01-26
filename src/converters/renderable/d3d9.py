from dataclasses import dataclass
from enum import Enum


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
    UYVY = b'UYVY'
    R8G8_B8G8 = b'RGBG'
    YUY2 = b'YUY2'
    G8R8_G8B8 = b'GRGB'
    DXT1 = b'DXT1'
    DXT2 = b'DXT2'
    DXT3 = b'DXT3'
    DXT4 = b'DXT4'
    DXT5 = b'DXT5'
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
    MULTI2_ARGB8 = b'MET1'
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


class PrimitiveType(Enum):
    POINTLIST = 1
    LINELIST = 2
    LINESTRIP = 3
    TRIANGLELIST = 4
    TRIANGLESTRIP = 5
    TRIANGLEFAN = 6


@dataclass
class IndexBuffer:
    indices_count: int = None
    data_offset: int = None
    format: Format = None


@dataclass
class VertexBuffer:
    data_offset: int = None
    data_size: int = None


@dataclass
class Mesh:
    affine_transformation_matrix: list[float] = None
    primitive_type: PrimitiveType = None
    base_vertex_index: int = None
    start_inedx: int = None
    vertices_count: int = None
    minimum_vertex_index: int = None
    primitives_count: int = None
    vertex_descriptors_count: int = None
    instance_count: int = None
    vertex_buffers_count: int = None
    flags: int = None


@dataclass
class Renderable:
    bounding_sphere: list[float] = None
    version_number: int = None
    meshes_count: int = None
    flags: int = None
    index_buffer: IndexBuffer
    vertex_buffer: VertexBuffer
    meshes: list[Mesh] = None
