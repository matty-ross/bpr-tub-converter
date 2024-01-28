import tkinter, tkinter.filedialog

from bnd2 import bundle_v2

from converters.texture.texture import Texture
from converters.vertex_descriptor.vertex_descriptor import VertexDescriptor
from converters.renderable.renderable import Renderable
from converters.texture_state.texture_state import TextureState
from converters.material_state.material_state import MaterialState


CONVERTERS = {
    0: Texture,
    10: VertexDescriptor,
    12: Renderable,
    14: TextureState,
    15: MaterialState,
}


def convert_bundle(bundle: bundle_v2.BundleV2) -> None:
    for resource_entry in bundle.resource_entries:
        cls = CONVERTERS.get(resource_entry.type)
        if cls:
            converter = cls(resource_entry)
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
