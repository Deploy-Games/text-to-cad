"""
ISO Engineering Drawing for the Multi-Stage Slide Mechanism.
Run: cad run src/multistage_slide_drawing.py
"""

from pathlib import Path
from cad.eng_drawing import Sheet, eng_drawing
from multistage_slide import multistage_slide

OUT_PDF = Path(__file__).resolve().parent.parent / "drawings" / "multistage_slide_drawing.pdf"


@eng_drawing(out=str(OUT_PDF))
def multistage_slide_drawing():
    """Generates a standard ISO dimensioned shop print as a vector PDF."""
    part = multistage_slide().shape

    sheet = Sheet(
        "A4",
        scale=0.25,
        title="MULTI-STAGE SLIDE MECHANISM",
        part_number="MSS-SKETCH-01",
        material="EN AW-6082-T6 / POM-C",
        revision="A",
        general_tolerance="ISO 2768-m",
        notes=[
            "1. DIGITIZED FROM PENCIL CONCEPT SKETCH ON 5MM GRID.",
            "2. BREAK ALL SHARP EDGES 0.5 MM MAX.",
            "3. DUAL-STAGE EXTENSION WITH T-SLOT LINEAR GUIDE TRACK.",
            "4. ALL DIMENSIONS IN MILLIMETERS (MM).",
        ],
    )

    # 3rd-angle orthographic projection: Top, Front, Right, Isometric
    top, front, right, iso = sheet.three_views(part, iso=True)

    # Add overall bounding dimensions
    top.overall()
    front.overall()

    return sheet


if __name__ == "__main__":
    multistage_slide_drawing()
