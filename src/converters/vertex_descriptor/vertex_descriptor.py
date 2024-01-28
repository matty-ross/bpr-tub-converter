import io
import struct

from bnd2 import bundle_v2

from . import d3d9
from . import d3d11


D3D9_DATA_TYPE_TO_D3D11_FORMAT = {
    d3d9.DataType.FLOAT1: d3d11.Format.R32_FLOAT,
    d3d9.DataType.FLOAT2: d3d11.Format.R32G32_FLOAT,
    d3d9.DataType.FLOAT3: d3d11.Format.R32G32B32_FLOAT,
    d3d9.DataType.FLOAT4: d3d11.Format.R32G32B32A32_FLOAT,
    # d3d9.DataType.D3DCOLOR:
    d3d9.DataType.UBYTE4: d3d11.Format.R8G8B8A8_UINT,
    d3d9.DataType.SHORT2: d3d11.Format.R16G16_SINT,
    d3d9.DataType.SHORT4: d3d11.Format.R16G16B16A16_SINT,
    d3d9.DataType.UBYTE4N: d3d11.Format.R8G8B8A8_UNORM,
    d3d9.DataType.SHORT2N: d3d11.Format.R16G16_SNORM,
    d3d9.DataType.SHORT4N: d3d11.Format.R16G16B16A16_SNORM,
    d3d9.DataType.USHORT2N: d3d11.Format.R16G16_UNORM,
    d3d9.DataType.USHORT4N: d3d11.Format.R16G16B16A16_UNORM,
    # d3d9.DataType.UDEC3:
    # d3d9.DataType.DEC3N:
    d3d9.DataType.FLOAT16_2: d3d11.Format.R16G16_FLOAT,
    d3d9.DataType.FLOAT16_4: d3d11.Format.R16G16B16A16_FLOAT,
    d3d9.DataType.UNUSED: d3d11.Format.UNKNOWN,
}


D3D9_USAGE_TO_D3D11_SEMANTIC_NAME = {
    d3d9.Usage.POSITION: d3d11.SemanticName.POSITION,
    d3d9.Usage.BLENDWEIGHT: d3d11.SemanticName.BLENDWEIGHT,
    d3d9.Usage.BLENDINDICES: d3d11.SemanticName.BLENDINDICES,
    d3d9.Usage.NORMAL: d3d11.SemanticName.NORMAL,
    d3d9.Usage.PSIZE: d3d11.SemanticName.PSIZE,
    # d3d9.Usage.TEXCOORD: TODO
    d3d9.Usage.TANGENT: d3d11.SemanticName.TANGENT,
    d3d9.Usage.BINORMAL: d3d11.SemanticName.BINORMAL.BINORMAL,
    # d3d9.Usage.TESSFACTOR:
    d3d9.Usage.POSITIONT: d3d11.SemanticName.POSITIONT,
    # d3d9.Usage.COLOR: TODO
    # d3d9.Usage.FOG:
    # d3d9.Usage.DEPTH:
    # d3d9.Usage.SAMPLE:
}


D3D9_MAP_INDEX_TO_D3D11_SEMANTIC_NAME = {
    0: d3d11.SemanticName.NONE,
    1: d3d11.SemanticName.POSITION,
    2: d3d11.SemanticName.POSITION,
    3: d3d11.SemanticName.NORMAL,
    4: d3d11.SemanticName.COLOR0,
    5: d3d11.SemanticName.COLOR1,
    6: d3d11.SemanticName.TEXCOORD0,
    7: d3d11.SemanticName.TEXCOORD1,
    8: d3d11.SemanticName.TEXCOORD2,
    9: d3d11.SemanticName.TEXCOORD3,
    10: d3d11.SemanticName.TEXCOORD4,
    11: d3d11.SemanticName.TEXCOORD5,
    12: d3d11.SemanticName.TEXCOORD6,
    13: d3d11.SemanticName.TEXCOORD7,
    14: d3d11.SemanticName.BLENDINDICES,
    15: d3d11.SemanticName.BLENDWEIGHT,
    16: d3d11.SemanticName.POSITION,
    17: d3d11.SemanticName.NORMAL,
    18: d3d11.SemanticName.POSITION,
    19: d3d11.SemanticName.POSITION,
    20: d3d11.SemanticName.POSITION,
    21: d3d11.SemanticName.TANGENT,
    22: d3d11.SemanticName.BINORMAL,
    # 23:
    # 24:
    25: d3d11.SemanticName.PSIZE,
    26: d3d11.SemanticName.BLENDINDICES,
    27: d3d11.SemanticName.BLENDWEIGHT,
}


