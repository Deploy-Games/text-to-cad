"""
Parametric CAD model of the partitioned storage frame / desk organizer
reconstructed from the user's hand sketch (1000095011.jpg).

Overall Dimensions:
- Length (X): 1600 mm (160 cm)
- Depth  (Y): 800 mm  (80 cm)
- Height (Z): 300 mm  (30 cm)

Compartments (Top view):
- Left full-depth bay: 400 x 800 mm
- Rear center-left bay: 600 x 400 mm
- Rear center-right bay: 200 x 400 mm
- Front center bay: 800 x 400 mm
- Rear right bay: 400 x 400 mm
- Front right bay: 400 x 400 mm

Run: cad run src/desk_storage_frame.py
"""

from __future__ import annotations

import build123d as bd
from cad import model

# --- Nominal Parametric Dimensions (mm) ---
OVERALL_LENGTH = 1600.0   # 160 cm
OVERALL_DEPTH = 800.0     # 80 cm
OVERALL_HEIGHT = 300.0    # 30 cm

WALL_THICKNESS = 18.0     # Standard 18 mm sheet / carcass panel thickness
BOTTOM_THICKNESS = 18.0   # 18 mm bottom base plate

# Divider Nominal Grid Positions (measured from bottom-left corner (0,0))
X_DIV_1 = 400.0           # Left bay boundary
X_DIV_2 = 1000.0          # 400 + 600: rear middle partition
X_DIV_3 = 1200.0          # 1000 + 200: right bay boundary
Y_DIV_1 = 400.0           # Horizontal center dividing wall (depth 400 mm)


@model
def desk_storage_frame():
    """Builds the 3D solid model of the partitioned storage frame."""
    pocket_depth = OVERALL_HEIGHT - BOTTOM_THICKNESS

    with bd.BuildPart() as p:
        # 1. Solid bounding block
        bd.Box(
            OVERALL_LENGTH,
            OVERALL_DEPTH,
            OVERALL_HEIGHT,
            align=(bd.Align.MIN, bd.Align.MIN, bd.Align.MIN),
        )

        # 2. Cut out the 6 interior compartments leaving uniform wall thickness
        # Compartment definitions: (x_min, x_max, y_min, y_max)
        compartments = [
            # 1. Left full-depth compartment (400 x 800 mm)
            (
                WALL_THICKNESS,
                X_DIV_1 - WALL_THICKNESS / 2.0,
                WALL_THICKNESS,
                OVERALL_DEPTH - WALL_THICKNESS,
            ),
            # 2. Rear center-left compartment (600 x 400 mm)
            (
                X_DIV_1 + WALL_THICKNESS / 2.0,
                X_DIV_2 - WALL_THICKNESS / 2.0,
                Y_DIV_1 + WALL_THICKNESS / 2.0,
                OVERALL_DEPTH - WALL_THICKNESS,
            ),
            # 3. Rear center-right compartment (200 x 400 mm)
            (
                X_DIV_2 + WALL_THICKNESS / 2.0,
                X_DIV_3 - WALL_THICKNESS / 2.0,
                Y_DIV_1 + WALL_THICKNESS / 2.0,
                OVERALL_DEPTH - WALL_THICKNESS,
            ),
            # 4. Front center compartment (800 x 400 mm)
            (
                X_DIV_1 + WALL_THICKNESS / 2.0,
                X_DIV_3 - WALL_THICKNESS / 2.0,
                WALL_THICKNESS,
                Y_DIV_1 - WALL_THICKNESS / 2.0,
            ),
            # 5. Rear right compartment (400 x 400 mm)
            (
                X_DIV_3 + WALL_THICKNESS / 2.0,
                OVERALL_LENGTH - WALL_THICKNESS,
                Y_DIV_1 + WALL_THICKNESS / 2.0,
                OVERALL_DEPTH - WALL_THICKNESS,
            ),
            # 6. Front right compartment (400 x 400 mm)
            (
                X_DIV_3 + WALL_THICKNESS / 2.0,
                OVERALL_LENGTH - WALL_THICKNESS,
                WALL_THICKNESS,
                Y_DIV_1 - WALL_THICKNESS / 2.0,
            ),
        ]

        for x1, x2, y1, y2 in compartments:
            w = x2 - x1
            d = y2 - y1
            cx = (x1 + x2) / 2.0
            cy = (y1 + y2) / 2.0
            cz = BOTTOM_THICKNESS + pocket_depth / 2.0

            with bd.Locations((cx, cy, cz)):
                bd.Box(
                    w,
                    d,
                    pocket_depth,
                    align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.CENTER),
                    mode=bd.Mode.SUBTRACT,
                )

    part = p.part
    part.label = "desk_storage_frame"
    return part


if __name__ == "__main__":
    desk_storage_frame()
