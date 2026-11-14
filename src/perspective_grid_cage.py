"""
Parametric 3D solid model of the perspective grid and cage sculpture,
reconstructed from the user's hand sketch (21612.jpg).

Features:
- Solid base plate with engraved perspective grid network
- Stepped cascading terraces leading from the floor to the elevated platform
- Slotted 3D cage / pavilion with vertical bars and hollow interior
- Rear connecting wall and right-hand ribbed / accordion tower structure
- Monolithic, watertight, manifold solid ideal for 3D printing (STL) and ISO engineering drawings

Run: cad run src/perspective_grid_cage.py
"""

from __future__ import annotations

import build123d as bd
from cad import model

# --- Parametric Dimensions (mm) ---
# Base Envelope
BASE_WIDTH = 100.0   # X dimension
BASE_DEPTH = 100.0   # Y dimension
BASE_HEIGHT = 6.0    # Z floor thickness

# Stepped Terraces (ascends from front-center toward rear-left)
TERRACE_1_HEIGHT = 16.0
TERRACE_2_HEIGHT = 28.0
TERRACE_3_HEIGHT = 42.0   # Elevated platform supporting the cage

# Cage Dimensions
CAGE_WIDTH = 26.0    # X dimension
CAGE_DEPTH = 22.0    # Y dimension
CAGE_HEIGHT = 20.0   # Z height above terrace 3
CAGE_POS_X = 16.0    # X start on terrace 3
CAGE_POS_Y = 66.0    # Y start on terrace 3
CAGE_WALL_THICK = 2.5
CAGE_SLOT_WIDTH = 2.6
CAGE_BAR_WIDTH = 2.0

# Right-hand Ribbed Tower / Accordion Column
TOWER_POS_X = 70.0
TOWER_POS_Y = 50.0
TOWER_WIDTH = 25.0
TOWER_DEPTH = 45.0
TOWER_HEIGHT = 56.0

# Rear Wall Connection
REAR_WALL_POS_X = 42.0
REAR_WALL_POS_Y = 75.0
REAR_WALL_WIDTH = 28.0
REAR_WALL_DEPTH = 20.0
REAR_WALL_HEIGHT = 36.0


