import tkinter, tkinter.filedialog

from bnd2 import bundle_v2

from converters.texture.texture import Texture
from converters.vertex_descriptor.vertex_descriptor import VertexDescriptor
from converters.renderable.renderable import Renderable
from converters.texture_state.texture_state import TextureState
from converters.material_state.material_state import MaterialState


def convert_bundle(bundle: bundle_v2.BundleV2) -> None:
    for resource_entry in bundle.resource_entries:
        converter = None
        if resource_entry.type == 0:
            converter = Texture(resource_entry)
        elif resource_entry.type == 10:
            converter = VertexDescriptor(resource_entry)
        elif resource_entry.type == 12:
            converter = Renderable(resource_entry)
        elif resource_entry.type == 14:
            converter = TextureState(resource_entry)
        elif resource_entry.type == 15:
            converter = MaterialState(resource_entry)
        
        if converter is not None:
            converter.convert()


def main() -> None:
    tkinter.Tk().withdraw()
    
    file_name = tkinter.filedialog.askopenfilename()

    bundle = bundle_v2.BundleV2(file_name)
    bundle.load()
    convert_bundle(bundle)
    bundle.save()


if __name__ == '__main__':
    main()
