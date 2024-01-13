import io
import struct

import bnd2

import d3d9
import d3d11


BLEND_MAP = {
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
    # d3d9.Blend.BOTH_SRC_ALPHA: d3d11.Blend.,
    # d3d9.Blend.BOTH_INV_SRC_ALPHA: d3d11.Blend.,
    d3d9.Blend.BLEND_FACTOR: d3d11.Blend.BLEND_FACTOR,
    d3d9.Blend.INV_BLEND_FACTOR: d3d11.Blend.INV_BLEND_FACTOR,
    # d3d9.Blend.SRC_COLOR_2: d3d11.Blend.,
    # d3d9.Blend.INV_SRC_COLOR_2: d3d11.Blend.,
}


BLEND_OPERATION_MAP = {
    d3d9.BlendOperation.ADD: d3d11.BlendOperation.ADD,
    d3d9.BlendOperation.SUBTRACT: d3d11.BlendOperation.SUBTRACT,
    d3d9.BlendOperation.REV_SUBTRACT: d3d11.BlendOperation.REV_SUBTRACT,
    d3d9.BlendOperation.MIN: d3d11.BlendOperation.MIN,
    d3d9.BlendOperation.MAX: d3d11.BlendOperation.MAX,
}


COMPARSION_FUNCTION_MAP = {
    d3d9.ComparsionFunction.NEVER: d3d11.ComparsionFunction.NEVER,
    d3d9.ComparsionFunction.LESS: d3d11.ComparsionFunction.LESS,
    d3d9.ComparsionFunction.EQUAL: d3d11.ComparsionFunction.EQUAL,
    d3d9.ComparsionFunction.LESS_EQUAL: d3d11.ComparsionFunction.LESS_EQUAL,
    d3d9.ComparsionFunction.GREATER: d3d11.ComparsionFunction.GREATER,
    d3d9.ComparsionFunction.NOT_EQUAL: d3d11.ComparsionFunction.NOT_EQUAL,
    d3d9.ComparsionFunction.GREATER_EQUAL: d3d11.ComparsionFunction.GREATER_EQUAL,
    d3d9.ComparsionFunction.ALWAYS: d3d11.ComparsionFunction.ALWAYS,
}


STENCIL_OPERATION_MAP = {
    d3d9.StencilOperation.KEEP: d3d11.StencilOperation.KEEP,
    d3d9.StencilOperation.ZERO: d3d11.StencilOperation.ZERO,
    d3d9.StencilOperation.REPLACE: d3d11.StencilOperation.REPLACE,
    d3d9.StencilOperation.INCR_SAT: d3d11.StencilOperation.INCR_SAT,
    d3d9.StencilOperation.DECR_SAT: d3d11.StencilOperation.DECR_SAT,
    d3d9.StencilOperation.INVERT: d3d11.StencilOperation.INVERT,
    d3d9.StencilOperation.INCR: d3d11.StencilOperation.INCR,
    d3d9.StencilOperation.DECR: d3d11.StencilOperation.DECR,
}


FILL_MODE_MAP = {
    d3d9.FillMode.WIREFRAME: d3d11.FillMode.WIREFRAME,
    d3d9.FillMode.SOLID: d3d11.FillMode.SOLID,
}


CULL_MODE_MAP = {
    d3d9.CullMode.NONE: d3d11.CullMode.NONE,
    d3d9.CullMode.CW: d3d11.CullMode.FRONT,
    d3d9.CullMode.CCW: d3d11.CullMode.BACK,
}


