"""
Professional ISO Engineering Drawing (PDF) for the perspective grid and cage sculpture.
Derived from the 3D solid model in src/perspective_grid_cage.py.

Run: cad run src/perspective_grid_cage_drawing.py
"""

from pathlib import Path

from cad.eng_drawing import Sheet, eng_drawing
from perspective_grid_cage import (
    BASE_DEPTH,
    BASE_HEIGHT,
    BASE_WIDTH,
    CAGE_DEPTH,
    CAGE_HEIGHT,
    CAGE_POS_X,
    CAGE_POS_Y,
    CAGE_WIDTH,
    REAR_WALL_HEIGHT,
    REAR_WALL_POS_X,
    REAR_WALL_POS_Y,
    TERRACE_1_HEIGHT,
    TERRACE_2_HEIGHT,
    TERRACE_3_HEIGHT,
    TOWER_DEPTH,
    TOWER_HEIGHT,
    TOWER_POS_X,
    TOWER_POS_Y,
    TOWER_WIDTH,
    perspective_grid_cage,
)

OUT_PDF = Path(__file__).resolve().parent.parent / "drawings" / "perspective_grid_cage_drawing.pdf"


@eng_drawing(out=str(OUT_PDF))
def perspective_grid_cage_drawing():
    """Generates standard ISO dimensioned shop drawing with 3rd-angle orthographic projections."""
    part = perspective_grid_cage().shape

    sheet = Sheet(
        "A3",
        scale=0.5,
        title="PERSPECTIVE GRID & CAGE SCULPTURE",
        part_number="CAD-SKETCH-21612",
        material="PLA / RESIN / SOLID",
        revision="A",
        general_tolerance="ISO 2768-m",
        notes=[
            "1. TOLERANCES PER ISO 2768-m UNLESS OTHERWISE SPECIFIED.",
            "2. ALL DIMENSIONS IN MILLIMETERS (MM).",
            "3. 3D PRINTABLE MONOLITHIC SOLID MODEL.",
            "4. BREAK ALL SHARP EDGES 0.5 MM.",
        ],
    )

    # 3rd-angle orthographic projection: Top, Front, Right, Isometric in free corner
    top, front, right, iso = sheet.three_views(part, iso=True)

    # Overall bounding dimensions
    top.overall()

    # Top View: Feature Placement & Widths
    top.dim((0.0, 0.0, 0.0), (BASE_WIDTH, 0.0, 0.0))
    top.dim((0.0, 0.0, 0.0), (0.0, BASE_DEPTH, 0.0))
    top.dim((CAGE_POS_X, CAGE_POS_Y, 0.0), (CAGE_POS_X + CAGE_WIDTH, CAGE_POS_Y, 0.0))
    top.dim((CAGE_POS_X, CAGE_POS_Y, 0.0), (CAGE_POS_X, CAGE_POS_Y + CAGE_DEPTH, 0.0))
    top.dim((TOWER_POS_X, TOWER_POS_Y, 0.0), (TOWER_POS_X + TOWER_WIDTH, TOWER_POS_Y, 0.0))

    # Front View: Heights of Base, Terraces, Tower and Cage
    front.dim((0.0, 0.0, 0.0), (0.0, 0.0, BASE_HEIGHT))
    front.dim((10.0, 15.0, 0.0), (10.0, 15.0, TERRACE_1_HEIGHT))
    front.dim((10.0, 35.0, 0.0), (10.0, 35.0, TERRACE_2_HEIGHT))
    front.dim((10.0, 58.0, 0.0), (10.0, 58.0, TERRACE_3_HEIGHT))
    front.dim((TOWER_POS_X, TOWER_POS_Y, 0.0), (TOWER_POS_X, TOWER_POS_Y, TOWER_HEIGHT))
    front.dim(
        (CAGE_POS_X, CAGE_POS_Y, 0.0),
        (CAGE_POS_X, CAGE_POS_Y, TERRACE_3_HEIGHT + CAGE_HEIGHT),
    )

    # Right View: Depth features
    right.dim((0.0, TOWER_POS_Y, 0.0), (0.0, TOWER_POS_Y + TOWER_DEPTH, 0.0))
    right.dim((0.0, REAR_WALL_POS_Y, 0.0), (0.0, REAR_WALL_POS_Y, REAR_WALL_HEIGHT))

    return sheet


if __name__ == "__main__":
    perspective_grid_cage_drawing()
