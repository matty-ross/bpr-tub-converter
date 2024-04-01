from dataclasses import dataclass
from enum import Enum


class IndexFormat(Enum):
    INDEX_16 = 101
    INDEX_32 = 102


@dataclass
class IndexBuffer:
    indices_count: int = None
    data_offset: int = None
    format: IndexFormat = None


@dataclass
class VertexBuffer:
    data_offset: int = None
    data_size: int = None


@dataclass
class Mesh:
    transformation: tuple[float] = None
    start_index: int = None
    vertices_count: int = None
    minimum_vertex_index: int = None
    primitives_count: int = None
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
