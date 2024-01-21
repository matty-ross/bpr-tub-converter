from dataclasses import dataclass
from enum import Enum


class DataType(Enum):
    FLOAT1 = 0
    FLOAT2 = 1
    FLOAT3 = 2
    FLOAT4 = 3
    D3DCOLOR = 4
    UBYTE4 = 5
    SHORT2 = 6
    SHORT4 = 7
    UBYTE4N = 8
    SHORT2N = 9
    SHORT4N = 10
    USHORT2N = 11
    USHORT4N = 12
    UDEC3 = 13
    DEC3N = 14
    FLOAT16_2 = 15
    FLOAT16_4 = 16
    UNUSED = 17


class Method(Enum):
    DEFAULT = 0,
    PARTIALU = 1,
    PARTIALV = 2,
    CROSSUV = 3,
    UV = 4,
    LOOKUP = 5,
    LOOKUPPRESAMPLED = 6,


class Usage(Enum):
    POSITION = 0,
    BLENDWEIGHT = 1,
    BLENDINDICES = 2,
    NORMAL = 3,
    PSIZE = 4,
    TEXCOORD = 5,
    TANGENT = 6,
    BINORMAL = 7,
    TESSFACTOR = 8,
    POSITIONT = 9,
    COLOR = 10,
    FOG = 11,
    DEPTH = 12,
    SAMPLE = 13,


@dataclass
class Element:
    stream_number: int = None
    vertex_stride: int = None
    offset: int = None
    data_type: DataType = None
    method: Method = None
    usage: Usage = None
    usage_index: int = None
    map_index: int = None


@dataclass
class VertexDescriptor:
    elements_hash: int = None
    elements_count: int = None
    streams_count: int = None
    elements: list[Element] = None
