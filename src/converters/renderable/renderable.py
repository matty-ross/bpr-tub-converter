import io
import struct

import bnd2

from . import d3d9
from . import d3d11


D3D3_FORMAT_TO_D3D11_INDEX_SIZE = {
    # Only these 2 formats are allowed.
    d3d9.Format.INDEX16: 2,
    d3d9.Format.INDEX32: 4,
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

    def __init__(self, resource_entry: bnd2.ResourceEntry):
        assert resource_entry.type == 12, f"Resource entry with ID {resource_entry.id :08X} isn't Renderable."
        self.resource_entry = resource_entry
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
        _ = data.read(4)
        self.d3d9_renderable.flags = struct.unpack('<H', data.read(2))[0]
        _ = data.read(2) # padding
        index_buffer_offset = struct.unpack('<L', data.read(4))[0]
        vertex_buffer_offset = struct.unpack('<L', data.read(4))[0]

        data.seek(index_buffer_offset)
        self.d3d9_renderable.index_buffer.indices_count = struct.unpack('<L', data.read(4))[0]
        self.d3d9_renderable.index_buffer.data_offset = struct.unpack('<L', data.read(4))[0]
        _ = data.read(4)
        self.d3d9_renderable.index_buffer.format = d3d9.Format(struct.unpack('<l', data.read(4))[0])

        data.seek(vertex_buffer_offset)
        self.d3d9_renderable.vertex_buffer.data_offset = struct.unpack('<L', data.read(4))[0]
        _ = data.read(4)
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
            _ = data.read(4)
            mesh.vertex_descriptors_count = struct.unpack('B', data.read(1))[0]
            mesh.instance_count = struct.unpack('B', data.read(1))[0]
            mesh.vertex_buffers_count = struct.unpack('B', data.read(1))[0]
            mesh.flags = struct.unpack('B', data.read(1))[0]


    def _store(self) -> None:
        data = io.BytesIO()

        data.seek(0x0)
        data.write(struct.pack('<ffff', *self.d3d11_renderable.bounding_sphere))
        data.write(struct.pack('<H', self.d3d11_renderable.version_number))
        data.write(struct.pack('<H', self.d3d11_renderable.meshes_count))
        data.write(struct.pack('<L', 0))
        data.write(struct.pack('<L', 0))
        data.write(struct.pack('<H', self.d3d11_renderable.flags))
        data.write(bytes(2)) # padding
        data.write(struct.pack('<L', 0))
        data.write(struct.pack('<L', 0))

        meshes_offset = bnd2.util.align_offset(data.tell(), 0x10)
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

        meshes_offstes = []
        import_index = 0
        for i, mesh in enumerate(self.d3d11_renderable.meshes):
            mesh_offset = bnd2.util.align_offset(data.tell(), 0x10)
            meshes_offstes.append(mesh_offset)
            data.seek(mesh_offset)
            for j in range(16):
                data.write(struct.pack('<f', mesh.affine_transformation_matrix[j]))
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
