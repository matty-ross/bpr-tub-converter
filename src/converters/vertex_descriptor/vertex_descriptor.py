import io
import struct

import bnd2

import d3d9
import d3d11


class VertexDescriptor:

    def __init__(self, resource_entry: bnd2.ResourceEntry):
        assert resource_entry.type == 10, f"Resource entry with ID {resource_entry.id :08X} isn't VertexDescriptor."
        self.resource_entry: bnd2.ResourceEntry = resource_entry

        self.d3d9_vertex_descriptor = d3d9.VertexDescriptor()
        self.d3d11_vertex_descriptor = d3d11.VertexDescriptor()


    def convert(self) -> None:
        pass


    def _load(self) -> None:
        pass


    def _store(self) -> None:
        pass
