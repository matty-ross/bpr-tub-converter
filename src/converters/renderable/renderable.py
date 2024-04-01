import io
import struct

import bnd2

from . import d3d9
from . import d3d11


D3D3_INDEX_FORMAT_TO_D3D11_INDEX_SIZE = {
    d3d9.IndexFormat.INDEX_16: 2,
    d3d9.IndexFormat.INDEX_32: 4,
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
        self.d3d11_renderable.meshes_count = self.d3d9_renderable.meshes_count
        self.d3d11_renderable.flags = self.d3d9_renderable.flags

        self.d3d11_renderable.index_buffer.type = d3d11.BufferType.INDEX_BUFFER
        self.d3d11_renderable.index_buffer.data_offset = self.d3d9_renderable.index_buffer.data_offset
        self.d3d11_renderable.index_buffer.data_size = D3D3_INDEX_FORMAT_TO_D3D11_INDEX_SIZE[self.d3d9_renderable.index_buffer.format] * self.d3d9_renderable.index_buffer.indices_count
        self.d3d11_renderable.index_buffer.index_size = D3D3_INDEX_FORMAT_TO_D3D11_INDEX_SIZE[self.d3d9_renderable.index_buffer.format]

        self.d3d11_renderable.vertex_buffer.type = d3d11.BufferType.VERTEX_BUFFER
        self.d3d11_renderable.vertex_buffer.data_offset = self.d3d9_renderable.vertex_buffer.data_offset
        self.d3d11_renderable.vertex_buffer.data_size = self.d3d9_renderable.vertex_buffer.data_size

        self.d3d11_renderable.meshes = [d3d11.Mesh() for _ in range(self.d3d9_renderable.meshes_count)]
        for i in range(self.d3d9_renderable.meshes_count):
            self.d3d11_renderable.meshes[i].transformation = self.d3d9_renderable.meshes[i].transformation
            self.d3d11_renderable.meshes[i].start_index_location = self.d3d9_renderable.meshes[i].start_index
            self.d3d11_renderable.meshes[i].indices_count = 3 * self.d3d9_renderable.meshes[i].primitives_count
            self.d3d11_renderable.meshes[i].vertex_descriptors_count = self.d3d9_renderable.meshes[i].vertex_descriptors_count
            self.d3d11_renderable.meshes[i].flags = self.d3d9_renderable.meshes[i].flags

        self._store()


    def _load(self) -> None:
        data = io.BytesIO(self.resource_entry.data[0])

        data.seek(0x0)
        self.d3d9_renderable.bounding_sphere = struct.unpack('<4f', data.read(4 * 4))
        _ = data.read(2)
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
        self.d3d9_renderable.index_buffer.format = d3d9.IndexFormat(struct.unpack('<l', data.read(4))[0])

        data.seek(vertex_buffer_offset)
        self.d3d9_renderable.vertex_buffer.data_offset = struct.unpack('<L', data.read(4))[0]
        _ = data.read(4)
        self.d3d9_renderable.vertex_buffer.data_size = struct.unpack('<L', data.read(4))[0]
        _ = data.read(4)

        self.d3d9_renderable.meshes = [d3d9.Mesh() for _ in range(self.d3d9_renderable.meshes_count)]
        for i, mesh in enumerate(self.d3d9_renderable.meshes):
            data.seek(meshes_offset + i * 0x4)
            mesh_offset = struct.unpack('<L', data.read(4))[0]
            data.seek(mesh_offset)
            mesh.transformation = struct.unpack('<16f', data.read(16 * 4))
            _ = data.read(4)
            _ = data.read(4)
            mesh.start_index = struct.unpack('<L', data.read(4))[0]
            mesh.vertices_count = struct.unpack('<L', data.read(4))[0]
            mesh.minimum_vertex_index = struct.unpack('<L', data.read(4))[0]
            mesh.primitives_count = struct.unpack('<L', data.read(4))[0]
            _ = data.read(4)
            mesh.vertex_descriptors_count = struct.unpack('B', data.read(1))[0]
            _ = data.read(1)
            _ = data.read(1)
            mesh.flags = struct.unpack('B', data.read(1))[0]


    def _store(self) -> None:
        data = io.BytesIO()

        data.seek(0x0)
        data.write(struct.pack('<4f', *self.d3d11_renderable.bounding_sphere))
        data.write(struct.pack('<H', 11))
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
        data.write(struct.pack('<l', 0))
        data.write(struct.pack('<l', self.d3d11_renderable.index_buffer.type.value))
        data.write(struct.pack('<L', self.d3d11_renderable.index_buffer.data_offset))
        data.write(struct.pack('<L', self.d3d11_renderable.index_buffer.data_size))
        data.write(struct.pack('<L', self.d3d11_renderable.index_buffer.index_size))

        vertex_buffer_offset = data.tell()
        data.write(struct.pack('<L', 0))
        data.write(struct.pack('<l', 0))
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
            data.write(struct.pack('<16f', *mesh.transformation))
            data.write(struct.pack('<l', 4))
            data.write(struct.pack('<l', 0))
            data.write(struct.pack('<L', mesh.start_index_location))
            data.write(struct.pack('<L', mesh.indices_count))
            self.resource_entry.import_entries[import_index].offset = data.tell()
            import_index += 1
            data.write(struct.pack('<L', 0))
            data.write(struct.pack('B', mesh.vertex_descriptors_count))
            data.write(struct.pack('B', 0))
            data.write(struct.pack('B', 1))
            data.write(struct.pack('B', mesh.flags))
            data.write(struct.pack('<L', index_buffer_offset))
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
