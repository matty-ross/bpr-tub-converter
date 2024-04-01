from dataclasses import dataclass
from enum import Enum


class BufferType(Enum):
    VERTEX_BUFFER = 2
    INDEX_BUFFER = 3
    CONSTANT_BUFFER = 4


@dataclass
class Buffer:
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
    transformation: tuple[float] = None
    start_index_location: int = None
    indices_count: int = None
    vertex_descriptors_count: int = None
    flags: int = None


@dataclass
class Renderable:
    bounding_sphere: tuple[float] = None
    meshes_count: int = None
    flags: int = None
    index_buffer: IndexBuffer = None
    vertex_buffer: VertexBuffer = None
    meshes: list[Mesh] = None

    def __post_init__(self):
        self.index_buffer = IndexBuffer()
        self.vertex_buffer = VertexBuffer()
