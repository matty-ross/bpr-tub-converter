import io
import struct

import bnd2

import d3d9
import d3d11


class VertexDescriptor:

    def __init__(self, resource_entry: bnd2.ResourceEntry):
        assert resource_entry.type == 10, f"Resource entry with ID {resource_entry.id :08X} isn't VertexDescriptor."
        self.resource_entry: bnd2.ResourceEntry = resource_entry

        self.d3d9_vertex_descriptor = d3d9.VertexDescriptor()
        self.d3d11_vertex_descriptor = d3d11.VertexDescriptor()


    def convert(self) -> None:
        self._load()

        self.d3d11_vertex_descriptor.elements_hash = 0
        self.d3d11_vertex_descriptor.input_slots_hash = 0
        self.d3d11_vertex_descriptor.elements_count = self.d3d9_vertex_descriptor.elements_count
        self.d3d11_vertex_descriptor.input_slots_count = 0

        # TODO: convert elements

        self._store()


    def _load(self) -> None:
        data = io.BytesIO(self.resource_entry.data[0])

        data.seek(0x8)
        self.d3d9_vertex_descriptor.elements_hash = struct.unpack('<L', data.read(4))[0]
        self.d3d9_vertex_descriptor.elements_count = struct.unpack('B', data.read(1))[0]
        self.d3d9_vertex_descriptor.streams_count = struct.unpack('B', data.read(1))[0]

        self.d3d9_vertex_descriptor.elements = []
        for i in range(self.d3d9_vertex_descriptor.elements_count):
            data.seek(0x10 + i * 0x10)
            element = d3d9.Element()
            element.stream_number = struct.unpack('B', data.read(1))[0]
            element.vertex_stride = struct.unpack('B', data.read(1))[0]
            element.offset = struct.unpack('<H', data.read(2))[0]
            element.data_type = d3d9.DataType(struct.unpack('<l', data.read(4))[0])
            element.method = d3d9.Method(struct.unpack('b', data.read(1))[0])
            element.usage = d3d9.Usage(struct.unpack('b', data.read(1))[0])
            element.usage_index = struct.unpack('B', data.read(1))[0]
            element.map_index = struct.unpack('B', data.read(1))[0]
            self.d3d9_vertex_descriptor.elements.append(element)


    def _store(self) -> None:
        data = io.BytesIO()

        data.seek(0x0)
        data.write(struct.pack('<L', 1))
        data.write(struct.pack('<L', self.d3d11_vertex_descriptor.elements_hash))
        data.write(struct.pack('<L', self.d3d11_vertex_descriptor.input_slots_hash))
        data.write(struct.pack('B', self.d3d11_vertex_descriptor.elements_count))
        data.write(struct.pack('B', self.d3d11_vertex_descriptor.input_slots_count))
        data.write(struct.pack('<H', 0))
        
        for i, element in enumerate(self.d3d11_vertex_descriptor.elements):
            data.seek(0x10 + i * 0x14)
            data.write(struct.pack('b', element.semantic_name.value))
            data.write(struct.pack('B', element.semantic_index))
            data.write(struct.pack('B', element.input_slot))
            data.write(struct.pack('b', element.input_slot_class.value))
            data.write(struct.pack('<l', element.format.value))
            data.write(struct.pack('<L', element.offset))
            data.write(struct.pack('<L', element.instance_data_step_rate))
            data.write(struct.pack('<L', element.vertex_stride))
