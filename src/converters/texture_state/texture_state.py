import io
import struct

import bnd2

from . import d3d9
from . import d3d11


D3D9_TEXTURE_ADDRESS_MODE_TO_D3D11_TEXTURE_ADDRESS_MODE = {
    d3d9.TextureAddressMode.WRAP: d3d11.TextureAddressMode.WRAP,
    d3d9.TextureAddressMode.MIRROR: d3d11.TextureAddressMode.MIRROR,
    d3d9.TextureAddressMode.CLAMP: d3d11.TextureAddressMode.CLAMP,
    d3d9.TextureAddressMode.BORDER: d3d11.TextureAddressMode.BORDER,
    d3d9.TextureAddressMode.MIRROR_ONCE: d3d11.TextureAddressMode.MIRROR_ONCE,
}


D3D9_TEXTURE_FILTER_TYPE_TO_D3D11_TEXTURE_FILTER_TYPE = {
    # d3d9.TextureFilterType.NONE:
    d3d9.TextureFilterType.POINT: d3d11.TextureFilterType.POINT,
    d3d9.TextureFilterType.LINEAR: d3d11.TextureFilterType.LINEAR,
    # d3d9.TextureFilterType.ANISOTROPIC:
    # d3d9.TextureFilterType.PYRAMIDAL_QUAD:
    # d3d9.TextureFilterType.GAUSSIAN_QUAD:
    # d3d9.TextureFilterType.CONVOLUTION_MONO:
}


class TextureState:

    def __init__(self, resource_entry: bnd2.ResourceEntry):
        assert resource_entry.type == 14, f"Resource entry with ID {resource_entry.id :08X} isn't TextureState."
        self.resource_entry = resource_entry
        self.d3d9_texture_state = d3d9.TextureState()
        self.d3d11_texture_state = d3d11.TextureState()
    
    
    def convert(self) -> None:
        self._load()

        self.d3d11_texture_state.sampler_state.address_mode_u = D3D9_TEXTURE_ADDRESS_MODE_TO_D3D11_TEXTURE_ADDRESS_MODE[self.d3d9_texture_state.sampler_state.address_mode_u]
        self.d3d11_texture_state.sampler_state.address_mode_v = D3D9_TEXTURE_ADDRESS_MODE_TO_D3D11_TEXTURE_ADDRESS_MODE[self.d3d9_texture_state.sampler_state.address_mode_v]
        self.d3d11_texture_state.sampler_state.address_mode_w = D3D9_TEXTURE_ADDRESS_MODE_TO_D3D11_TEXTURE_ADDRESS_MODE[self.d3d9_texture_state.sampler_state.address_mode_w]
        self.d3d11_texture_state.sampler_state.magnification_filter = D3D9_TEXTURE_FILTER_TYPE_TO_D3D11_TEXTURE_FILTER_TYPE[self.d3d9_texture_state.sampler_state.magnification_filter]
        self.d3d11_texture_state.sampler_state.minification_filter = D3D9_TEXTURE_FILTER_TYPE_TO_D3D11_TEXTURE_FILTER_TYPE[self.d3d9_texture_state.sampler_state.minification_filter]
        self.d3d11_texture_state.sampler_state.mipmap_filter = D3D9_TEXTURE_FILTER_TYPE_TO_D3D11_TEXTURE_FILTER_TYPE[self.d3d9_texture_state.sampler_state.mipmap_filter]
        self.d3d11_texture_state.sampler_state.min_lod = struct.unpack('<f', b'\xFF\xFF\x7F\xFF')[0] # -FLT_MAX
        self.d3d11_texture_state.sampler_state.max_lod = struct.unpack('<f', b'\xFF\xFF\x7F\x7F')[0] # FLT_MAX
        self.d3d11_texture_state.sampler_state.max_anisotropy = self.d3d9_texture_state.sampler_state.max_anisotropy
        self.d3d11_texture_state.sampler_state.mipmap_lod_bias = self.d3d9_texture_state.sampler_state.mipmap_lod_bias
        self.d3d11_texture_state.sampler_state.comparsion_function = d3d11.CompasrionFunction.ALWAYS
        self.d3d11_texture_state.sampler_state.use_border_color = self.d3d9_texture_state.sampler_state.border_color != 0x00000000

        self._store()

    
    def _load(self) -> None:
        data = io.BytesIO(self.resource_entry.data[0])
        
        data.seek(0x0)
        self.d3d9_texture_state.sampler_state.address_mode_u = d3d9.TextureAddressMode(struct.unpack('<l', data.read(4))[0])
        self.d3d9_texture_state.sampler_state.address_mode_v = d3d9.TextureAddressMode(struct.unpack('<l', data.read(4))[0])
        self.d3d9_texture_state.sampler_state.address_mode_w = d3d9.TextureAddressMode(struct.unpack('<l', data.read(4))[0])
        self.d3d9_texture_state.sampler_state.magnification_filter = d3d9.TextureFilterType(struct.unpack('<l', data.read(4))[0])
        self.d3d9_texture_state.sampler_state.minification_filter = d3d9.TextureFilterType(struct.unpack('<l', data.read(4))[0])
        self.d3d9_texture_state.sampler_state.mipmap_filter = d3d9.TextureFilterType(struct.unpack('<l', data.read(4))[0])
        self.d3d9_texture_state.sampler_state.max_mipmap_level = struct.unpack('<L', data.read(4))[0]
        self.d3d9_texture_state.sampler_state.max_anisotropy = struct.unpack('<L', data.read(4))[0]
        self.d3d9_texture_state.sampler_state.mipmap_lod_bias = struct.unpack('<f', data.read(4))[0]
        self.d3d9_texture_state.sampler_state.border_color = struct.unpack('<L', data.read(4))[0]
    

    def _store(self) -> None:
        data = io.BytesIO()
        
        data.seek(0x0)
        data.write(struct.pack('<l', self.d3d11_texture_state.sampler_state.address_mode_u.value))
        data.write(struct.pack('<l', self.d3d11_texture_state.sampler_state.address_mode_v.value))
        data.write(struct.pack('<l', self.d3d11_texture_state.sampler_state.address_mode_w.value))
        data.write(struct.pack('<l', self.d3d11_texture_state.sampler_state.magnification_filter.value))
        data.write(struct.pack('<l', self.d3d11_texture_state.sampler_state.minification_filter.value))
        data.write(struct.pack('<l', self.d3d11_texture_state.sampler_state.mipmap_filter.value))
        data.write(struct.pack('<f', self.d3d11_texture_state.sampler_state.min_lod))
        data.write(struct.pack('<f', self.d3d11_texture_state.sampler_state.max_lod))
        data.write(struct.pack('<L', self.d3d11_texture_state.sampler_state.max_anisotropy))
        data.write(struct.pack('<f', self.d3d11_texture_state.sampler_state.mipmap_lod_bias))
        data.write(struct.pack('<l', self.d3d11_texture_state.sampler_state.comparsion_function.value))
        data.write(struct.pack('?', self.d3d11_texture_state.sampler_state.use_border_color))
        data.write(bytes(3)) # padding
        data.write(struct.pack('<L', 1))
        data.write(struct.pack('<L', 0))
        self.resource_entry.import_entries[0].offset = data.tell()
        data.write(struct.pack('<L', 0))

        self.resource_entry.data[0] = data.getvalue()
