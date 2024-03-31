from dataclasses import dataclass
from enum import Enum


class SemanticName(Enum):
    NONE = 0
    POSITION = 1
    NORMAL = 3
    TEXCOORD_0 = 5
    TEXCOORD_1 = 6
    BLEND_INDICES = 13
    BLEND_WEIGHT = 14
    TANGENT = 15


class Format(Enum):
    UNKNOWN = 0
    R32G32B32A32_FLOAT = 2
    R32G32B32_FLOAT = 6
    R16G16B16A16_UNORM = 11
    R16G16B16A16_SNORM = 13
    R16G16B16A16_SINT = 14
    R32G32_FLOAT = 16
    R8G8B8A8_UNORM = 28
    R8G8B8A8_UINT = 30
    R16G16_UNORM = 35
    R16G16_SNORM = 37
    R16G16_SINT = 38
    R32_FLOAT = 41


@dataclass
class Element:
    semantic_name: SemanticName = None
    format: Format = None
    offset: int = None
    vertex_stride: int = None


@dataclass
class VertexDescriptor:
    elements_hash: int = None
    elements_count: int = None
    elements: list[Element] = None
