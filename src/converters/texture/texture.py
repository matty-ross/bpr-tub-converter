import io
import struct

import bnd2

import d3d9
import d3d11


TEXTURE_TYPE_MAP = {
    d3d9.TextureType.TEXTURE: d3d11.TextureType.TEXTURE_2D,
    d3d9.TextureType.CUBE_TEXTURE: d3d11.TextureType.TEXTURE_1D,
    d3d9.TextureType.VOLUME_TEXTURE: d3d11.TextureType.TEXTURE_3D,
}


# https://learn.microsoft.com/en-us/windows/win32/direct3d10/d3d10-graphics-programming-guide-resources-legacy-formats
FORMAT_MAP = {
    d3d9.Format.UNKNOWN: d3d11.Format.UNKNOWN,
    # d3d9.Format.R8G8B8: d3d11.Format.,
    d3d9.Format.A8R8G8B8: d3d11.Format.B8G8R8A8_UNORM,
    d3d9.Format.X8R8G8B8: d3d11.Format.B8G8R8X8_UNORM,
    d3d9.Format.R5G6B5: d3d11.Format.B5G6R5_UNORM,
    # d3d9.Format.X1R5G5B5: d3d11.Format.,
    d3d9.Format.A1R5G5B5: d3d11.Format.B5G5R5A1_UNORM,
    d3d9.Format.A4R4G4B4: d3d11.Format.B4G4R4A4_UNORM,
    # d3d9.Format.R3G3B2: d3d11.Format.,
    d3d9.Format.A8: d3d11.Format.A8_UNORM,
    # d3d9.Format.A8R3G3B2: d3d11.Format.,
    # d3d9.Format.X4R4G4B4: d3d11.Format.,
    # d3d9.Format.A2B10G10R10: d3d11.Format.,
    d3d9.Format.A8B8G8R8: d3d11.Format.R8G8B8A8_UNORM,
    # d3d9.Format.X8B8G8R8: d3d11.Format.,
    d3d9.Format.G16R16: d3d11.Format.R16G16_UNORM,
    # d3d9.Format.A2R10G10B10: d3d11.Format.,
    d3d9.Format.A16B16G16R16: d3d11.Format.R16G16B16A16_UNORM,
    # d3d9.Format.A8P8: d3d11.Format.,
    # d3d9.Format.P8: d3d11.Format.,
    d3d9.Format.L8: d3d11.Format.R8_UNORM,
    # d3d9.Format.A8L8: d3d11.Format.,
    # d3d9.Format.A4L4: d3d11.Format.,
    d3d9.Format.V8U8: d3d11.Format.R8G8_SNORM,
    # d3d9.Format.L6V5U5: d3d11.Format.,
    # d3d9.Format.X8L8V8U8: d3d11.Format.,
    d3d9.Format.Q8W8V8U8: d3d11.Format.R8G8B8A8_SNORM,
    d3d9.Format.V16U16: d3d11.Format.R16G16_SNORM,
    # d3d9.Format.A2W10V10U10: d3d11.Format.,
    # d3d9.Format.UYVY: d3d11.Format.,
    d3d9.Format.R8G8_B8G8: d3d11.Format.G8R8_G8B8_UNORM,
    # d3d9.Format.YUY2: d3d11.Format.,
    d3d9.Format.G8R8_G8B8: d3d11.Format.R8G8_B8G8_UNORM,
    d3d9.Format.DXT1: d3d11.Format.BC1_UNORM,
    d3d9.Format.DXT2: d3d11.Format.BC2_UNORM,
    d3d9.Format.DXT3: d3d11.Format.BC2_UNORM,
    d3d9.Format.DXT4: d3d11.Format.BC3_UNORM,
    d3d9.Format.DXT5: d3d11.Format.BC3_UNORM,
    d3d9.Format.D16_LOCKABLE: d3d11.Format.D16_UNORM,
    # d3d9.Format.D32: d3d11.Format.,
    # d3d9.Format.D15S1: d3d11.Format.,
    # d3d9.Format.D24S8: d3d11.Format.,
    # d3d9.Format.D24X8: d3d11.Format.,
    # d3d9.Format.D24X4S4: d3d11.Format.,
    d3d9.Format.D16: d3d11.Format.D16_UNORM,
    d3d9.Format.D32F_LOCKABLE: d3d11.Format.D32_FLOAT,
    # d3d9.Format.D24FS8: d3d11.Format.,
    # d3d9.Format.D32_LOCKABLE: d3d11.Format.,
    # d3d9.Format.S8_LOCKABLE: d3d11.Format.,
    d3d9.Format.L16: d3d11.Format.R16_UNORM,
    # d3d9.Format.VERTEXDATA: d3d11.Format.,
    d3d9.Format.INDEX16: d3d11.Format.R16_UINT,
    d3d9.Format.INDEX32: d3d11.Format.R32_UINT,
    d3d9.Format.Q16W16V16U16: d3d11.Format.R16G16B16A16_SNORM,
    # d3d9.Format.MULTI2_ARGB8: d3d11.Format.,
    d3d9.Format.R16F: d3d11.Format.R16_FLOAT,
    d3d9.Format.G16R16F: d3d11.Format.R16G16_FLOAT,
    d3d9.Format.A16B16G16R16F: d3d11.Format.R16G16B16A16_FLOAT,
    d3d9.Format.R32F: d3d11.Format.R32_FLOAT,
    d3d9.Format.G32R32F: d3d11.Format.R32G32_FLOAT,
    d3d9.Format.A32B32G32R32F: d3d11.Format.R32G32B32A32_FLOAT,
    # d3d9.Format.CxV8U8: d3d11.Format.,
    # d3d9.Format.A1: d3d11.Format.,
    # d3d9.Format.A2B10G10R10_XR_BIAS: d3d11.Format.,
    # d3d9.Format.BINARYBUFFER: d3d11.Format.,
}


class Texture:

    def __init__(self, resource_entry: bnd2.ResourceEntry):
        assert resource_entry.type == 0, f"Resource entry with ID {resource_entry.id :08X} isn't Texture."
        self.resource_entry: bnd2.ResourceEntry = resource_entry

        self.d3d9_texture = d3d9.Texture()
        self.d3d11_texture = d3d11.Texture()


    def convert(self) -> None:
        self._load()
        
        self.d3d11_texture.usage = d3d11.Usage.DEFAULT
        self.d3d11_texture.type = TEXTURE_TYPE_MAP.get(self.d3d9_texture.type)
        self.d3d11_texture.data_offset = self.d3d9_texture.data_offset
        self.d3d11_texture.format = FORMAT_MAP.get(self.d3d9_texture.format)
        self.d3d11_texture.width = self.d3d9_texture.width
        self.d3d11_texture.height = self.d3d9_texture.height
        self.d3d11_texture.depth = self.d3d9_texture.depth
        self.d3d11_texture.count = 1
        self.d3d11_texture.most_detailed_mipmap_level = 0
        self.d3d11_texture.mipmap_levels_count = self.d3d9_texture.mipmap_levels_count

        self._store()


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
