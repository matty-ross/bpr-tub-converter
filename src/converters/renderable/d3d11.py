from dataclasses import dataclass
from enum import Enum


class BufferType(Enum):
    VERTEX_BUFFER = 2
    INDEX_BUFFER = 3
    CONSTANT_BUFFER = 4


class Usage(Enum):
    DEFAULT = 0
    IMMUTABLE = 1
    DYNAMIC = 2
    STAGING = 3


class PrimitiveTopology(Enum):
    UNDEFINED = 0
    POINTLIST = 1
    LINELIST = 2
    LINESTRIP = 3
    TRIANGLELIST = 4
    TRIANGLESTRIP = 5
    LINELIST_ADJ = 10
    LINESTRIP_ADJ = 11
    TRIANGLELIST_ADJ = 12
    TRIANGLESTRIP_ADJ = 13
    CONTROL_POINT_PATCHLIST_1 = 33
    CONTROL_POINT_PATCHLIST_2 = 34
    CONTROL_POINT_PATCHLIST_3 = 35
    CONTROL_POINT_PATCHLIST_4 = 36
    CONTROL_POINT_PATCHLIST_5 = 37
    CONTROL_POINT_PATCHLIST_6 = 38
    CONTROL_POINT_PATCHLIST_7 = 39
    CONTROL_POINT_PATCHLIST_8 = 40
    CONTROL_POINT_PATCHLIST_9 = 41
    CONTROL_POINT_PATCHLIST10 = 42
    CONTROL_POINT_PATCHLIST11 = 43
    CONTROL_POINT_PATCHLIST12 = 44
    CONTROL_POINT_PATCHLIST13 = 45
    CONTROL_POINT_PATCHLIST14 = 46
    CONTROL_POINT_PATCHLIST15 = 47
    CONTROL_POINT_PATCHLIST16 = 48
    CONTROL_POINT_PATCHLIST17 = 49
    CONTROL_POINT_PATCHLIST18 = 50
    CONTROL_POINT_PATCHLIST19 = 51
    CONTROL_POINT_PATCHLIST20 = 52
    CONTROL_POINT_PATCHLIST21 = 53
    CONTROL_POINT_PATCHLIST22 = 54
    CONTROL_POINT_PATCHLIST23 = 55
    CONTROL_POINT_PATCHLIST24 = 56
    CONTROL_POINT_PATCHLIST25 = 57
    CONTROL_POINT_PATCHLIST26 = 58
    CONTROL_POINT_PATCHLIST27 = 59
    CONTROL_POINT_PATCHLIST28 = 60
    CONTROL_POINT_PATCHLIST29 = 61
    CONTROL_POINT_PATCHLIST30 = 62
    CONTROL_POINT_PATCHLIST31 = 63
    CONTROL_POINT_PATCHLIST32 = 64


@dataclass
class Buffer:
    usage: Usage = None
    type: BufferType = None
    data_offset: int = None
    data_size: int = None


@dataclass
class IndexBuffer(Buffer):
    index_size: int = None


@dataclass
class VertexBuffer(Buffer):
    pass


@dataclass
class Mesh:
    affine_transformation_matrix: list[float] = None
    primitive_topology: PrimitiveTopology = None
    base_vertex_location: int = None
    start_index_location: int = None
    indices_count: int = None
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
    index_buffer: IndexBuffer = None
    vertex_buffer: VertexBuffer = None
    meshes: list[Mesh] = None

    def __post_init__(self):
        self.index_buffer = IndexBuffer()
        self.vertex_buffer = VertexBuffer()
