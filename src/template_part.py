"""
Starter template for parametric CAD models using build123d.
Run: cad run src/template_part.py
"""

import build123d as bd
from cad import model

# 1. Define parametric dimensions (mm)
LENGTH = 100.0
WIDTH = 60.0
HEIGHT = 20.0
HOLE_DIAMETER = 8.5
WALL_THICKNESS = 3.0


@model
def template_part():
    """Builds a parametric solid model."""
    with bd.BuildPart() as p:
        # Base body
        bd.Box(LENGTH, WIDTH, HEIGHT)

        # Center bore / cutout
        with bd.Locations((0, 0, 0)):
            bd.Cylinder(radius=HOLE_DIAMETER / 2, height=HEIGHT, mode=bd.Mode.SUBTRACT)

        # Fillet top edges
        top_edges = p.edges().filter_by(bd.Axis.Z, reverse=True)
        # bd.fillet(top_edges, radius=2.0)

    part = p.part
    part.label = "template_part"
    return part


if __name__ == "__main__":
    template_part()