@model
def perspective_grid_cage():
    """Builds the monolithic 3D solid model of the perspective grid and cage sculpture."""
    with bd.BuildPart() as p:
        # 1. Base Plate Floor
        bd.Box(
            BASE_WIDTH,
            BASE_DEPTH,
            BASE_HEIGHT,
            align=(bd.Align.MIN, bd.Align.MIN, bd.Align.MIN),
        )

        # 2. Lower Terrace 1
        with bd.Locations((10.0, 15.0, BASE_HEIGHT)):
            bd.Box(
                45.0,
                35.0,
                TERRACE_1_HEIGHT - BASE_HEIGHT,
                align=(bd.Align.MIN, bd.Align.MIN, bd.Align.MIN),
                mode=bd.Mode.ADD,
            )

        # 3. Mid Terrace 2
        with bd.Locations((10.0, 35.0, TERRACE_1_HEIGHT)):
            bd.Box(
                40.0,
                35.0,
                TERRACE_2_HEIGHT - TERRACE_1_HEIGHT,
                align=(bd.Align.MIN, bd.Align.MIN, bd.Align.MIN),
                mode=bd.Mode.ADD,
            )

        # 4. High Terrace 3 (Cage Platform)
        with bd.Locations((10.0, 58.0, TERRACE_2_HEIGHT)):
            bd.Box(
                36.0,
                37.0,
                TERRACE_3_HEIGHT - TERRACE_2_HEIGHT,
                align=(bd.Align.MIN, bd.Align.MIN, bd.Align.MIN),
                mode=bd.Mode.ADD,
            )

        # 5. Right-Hand Ribbed Column / Tower
        with bd.Locations((TOWER_POS_X, TOWER_POS_Y, BASE_HEIGHT)):
            bd.Box(
                TOWER_WIDTH,
                TOWER_DEPTH,
                TOWER_HEIGHT - BASE_HEIGHT,
                align=(bd.Align.MIN, bd.Align.MIN, bd.Align.MIN),
                mode=bd.Mode.ADD,
            )

        # 6. Connecting Rear Wall
        with bd.Locations((REAR_WALL_POS_X, REAR_WALL_POS_Y, BASE_HEIGHT)):
            bd.Box(
                REAR_WALL_WIDTH,
                REAR_WALL_DEPTH,
                REAR_WALL_HEIGHT - BASE_HEIGHT,
                align=(bd.Align.MIN, bd.Align.MIN, bd.Align.MIN),
                mode=bd.Mode.ADD,
            )

        # 7. Cage Outer Shell
        with bd.Locations((CAGE_POS_X, CAGE_POS_Y, TERRACE_3_HEIGHT)):
            bd.Box(
                CAGE_WIDTH,
                CAGE_DEPTH,
                CAGE_HEIGHT,
                align=(bd.Align.MIN, bd.Align.MIN, bd.Align.MIN),
                mode=bd.Mode.ADD,
            )

        # 8. Hollow Cage Interior Cavity
        with bd.Locations((
            CAGE_POS_X + CAGE_WALL_THICK,
            CAGE_POS_Y + CAGE_WALL_THICK,
            TERRACE_3_HEIGHT + 2.0,
        )):
            bd.Box(
                CAGE_WIDTH - 2 * CAGE_WALL_THICK,
                CAGE_DEPTH - 2 * CAGE_WALL_THICK,
                CAGE_HEIGHT - 4.0,
                align=(bd.Align.MIN, bd.Align.MIN, bd.Align.MIN),
                mode=bd.Mode.SUBTRACT,
            )

        # 9. Slotted Cage Front Grille (Vertical Bars on Front Face Y = CAGE_POS_Y)
        # 4 vertical slot cutouts creating 5 vertical bar elements
        for i in range(4):
            slot_x = CAGE_POS_X + 2.5 + i * (CAGE_SLOT_WIDTH + CAGE_BAR_WIDTH)
            with bd.Locations((slot_x, CAGE_POS_Y - 1.0, TERRACE_3_HEIGHT + 3.0)):
                bd.Box(
                    CAGE_SLOT_WIDTH,
                    CAGE_WALL_THICK + 2.0,
                    CAGE_HEIGHT - 6.0,
                    align=(bd.Align.MIN, bd.Align.MIN, bd.Align.MIN),
                    mode=bd.Mode.SUBTRACT,
                )

        # 10. Slotted Cage Left Grille (Vertical Bars on Side Face X = CAGE_POS_X)
        # 2 vertical slot cutouts on the side
        for j in range(2):
            slot_y = CAGE_POS_Y + 3.5 + j * (CAGE_SLOT_WIDTH + 4.0)
            with bd.Locations((CAGE_POS_X - 1.0, slot_y, TERRACE_3_HEIGHT + 3.0)):
                bd.Box(
                    CAGE_WALL_THICK + 2.0,
                    CAGE_SLOT_WIDTH,
                    CAGE_HEIGHT - 6.0,
                    align=(bd.Align.MIN, bd.Align.MIN, bd.Align.MIN),
                    mode=bd.Mode.SUBTRACT,
                )

        # 11. Ribbed Grooves on Right Tower (Horizontal louvers / accordion folds)
        for r_z in [16.0, 24.0, 32.0, 40.0, 48.0]:
            # Front face ribs of tower
            with bd.Locations((TOWER_POS_X - 0.5, TOWER_POS_Y - 0.5, r_z)):
                bd.Box(
                    TOWER_WIDTH + 1.0,
                    2.0,
                    2.5,
                    align=(bd.Align.MIN, bd.Align.MIN, bd.Align.MIN),
                    mode=bd.Mode.SUBTRACT,
                )
            # Right face ribs of tower
            with bd.Locations((TOWER_POS_X + TOWER_WIDTH - 1.5, TOWER_POS_Y - 0.5, r_z)):
                bd.Box(
                    2.5,
                    TOWER_DEPTH + 1.0,
                    2.5,
                    align=(bd.Align.MIN, bd.Align.MIN, bd.Align.MIN),
                    mode=bd.Mode.SUBTRACT,
                )

        # 12. Floor Grid Grooves (Engraved perspective floor pattern)
        for grid_y in [12.0, 24.0, 36.0, 48.0]:
            with bd.Locations((50.0, grid_y, BASE_HEIGHT - 0.8)):
                bd.Box(
                    48.0,
                    1.2,
                    1.0,
                    align=(bd.Align.MIN, bd.Align.CENTER, bd.Align.MIN),
                    mode=bd.Mode.SUBTRACT,
                )

        for grid_x in [58.0, 70.0, 82.0, 94.0]:
            with bd.Locations((grid_x, 3.0, BASE_HEIGHT - 0.8)):
                bd.Box(
                    1.2,
                    46.0,
                    1.0,
                    align=(bd.Align.CENTER, bd.Align.MIN, bd.Align.MIN),
                    mode=bd.Mode.SUBTRACT,
                )

    solid = p.part
    solid.label = "perspective_grid_cage"
    solid.color = "#3a6073"
    return solid


if __name__ == "__main__":
    perspective_grid_cage()
