import io
import struct
import random
import copy
import tkinter, tkinter.filedialog

import bnd2

from converters.texture.texture import Texture
from converters.vertex_descriptor.vertex_descriptor import VertexDescriptor
from converters.renderable.renderable import Renderable
from converters.texture_state.texture_state import TextureState
from converters.material_state.material_state import MaterialState, D3D9_MATERIAL_STATE_ID_TO_D3D11_MATERIAL_STATE_ID


def convert_resource_entry(bundle: bnd2.BundleV2, resource_entry: bnd2.ResourceEntry) -> None:
    new_id = random.randint(0x00000000, 0xFFFFFFFF)

    match resource_entry.type:
        # Texture
        case 0:
            converter = Texture(resource_entry)
            converter.convert()
            bundle.change_resource_id(resource_entry.id, new_id)

        # Material
        case 1:
            data = io.BytesIO(resource_entry.data[0])
            data.seek(0x4)
            data.write(struct.pack('<L', new_id))
            resource_entry.data[0] = data.getvalue()
            bundle.change_resource_id(resource_entry.id, new_id)

        # Vertex Descriptor
        case 10:
            converter = VertexDescriptor(resource_entry)
            converter.convert()
            bundle.change_resource_id(resource_entry.id, new_id)

        # Renderable
        case 12:
            converter = Renderable(resource_entry)
            converter.convert()
            bundle.change_resource_id(resource_entry.id, new_id)

        # Texture State
        case 14:
            converter = TextureState(resource_entry)
            converter.convert()
            bundle.change_resource_id(resource_entry.id, new_id)

        # Material State
        case 15:
            converter = MaterialState(resource_entry)
            converter.convert()
            bundle.change_resource_id(resource_entry.id, D3D9_MATERIAL_STATE_ID_TO_D3D11_MATERIAL_STATE_ID[resource_entry.id])

        # Model
        case 42:
            bundle.change_resource_id(resource_entry.id, new_id)


def convert_bundle(bundle: bnd2.BundleV2, external_bundles: list[bnd2.BundleV2]) -> None:
    external_resource_ids = bundle.get_external_resource_ids()
    for external_resource_id in external_resource_ids:
        for external_bundle in external_bundles:
            external_resource_entry = external_bundle.get_resource_entry(external_resource_id)
            if external_resource_entry is not None:
                bundle.resource_entries.append(copy.deepcopy(external_resource_entry))
                break
        else:
            print(f"Cannot find external resource entry with ID {external_resource_id :08X}.")

    for resource_entry in bundle.resource_entries:
        convert_resource_entry(bundle, resource_entry)

    indexes: list[int] = []
    resource_ids = set()
    for index, resource_entry in enumerate(bundle.resource_entries):
        if resource_entry.id in resource_ids:
            indexes.append(index)
        else:
            resource_ids.add(resource_entry.id)
    for index in indexes:
        bundle.resource_entries.pop(index)
        print(f"Removed duplicate resource entry with ID {bundle.resource_entries[index].id :08X}.")


def main() -> None:
    tkinter.Tk().withdraw()

    file_names = tkinter.filedialog.askopenfilenames()
    bundles: list[bnd2.BundleV2] = []
    for file_name in file_names:
        bundle = bnd2.BundleV2(file_name)
        bundle.load()
        bundles.append(bundle)

    external_file_names = tkinter.filedialog.askopenfilenames()
    external_bundles: list[bnd2.BundleV2] = []
    for external_file_name in external_file_names:
        external_bundle = bnd2.BundleV2(external_file_name)
        external_bundle.load()
        external_bundles.append(external_bundle)

    for bundle in bundles:
        print(f"Converting bundle '{bundle.file_name}'...")
        convert_bundle(bundle, external_bundles)
        bundle.save()
        print("Done.")


if __name__ == '__main__':
    main()
