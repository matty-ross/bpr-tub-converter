import io
import struct

import bnd2

from . import d3d9
from . import d3d11


D3D9_TEXTURE_TYPE_TO_D3D11_TEXTURE_TYPE = {
    d3d9.TextureType.TEXTURE: d3d11.TextureType.TEXTURE_2D,
    d3d9.TextureType.CUBE_TEXTURE: d3d11.TextureType.CUBE_TEXTURE,
    d3d9.TextureType.VOLUME_TEXTURE: d3d11.TextureType.TEXTURE_3D,
}


D3D9_TEXTURE_FORMAT_TO_D3D11_TEXTURE_FORMAT = {
    d3d9.TextureFormat.UNKNOWN: d3d11.TextureFormat.UNKNOWN,
    d3d9.TextureFormat.A8R8G8B8: d3d11.TextureFormat.R8G8B8A8_UNORM,
    d3d9.TextureFormat.DXT1: d3d11.TextureFormat.BC1_UNORM,
    d3d9.TextureFormat.DXT5: d3d11.TextureFormat.BC3_UNORM,
}


class Texture:

    def __init__(self, resource_entry: bnd2.ResourceEntry):
        assert resource_entry.type == 0, f"Resource entry with ID {resource_entry.id :08X} isn't Texture."
        self.resource_entry = resource_entry
        self.d3d9_texture = d3d9.Texture()
        self.d3d11_texture = d3d11.Texture()


    def convert(self) -> None:
        self._load()

        self.d3d11_texture.type = D3D9_TEXTURE_TYPE_TO_D3D11_TEXTURE_TYPE[self.d3d9_texture.type]
        self.d3d11_texture.format = D3D9_TEXTURE_FORMAT_TO_D3D11_TEXTURE_FORMAT[self.d3d9_texture.format]
        self.d3d11_texture.width = self.d3d9_texture.width
        self.d3d11_texture.height = self.d3d9_texture.height
        self.d3d11_texture.depth = 0 if self.d3d11_texture.type == d3d11.TextureType.CUBE_TEXTURE else 1
        self.d3d11_texture.count = 6 if self.d3d11_texture.type == d3d11.TextureType.CUBE_TEXTURE else 1
        self.d3d11_texture.mipmap_levels_count = self.d3d9_texture.mipmap_levels_count

        self._store()


    def _load(self) -> None:
        data = io.BytesIO(self.resource_entry.data[0])

        data.seek(0x0)
        _ = data.read(4)
        _ = data.read(4)
        _ = data.read(4)
        _ = data.read(2)
        _ = data.read(1)
        _ = data.read(1)
        self.d3d9_texture.format = d3d9.TextureFormat(struct.unpack('<l', data.read(4))[0])
        self.d3d9_texture.width = struct.unpack('<H', data.read(2))[0]
        self.d3d9_texture.height = struct.unpack('<H', data.read(2))[0]
        self.d3d9_texture.depth = struct.unpack('B', data.read(1))[0]
        self.d3d9_texture.mipmap_levels_count = struct.unpack('B', data.read(1))[0]
        self.d3d9_texture.type = d3d9.TextureType(struct.unpack('b', data.read(1))[0])
        _ = data.read(1)


    def _store(self) -> None:
        data = io.BytesIO()

        data.seek(0x0)
        data.write(struct.pack('<L', 0))
        data.write(struct.pack('<l', 0))
        data.write(struct.pack('<l', self.d3d11_texture.type.value))
        data.write(struct.pack('<L', 0))
        data.write(struct.pack('<L', 0))
        data.write(struct.pack('<L', 0))
        data.write(struct.pack('<L', 0))
        data.write(struct.pack('<l', self.d3d11_texture.format.value))
        data.write(struct.pack('<L', 0))
        data.write(struct.pack('<H', self.d3d11_texture.width))
        data.write(struct.pack('<H', self.d3d11_texture.height))
        data.write(struct.pack('<H', self.d3d11_texture.depth))
        data.write(struct.pack('<H', self.d3d11_texture.count))
        data.write(struct.pack('B', 0))
        data.write(struct.pack('B', self.d3d11_texture.mipmap_levels_count))
        data.write(bytes(2)) # padding
        data.write(struct.pack('<L', 0))
        data.write(struct.pack('<L', 0))
        data.write(struct.pack('<L', 0))
        data.write(struct.pack('<L', 0))

        self.resource_entry.data[0] = data.getvalue()
