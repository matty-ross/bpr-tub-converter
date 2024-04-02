import io
import struct

import bnd2

from . import d3d9
from . import d3d11


D3D9_BLEND_TO_D3D11_BLEND = {
    d3d9.Blend.ZERO: d3d11.Blend.ZERO,
    d3d9.Blend.ONE: d3d11.Blend.ONE,
    d3d9.Blend.SRC_COLOR: d3d11.Blend.SRC_COLOR,
    d3d9.Blend.INV_SRC_COLOR: d3d11.Blend.INV_SRC_COLOR,
    d3d9.Blend.SRC_ALPHA: d3d11.Blend.SRC_ALPHA,
    d3d9.Blend.INV_SRC_ALPHA: d3d11.Blend.INV_SRC_ALPHA,
    d3d9.Blend.DEST_ALPHA: d3d11.Blend.DEST_ALPHA,
    d3d9.Blend.INV_DEST_ALPHA: d3d11.Blend.INV_DEST_ALPHA,
    d3d9.Blend.DEST_COLOR: d3d11.Blend.DEST_COLOR,
    d3d9.Blend.INV_DEST_COLOR: d3d11.Blend.INV_DEST_COLOR,
    d3d9.Blend.SRC_ALPHA_SAT: d3d11.Blend.SRC_ALPHA_SAT,
}


D3D9_CULL_MODE_TO_D3D11_CULL_MODE = {
    d3d9.CullMode.NONE: d3d11.CullMode.NONE,
    d3d9.CullMode.CW: d3d11.CullMode.BACK,
    d3d9.CullMode.CCW: d3d11.CullMode.FRONT,
}


