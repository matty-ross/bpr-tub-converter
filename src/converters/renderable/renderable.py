import io
import struct

from bnd2 import bundle_v2

import d3d9
import d3d11


D3D3_FORMAT_TO_D3D11_INDEX_SIZE = {
    # d3d9.Format.UNKNOWN:
    # d3d9.Format.R8G8B8:
    # d3d9.Format.A8R8G8B8:
    # d3d9.Format.X8R8G8B8:
    # d3d9.Format.R5G6B5:
    # d3d9.Format.X1R5G5B5:
    # d3d9.Format.A1R5G5B5:
    # d3d9.Format.A4R4G4B4:
    # d3d9.Format.R3G3B2:
    # d3d9.Format.A8:
    # d3d9.Format.A8R3G3B2:
    # d3d9.Format.X4R4G4B4:
    # d3d9.Format.A2B10G10R10:
    # d3d9.Format.A8B8G8R8:
    # d3d9.Format.X8B8G8R8:
    # d3d9.Format.G16R16:
    # d3d9.Format.A2R10G10B10:
    # d3d9.Format.A16B16G16R16:
    # d3d9.Format.A8P8:
    # d3d9.Format.P8:
    # d3d9.Format.L8:
    # d3d9.Format.A8L8:
    # d3d9.Format.A4L4:
    # d3d9.Format.V8U8:
    # d3d9.Format.L6V5U5:
    # d3d9.Format.X8L8V8U8:
    # d3d9.Format.Q8W8V8U8:
    # d3d9.Format.V16U16:
    # d3d9.Format.A2W10V10U10:
    # d3d9.Format.UYVY:
    # d3d9.Format.R8G8_B8G8:
    # d3d9.Format.YUY2:
    # d3d9.Format.G8R8_G8B8:
    # d3d9.Format.DXT1:
    # d3d9.Format.DXT2:
    # d3d9.Format.DXT3:
    # d3d9.Format.DXT4:
    # d3d9.Format.DXT5:
    # d3d9.Format.D16_LOCKABLE:
    # d3d9.Format.D32:
    # d3d9.Format.D15S1:
    # d3d9.Format.D24S8:
    # d3d9.Format.D24X8:
    # d3d9.Format.D24X4S4:
    # d3d9.Format.D16:
    # d3d9.Format.D32F_LOCKABLE:
    # d3d9.Format.D24FS8:
    # d3d9.Format.D32_LOCKABLE:
    # d3d9.Format.S8_LOCKABLE:
    # d3d9.Format.L16:
    # d3d9.Format.VERTEXDATA:
    d3d9.Format.INDEX16: 2,
    d3d9.Format.INDEX32: 4,
    # d3d9.Format.Q16W16V16U16:
    # d3d9.Format.MULTI2_ARGB8:
    # d3d9.Format.R16F:
    # d3d9.Format.G16R16F:
    # d3d9.Format.A16B16G16R16F:
    # d3d9.Format.R32F:
    # d3d9.Format.G32R32F:
    # d3d9.Format.A32B32G32R32F:
    # d3d9.Format.CxV8U8:
    # d3d9.Format.A1:
    # d3d9.Format.A2B10G10R10_XR_BIAS:
    # d3d9.Format.BINARYBUFFER:
}


D3D9_PRIMITIVE_TYPE_TO_D3D11_PRIMITIVE_TOPOLOGY = {
    d3d9.PrimitiveType.POINTLIST: d3d11.PrimitiveTopology.POINTLIST,
    d3d9.PrimitiveType.LINELIST: d3d11.PrimitiveTopology.LINELIST,
    d3d9.PrimitiveType.LINESTRIP: d3d11.PrimitiveTopology.LINESTRIP,
    d3d9.PrimitiveType.TRIANGLELIST: d3d11.PrimitiveTopology.TRIANGLELIST,
    d3d9.PrimitiveType.TRIANGLESTRIP: d3d11.PrimitiveTopology.TRIANGLESTRIP,
    # d3d9.PrimitiveType.TRIANGLEFAN:
}


D3D9_PRIMITIVE_TYPE_TO_D3D11_INDICES_COUNT = {
    d3d9.PrimitiveType.POINTLIST: 1,
    d3d9.PrimitiveType.LINELIST: 2,
    d3d9.PrimitiveType.LINESTRIP: 2,
    d3d9.PrimitiveType.TRIANGLELIST: 3,
    d3d9.PrimitiveType.TRIANGLESTRIP: 3,
    # d3d9.PrimitiveType.TRIANGLEFAN:
}


