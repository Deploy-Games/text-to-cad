"""
ISO engineering drawing for the tiled room corner (src/perspective_grid_cage.py).

Run: cad run src/perspective_grid_cage_drawing.py
"""

from pathlib import Path

from cad.eng_drawing import Sheet, eng_drawing
from perspective_grid_cage import (
    CAGE_H, CAGE_P, CAGE_W, CAGE_X, CAGE_Z, D, FLOOR_T, L, PIER_D, PIER_W, PIER_Y,
    STAIR_N, STAIR_RISE, STAIR_RUN, STAIR_W, WALL_H, WALL_T, perspective_grid_cage,
)

OUT_PDF = Path(__file__).resolve().parent.parent / "drawings" / "perspective_grid_cage_drawing.pdf"


@eng_drawing(out=str(OUT_PDF))
def perspective_grid_cage_drawing():
    part = perspective_grid_cage().shape

    sheet = Sheet(
        "A3",
        scale=0.5,
        title="TILED ROOM CORNER WITH STAIR",
        part_number="CAD-SKETCH-21612",
        material="PLA (3D PRINT)",
        revision="B",
        general_tolerance="ISO 2768-m",
        notes=[
            f"TILE JOINTS {TILE_TXT} ON FLOOR AND INNER WALL FACES.",
            f"STAIR {STAIR_N} STEPS, RISE {STAIR_RISE:g} x RUN {STAIR_RUN:g}. WINDOW BOX: 4 BARS, OPEN FRONT.",
        ],
    )

    top, front, right, iso = sheet.three_views(part, iso=True, hidden=False)
    top.overall()

    z0 = FLOOR_T
    yb = D - WALL_T
    xr = L - WALL_T

    # Top: walls, stair, pier, window box
    top.dim((0, D, 0), (STAIR_W, D, 0))
    top.dim((L - WALL_T, 0, 0), (L, 0, 0), offset=-24)
    top.dim((0, yb - STAIR_RUN * STAIR_N, 0), (0, yb, 0))
    top.dim((L, PIER_Y, 0), (L, PIER_Y + PIER_D, 0))
    top.dim((xr - PIER_W, 0, 0), (xr, 0, 0), offset=-12)
    top.dim((L, yb, 0), (L, D, 0))
    top.dim((CAGE_X, 0, 0), (CAGE_X + CAGE_W, 0, 0), offset=-12)

    # Front: floor, stair head, window box
    front.dim((L, 0, 0), (L, 0, z0))
    front.dim((STAIR_W, 0, 0), (STAIR_W, 0, z0 + STAIR_RISE * STAIR_N))

    front.dim((0, 0, 0), (0, 0, z0 + WALL_H))
    front.dim((CAGE_X, 0, z0 + CAGE_Z), (CAGE_X, 0, z0 + CAGE_Z + CAGE_H), offset=-8)
    top.dim((0, yb - CAGE_P, 0), (0, yb, 0), offset=-24)

    return sheet


TILE_TXT = "10 x 10 GRID, 0.8 WIDE x 0.6 DEEP"

if __name__ == "__main__":
    perspective_grid_cage_drawing()
