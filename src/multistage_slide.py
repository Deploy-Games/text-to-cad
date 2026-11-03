"""
Parametric CAD model of the multi-stage slide / layout mechanism from hand sketch.
Run: cad run src/multistage_slide.py
"""

import build123d as bd
from cad import model

# 1. Nominal Dimensions derived from the 5mm grid sketch
GRID = 5.0  # 1 grid square = 5 mm

# Left Guide Rail / Partition
RAIL_WIDTH = 2 * GRID       # 10.0 mm
RAIL_LENGTH = 25 * GRID     # 125.0 mm
RAIL_HEIGHT = 15.0          # 15.0 mm

# Upper Offset Sub-Rail
UPPER_RAIL_WIDTH = 2 * GRID   # 10.0 mm
UPPER_RAIL_LENGTH = 7 * GRID  # 35.0 mm
UPPER_RAIL_OFFSET_X = 6.5 * GRID  # 32.5 mm

# Stage 1 (Lower Central Carriage / Table)
STAGE1_WIDTH = 10.5 * GRID   # 52.5 mm
STAGE1_LENGTH = 15.5 * GRID  # 77.5 mm
STAGE1_HEIGHT = 10.0         # 10.0 mm

# Stage 2 (Upper Central Carriage / Extension)
STAGE2_WIDTH = 7.0 * GRID    # 35.0 mm
STAGE2_LENGTH = 12.5 * GRID  # 62.5 mm
STAGE2_HEIGHT = 12.0         # 12.0 mm

# T-Guide Feature
T_STEM_WIDTH = 1.0 * GRID    # 5.0 mm
T_STEM_LENGTH = 4.0 * GRID   # 20.0 mm
T_HEAD_WIDTH = 3.0 * GRID    # 15.0 mm
T_HEAD_THICKNESS = 1.0 * GRID # 5.0 mm

# Top and Bottom Perimeter Guides
TOP_GUIDE_LENGTH = 22 * GRID  # 110.0 mm
TOP_GUIDE_WIDTH = 1.5 * GRID  # 7.5 mm
BOTTOM_GUIDE_LENGTH = 16 * GRID # 80.0 mm
BOTTOM_GUIDE_WIDTH = 2.0 * GRID # 10.0 mm

TOTAL_WIDTH = 180.0
TOTAL_LENGTH = 180.0


@model
def multistage_slide():
    """Builds the multi-stage mechanism / technical layout solid model."""
    with bd.BuildPart() as p:
        # Base plate / reference frame
        with bd.BuildSketch(bd.Plane.XY):
            # Left main rail
            bd.Rectangle(RAIL_WIDTH, RAIL_LENGTH, align=(bd.Align.CENTER, bd.Align.CENTER))
            
            # Upper offset rail
            with bd.Locations((UPPER_RAIL_OFFSET_X - RAIL_WIDTH / 2, (RAIL_LENGTH - UPPER_RAIL_LENGTH) / 2)):
                bd.Rectangle(UPPER_RAIL_WIDTH, UPPER_RAIL_LENGTH, align=(bd.Align.CENTER, bd.Align.CENTER))
            
            # Rail link bracket
            with bd.Locations(((UPPER_RAIL_OFFSET_X - RAIL_WIDTH) / 2, (RAIL_LENGTH - UPPER_RAIL_LENGTH) / 2 - UPPER_RAIL_LENGTH / 2 + GRID)):
                bd.Rectangle(UPPER_RAIL_OFFSET_X, 1.5 * GRID, align=(bd.Align.CENTER, bd.Align.CENTER))

            # Top perimeter guide
            with bd.Locations((TOP_GUIDE_LENGTH / 2 + GRID * 2, RAIL_LENGTH / 2 - GRID)):
                bd.Rectangle(TOP_GUIDE_LENGTH, TOP_GUIDE_WIDTH, align=(bd.Align.CENTER, bd.Align.CENTER))

            # Bottom perimeter stepped guide
            with bd.Locations((BOTTOM_GUIDE_LENGTH / 2 + GRID * 6, -RAIL_LENGTH / 2 + GRID * 2)):
                bd.Rectangle(BOTTOM_GUIDE_LENGTH, BOTTOM_GUIDE_WIDTH, align=(bd.Align.CENTER, bd.Align.CENTER))
                
        bd.extrude(amount=RAIL_HEIGHT)

        # Stage 1 Carriage (Lower Central)
        with bd.BuildSketch(bd.Plane.XY.offset(2.0)):
            with bd.Locations((STAGE1_WIDTH / 2 + RAIL_WIDTH / 2 + 1.0, -STAGE1_LENGTH / 4)):
                bd.Rectangle(STAGE1_WIDTH, STAGE1_LENGTH, align=(bd.Align.CENTER, bd.Align.CENTER))
        bd.extrude(amount=STAGE1_HEIGHT)

        # Stage 2 Carriage (Upper Central)
        with bd.BuildSketch(bd.Plane.XY.offset(4.0)):
            with bd.Locations((STAGE2_WIDTH / 2 + UPPER_RAIL_OFFSET_X - RAIL_WIDTH / 2, STAGE2_LENGTH / 2 + 5.0)):
                bd.Rectangle(STAGE2_WIDTH, STAGE2_LENGTH, align=(bd.Align.CENTER, bd.Align.CENTER))
        bd.extrude(amount=STAGE2_HEIGHT)

        # T-Slot Guide Interlock
        with bd.BuildSketch(bd.Plane.XY.offset(5.0)):
            with bd.Locations((RAIL_WIDTH / 2 + T_STEM_LENGTH / 2 - 2.0, 0)):
                bd.Rectangle(T_STEM_LENGTH, T_STEM_WIDTH, align=(bd.Align.CENTER, bd.Align.CENTER))
            with bd.Locations((RAIL_WIDTH / 2 + T_STEM_LENGTH, 0)):
                bd.Rectangle(T_HEAD_THICKNESS, T_HEAD_WIDTH, align=(bd.Align.CENTER, bd.Align.CENTER))
        bd.extrude(amount=8.0)

        # Mounting and Detent Bores (5mm dia standard)
        with bd.Locations(
            (0, RAIL_LENGTH / 2 - 3 * GRID, 0),
            (0, -RAIL_LENGTH / 2 + 3 * GRID, 0),
            (0, 0, 0),
            (UPPER_RAIL_OFFSET_X - RAIL_WIDTH / 2, RAIL_LENGTH / 2 - 2 * GRID, 0),
        ):
            bd.Cylinder(radius=2.5, height=RAIL_HEIGHT + 10, mode=bd.Mode.SUBTRACT)

    part = p.part
    part.label = "multistage_slide"
    return part


if __name__ == "__main__":
    multistage_slide()