class MaterialState:

    def __init__(self, resource_entry: bnd2.ResourceEntry):
        assert resource_entry.type == 15, f"Resource entry with ID {resource_entry.id :08X} isn't MaterialState."
        self.resource_entry: bnd2.ResourceEntry = resource_entry


    def convert(self) -> None:
        pass


    def _get_d3d9(self) -> d3d9.MaterialState:
        data = io.BytesIO(self.resource_entry.data[0])
        d3d9_material_state = d3d9.MaterialState()

        data.seek(0x0)
        blend_state_offset = struct.unpack('<L', data.read(4))[0]
        depth_stencil_state_offset = struct.unpack('<L', data.read(4))[0]
        rasterizer_state_offset = struct.unpack('<L', data.read(4))[0]

        data.seek(blend_state_offset)
        dword = struct.unpack('<L', data.read(4))[0]
        d3d9_material_state.blend_state.source_blend = d3d9.Blend((dword >> 0) & (2 ** 5 - 1))
        d3d9_material_state.blend_state.blend_oepration = d3d9.BlendOperation((dword >> 5) & (2 ** 3 - 1))
        d3d9_material_state.blend_state.destination_blend = d3d9.Blend((dword >> 8) & (2 ** 8 - 1))
        d3d9_material_state.blend_state.source_blend_alpha = d3d9.Blend((dword >> 16) & (2 ** 5 - 1))
        d3d9_material_state.blend_state.blend_operation_alpha = d3d9.BlendOperation((dword >> 21) & (2 ** 3 - 1))
        d3d9_material_state.blend_state.destination_blend_alpha = d3d9.Blend((dword >> 24) & (2 ** 8 - 1))
        d3d9_material_state.blend_state.color_write_enable = struct.unpack('<LLLL', data.read(4 * 4))[0]
        d3d9_material_state.blend_state.blend_factor = struct.unpack('<ffff', data.read(4 * 4))[0]
        d3d9_material_state.blend_state.alpha_blend_enable = bool(struct.unpack('<L', data.read(4))[0])
        d3d9_material_state.blend_state.separate_alpha_blend_enable = bool(struct.unpack('<L', data.read(4))[0])
        d3d9_material_state.blend_state.alpha_test_enable = bool(struct.unpack('<L', data.read(4))[0])
        d3d9_material_state.blend_state.alpha_function = d3d9.ComparsionFunction(struct.unpack('<L', data.read(4))[0])
        d3d9_material_state.blend_state.alpha_reference = struct.unpack('<L', data.read(4))[0]
        d3d9_material_state.blend_state.alpha_to_coverage_enable = bool(struct.unpack('<L', data.read(4))[0])

        data.seek(depth_stencil_state_offset)
        d3d9_material_state.depth_stencil_state.z_function = d3d9.ComparsionFunction(struct.unpack('<l', data.read(4)))[0]
        d3d9_material_state.depth_stencil_state.stencil_fail_operation = d3d9.StencilOperation(struct.unpack('<l', data.read(4)))[0]
        d3d9_material_state.depth_stencil_state.stencil_z_fail_operation = d3d9.StencilOperation(struct.unpack('<l', data.read(4)))[0]
        d3d9_material_state.depth_stencil_state.stencil_pass_operation = d3d9.StencilOperation(struct.unpack('<l', data.read(4)))[0]
        d3d9_material_state.depth_stencil_state.stencil_function = d3d9.ComparsionFunction(struct.unpack('<l', data.read(4)))[0]
        d3d9_material_state.depth_stencil_state.ccw_stencil_fail_operation = d3d9.StencilOperation(struct.unpack('<l', data.read(4)))[0]
        d3d9_material_state.depth_stencil_state.ccw_stencil_z_fail_operation = d3d9.StencilOperation(struct.unpack('<l', data.read(4)))[0]
        d3d9_material_state.depth_stencil_state.ccw_stencil_pass_operation = d3d9.StencilOperation(struct.unpack('<l', data.read(4)))[0]
        d3d9_material_state.depth_stencil_state.ccw_stencil_function = d3d9.ComparsionFunction(struct.unpack('<l', data.read(4)))[0]
        d3d9_material_state.depth_stencil_state.stencil_reference = struct.unpack('<L', data.read(4))[0]
        d3d9_material_state.depth_stencil_state.stencil_mask = struct.unpack('<L', data.read(4))[0]
        d3d9_material_state.depth_stencil_state.stencil_write_mask = struct.unpack('<L', data.read(4))[0]
        d3d9_material_state.depth_stencil_state.z_enable = d3d9.ZBufferType(struct.unpack('<L', data.read(4))[0])
        d3d9_material_state.depth_stencil_state.z_write_enable = bool(struct.unpack('<L', data.read(4))[0])
        d3d9_material_state.depth_stencil_state.stencil_enable = bool(struct.unpack('<L', data.read(4))[0])
        d3d9_material_state.depth_stencil_state.two_sided_stencil_mode_enable = bool(struct.unpack('<L', data.read(4))[0])

        data.seek(rasterizer_state_offset)
        d3d9_material_state.rasterizer_state.fill_mode = d3d9.FillMode(struct.unpack('<l', data.read(4)))[0]
        d3d9_material_state.rasterizer_state.cull_mode = d3d9.CullMode(struct.unpack('<l', data.read(4)))[0]
        d3d9_material_state.rasterizer_state.depth_bias = struct.unpack('<f', data.read(4))[0]
        d3d9_material_state.rasterizer_state.slope_scale_depth_bias = struct.unpack('<f', data.read(4))[0]
        d3d9_material_state.rasterizer_state.multisample_mask = struct.unpack('<L', data.read(4))[0]
        d3d9_material_state.rasterizer_state.scissor_test_enable = bool(struct.unpack('<L', data.read(4))[0])
        d3d9_material_state.rasterizer_state.multisample_antialias_enable = bool(struct.unpack('<L', data.read(4))[0])
        d3d9_material_state.rasterizer_state.srgb_write_enable = bool(struct.unpack('<L', data.read(4))[0])
        d3d9_material_state.rasterizer_state.antialiased_line_enable = bool(struct.unpack('<L', data.read(4))[0])

        return d3d9_material_state
    

    def _set_d3d11(self, d3d11_material_state: d3d11.MaterialState) -> None:
        pass
