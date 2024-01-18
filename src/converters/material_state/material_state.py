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
    d3d9.Blend.BLEND_FACTOR: d3d11.Blend.BLEND_FACTOR,
    d3d9.Blend.INV_BLEND_FACTOR: d3d11.Blend.INV_BLEND_FACTOR,
    d3d9.Blend.SRC_COLOR_2: d3d11.Blend.SRC1_COLOR,
    d3d9.Blend.INV_SRC_COLOR_2: d3d11.Blend.INV_SRC1_COLOR,
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

        self.d3d9_material_state = d3d9.MaterialState()
        self.d3d11_material_state = d3d11.MaterialState()


    def convert(self) -> None:
        self._load()

        self.d3d11_material_state.blend_state.render_target_blend_states = []
        for _ in range(8):
            render_target_blend_state = d3d11.RenderTargetBlendState()
            render_target_blend_state.blend_enable = self.d3d9_material_state.blend_state.alpha_blend_enable
            render_target_blend_state.source_blend = BLEND_MAP[self.d3d9_material_state.blend_state.source_blend]
            render_target_blend_state.destination_blend = BLEND_MAP[self.d3d9_material_state.blend_state.destination_blend]
            render_target_blend_state.blend_oepration = BLEND_OPERATION_MAP[self.d3d9_material_state.blend_state.blend_oepration]
            render_target_blend_state.source_blend_alpha = BLEND_MAP[self.d3d9_material_state.blend_state.source_blend_alpha]
            render_target_blend_state.destination_blend_alpha = BLEND_MAP[self.d3d9_material_state.blend_state.destination_blend_alpha]
            render_target_blend_state.blend_operation_alpha = BLEND_OPERATION_MAP[self.d3d9_material_state.blend_state.blend_operation_alpha]
            render_target_blend_state.color_write_mask = self.d3d9_material_state.blend_state.color_write_enable[0]
            self.d3d11_material_state.blend_state.render_target_blend_states.append(render_target_blend_state)
        self.d3d11_material_state.blend_state.blend_factor = self.d3d9_material_state.blend_state.blend_factor
        self.d3d11_material_state.blend_state.alpha_to_coverage_enable = self.d3d9_material_state.blend_state.alpha_to_coverage_enable
        self.d3d11_material_state.blend_state.independent_blend_enable = self.d3d9_material_state.blend_state.separate_alpha_blend_enable

        self.d3d11_material_state.depth_stencil_state.depth_function = COMPARSION_FUNCTION_MAP[self.d3d9_material_state.depth_stencil_state.z_function]
        self.d3d11_material_state.depth_stencil_state.front_face_stencil_fail_operation = STENCIL_OPERATION_MAP[self.d3d9_material_state.depth_stencil_state.stencil_fail_operation]
        self.d3d11_material_state.depth_stencil_state.front_face_stencil_depth_fail_operation = STENCIL_OPERATION_MAP[self.d3d9_material_state.depth_stencil_state.stencil_z_fail_operation]
        self.d3d11_material_state.depth_stencil_state.front_face_stencil_pass_operation = STENCIL_OPERATION_MAP[self.d3d9_material_state.depth_stencil_state.stencil_pass_operation]
        self.d3d11_material_state.depth_stencil_state.front_face_stencil_function = COMPARSION_FUNCTION_MAP[self.d3d9_material_state.depth_stencil_state.stencil_function]
        self.d3d11_material_state.depth_stencil_state.back_face_stencil_fail_operation = STENCIL_OPERATION_MAP[self.d3d9_material_state.depth_stencil_state.ccw_stencil_fail_operation]
        self.d3d11_material_state.depth_stencil_state.back_face_stencil_depth_fail_operation = STENCIL_OPERATION_MAP[self.d3d9_material_state.depth_stencil_state.ccw_stencil_z_fail_operation]
        self.d3d11_material_state.depth_stencil_state.back_face_stencil_pass_operation = STENCIL_OPERATION_MAP[self.d3d9_material_state.depth_stencil_state.ccw_stencil_pass_operation]
        self.d3d11_material_state.depth_stencil_state.back_face_stencil_function = COMPARSION_FUNCTION_MAP[self.d3d9_material_state.depth_stencil_state.ccw_stencil_function]
        self.d3d11_material_state.depth_stencil_state.stencil_reference = self.d3d9_material_state.depth_stencil_state.stencil_reference
        self.d3d11_material_state.depth_stencil_state.stencil_read_mask = self.d3d9_material_state.depth_stencil_state.stencil_mask
        self.d3d11_material_state.depth_stencil_state.stencil_write_mask = self.d3d9_material_state.depth_stencil_state.stencil_write_mask
        self.d3d11_material_state.depth_stencil_state.depth_enable = bool(self.d3d9_material_state.depth_stencil_state.z_enable.value)
        self.d3d11_material_state.depth_stencil_state.depth_write_enable = self.d3d9_material_state.depth_stencil_state.z_write_enable
        self.d3d11_material_state.depth_stencil_state.stencil_enable = self.d3d9_material_state.depth_stencil_state.stencil_enable

        self.d3d11_material_state.rasterizer_state.fill_mode = FILL_MODE_MAP[self.d3d9_material_state.rasterizer_state.fill_mode]
        self.d3d11_material_state.rasterizer_state.cull_mode = CULL_MODE_MAP[self.d3d9_material_state.rasterizer_state.cull_mode]
        self.d3d11_material_state.rasterizer_state.front_face = 1
        self.d3d11_material_state.rasterizer_state.depth_bias = int(self.d3d9_material_state.rasterizer_state.depth_bias)
        self.d3d11_material_state.rasterizer_state.depth_bias_clamp = 0.0
        self.d3d11_material_state.rasterizer_state.slope_scaled_depth_bias = self.d3d9_material_state.rasterizer_state.slope_scale_depth_bias
        self.d3d11_material_state.rasterizer_state.depth_clip_enable = False
        self.d3d11_material_state.rasterizer_state.scissor_enable = self.d3d9_material_state.rasterizer_state.scissor_test_enable
        self.d3d11_material_state.rasterizer_state.multisample_enable = self.d3d9_material_state.rasterizer_state.multisample_antialias_enable
        self.d3d11_material_state.rasterizer_state.antialiased_line_enable = self.d3d9_material_state.rasterizer_state.antialiased_line_enable

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
        self.d3d9_material_state.blend_state.blend_oepration = d3d9.BlendOperation((dword >> 5) & (2 ** 3 - 1))
        self.d3d9_material_state.blend_state.destination_blend = d3d9.Blend((dword >> 8) & (2 ** 8 - 1))
        self.d3d9_material_state.blend_state.source_blend_alpha = d3d9.Blend((dword >> 16) & (2 ** 5 - 1))
        self.d3d9_material_state.blend_state.blend_operation_alpha = d3d9.BlendOperation((dword >> 21) & (2 ** 3 - 1))
        self.d3d9_material_state.blend_state.destination_blend_alpha = d3d9.Blend((dword >> 24) & (2 ** 8 - 1))
        self.d3d9_material_state.blend_state.color_write_enable = struct.unpack('<LLLL', data.read(4 * 4))
        self.d3d9_material_state.blend_state.blend_factor = struct.unpack('<ffff', data.read(4 * 4))
        self.d3d9_material_state.blend_state.alpha_blend_enable = bool(struct.unpack('<L', data.read(4))[0])
        self.d3d9_material_state.blend_state.separate_alpha_blend_enable = bool(struct.unpack('<L', data.read(4))[0])
        self.d3d9_material_state.blend_state.alpha_test_enable = bool(struct.unpack('<L', data.read(4))[0])
        self.d3d9_material_state.blend_state.alpha_function = d3d9.ComparsionFunction(struct.unpack('<L', data.read(4))[0])
        self.d3d9_material_state.blend_state.alpha_reference = struct.unpack('<L', data.read(4))[0]
        self.d3d9_material_state.blend_state.alpha_to_coverage_enable = bool(struct.unpack('<L', data.read(4))[0])

        data.seek(depth_stencil_state_offset)
        self.d3d9_material_state.depth_stencil_state.z_function = d3d9.ComparsionFunction(struct.unpack('<l', data.read(4)))[0]
        self.d3d9_material_state.depth_stencil_state.stencil_fail_operation = d3d9.StencilOperation(struct.unpack('<l', data.read(4)))[0]
        self.d3d9_material_state.depth_stencil_state.stencil_z_fail_operation = d3d9.StencilOperation(struct.unpack('<l', data.read(4)))[0]
        self.d3d9_material_state.depth_stencil_state.stencil_pass_operation = d3d9.StencilOperation(struct.unpack('<l', data.read(4)))[0]
        self.d3d9_material_state.depth_stencil_state.stencil_function = d3d9.ComparsionFunction(struct.unpack('<l', data.read(4)))[0]
        self.d3d9_material_state.depth_stencil_state.ccw_stencil_fail_operation = d3d9.StencilOperation(struct.unpack('<l', data.read(4)))[0]
        self.d3d9_material_state.depth_stencil_state.ccw_stencil_z_fail_operation = d3d9.StencilOperation(struct.unpack('<l', data.read(4)))[0]
        self.d3d9_material_state.depth_stencil_state.ccw_stencil_pass_operation = d3d9.StencilOperation(struct.unpack('<l', data.read(4)))[0]
        self.d3d9_material_state.depth_stencil_state.ccw_stencil_function = d3d9.ComparsionFunction(struct.unpack('<l', data.read(4)))[0]
        self.d3d9_material_state.depth_stencil_state.stencil_reference = struct.unpack('<L', data.read(4))[0]
        self.d3d9_material_state.depth_stencil_state.stencil_mask = struct.unpack('<L', data.read(4))[0]
        self.d3d9_material_state.depth_stencil_state.stencil_write_mask = struct.unpack('<L', data.read(4))[0]
        self.d3d9_material_state.depth_stencil_state.z_enable = d3d9.ZBufferType(struct.unpack('<L', data.read(4))[0])
        self.d3d9_material_state.depth_stencil_state.z_write_enable = bool(struct.unpack('<L', data.read(4))[0])
        self.d3d9_material_state.depth_stencil_state.stencil_enable = bool(struct.unpack('<L', data.read(4))[0])
        self.d3d9_material_state.depth_stencil_state.two_sided_stencil_mode_enable = bool(struct.unpack('<L', data.read(4))[0])

        data.seek(rasterizer_state_offset)
        self.d3d9_material_state.rasterizer_state.fill_mode = d3d9.FillMode(struct.unpack('<l', data.read(4)))[0]
        self.d3d9_material_state.rasterizer_state.cull_mode = d3d9.CullMode(struct.unpack('<l', data.read(4)))[0]
        self.d3d9_material_state.rasterizer_state.depth_bias = struct.unpack('<f', data.read(4))[0]
        self.d3d9_material_state.rasterizer_state.slope_scale_depth_bias = struct.unpack('<f', data.read(4))[0]
        self.d3d9_material_state.rasterizer_state.multisample_mask = struct.unpack('<L', data.read(4))[0]
        self.d3d9_material_state.rasterizer_state.scissor_test_enable = bool(struct.unpack('<L', data.read(4))[0])
        self.d3d9_material_state.rasterizer_state.multisample_antialias_enable = bool(struct.unpack('<L', data.read(4))[0])
        self.d3d9_material_state.rasterizer_state.srgb_write_enable = bool(struct.unpack('<L', data.read(4))[0])
        self.d3d9_material_state.rasterizer_state.antialiased_line_enable = bool(struct.unpack('<L', data.read(4))[0])
    

    def _store(self) -> None:
        data = io.BytesIO()

        data.seek(0x0)
        data.write(struct.pack('<L', 0))
        data.write(struct.pack('<L', 0))
        data.write(struct.pack('<L', 0))

        blend_state_offset = data.tell()
        for render_target_blend_state in self.d3d11_material_state.blend_state.render_target_blend_states:
            dword = 0x00000000
            dword |= (int(render_target_blend_state.blend_enable) << 0) & (2 ** 1 - 1)
            dword |= (render_target_blend_state.source_blend.value << 1) & (2 ** 5 - 1)
            dword |= (render_target_blend_state.destination_blend.value << 6) & (2 ** 5 - 1)
            dword |= (render_target_blend_state.blend_oepration.value << 11) & (2 ** 3 - 1)
            dword |= (render_target_blend_state.source_blend_alpha.value << 14) & (2 ** 5 - 1)
            dword |= (render_target_blend_state.destination_blend_alpha.value << 19) & (2 ** 5 - 1)
            dword |= (render_target_blend_state.blend_operation_alpha.value << 24) & (2 ** 3 - 1)
            dword |= (render_target_blend_state.color_write_mask << 27) & (2 ** 4 - 1)
            data.write(struct.pack('<L', dword))
        data.write(struct.pack('<ffff', *self.d3d11_material_state.blend_state.blend_factor))
        data.write(struct.pack('?', self.d3d11_material_state.blend_state.alpha_to_coverage_enable))
        data.write(struct.pack('?', self.d3d11_material_state.blend_state.independent_blend_enable))
        data.seek(blend_state_offset + 0x34)
        data.write(struct.pack('<L', 1))
        data.write(struct.pack('<L', 0))
        
        depth_stencil_state_offset = data.tell()
        data.write(struct.pack('<l', self.d3d11_material_state.depth_stencil_state.depth_function.value))
        data.write(struct.pack('<l', self.d3d11_material_state.depth_stencil_state.front_face_stencil_fail_operation.value))
        data.write(struct.pack('<l', self.d3d11_material_state.depth_stencil_state.front_face_stencil_depth_fail_operation.value))
        data.write(struct.pack('<l', self.d3d11_material_state.depth_stencil_state.front_face_stencil_pass_operation.value))
        data.write(struct.pack('<l', self.d3d11_material_state.depth_stencil_state.front_face_stencil_function.value))
        data.write(struct.pack('<l', self.d3d11_material_state.depth_stencil_state.back_face_stencil_fail_operation.value))
        data.write(struct.pack('<l', self.d3d11_material_state.depth_stencil_state.back_face_stencil_depth_fail_operation.value))
        data.write(struct.pack('<l', self.d3d11_material_state.depth_stencil_state.back_face_stencil_pass_operation.value))
        data.write(struct.pack('<l', self.d3d11_material_state.depth_stencil_state.back_face_stencil_function.value))
        data.write(struct.pack('<L', self.d3d11_material_state.depth_stencil_state.stencil_reference))
        data.write(struct.pack('<L', self.d3d11_material_state.depth_stencil_state.stencil_read_mask))
        data.write(struct.pack('<L', self.d3d11_material_state.depth_stencil_state.stencil_write_mask))
        data.write(struct.pack('?', self.d3d11_material_state.depth_stencil_state.depth_enable))
        data.write(struct.pack('?', self.d3d11_material_state.depth_stencil_state.depth_write_enable))
        data.write(struct.pack('?', self.d3d11_material_state.depth_stencil_state.stencil_enable))
        data.seek(depth_stencil_state_offset + 0x34)
        data.write(struct.pack('<L', 1))
        data.write(struct.pack('<L', 0))

        rasterizer_state_offset = data.tell()
        data.write(struct.pack('<l', self.d3d11_material_state.rasterizer_state.fill_mode.value))
        data.write(struct.pack('<l', self.d3d11_material_state.rasterizer_state.cull_mode.value))
        data.write(struct.pack('<l', self.d3d11_material_state.rasterizer_state.front_face))
        data.write(struct.pack('<l', self.d3d11_material_state.rasterizer_state.depth_bias))
        data.write(struct.pack('<f', self.d3d11_material_state.rasterizer_state.depth_bias_clamp))
        data.write(struct.pack('<f', self.d3d11_material_state.rasterizer_state.slope_scaled_depth_bias))
        data.write(struct.pack('?', self.d3d11_material_state.rasterizer_state.depth_clip_enable))
        data.write(struct.pack('?', self.d3d11_material_state.rasterizer_state.scissor_enable))
        data.write(struct.pack('?', self.d3d11_material_state.rasterizer_state.multisample_enable))
        data.write(struct.pack('?', self.d3d11_material_state.rasterizer_state.antialiased_line_enable))
        data.seek(rasterizer_state_offset + 0x1C)
        data.write(struct.pack('<L', 1))
        data.write(struct.pack('<L', 0))

        data.seek(0x0)
        data.write(struct.pack('<L', blend_state_offset))
        data.write(struct.pack('<L', depth_stencil_state_offset))
        data.write(struct.pack('<L', rasterizer_state_offset))

        self.resource_entry.data[0] = data.getvalue()
