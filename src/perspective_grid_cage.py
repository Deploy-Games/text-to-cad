"""
Parametric 3D model of the tiled room corner from the hand sketch (21612.jpg).

Reading of the sketch (bird's-eye perspective into a corner):
- Tiled floor plate (10 mm grid) in the foreground
- Tall tiled back wall and right wall meeting in the rear-right corner
- Square pier standing proud of the right wall
- Staircase along the left side, climbing from the floor toward the back wall
- Small barred window box (the "cage") jutting out of the back wall above the stair head

Run: cad run src/perspective_grid_cage.py
"""

from __future__ import annotations

import build123d as bd
from cad import model

# --- Envelope (mm) ---
L = 120.0            # X width
D = 120.0            # Y depth
FLOOR_T = 4.0        # floor plate thickness
WALL_T = 10.0        # back / right wall thickness
WALL_H = 100.0       # wall height above floor top

# --- Tile grid ---
TILE = 10.0          # tile pitch
GROOVE_W = 0.8       # joint width
GROOVE_D = 0.6       # joint depth

# --- Staircase (left side, climbing toward the back wall) ---
STAIR_W = 50.0       # X width of the flight
STAIR_N = 7          # number of steps
STAIR_RISE = 10.0
STAIR_RUN = 10.0

# --- Pier on the right wall ---
PIER_W = 15.0        # projection from the right wall (X)
PIER_D = 25.0        # Y width
PIER_Y = 20.0        # Y start

# --- Barred window box on the back wall ---
CAGE_X = 10.0        # X start
CAGE_W = 22.0        # X width
CAGE_P = 14.0        # projection from the back wall (Y)
CAGE_Z = 82.0        # underside height above floor top
CAGE_H = 14.0        # height
CAGE_WALL = 2.0
CAGE_BARS = 4        # vertical bars across the open front
BAR_W = 1.6


@model
def perspective_grid_cage():
    """Tiled room corner: floor, two walls, pier, staircase and barred window box."""
    z0 = FLOOR_T                 # floor top
    wall_in_y = D - WALL_T       # inner face of back wall
    wall_in_x = L - WALL_T       # inner face of right wall

    def box(x, y, z, dx, dy, dz):
        return bd.Pos(x, y, z) * bd.Box(dx, dy, dz, align=(bd.Align.MIN,) * 3)

    # Floor, walls, pier
    part = box(0, 0, 0, L, D, FLOOR_T)
    part += box(0, wall_in_y, z0, L, WALL_T, WALL_H)
    part += box(wall_in_x, 0, z0, WALL_T, wall_in_y, WALL_H)
    part += box(wall_in_x - PIER_W, PIER_Y, z0, PIER_W, PIER_D, WALL_H)

    # Staircase: step i spans from its nosing back to the wall
    for i in range(STAIR_N):
        y_front = wall_in_y - STAIR_RUN * (STAIR_N - i)
        part += box(0, y_front, z0, STAIR_W, wall_in_y - y_front, STAIR_RISE * (i + 1))

    # Barred window box: solid block, hollowed, front opened, bars left standing
    cz = z0 + CAGE_Z
    cy = wall_in_y - CAGE_P
    part += box(CAGE_X, cy, cz, CAGE_W, CAGE_P, CAGE_H)
    part -= box(CAGE_X + CAGE_WALL, cy + CAGE_WALL, cz + CAGE_WALL,
                CAGE_W - 2 * CAGE_WALL, CAGE_P + 2.0, CAGE_H - 2 * CAGE_WALL)
    gap = (CAGE_W - 2 * CAGE_WALL - CAGE_BARS * BAR_W) / (CAGE_BARS + 1)
    open_x = CAGE_X + CAGE_WALL
    for k in range(CAGE_BARS + 1):
        x = open_x + k * (gap + BAR_W)
        part -= box(x, cy - 0.1, cz + CAGE_WALL, gap, CAGE_WALL + 0.2, CAGE_H - 2 * CAGE_WALL)

    # Tile joints: floor, back-wall face, right-wall face
    joints = []
    for i in range(1, int(L / TILE)):
        joints.append(box(i * TILE - GROOVE_W / 2, 0, z0 - GROOVE_D, GROOVE_W, wall_in_y, GROOVE_D))
        joints.append(box(i * TILE - GROOVE_W / 2, wall_in_y - GROOVE_D, z0, GROOVE_W, GROOVE_D, WALL_H))
    for j in range(1, int(D / TILE)):
        joints.append(box(0, j * TILE - GROOVE_W / 2, z0 - GROOVE_D, wall_in_x, GROOVE_W, GROOVE_D))
        joints.append(box(wall_in_x - GROOVE_D, j * TILE - GROOVE_W / 2, z0, GROOVE_D, GROOVE_W, WALL_H))
    for k in range(1, int(WALL_H / TILE)):
        joints.append(box(0, wall_in_y - GROOVE_D, z0 + k * TILE - GROOVE_W / 2, wall_in_x, GROOVE_D, GROOVE_W))
        joints.append(box(wall_in_x - GROOVE_D, 0, z0 + k * TILE - GROOVE_W / 2, GROOVE_D, wall_in_y, GROOVE_W))
    part -= bd.Compound(joints)

    solid = part.solid() if hasattr(part, "solid") else part
    solid.label = "perspective_grid_cage"
    solid.color = "#3a6073"
    return solid


if __name__ == "__main__":
    perspective_grid_cage()
