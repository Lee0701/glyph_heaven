
from svgwrite import Drawing

from kage import Kage
from kage.font.sans import Sans
from .kage_data import load

kage_data = load()

kage = Kage(ignore_component_version=True)
kage.font = Sans()
for name, data in kage_data.items():
    kage.components.push(name, data)

def render(data):
    drawing = Drawing(size=(16, 16))
    drawing = kage.make_glyph_with_data(drawing, data)
    if drawing is not None:
        drawing.viewbox(0, 0, 200, 200)
        return drawing.tostring()
    else:
        return None
