"""
ISO Engineering Drawing for Partitioned Desk / Storage Frame.
Run: cad run src/desk_storage_frame_drawing.py
"""

from pathlib import Path
from cad.eng_drawing import Sheet, eng_drawing
from desk_storage_frame import (
    BOTTOM_THICKNESS,
    OVERALL_DEPTH,
    OVERALL_HEIGHT,
    OVERALL_LENGTH,
    WALL_THICKNESS,
    X_DIV_1,
    X_DIV_2,
    X_DIV_3,
    Y_DIV_1,
    desk_storage_frame,
)

OUT_PDF = Path(__file__).resolve().parent.parent / "drawings" / "desk_storage_frame_drawing.pdf"


@eng_drawing(out=str(OUT_PDF))
def desk_storage_frame_drawing():
    """Generates a standard ISO dimensioned shop print as a vector PDF."""
    part = desk_storage_frame().shape

    sheet = Sheet(
        "A3",
        scale=0.1,  # 1:10 standard furniture/cabinetry drawing scale
        title="PARTITIONED STORAGE FRAME / BASE",
        part_number="DSF-160-80-30",
        material="18mm BIRCH PLYWOOD / MDF",
        revision="A",
        general_tolerance="ISO 2768-m",
        notes=[
            "1. DIGITIZED FROM NOTEPAD CONCEPT SKETCH (TOP & SIDE ELEVATION).",
            "2. NOMINAL DIMENSIONS: 1600 x 800 x 300 MM (160 x 80 x 30 CM).",
            "3. 6 COMPARTMENTS WITH 18 MM UNIFORM INTERNAL & PERIMETER WALLS.",
            "4. BREAK ALL SHARP EDGES 0.5 MM MAX.",
            "5. ALL DIMENSIONS IN MILLIMETERS (MM) UNLESS OTHERWISE SPECIFIED.",
        ],
    )

    # 3rd-angle orthographic projection: Top, Front, Right, Isometric
    top, front, right, iso = sheet.three_views(part, iso=True)

    # 1. Overall Bounding Dimensions
    top.overall()
    front.overall()
    right.overall()

    # 2. Top View: Dimension the divider bays along top/rear (X-axis)
    # Rear bays: 400, 600, 200, 400
    top.dim((0, OVERALL_DEPTH, OVERALL_HEIGHT), (X_DIV_1, OVERALL_DEPTH, OVERALL_HEIGHT))
    top.dim((X_DIV_1, OVERALL_DEPTH, OVERALL_HEIGHT), (X_DIV_2, OVERALL_DEPTH, OVERALL_HEIGHT))
    top.dim((X_DIV_2, OVERALL_DEPTH, OVERALL_HEIGHT), (X_DIV_3, OVERALL_DEPTH, OVERALL_HEIGHT))
    top.dim((X_DIV_3, OVERALL_DEPTH, OVERALL_HEIGHT), (OVERALL_LENGTH, OVERALL_DEPTH, OVERALL_HEIGHT))

    # Top View: Dimension along Y-axis (depth split at 400 mm)
    top.dim((OVERALL_LENGTH, 0, OVERALL_HEIGHT), (OVERALL_LENGTH, Y_DIV_1, OVERALL_HEIGHT))
    top.dim((OVERALL_LENGTH, Y_DIV_1, OVERALL_HEIGHT), (OVERALL_LENGTH, OVERALL_DEPTH, OVERALL_HEIGHT))

    # Front View: Height of bottom base and wall height
    front.dim((0, 0, 0), (0, 0, BOTTOM_THICKNESS))
    front.dim((0, 0, 0), (X_DIV_1, 0, 0))
    front.dim((X_DIV_1, 0, 0), (X_DIV_3, 0, 0))
    front.dim((X_DIV_3, 0, 0), (OVERALL_LENGTH, 0, 0))

    # Right View: Depth divisions
    right.dim((OVERALL_LENGTH, 0, 0), (OVERALL_LENGTH, Y_DIV_1, 0))
    right.dim((OVERALL_LENGTH, Y_DIV_1, 0), (OVERALL_LENGTH, OVERALL_DEPTH, 0))

    return sheet


if __name__ == "__main__":
    desk_storage_frame_drawing()
