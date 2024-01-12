import io
import struct

import bnd2

import d3d9
import d3d11


TEXTURE_ADDRESS_MODE_MAP = {
    d3d9.TextureAddressMode.WRAP: d3d11.TextureAddressMode.WRAP,
    d3d9.TextureAddressMode.MIRROR: d3d11.TextureAddressMode.MIRROR,
    d3d9.TextureAddressMode.CLAMP: d3d11.TextureAddressMode.CLAMP,
    d3d9.TextureAddressMode.BORDER: d3d11.TextureAddressMode.BORDER,
    d3d9.TextureAddressMode.MIRROR_ONCE: d3d11.TextureAddressMode.MIRROR_ONCE,
}


TEXTURE_FILTER_TYPE_MAP = {
    d3d9.TextureFilterType.POINT: d3d11.TextureFilterType.POINT,
    d3d9.TextureFilterType.LINEAR: d3d11.TextureFilterType.LINEAR,
}


class TextureState:

    def __init__(self, resource_entry: bnd2.ResourceEntry):
        self.resource_entry: bnd2.ResourceEntry = resource_entry
    
    
    def convert(self) -> d3d11.TextureState:
        d3d9_texture_state = self._get_d3d9()
        d3d11_texture_state = d3d11.TextureState()

        d3d11_texture_state.sampler_state.address_mode_u = TEXTURE_ADDRESS_MODE_MAP.get(d3d9_texture_state.sampler_state.address_mode_u, d3d11.TextureAddressMode.WRAP)
        d3d11_texture_state.sampler_state.address_mode_v = TEXTURE_ADDRESS_MODE_MAP.get(d3d9_texture_state.sampler_state.address_mode_v, d3d11.TextureAddressMode.WRAP)
        d3d11_texture_state.sampler_state.address_mode_w = TEXTURE_ADDRESS_MODE_MAP.get(d3d9_texture_state.sampler_state.address_mode_w, d3d11.TextureAddressMode.WRAP)
        d3d11_texture_state.sampler_state.magnification_filter = TEXTURE_FILTER_TYPE_MAP.get(d3d9_texture_state.sampler_state.magnification_filter, d3d11.TextureFilterType.POINT)
        d3d11_texture_state.sampler_state.minification_filter = TEXTURE_FILTER_TYPE_MAP.get(d3d9_texture_state.sampler_state.minification_filter, d3d11.TextureFilterType.POINT)
        d3d11_texture_state.sampler_state.mipmap_filter = TEXTURE_FILTER_TYPE_MAP.get(d3d9_texture_state.sampler_state.mipmap_filter, d3d11.TextureFilterType.POINT)
        d3d11_texture_state.sampler_state.min_lod = struct.unpack('<f', b'\xFF\xFF\x7F\xFF')[0] # -FLT_MAX
        d3d11_texture_state.sampler_state.max_lod = struct.unpack('<f', b'\xFF\xFF\x7F\x7F')[0] # FLT_MAX
        d3d11_texture_state.sampler_state.max_anisotropy = d3d9_texture_state.sampler_state.max_anisotropy
        d3d11_texture_state.sampler_state.mipmap_lod_bias = d3d9_texture_state.sampler_state.mipmap_lod_bias
        d3d11_texture_state.sampler_state.use_border_color = d3d9_texture_state.sampler_state.border_color != 0x00000000

        self._set_d3d11(d3d11_texture_state)

    
    def _get_d3d9(self) -> d3d9.TextureState:
        data = io.BytesIO(self.resource_entry.data[0])
        d3d9_texture_state = d3d9.TextureState()
        
        data.seek(0x0)
        d3d9_texture_state.sampler_state.address_mode_u = d3d9.TextureAddressMode(struct.unpack('<l', data.read(4))[0])
        d3d9_texture_state.sampler_state.address_mode_v = d3d9.TextureAddressMode(struct.unpack('<l', data.read(4))[0])
        d3d9_texture_state.sampler_state.address_mode_w = d3d9.TextureAddressMode(struct.unpack('<l', data.read(4))[0])
        d3d9_texture_state.sampler_state.magnification_filter = d3d9.TextureFilterType(struct.unpack('<l', data.read(4))[0])
        d3d9_texture_state.sampler_state.minification_filter = d3d9.TextureFilterType(struct.unpack('<l', data.read(4))[0])
        d3d9_texture_state.sampler_state.mipmap_filter = d3d9.TextureFilterType(struct.unpack('<l', data.read(4))[0])
        d3d9_texture_state.sampler_state.max_mipmap_level = struct.unpack('<L', data.read(4))[0]
        d3d9_texture_state.sampler_state.max_anisotropy = struct.unpack('<L', data.read(4))[0]
        d3d9_texture_state.sampler_state.mipmap_lod_bias = struct.unpack('<f', data.read(4))[0]
        d3d9_texture_state.sampler_state.border_color = struct.unpack('<L', data.read(4))[0]

        return d3d9_texture_state
    

    def _set_d3d11(self, d3d11_texture_state: d3d11.TextureState) -> None:
        data = io.BytesIO()
        
        data.seek(0x0)
        data.write(struct.pack('<l', d3d11_texture_state.sampler_state.address_mode_u.value))
        data.write(struct.pack('<l', d3d11_texture_state.sampler_state.address_mode_v.value))
        data.write(struct.pack('<l', d3d11_texture_state.sampler_state.address_mode_w.value))
        data.write(struct.pack('<l', d3d11_texture_state.sampler_state.magnification_filter.value))
        data.write(struct.pack('<l', d3d11_texture_state.sampler_state.minification_filter.value))
        data.write(struct.pack('<l', d3d11_texture_state.sampler_state.mipmap_filter.value))
        data.write(struct.pack('<f', d3d11_texture_state.sampler_state.min_lod))
        data.write(struct.pack('<f', d3d11_texture_state.sampler_state.max_lod))
        data.write(struct.pack('<L', d3d11_texture_state.sampler_state.max_anisotropy))
        data.write(struct.pack('<f', d3d11_texture_state.sampler_state.mipmap_lod_bias))
        data.write(struct.pack('<l', d3d11_texture_state.sampler_state.comparsion_function))
        data.write(struct.pack('?', d3d11_texture_state.sampler_state.use_border_color))
        
        data.seek(0x30)
        data.write(struct.pack('<L', 1))
        data.write(struct.pack('<L', 0))

        self.resource_entry.data[0] = data.getvalue()
