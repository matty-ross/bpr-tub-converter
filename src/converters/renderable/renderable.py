import io
import struct

import bnd2

import d3d9
import d3d11


class Renderable:

    def __init__(self, resource_entry: bnd2.ResourceEntry):
        assert resource_entry.type == 12, f"Resource entry with ID {resource_entry.id :08X} isn't Renderable."
        self.resource_entry: bnd2.ResourceEntry = resource_entry

        self.d3d9_renderable = d3d9.Renderable()
        self.d3d11_renderable = d3d11.Renderable()


    def convert(self) -> None:
        pass


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

        meshes_offset = bnd2.BundleV2._align_offset(data.tell(), 0x10)
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

        for i, mesh in enumerate(self.d3d11_renderable.meshes):
            mesh_offset = bnd2.BundleV2._align_offset(data.tell(), 0x10)
            meshes_offstes.append(mesh_offset)
            data.seek(mesh_offset)
            for _ in range(16):
                data.write('<f', mesh.affine_transformation_matrix[i])
            data.write(struct.pack('<l', mesh.primitive_topology.value))
            data.write(struct.pack('<l', mesh.base_vertex_location))
            data.write(struct.pack('<L', mesh.start_index_location))
            data.write(struct.pack('<L', mesh.indices_count))
            data.write(struct.pack('<L', 0))
            data.write(struct.pack('B', mesh.vertex_descriptors_count))
            data.write(struct.pack('B', mesh.instance_count))
            data.write(struct.pack('B', mesh.vertex_buffers_count))
            data.write(struct.pack('B', mesh.flags))
            data.write(struct.pack('<L', index_buffer_offset))
            for _ in range(mesh.vertex_buffers_count):
                data.write(struct.pack('<L', vertex_buffer_offset))
            for _ in range(mesh.vertex_descriptors_count):
                data.write(struct.pack('<L', 0))

        # TODO: update import entries
                
        data.seek(0x14)
        data.write(struct.pack('<L', meshes_offset))
        data.seek(0x20)
        data.write(struct.pack('<L', index_buffer_offset))
        data.write(struct.pack('<L', vertex_buffer_offset))

        data.seek(meshes_offset)
        for mesh_offset in meshes_offstes:
            data.write(struct.pack('<L', mesh_offset))

        self.resource_entry.data[0] = data.getvalue()
