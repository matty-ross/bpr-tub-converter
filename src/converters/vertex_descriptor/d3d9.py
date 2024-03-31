from dataclasses import dataclass
from enum import Enum


class ElementType(Enum):
    NONE = 0
    POSITION = 1
    NORMAL = 3
    TEXCOORD_0 = 6
    TEXCOORD_1 = 7
    BLEND_INDICES = 14
    BLEND_WEIGHT = 15
    TANGENT = 21


class DataType(Enum):
    FLOAT1 = 0
    FLOAT2 = 1
    FLOAT3 = 2
    FLOAT4 = 3
    UBYTE4 = 5
    SHORT2 = 6
    SHORT4 = 7
    UBYTE4N = 8
    SHORT2N = 9
    SHORT4N = 10
    USHORT2N = 11
    USHORT4N = 12
    UNUSED = 17


@dataclass
class Element:
    vertex_stride: int = None
    offset: int = None
    data_type: DataType = None
    type: ElementType = None


@dataclass
class VertexDescriptor:
    elements_hash: int = None
    elements_count: int = None
    elements: list[Element] = None
