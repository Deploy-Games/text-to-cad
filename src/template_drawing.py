"""
Starter template for generating professional ISO engineering drawings (PDF).
Run: cad run src/template_drawing.py
"""

from pathlib import Path
from cad.eng_drawing import Sheet, eng_drawing
from template_part import HEIGHT, HOLE_DIAMETER, LENGTH, WIDTH, template_part

OUT_PDF = Path(__file__).resolve().parent.parent / "drawings" / "template_drawing.pdf"


@eng_drawing(out=str(OUT_PDF))
def template_drawing():
    """Generates a standard ISO dimensioned shop print as a vector PDF."""
    part = template_part().shape

    # Choose sheet size: A4, A3, A2...
    # scale: 1.0 (1:1), 0.5 (1:2)
    sheet = Sheet(
        "A4",
        scale=0.5,
        title="TEMPLATE PART",
        part_number="PART-001",
        material="ALUMINUM 6061-T6",
        revision="A",
        general_tolerance="ISO 2768-m",
        notes=[
            "BREAK ALL SHARP EDGES 0.5 MM MAX.",
            "ALL DIMENSIONS IN MILLIMETERS (MM).",
        ],
    )

    # 3rd-angle orthographic projection: Top, Front, Right, Isometric
    top, front, right, iso = sheet.three_views(part, iso=True)

    # Add overall bounding dimensions
    top.overall()

    # Add hole callout with standard ISO hole symbol
    top.hole((0, 0, HEIGHT / 2), diameter=HOLE_DIAMETER, thru=True)

    # Add specific feature dimensions
    front.dim((-LENGTH / 2, -WIDTH / 2, -HEIGHT / 2), (-LENGTH / 2, -WIDTH / 2, HEIGHT / 2))

    return sheet


if __name__ == "__main__":
    template_drawing()
