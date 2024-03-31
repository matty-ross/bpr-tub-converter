import io
import struct

import bnd2

from . import d3d9
from . import d3d11


D3D9_DATA_TYPE_TO_D3D11_FORMAT = {
    d3d9.DataType.FLOAT1: d3d11.Format.R32_FLOAT,
    d3d9.DataType.FLOAT2: d3d11.Format.R32G32_FLOAT,
    d3d9.DataType.FLOAT3: d3d11.Format.R32G32B32_FLOAT,
    d3d9.DataType.FLOAT4: d3d11.Format.R32G32B32A32_FLOAT,
    d3d9.DataType.UBYTE4: d3d11.Format.R8G8B8A8_UINT,
    d3d9.DataType.SHORT2: d3d11.Format.R16G16_SINT,
    d3d9.DataType.SHORT4: d3d11.Format.R16G16B16A16_SINT,
    d3d9.DataType.UBYTE4N: d3d11.Format.R8G8B8A8_UNORM,
    d3d9.DataType.SHORT2N: d3d11.Format.R16G16_SNORM,
    d3d9.DataType.SHORT4N: d3d11.Format.R16G16B16A16_SNORM,
    d3d9.DataType.USHORT2N: d3d11.Format.R16G16_UNORM,
    d3d9.DataType.USHORT4N: d3d11.Format.R16G16B16A16_UNORM,
    d3d9.DataType.UNUSED: d3d11.Format.UNKNOWN,
}


D3D9_ELEMENT_TYPE_TO_D3D11_SEMANTIC_NAME = {
    d3d9.ElementType.NONE: d3d11.SemanticName.NONE,
    d3d9.ElementType.POSITION: d3d11.SemanticName.POSITION,
    d3d9.ElementType.NORMAL: d3d11.SemanticName.NORMAL,
    d3d9.ElementType.TEXCOORD_0: d3d11.SemanticName.TEXCOORD_0,
    d3d9.ElementType.TEXCOORD_1: d3d11.SemanticName.TEXCOORD_1,
    d3d9.ElementType.BLEND_INDICES: d3d11.SemanticName.BLEND_INDICES,
    d3d9.ElementType.BLEND_WEIGHT: d3d11.SemanticName.BLEND_WEIGHT,
    d3d9.ElementType.TANGENT: d3d11.SemanticName.TANGENT,
}


class VertexDescriptor:

    def __init__(self, resource_entry: bnd2.ResourceEntry):
        assert resource_entry.type == 10, f"Resource entry with ID {resource_entry.id :08X} isn't VertexDescriptor."
        self.resource_entry = resource_entry
        self.d3d9_vertex_descriptor = d3d9.VertexDescriptor()
        self.d3d11_vertex_descriptor = d3d11.VertexDescriptor()


    def convert(self) -> None:
        self._load()

        self.d3d11_vertex_descriptor.elements_hash = 0x00000000
        self.d3d11_vertex_descriptor.elements_count = self.d3d9_vertex_descriptor.elements_count

        self.d3d11_vertex_descriptor.elements = [d3d11.Element() for _ in range(self.d3d9_vertex_descriptor.elements_count)]
        for i in range(self.d3d9_vertex_descriptor.elements_count):
            self.d3d11_vertex_descriptor.elements[i].semantic_name = D3D9_ELEMENT_TYPE_TO_D3D11_SEMANTIC_NAME[self.d3d9_vertex_descriptor.elements[i].type]
            self.d3d11_vertex_descriptor.elements[i].format = D3D9_DATA_TYPE_TO_D3D11_FORMAT[self.d3d9_vertex_descriptor.elements[i].data_type]
            self.d3d11_vertex_descriptor.elements[i].offset = self.d3d9_vertex_descriptor.elements[i].offset
            self.d3d11_vertex_descriptor.elements[i].vertex_stride = self.d3d9_vertex_descriptor.elements[i].vertex_stride
            self.d3d11_vertex_descriptor.elements_hash |= (1 << self.d3d11_vertex_descriptor.elements[i].semantic_name.value)

        self._store()


    def _load(self) -> None:
        data = io.BytesIO(self.resource_entry.data[0])

        data.seek(0x0)
        _ = data.read(4)
        _ = data.read(4)
        self.d3d9_vertex_descriptor.elements_hash = struct.unpack('<L', data.read(4))[0]
        self.d3d9_vertex_descriptor.elements_count = struct.unpack('B', data.read(1))[0]
        _ = data.read(1)
        _ = data.read(2)

        self.d3d9_vertex_descriptor.elements = [d3d9.Element() for _ in range(self.d3d9_vertex_descriptor.elements_count)]
        for i, element in enumerate(self.d3d9_vertex_descriptor.elements):
            data.seek(0x10 + i * 0x10)
            _ = data.read(1)
            element.vertex_stride = struct.unpack('B', data.read(1))[0]
            element.offset = struct.unpack('<H', data.read(2))[0]
            element.data_type = d3d9.DataType(struct.unpack('<l', data.read(4))[0])
            _ = data.read(1)
            _ = data.read(1)
            _ = data.read(1)
            element.type = d3d9.ElementType(struct.unpack('b', data.read(1))[0])
            _ = data.read(4)


    def _store(self) -> None:
        data = io.BytesIO()

        data.seek(0x0)
        data.write(struct.pack('<L', 1))
        data.write(struct.pack('<L', self.d3d11_vertex_descriptor.elements_hash))
        data.write(struct.pack('<L', 0))
        data.write(struct.pack('B', self.d3d11_vertex_descriptor.elements_count))
        data.write(struct.pack('B', 0))
        data.write(struct.pack('<H', 0))

        for i, element in enumerate(self.d3d11_vertex_descriptor.elements):
            data.seek(0x10 + i * 0x14)
            data.write(struct.pack('b', element.semantic_name.value))
            data.write(struct.pack('B', 0))
            data.write(struct.pack('B', 0))
            data.write(struct.pack('b', 0))
            data.write(struct.pack('<l', element.format.value))
            data.write(struct.pack('<L', element.offset))
            data.write(struct.pack('<L', 0))
            data.write(struct.pack('<L', element.vertex_stride))

        self.resource_entry.data[0] = data.getvalue()
