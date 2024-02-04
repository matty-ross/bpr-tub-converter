import io
import struct
import random
import tkinter, tkinter.filedialog

from bnd2 import bundle_v2

from converters.texture.texture import Texture
from converters.vertex_descriptor.vertex_descriptor import VertexDescriptor
from converters.renderable.renderable import Renderable
from converters.texture_state.texture_state import TextureState
from converters.material_state.material_state import MaterialState


def convert_resource_entry(bundle: bundle_v2.BundleV2, resource_entry: bundle_v2.ResourceEntry) -> None:
    new_id = random.randint(0x00000000, 0xFFFFFFFF)
    
    # Texture
    if resource_entry.type == 0:
        converter = Texture(resource_entry)
        converter.convert()
        bundle.change_resource_id(resource_entry.id, new_id)
        return
    
    # Material
    if resource_entry.type == 1:
        data = io.BytesIO(resource_entry.data[0])
        data.seek(0x4)
        data.write(struct.pack('<L', new_id))
        resource_entry.data[0] = data.getvalue()
        bundle.change_resource_id(resource_entry.id, new_id)
        return
    
    # Vertex Descriptor
    if resource_entry.type == 10:
        converter = VertexDescriptor(resource_entry)
        converter.convert()
        bundle.change_resource_id(resource_entry.id, new_id)
        return

    # Renderable
    if resource_entry.type == 12:
        converter = Renderable(resource_entry)
        converter.convert()
        bundle.change_resource_id(resource_entry.id, new_id)
        return

    # Texture State
    if resource_entry.type == 14:
        converter = TextureState(resource_entry)
        converter.convert()
        bundle.change_resource_id(resource_entry.id, new_id)
        return
    
    # Material State
    if resource_entry.type == 15:
        converter = MaterialState(resource_entry)
        converter.convert()
        bundle.change_resource_id(resource_entry.id, new_id)
        return
    
    # Model
    if resource_entry.type == 42:
        bundle.change_resource_id(resource_entry.id, new_id)
        return


def main() -> None:
    tkinter.Tk().withdraw()

    file_name = tkinter.filedialog.askopenfilename()
    bundle = bundle_v2.BundleV2(file_name)
    bundle.load()
    
    external_file_names = tkinter.filedialog.askopenfilenames()
    external_bundles: list[bundle_v2.BundleV2] = []
    for external_file_name in external_file_names:
        external_bundle = bundle_v2.BundleV2(external_file_name)
        external_bundle.load()    
        external_bundles.append(external_bundle)

    external_resource_ids = bundle.get_external_resource_ids()

    external_resource_entries: list[bundle_v2.ResourceEntry] = []
    for external_resource_id in external_resource_ids:
        for external_bundle in external_bundles:
            external_resource_entry = external_bundle.get_resource_entry(external_resource_id)
            if external_resource_entry is not None:
                external_resource_entries.append(external_resource_entry)
                break
        else:
            print(f"Cannot find external resource entry with ID {external_resource_id :08X}.")

    for external_resource_entry in external_resource_entries:
        bundle.resource_entries.append(external_resource_entry)
    
    for resource_entry in bundle.resource_entries:
        convert_resource_entry(bundle, resource_entry)
    
    # bundle.save()
    print("Done.")


if __name__ == '__main__':
    main()