class Renderable:

    def __init__(self, resource_entry: bundle_v2.ResourceEntry):
        assert resource_entry.type == 12, f"Resource entry with ID {resource_entry.id :08X} isn't Renderable."
        self.resource_entry: bundle_v2.ResourceEntry = resource_entry

        self.d3d9_renderable = d3d9.Renderable()
        self.d3d11_renderable = d3d11.Renderable()


    def convert(self) -> None:
        self._load()

        self.d3d11_renderable.bounding_sphere = self.d3d9_renderable.bounding_sphere
        self.d3d11_renderable.version_number = self.d3d9_renderable.version_number
        self.d3d11_renderable.meshes_count = self.d3d9_renderable.meshes_count
        self.d3d11_renderable.flags = self.d3d9_renderable.flags
        
        self.d3d11_renderable.index_buffer.usage = d3d11.Usage.DEFAULT
        self.d3d11_renderable.index_buffer.type = d3d11.BufferType.INDEX_BUFFER
        self.d3d11_renderable.index_buffer.data_offset = self.d3d9_renderable.index_buffer.data_offset
        self.d3d11_renderable.index_buffer.data_size = D3D3_FORMAT_TO_D3D11_INDEX_SIZE[self.d3d9_renderable.index_buffer.format] * self.d3d9_renderable.index_buffer.indices_count
        self.d3d11_renderable.index_buffer.index_size = D3D3_FORMAT_TO_D3D11_INDEX_SIZE[self.d3d9_renderable.index_buffer.format]

        self.d3d11_renderable.vertex_buffer.usage = d3d11.Usage.DEFAULT
        self.d3d11_renderable.vertex_buffer.type = d3d11.BufferType.VERTEX_BUFFER
        self.d3d11_renderable.vertex_buffer.data_offset = self.d3d9_renderable.vertex_buffer.data_offset
        self.d3d11_renderable.vertex_buffer.data_size = self.d3d9_renderable.vertex_buffer.data_size

        self.d3d11_renderable.meshes = [d3d11.Mesh() for _ in range(self.d3d9_renderable.meshes_count)]
        for i in range(self.d3d9_renderable.meshes_count):
            self.d3d11_renderable.meshes[i].affine_transformation_matrix = self.d3d9_renderable.meshes[i].affine_transformation_matrix
            self.d3d11_renderable.meshes[i].primitive_topology = D3D9_PRIMITIVE_TYPE_TO_D3D11_PRIMITIVE_TOPOLOGY[self.d3d9_renderable.meshes[i].primitive_type]
            self.d3d11_renderable.meshes[i].base_vertex_location = self.d3d9_renderable.meshes[i].base_vertex_index
            self.d3d11_renderable.meshes[i].start_index_location = self.d3d9_renderable.meshes[i].start_index
            self.d3d11_renderable.meshes[i].indices_count = D3D9_PRIMITIVE_TYPE_TO_D3D11_INDICES_COUNT[self.d3d9_renderable.meshes[i].primitive_type] * self.d3d9_renderable.meshes[i].primitives_count
            self.d3d11_renderable.meshes[i].vertex_descriptors_count = self.d3d9_renderable.meshes[i].vertex_descriptors_count
            self.d3d11_renderable.meshes[i].instance_count = self.d3d9_renderable.meshes[i].instance_count
            self.d3d11_renderable.meshes[i].vertex_buffers_count = self.d3d9_renderable.meshes[i].vertex_buffers_count
            self.d3d11_renderable.meshes[i].flags = self.d3d9_renderable.meshes[i].flags

        self._store()


    def _load(self) -> None:
        data = io.BytesIO(self.resource_entry.data[0])
        
        data.seek(0x0)
        self.d3d9_renderable.bounding_sphere = struct.unpack('<ffff', data.read(4 * 4))
        self.d3d9_renderable.version_number = struct.unpack('<H', data.read(2))[0]
        self.d3d9_renderable.meshes_count = struct.unpack('<H', data.read(2))[0]
        meshes_offset = struct.unpack('<L', data.read(4))[0]
        data.seek(0x1C)
        self.d3d9_renderable.flags = struct.unpack('<H', data.read(2))[0]
        data.seek(0x20)
        index_buffer_offset = struct.unpack('<L', data.read(4))[0]
        vertex_buffer_offset = struct.unpack('<L', data.read(4))[0]

        data.seek(index_buffer_offset)
        self.d3d9_renderable.index_buffer.indices_count = struct.unpack('<L', data.read(4))[0]
        self.d3d9_renderable.index_buffer.data_offset = struct.unpack('<L', data.read(4))[0]
        data.seek(index_buffer_offset + 0xC)
        self.d3d9_renderable.index_buffer.format = d3d9.Format(struct.unpack('<l', data.read(4))[0])

        data.seek(vertex_buffer_offset)
        self.d3d9_renderable.vertex_buffer.data_offset = struct.unpack('<L', data.read(4))[0]
        data.seek(vertex_buffer_offset + 0x8)
        self.d3d9_renderable.vertex_buffer.data_size = struct.unpack('<L', data.read(4))[0]
        self.d3d9_renderable.vertex_buffer.flags = struct.unpack('<L', data.read(4))[0]

        self.d3d9_renderable.meshes = [d3d9.Mesh() for _ in range(self.d3d9_renderable.meshes_count)]
        for i, mesh in enumerate(self.d3d9_renderable.meshes):
            data.seek(meshes_offset + i * 0x4)
            mesh_offset = struct.unpack('<L', data.read(4))[0]
            data.seek(mesh_offset)
            mesh.affine_transformation_matrix = [struct.unpack('<f', data.read(4))[0] for _ in range(16)]
            mesh.primitive_type = d3d9.PrimitiveType(struct.unpack('<l', data.read(4))[0])
            mesh.base_vertex_index = struct.unpack('<l', data.read(4))[0]
            mesh.start_index = struct.unpack('<L', data.read(4))[0]
            mesh.vertices_count = struct.unpack('<L', data.read(4))[0]
            mesh.minimum_vertex_index = struct.unpack('<L', data.read(4))[0]
            mesh.primitives_count = struct.unpack('<L', data.read(4))[0]
            data.seek(mesh_offset + 0x5C)
            mesh.vertex_descriptors_count = struct.unpack('B', data.read(1))[0]
            mesh.instance_count = struct.unpack('B', data.read(1))[0]
            mesh.vertex_buffers_count = struct.unpack('B', data.read(1))[0]
            mesh.flags = struct.unpack('B', data.read(1))[0]


    def _store(self) -> None:
        data = io.BytesIO()

        data.seek(0x0)
        data.write(struct.pack('<ffff', self.d3d11_renderable.bounding_sphere))
        data.write(struct.pack('<H', self.d3d11_renderable.version_number))
        data.write(struct.pack('<H', self.d3d11_renderable.meshes_count))
        data.write(struct.pack('<L', 0))
        data.write(struct.pack('<L', 0))
        data.write(struct.pack('<H', self.d3d11_renderable.flags))
        data.seek(0x20)
        data.write(struct.pack('<L', 0))
        data.write(struct.pack('<L', 0))

        meshes_offset = bundle_v2.BundleV2._align_offset(data.tell(), 0x10)
        meshes_offstes = []
        data.seek(meshes_offset)
        for _ in range(self.d3d11_renderable.meshes_count):
            data.write(struct.pack('<L', 0))

        index_buffer_offset = data.tell()
        data.write(struct.pack('<L', 0))
        data.write(struct.pack('<l', self.d3d11_renderable.index_buffer.usage.value))
        data.write(struct.pack('<l', self.d3d11_renderable.index_buffer.type.value))
        data.write(struct.pack('<L', self.d3d11_renderable.index_buffer.data_offset))
        data.write(struct.pack('<L', self.d3d11_renderable.index_buffer.data_size))
        data.write(struct.pack('<L', self.d3d11_renderable.index_buffer.index_size))

        vertex_buffer_offset = data.tell()
        data.write(struct.pack('<L', 0))
        data.write(struct.pack('<l', self.d3d11_renderable.vertex_buffer.usage.value))
        data.write(struct.pack('<l', self.d3d11_renderable.vertex_buffer.type.value))
        data.write(struct.pack('<L', self.d3d11_renderable.vertex_buffer.data_offset))
        data.write(struct.pack('<L', self.d3d11_renderable.vertex_buffer.data_size))
        data.write(struct.pack('<L', 0))
        data.write(struct.pack('<L', 0))

        import_index = 0
        for i, mesh in enumerate(self.d3d11_renderable.meshes):
            mesh_offset = bundle_v2.BundleV2._align_offset(data.tell(), 0x10)
            meshes_offstes.append(mesh_offset)
            data.seek(mesh_offset)
            for _ in range(16):
                data.write('<f', mesh.affine_transformation_matrix[i])
            data.write(struct.pack('<l', mesh.primitive_topology.value))
            data.write(struct.pack('<l', mesh.base_vertex_location))
            data.write(struct.pack('<L', mesh.start_index_location))
            data.write(struct.pack('<L', mesh.indices_count))
            self.resource_entry.import_entries[import_index].offset = data.tell()
            import_index += 1
            data.write(struct.pack('<L', 0))
            data.write(struct.pack('B', mesh.vertex_descriptors_count))
            data.write(struct.pack('B', mesh.instance_count))
            data.write(struct.pack('B', mesh.vertex_buffers_count))
            data.write(struct.pack('B', mesh.flags))
            data.write(struct.pack('<L', index_buffer_offset))
            for _ in range(mesh.vertex_buffers_count):
                data.write(struct.pack('<L', vertex_buffer_offset))
            for _ in range(mesh.vertex_descriptors_count):
                self.resource_entry.import_entries[import_index].offset = data.tell()
                import_index += 1
                data.write(struct.pack('<L', 0))
                
        data.seek(0x14)
        data.write(struct.pack('<L', meshes_offset))
        data.seek(0x20)
        data.write(struct.pack('<L', index_buffer_offset))
        data.write(struct.pack('<L', vertex_buffer_offset))

        data.seek(meshes_offset)
        for mesh_offset in meshes_offstes:
            data.write(struct.pack('<L', mesh_offset))

        self.resource_entry.data[0] = data.getvalue()
