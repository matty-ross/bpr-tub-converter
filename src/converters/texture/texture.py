import io
import struct

import bnd2

import d3d9
import d3d11


class Texture:

    def __init__(self, resource_entry: bnd2.ResourceEntry):
        assert resource_entry.type == 0, f"Resource entry with ID {resource_entry.id :08X} isn't Texture."
        self.resource_entry: bnd2.ResourceEntry = resource_entry

        self.d3d9_texture = d3d9.Texture()
        self.d3d11_texture = d3d11.Texture()


    def convert(self) -> None:
        pass


    def _load(self) -> None:
        data = io.BytesIO(self.resource_entry.data[0])

        data.seek(0x0)
        self.d3d9_texture.data_offset = struct.unpack('<L', data.read(4))[0]
        data.seek(0x10)
        self.d3d9_texture.format = d3d9.Format(struct.unpack('<l', data.read(4))[0])
        self.d3d9_texture.width = struct.unpack('<H', data.read(2))[0]
        self.d3d9_texture.height = struct.unpack('<H', data.read(2))[0]
        self.d3d9_texture.depth = struct.unpack('B', data.read(1))[0]
        self.d3d9_texture.mipmap_levels_count = struct.unpack('B', data.read(1))[0]
        self.d3d9_texture.type = d3d9.TextureType(struct.unpack('b', data.read(1))[0])

    
    def _store(self) -> None:
        data = io.BytesIO()
        
        data.seek(0x0)
        data.write(struct.pack('<L', 0))
        data.write(struct.pack('<l', self.d3d11_texture.usage.value))
        data.write(struct.pack('<l', self.d3d11_texture.type.value))
        data.write(struct.pack('<L', self.d3d11_texture.data_offset))
        data.write(struct.pack('<L', 0))
        data.write(struct.pack('<L', 0))
        data.write(struct.pack('<L', 0))
        data.write(struct.pack('<l', self.d3d11_texture.format.value))
        data.write(struct.pack('<L', 0))
        data.write(struct.pack('<H', self.d3d11_texture.width))
        data.write(struct.pack('<H', self.d3d11_texture.height))
        data.write(struct.pack('<H', self.d3d11_texture.depth))
        data.write(struct.pack('<H', self.d3d11_texture.count))
        data.write(struct.pack('B', self.d3d11_texture.most_detailed_mipmap_level))
        data.write(struct.pack('B', self.d3d11_texture.mipmap_levels_count))
        data.seek(0x30)
        data.write(struct.pack('<L', 0))
        data.write(struct.pack('<L', 0))
        data.write(struct.pack('<L', 0))
        data.write(struct.pack('<L', 0))

        self.resource_entry.data[0] = data.getvalue()