D3D9_MAP_INDEX_TO_D3D11_SEMANTIC_INDEX = {
    0: 0,
    1: 0,
    2: 0,
    3: 0,
    4: 0,
    5: 1,
    6: 0,
    7: 1,
    8: 2,
    9: 3,
    10: 4,
    11: 5,
    12: 6,
    13: 7,
    14: 0,
    15: 0,
    16: 1,
    17: 1,
    18: 0,
    19: 0,
    20: 0,
    21: 0,
    22: 0,
    23: 2,
    24: 0,
    25: 0,
    26: 1,
    27: 1,
}


class VertexDescriptor:

    def __init__(self, resource_entry: bundle_v2.ResourceEntry):
        assert resource_entry.type == 10, f"Resource entry with ID {resource_entry.id :08X} isn't VertexDescriptor."
        self.resource_entry: bundle_v2.ResourceEntry = resource_entry

        self.d3d9_vertex_descriptor = d3d9.VertexDescriptor()
        self.d3d11_vertex_descriptor = d3d11.VertexDescriptor()


    def convert(self) -> None:
        self._load()

        self.d3d11_vertex_descriptor.elements_hash = 0x00000000
        self.d3d11_vertex_descriptor.input_slots_hash = 0x00000000
        self.d3d11_vertex_descriptor.elements_count = self.d3d9_vertex_descriptor.elements_count
        self.d3d11_vertex_descriptor.input_slots_count = self.d3d9_vertex_descriptor.streams_count

        self.d3d11_vertex_descriptor.elements = [d3d11.Element() for _ in range(self.d3d9_vertex_descriptor.elements_count)]
        for i in range(self.d3d9_vertex_descriptor.elements_count):
            usage = self.d3d9_vertex_descriptor.elements[i].usage
            usage_index = self.d3d9_vertex_descriptor.elements[i].usage_index
            map_index = self.d3d9_vertex_descriptor.elements[i].map_index
            
            self.d3d11_vertex_descriptor.elements[i].semantic_name = D3D9_USAGE_TO_D3D11_SEMANTIC_NAME[usage] if usage is not None else D3D9_MAP_INDEX_TO_D3D11_SEMANTIC_NAME[map_index]
            self.d3d11_vertex_descriptor.elements[i].semantic_index = usage_index if usage_index is not None else D3D9_MAP_INDEX_TO_D3D11_SEMANTIC_INDEX[map_index]
            self.d3d11_vertex_descriptor.elements[i].input_slot = self.d3d9_vertex_descriptor.elements[i].stream_number
            self.d3d11_vertex_descriptor.elements[i].input_slot_class = d3d11.InputClassification.PER_VERTEX_DATA
            self.d3d11_vertex_descriptor.elements[i].format = D3D9_DATA_TYPE_TO_D3D11_FORMAT[self.d3d9_vertex_descriptor.elements[i].data_type]
            self.d3d11_vertex_descriptor.elements[i].offset = self.d3d9_vertex_descriptor.elements[i].offset
            self.d3d11_vertex_descriptor.elements[i].instance_data_step_rate = 0
            self.d3d11_vertex_descriptor.elements[i].vertex_stride = self.d3d9_vertex_descriptor.elements[i].vertex_stride
            
            self.d3d11_vertex_descriptor.elements_hash |= (1 << self.d3d11_vertex_descriptor.elements[i].semantic_name.value)
            if self.d3d11_vertex_descriptor.elements[i].input_slot_class == d3d11.InputClassification.PER_INSTANCE_DATA:
                self.d3d11_vertex_descriptor.input_slots_hash |= (1 << self.d3d11_vertex_descriptor.elements[i].input_slot)

        self._store()


    def _load(self) -> None:
        data = io.BytesIO(self.resource_entry.data[0])

        data.seek(0x8)
        self.d3d9_vertex_descriptor.elements_hash = struct.unpack('<L', data.read(4))[0]
        self.d3d9_vertex_descriptor.elements_count = struct.unpack('B', data.read(1))[0]
        self.d3d9_vertex_descriptor.streams_count = struct.unpack('B', data.read(1))[0]

        self.d3d9_vertex_descriptor.elements = [d3d9.Element() for _ in range(self.d3d9_vertex_descriptor.elements_count)]
        for i, element in enumerate(self.d3d9_vertex_descriptor.elements):
            data.seek(0x10 + i * 0x10)
            element.stream_number = struct.unpack('B', data.read(1))[0]
            element.vertex_stride = struct.unpack('B', data.read(1))[0]
            element.offset = struct.unpack('<H', data.read(2))[0]
            element.data_type = d3d9.DataType(struct.unpack('<l', data.read(4))[0])
            element.method = d3d9.Method(struct.unpack('b', data.read(1))[0])
            usage = struct.unpack('b', data.read(1))[0]
            usage_index = struct.unpack('b', data.read(1))[0]
            element.usage = d3d9.Usage(usage) if usage != -1 else None
            element.usage_index = usage_index if usage_index != -1 else None
            element.map_index = struct.unpack('B', data.read(1))[0]


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
