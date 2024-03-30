import bnd2


D3D9_MATERIAL_STATE_TO_D3D11_MATERIAL_STATE = {
    0x10B0FA41: 0xCDDA46F0,
    0x15D559B5: 0x7E72A026,
    0x161E6D1F: 0x0BA364FE,
    0x28943600: 0x7E72A026,
    0x2D65FDF3: 0x7E72A026,
    0x3BC485AF: 0x142FBEB9,
    0x55EFF8AF: 0xD4659F9B,
    0x56825599: 0xF744F0CD,
    0x5F9EF983: 0x142FBEB9,
    0x716C1EF4: 0xB46F4FEC,
    0x81D73454: 0xD4659F9B,
    0x82AB007B: 0x7E72A026,
    0x83026157: 0xF744F0CD,
    0x89722C1C: 0x0BA364FE,
    0xA02EBF50: 0xCDDA46F0,
    0xA3AA49C3: 0x0BA364FE,
    0xB9A9D0E4: 0x0BA364FE,
    0xF9D639DA: 0x78711562,
}


class MaterialState:

    def __init__(self, resource_entry: bnd2.ResourceEntry):
        assert resource_entry.type == 15, f"Resource entry with ID {resource_entry.id :08X} isn't MaterialState."
        self.resource_entry = resource_entry


    def convert(self) -> None:
        material_state_id = D3D9_MATERIAL_STATE_TO_D3D11_MATERIAL_STATE[self.resource_entry.id]

        with open(f'data/material_state/{material_state_id :08X}.bin', 'rb') as fp:
            self.resource_entry.data[0] = fp.read()

        self.resource_entry.id = material_state_id