class MaterialState:

    def __init__(self, resource_entry: bnd2.ResourceEntry):
        assert resource_entry.type == 15, f"Resource entry with ID {resource_entry.id :08X} isn't MaterialState."
        self.resource_entry = resource_entry
        self.d3d9_material_state = d3d9.MaterialState()
        self.d3d11_material_state = d3d11.MaterialState()


    def convert(self) -> None:
        self._load()

        self.d3d11_material_state.blend_state.blend_enable = self.d3d9_material_state.blend_state.alpha_blend_enable
        self.d3d11_material_state.blend_state.source_blend = D3D9_BLEND_TO_D3D11_BLEND[self.d3d9_material_state.blend_state.source_blend]
        self.d3d11_material_state.blend_state.destination_blend = D3D9_BLEND_TO_D3D11_BLEND[self.d3d9_material_state.blend_state.destination_blend]
        self.d3d11_material_state.blend_state.color_write_mask = self.d3d9_material_state.blend_state.color_write_enable
        self.d3d11_material_state.blend_state.alpha_to_coverage_enable = self.d3d9_material_state.blend_state.alpha_to_coverage_enable

        self.d3d11_material_state.depth_stencil_state.depth_write_enable = self.d3d9_material_state.depth_stencil_state.z_write_enable

        self.d3d11_material_state.rasterizer_state.cull_mode = D3D9_CULL_MODE_TO_D3D11_CULL_MODE[self.d3d9_material_state.rasterizer_state.cull_mode]

        self._store()


    def _load(self) -> None:
        data = io.BytesIO(self.resource_entry.data[0])

        data.seek(0x0)
        blend_state_offset = struct.unpack('<L', data.read(4))[0]
        depth_stencil_state_offset = struct.unpack('<L', data.read(4))[0]
        rasterizer_state_offset = struct.unpack('<L', data.read(4))[0]

        data.seek(blend_state_offset)
        dword = struct.unpack('<L', data.read(4))[0]
        self.d3d9_material_state.blend_state.source_blend = d3d9.Blend((dword >> 0) & (2 ** 5 - 1))
        self.d3d9_material_state.blend_state.destination_blend = d3d9.Blend((dword >> 8) & (2 ** 8 - 1))
        self.d3d9_material_state.blend_state.color_write_enable = struct.unpack('<L', data.read(4))[0]
        _ = data.read(3 * 4)
        _ = data.read(4 * 4)
        self.d3d9_material_state.blend_state.alpha_blend_enable = bool(struct.unpack('<L', data.read(4))[0])
        _ = data.read(4)
        _ = data.read(4)
        _ = data.read(4)
        _ = data.read(4)
        _ = data.read(4)
        self.d3d9_material_state.blend_state.alpha_to_coverage_enable = bool(struct.unpack('<L', data.read(4))[0])

        data.seek(depth_stencil_state_offset)
        _ = data.read(4)
        _ = data.read(4)
        _ = data.read(4)
        _ = data.read(4)
        _ = data.read(4)
        _ = data.read(4)
        _ = data.read(4)
        _ = data.read(4)
        _ = data.read(4)
        _ = data.read(4)
        _ = data.read(4)
        _ = data.read(4)
        _ = data.read(4)
        self.d3d9_material_state.depth_stencil_state.z_write_enable = bool(struct.unpack('<L', data.read(4))[0])
        _ = data.read(4)
        _ = data.read(4)

        data.seek(rasterizer_state_offset)
        _ = data.read(4)
        self.d3d9_material_state.rasterizer_state.cull_mode = d3d9.CullMode(struct.unpack('<l', data.read(4))[0])
        _ = data.read(4)
        _ = data.read(4)
        _ = data.read(4)
        _ = data.read(4)
        _ = data.read(4)
        _ = data.read(4)
        _ = data.read(4)


    def _store(self) -> None:
        data = io.BytesIO()

        data.seek(0x0)
        data.write(struct.pack('<L', 0))
        data.write(struct.pack('<L', 0))
        data.write(struct.pack('<L', 0))

        blend_state_offset = data.tell()
        dword = 0x00000000
        dword |= (int(self.d3d11_material_state.blend_state.blend_enable) & (2 ** 1 - 1)) << 0
        dword |= (self.d3d11_material_state.blend_state.source_blend.value & (2 ** 5 - 1)) << 1
        dword |= (self.d3d11_material_state.blend_state.destination_blend.value & (2 ** 5 - 1)) << 6
        dword |= 1 << 11
        dword |= 5 << 14
        dword |= 6 << 19
        dword |= 1 << 24
        dword |= (self.d3d11_material_state.blend_state.color_write_mask & (2 ** 4 - 1)) << 27
        data.write(struct.pack('<L', dword))
        for _ in range(7):
            data.write(struct.pack('<L', 0x7931498A))
        data.write(struct.pack('<4f', 1.0, 1.0, 1.0, 1.0))
        data.write(struct.pack('?', self.d3d11_material_state.blend_state.alpha_to_coverage_enable))
        data.write(struct.pack('?', False))
        data.write(bytes(2)) # padding
        data.write(struct.pack('<L', 1))
        data.write(struct.pack('<L', 0))

        depth_stencil_state_offset = data.tell()
        data.write(struct.pack('<l', 4))
        data.write(struct.pack('<l', 1))
        data.write(struct.pack('<l', 1))
        data.write(struct.pack('<l', 1))
        data.write(struct.pack('<l', 8))
        data.write(struct.pack('<l', 1))
        data.write(struct.pack('<l', 1))
        data.write(struct.pack('<l', 1))
        data.write(struct.pack('<l', 8))
        data.write(struct.pack('<L', 0))
        data.write(struct.pack('<L', 0xFFFFFFFF))
        data.write(struct.pack('<L', 0xFFFFFFFF))
        data.write(struct.pack('?', True))
        data.write(struct.pack('?', self.d3d11_material_state.depth_stencil_state.depth_write_enable))
        data.write(struct.pack('?', False))
        data.write(bytes(1)) # padding
        data.write(struct.pack('<L', 1))
        data.write(struct.pack('<L', 0))
        data.write(struct.pack('<L', 0))

        rasterizer_state_offset = data.tell()
        data.write(struct.pack('<l', 3))
        data.write(struct.pack('<l', self.d3d11_material_state.rasterizer_state.cull_mode.value))
        data.write(struct.pack('<l', 1))
        data.write(struct.pack('<l', 0))
        data.write(struct.pack('<f', 0.0))
        data.write(struct.pack('<f', 0.0))
        data.write(struct.pack('?', True)) # uninitialized
        data.write(struct.pack('?', True))
        data.write(struct.pack('?', True))
        data.write(struct.pack('?', False))
        data.write(struct.pack('<L', 1))
        data.write(struct.pack('<L', 0))

        data.seek(0x0)
        data.write(struct.pack('<L', blend_state_offset))
        data.write(struct.pack('<L', depth_stencil_state_offset))
        data.write(struct.pack('<L', rasterizer_state_offset))

        self.resource_entry.data[0] = data.getvalue()
