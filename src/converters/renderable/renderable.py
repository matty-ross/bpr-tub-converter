import io
import struct

import bnd2

import d3d9
import d3d11


class Renderable:

    def __init__(self, resource_entry: bnd2.ResourceEntry):
        assert resource_entry.type == 12, f"Resource entry with ID {resource_entry.id :08X} isn't Renderable."
        self.resource_entry: bnd2.ResourceEntry = resource_entry

        self.d3d9_renderable = d3d9.Renderable()
        self.d3d11_renderable = d3d11.Renderable()


    def convert(self) -> None:
        pass


    def _load(self) -> None:
        pass


    def _store(self) -> None:
        pass
