"""
Generator for DIN ISO Technical Drawings of Häcker Cutlery Trays (BE3056, BE4056, BE5056, BE6056).
Generates standalone vector PDF drawings and preview PNG images with all dimensions in cm.
Run: cad run scripts/generate_cutlery_drawings.py
"""

import os
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyArrowPatch, Rectangle, Polygon

# Ensure output directories exist
DRAWINGS_DIR = Path(__file__).resolve().parent.parent / "drawings"
SYNCTHING_DIR = Path("/home/tom/homeserver/infrastructure/syncthing/download/reports")
DRAWINGS_DIR.mkdir(parents=True, exist_ok=True)
if SYNCTHING_DIR.exists():
    OUT_DIRS = [DRAWINGS_DIR, SYNCTHING_DIR]
else:
    OUT_DIRS = [DRAWINGS_DIR]

# Common parameters (all in cm)
DEPTH = 48.0
HEIGHT = 5.6
WALL = 0.8
BOTTOM = 0.5
INNER_HEIGHT = HEIGHT - BOTTOM # 5.1 cm

MODELS = {
    "BE3056": {
        "title": "BESTECKEINSATZ BE3056 - KORPUS 30 CM",
        "model_no": "BE3056.2",
        "cabinet": "30 cm",
        "width": 21.0,
        "compartments": [
            {"id": "F1", "name": "Längsfach hinten links", "x": 0.8, "y": 21.2, "w": 9.3, "h": 26.0, "use": "Menügabeln"},
            {"id": "F2", "name": "Längsfach hinten rechts", "x": 10.9, "y": 21.2, "w": 9.3, "h": 26.0, "use": "Menümesser"},
            {"id": "F3", "name": "Querfach vorne mitte", "x": 0.8, "y": 11.0, "w": 19.4, "h": 9.4, "use": "Dessertbesteck / Kuchengabeln"},
            {"id": "F4", "name": "Querfach ganz vorne", "x": 0.8, "y": 0.8, "w": 19.4, "h": 9.4, "use": "Kaffeelöffel / Teelöffel"},
        ],
        "dim_x": [
            (0.8, 10.1, "9.3"),
            (10.9, 20.2, "9.3"),
        ],
        "dim_y": [
            (0.8, 10.2, "9.4"),
            (11.0, 20.4, "9.4"),
            (21.2, 47.2, "26.0"),
        ],
        "sec_walls": [10.1]
    },
    "BE4056": {
        "title": "BESTECKEINSATZ BE4056 - KORPUS 40 CM",
        "model_no": "BE4056.2",
        "cabinet": "40 cm",
        "width": 31.0,
        "compartments": [
            {"id": "F1", "name": "Längsfach hinten links", "x": 0.8, "y": 21.2, "w": 9.3, "h": 26.0, "use": "Menümesser"},
            {"id": "F2", "name": "Längsfach hinten mitte", "x": 10.9, "y": 21.2, "w": 9.3, "h": 26.0, "use": "Menügabeln"},
            {"id": "F3", "name": "Querfach vorne mitte-links", "x": 0.8, "y": 11.0, "w": 19.4, "h": 9.4, "use": "Suppen-/Dessertlöffel"},
            {"id": "F4", "name": "Querfach ganz vorne links", "x": 0.8, "y": 0.8, "w": 19.4, "h": 9.4, "use": "Kaffeelöffel / Kuchengabeln"},
            {"id": "F5", "name": "Längsfach rechts durchgehend", "x": 21.0, "y": 0.8, "w": 9.2, "h": 46.4, "use": "Kochbesteck / Kochlöffel / Schneidemesser"},
        ],
        "dim_x": [
            (0.8, 10.1, "9.3"),
            (10.9, 20.2, "9.3"),
            (21.0, 30.2, "9.2"),
        ],
        "dim_y": [
            (0.8, 10.2, "9.4"),
            (11.0, 20.4, "9.4"),
            (21.2, 47.2, "26.0"),
        ],
        "sec_walls": [10.1, 20.2]
    },
    "BE5056": {
        "title": "BESTECKEINSATZ BE5056 - KORPUS 50 CM",
        "model_no": "BE5056.2",
        "cabinet": "50 cm",
        "width": 41.0,
        "compartments": [
            {"id": "F1", "name": "Längsfach hinten links 1", "x": 0.8, "y": 21.2, "w": 9.25, "h": 26.0, "use": "Menümesser"},
            {"id": "F2", "name": "Längsfach hinten links 2", "x": 10.85, "y": 21.2, "w": 9.25, "h": 26.0, "use": "Menügabeln"},
            {"id": "F3", "name": "Querfach vorne mitte-links", "x": 0.8, "y": 11.0, "w": 19.3, "h": 9.4, "use": "Suppen-/Dessertlöffel"},
            {"id": "F4", "name": "Querfach ganz vorne links", "x": 0.8, "y": 0.8, "w": 19.3, "h": 9.4, "use": "Kaffeelöffel / Teelöffel"},
            {"id": "F5", "name": "Längsfach hinten mitte-rechts", "x": 20.9, "y": 21.2, "w": 9.25, "h": 26.0, "use": "Esslöffel / Servierbesteck"},
            {"id": "F6", "name": "Längsfach vorne mitte-rechts", "x": 20.9, "y": 0.8, "w": 9.25, "h": 19.6, "use": "Küchenhelfer / Sparschäler"},
            {"id": "F7", "name": "Längsfach rechts durchgehend", "x": 30.95, "y": 0.8, "w": 9.25, "h": 46.4, "use": "Kochbesteck / Schneidemesser"},
        ],
        "dim_x": [
            (0.8, 10.05, "9.25"),
            (10.85, 20.1, "9.25"),
            (20.9, 30.15, "9.25"),
            (30.95, 40.2, "9.25"),
        ],
        "dim_y": [
            (0.8, 10.2, "9.4"),
            (11.0, 20.4, "9.4"),
            (21.2, 47.2, "26.0"),
        ],
        "sec_walls": [10.05, 20.1, 30.15]
    },
    "BE6056": {
        "title": "BESTECKEINSATZ BE6056 - KORPUS 60 CM",
        "model_no": "BE6056.2",
        "cabinet": "60 cm",
        "width": 51.0,
        "compartments": [
            {"id": "F1", "name": "Längsfach hinten links 1", "x": 0.8, "y": 21.2, "w": 9.3, "h": 26.0, "use": "Menümesser"},
            {"id": "F2", "name": "Längsfach hinten links 2", "x": 10.9, "y": 21.2, "w": 9.3, "h": 26.0, "use": "Menügabeln"},
            {"id": "F3", "name": "Querfach vorne mitte-links", "x": 0.8, "y": 11.0, "w": 19.4, "h": 9.4, "use": "Dessertbesteck / Kuchengabeln"},
            {"id": "F4", "name": "Querfach ganz vorne links", "x": 0.8, "y": 0.8, "w": 19.4, "h": 9.4, "use": "Kaffeelöffel / Teelöffel"},
            {"id": "F5", "name": "Längsfach hinten mitte-rechts", "x": 21.0, "y": 21.2, "w": 14.2, "h": 26.0, "use": "Esslöffel / Servierlöffel"},
            {"id": "F6", "name": "Längsfach vorne mitte-rechts", "x": 21.0, "y": 0.8, "w": 14.2, "h": 19.6, "use": "Küchenzubehör / Schäler"},
            {"id": "F7", "name": "Großfach rechts durchgehend", "x": 36.0, "y": 0.8, "w": 14.2, "h": 46.4, "use": "Messerblock BME15 / Folienabroller BFA15"},
        ],
        "dim_x": [
            (0.8, 10.1, "9.3"),
            (10.9, 20.2, "9.3"),
            (21.0, 35.2, "14.2"),
            (36.0, 50.2, "14.2"),
        ],
        "dim_y": [
            (0.8, 10.2, "9.4"),
            (11.0, 20.4, "9.4"),
            (21.2, 47.2, "26.0"),
        ],
        "sec_walls": [10.1, 20.2, 35.2]
    }
}

def draw_dim_h(ax, x1, x2, y, text, offset=1.5, text_above=True, color="#003366", fontsize=7.5):
    """Draw a horizontal dimension line with extension lines and arrowheads."""
    yd = y + offset
    # Extension lines
    ax.plot([x1, x1], [y + (0.2 if offset > 0 else -0.2), yd + (0.3 if offset > 0 else -0.3)], color="#666666", lw=0.6)
    ax.plot([x2, x2], [y + (0.2 if offset > 0 else -0.2), yd + (0.3 if offset > 0 else -0.3)], color="#666666", lw=0.6)
    # Dimension line with double arrows
    ax.annotate("", xy=(x1, yd), xytext=(x2, yd),
                arrowprops=dict(arrowstyle="<->", color=color, lw=0.8, shrinkA=0, shrinkB=0))
    # Text
    ty = yd + (0.25 if text_above else -0.55)
    ax.text((x1 + x2)/2, ty, text, ha="center", va="bottom" if text_above else "top",
            color=color, fontsize=fontsize, fontweight="bold", backgroundcolor="white",
            bbox=dict(boxstyle="square,pad=0.1", fc="white", ec="none", alpha=0.9))

def draw_dim_v(ax, y1, y2, x, text, offset=1.5, text_left=True, color="#003366", fontsize=7.5):
    """Draw a vertical dimension line with extension lines and arrowheads."""
    xd = x + offset
    # Extension lines
    ax.plot([x + (0.2 if offset > 0 else -0.2), xd + (0.3 if offset > 0 else -0.3)], [y1, y1], color="#666666", lw=0.6)
    ax.plot([x + (0.2 if offset > 0 else -0.2), xd + (0.3 if offset > 0 else -0.3)], [y2, y2], color="#666666", lw=0.6)
    # Dimension line
    ax.annotate("", xy=(xd, y1), xytext=(xd, y2),
                arrowprops=dict(arrowstyle="<->", color=color, lw=0.8, shrinkA=0, shrinkB=0))
    # Text rotated
    tx = xd + (-0.25 if text_left else 0.25)
    ax.text(tx, (y1 + y2)/2, text, ha="right" if text_left else "left", va="center",
            color=color, fontsize=fontsize, fontweight="bold", rotation=90, backgroundcolor="white",
            bbox=dict(boxstyle="square,pad=0.1", fc="white", ec="none", alpha=0.9))

def generate_technical_drawing(key, data):
    """Renders a single professional DIN ISO technical drawing for the specified model."""
    fig = plt.figure(figsize=(11.69, 8.27), dpi=300) # DIN A4 landscape: 297 x 210 mm
    fig.patch.set_facecolor('white')

    # Main outer border and drawing frame (DIN ISO)
    ax_frame = fig.add_axes([0, 0, 1, 1])
    ax_frame.axis('off')
    # Sheet border (10 mm margin)
    ax_frame.add_patch(Rectangle((0.02, 0.02), 0.96, 0.96, fill=False, edgecolor="#111111", lw=1.5))
    # Inner border (20 mm left for binder, 10 mm others)
    ax_frame.add_patch(Rectangle((0.035, 0.035), 0.935, 0.93, fill=False, edgecolor="#222222", lw=0.8))

    # Grid reference ticks (A, B, C, D / 1, 2, 3, 4)
    for i, l in enumerate(["A", "B", "C", "D"]):
        ax_frame.text(0.027, 0.85 - i*0.23, l, fontsize=8, color="#555555", va="center", ha="center")
        ax_frame.text(0.975, 0.85 - i*0.23, l, fontsize=8, color="#555555", va="center", ha="center")
    for i in range(1, 7):
        ax_frame.text(0.08 + i*0.14, 0.973, str(i), fontsize=8, color="#555555", va="center", ha="center")
        ax_frame.text(0.08 + i*0.14, 0.027, str(i), fontsize=8, color="#555555", va="center", ha="center")

    # Title Banner
    ax_frame.text(0.05, 0.935, f"TECHNISCHE ZEICHNUNG — HÄCKER {data['title']}", fontsize=13, fontweight='bold', color="#111111")
    ax_frame.text(0.05, 0.918, f"Massivholz-Besteckeinsatz Esche dunkelgrau | Korpustiefe 560 mm (Nennmaß 480 mm) | Alle Maße in Zentimeter (cm)", fontsize=9, color="#444444")
    ax_frame.plot([0.05, 0.95], [0.91, 0.91], color="#222222", lw=0.8)

    # -------------------------------------------------------------
    # 1. DRAUFSICHT (TOP VIEW) - Print-friendly white line-art
    # -------------------------------------------------------------
    # Position: Left-center
    ax_top = fig.add_axes([0.07, 0.16, 0.44, 0.72])
    W = data["width"]
    D = DEPTH

    # Outer wooden rim (clean white background with sharp dark outline)
    ax_top.add_patch(Rectangle((0, 0), W, D, facecolor="white", edgecolor="#111111", lw=1.8, zorder=1))

    # Compartments cutout & labels (all white surfaces for ink-saving printing)
    for comp in data["compartments"]:
        ax_top.add_patch(Rectangle((comp["x"], comp["y"]), comp["w"], comp["h"],
                                   facecolor="white", edgecolor="#111111", lw=1.2, zorder=3))
        # Compartment ID & size label in high contrast black/dark gold
        cx = comp["x"] + comp["w"]/2
        cy = comp["y"] + comp["h"]/2
        ax_top.text(cx, cy + 1.3, comp["id"], color="#B8860B", fontsize=9.0, fontweight="bold", ha="center", va="center", zorder=5)
        w_str = f"{comp['w']:.2f}".rstrip('0').rstrip('.')
        ax_top.text(cx, cy - 0.2, f"{w_str} × {comp['h']:.1f} cm", color="#111111", fontsize=7.0 if comp['w'] < 10 else 7.5, fontweight="bold", ha="center", va="center", zorder=5)
        ax_top.text(cx, cy - 1.5, f"h={INNER_HEIGHT:.1f} cm", color="#555555", fontsize=6.2, ha="center", va="center", zorder=5)

    # Wall thickness markers (0.8 cm)
    ax_top.text(WALL/2, D/2, "0.8", color="#555555", fontsize=6.5, ha="center", va="center", rotation=90, zorder=6)
    ax_top.text(W - WALL/2, D/2, "0.8", color="#555555", fontsize=6.5, ha="center", va="center", rotation=90, zorder=6)
    ax_top.text(W/2, WALL/2, "0.8", color="#555555", fontsize=6.5, ha="center", va="center", zorder=6)
    ax_top.text(W/2, D - WALL/2, "0.8", color="#555555", fontsize=6.5, ha="center", va="center", zorder=6)

    # Dimension lines on Top View:
    # 1. Outer Dimensions (Outermost rows)
    draw_dim_h(ax_top, 0, W, D, f"GESAMTE BREITE: {W:.1f} cm", offset=4.5, text_above=True, color="#8B0000", fontsize=8.5)
    draw_dim_v(ax_top, 0, D, 0, f"GESAMTE TIEFE: {D:.1f} cm", offset=-4.5, text_left=True, color="#8B0000", fontsize=8.5)

    # 2. Inner Total Dimensions
    draw_dim_h(ax_top, WALL, W - WALL, D, f"Lichte Breite: {W - 2*WALL:.1f} cm", offset=2.2, text_above=True, color="#003366", fontsize=7.5)
    draw_dim_v(ax_top, WALL, D - WALL, 0, f"Lichte Tiefe: {D - 2*WALL:.1f} cm", offset=-2.2, text_left=True, color="#003366", fontsize=7.5)

    # 3. Individual compartment dimensions (X-axis at bottom)
    for x1, x2, txt in data["dim_x"]:
        draw_dim_h(ax_top, x1, x2, 0, f"{txt} cm", offset=-2.2, text_above=False, color="#005500", fontsize=7.0)

    # 4. Individual compartment dimensions (Y-axis on right)
    for y1, y2, txt in data["dim_y"]:
        draw_dim_v(ax_top, y1, y2, W, f"{txt} cm", offset=2.2, text_left=False, color="#005500", fontsize=7.0)

    # View Label
    ax_top.text(W/2, -5.8, "DRAUFSICHT (M 1:5)", fontsize=9.5, fontweight="bold", ha="center", va="center", color="#111111")
    ax_top.text(W/2, -7.0, "Blickrichtung senkrecht von oben in die Schublade", fontsize=7.5, ha="center", va="center", color="#555555")

    # Set axis limits with proper margins for dimension lines
    ax_top.set_xlim(-6.5, W + 4.5)
    ax_top.set_ylim(-8.5, D + 6.5)
    ax_top.set_aspect('equal')
    ax_top.axis('off')

    # -------------------------------------------------------------
    # 2. SCHNITT A-A & SEITENANSICHT (SECTION & HEIGHT PROFILE)
    # -------------------------------------------------------------
    # Position: Top-right quadrant
    ax_sec = fig.add_axes([0.56, 0.65, 0.39, 0.22])

    # Cross section along width (showing walls, base plate, cavity)
    ax_sec.text(0, HEIGHT + 3.0, "SCHNITT A-A / QUERSCHNITT (M 1:2.5)", fontsize=9.5, fontweight="bold", color="#111111")
    ax_sec.text(0, HEIGHT + 1.8, "Zeigt Wandstärke, Bodenplatte und nutzbare Innenhöhe", fontsize=7.5, color="#555555")

    # Draw solid base plate (5 mm = 0.5 cm) - hatched white
    ax_sec.add_patch(Rectangle((0, 0), W, BOTTOM, facecolor="white", edgecolor="#111111", hatch="///", lw=1.2))
    # Left outer wall
    ax_sec.add_patch(Rectangle((0, BOTTOM), WALL, HEIGHT - BOTTOM, facecolor="white", edgecolor="#111111", hatch="///", lw=1.2))
    # Right outer wall
    ax_sec.add_patch(Rectangle((W - WALL, BOTTOM), WALL, HEIGHT - BOTTOM, facecolor="white", edgecolor="#111111", hatch="///", lw=1.2))

    # Internal divider walls
    for wx in data.get("sec_walls", []):
        ax_sec.add_patch(Rectangle((wx, BOTTOM), 0.8, HEIGHT - BOTTOM, facecolor="white", edgecolor="#111111", hatch="///", lw=1.2))

    # Cavity fill
    ax_sec.add_patch(Rectangle((WALL, BOTTOM), W - 2*WALL, HEIGHT - BOTTOM, facecolor="white", edgecolor="none", zorder=0))

    # Dimensions on Section
    draw_dim_v(ax_sec, 0, HEIGHT, 0, f"Gesamthöhe: {HEIGHT:.1f} cm", offset=-2.2, text_left=True, color="#8B0000", fontsize=7.5)
    draw_dim_v(ax_sec, BOTTOM, HEIGHT, W/2, f"Innenhöhe: {INNER_HEIGHT:.1f} cm", offset=0, text_left=False, color="#003366", fontsize=7.5)
    draw_dim_v(ax_sec, 0, BOTTOM, W, f"Boden: {BOTTOM:.1f} cm", offset=1.5, text_left=False, color="#005500", fontsize=7.0)
    draw_dim_h(ax_sec, 0, WALL, HEIGHT, f"Wand: {WALL:.1f}", offset=0.8, text_above=True, color="#005500", fontsize=6.5)

    ax_sec.set_xlim(-4.5, W + 4.5)
    ax_sec.set_ylim(-1.5, HEIGHT + 4.0)
    ax_sec.set_aspect('equal')
    ax_sec.axis('off')

    # -------------------------------------------------------------
    # 3. FACH-TABELLE (COMPARTMENT SPECIFICATION TABLE)
    # -------------------------------------------------------------
    # Position: Middle-right
    ax_tbl = fig.add_axes([0.54, 0.29, 0.42, 0.35])
    ax_tbl.axis('off')

    col_labels = ["Fach", "Bezeichnung", "Breite", "Tiefe", "Höhe", "Fläche", "Empfohlene Nutzung"]
    table_data = []
    for c in data["compartments"]:
        area = c["w"] * c["h"]
        table_data.append([
            c["id"],
            c["name"],
            f"{c['w']:.2f}".rstrip('0').rstrip('.') + " cm",
            f"{c['h']:.1f} cm",
            f"{INNER_HEIGHT:.1f} cm",
            f"{area:.1f} cm²",
            c["use"]
        ])

    table = ax_tbl.table(
        cellText=table_data,
        colLabels=col_labels,
        loc='center',
        cellLoc='center',
        colColours=["#222222"] * len(col_labels)
    )
    table.auto_set_font_size(False)
    table.set_fontsize(6.8 if len(table_data) > 5 else 7.5)
    table.scale(1.0, 1.15 if len(table_data) > 5 else 1.35)

    # Style table header & alternating row colors
    for k, cell in table.get_celld().items():
        cell.set_edgecolor("#AAAAAA")
        cell.set_linewidth(0.6)
        if k[0] == 0:
            cell.set_text_props(weight='bold', color='#111111')
            cell.set_facecolor("#F0F0F0")
        else:
            cell.set_facecolor("#FFFFFF")
            # Highlight ID
            if k[1] == 0:
                cell.set_text_props(weight='bold', color='#8B0000')

    ax_tbl.text(0.5, 1.08, "DETAILLIERTE INNENMASSE & FACHEINTEILUNG", fontsize=9.5, fontweight="bold", ha="center", transform=ax_tbl.transAxes)

    # -------------------------------------------------------------
    # 4. DIN EN ISO 7200 SCHRIFTFELD (TITLE BLOCK)
    # -------------------------------------------------------------
    # Position: Bottom-right corner
    tb_x, tb_y, tb_w, tb_h = 0.55, 0.05, 0.40, 0.22
    ax_tb = fig.add_axes([tb_x, tb_y, tb_w, tb_h])
    ax_tb.axis('off')

    # Main outer rectangle of title block
    ax_tb.add_patch(Rectangle((0, 0), 1, 1, facecolor="#FAFAFA", edgecolor="#222222", lw=1.2))

    # Grid dividing lines
    ax_tb.plot([0, 1], [0.72, 0.72], color="#222222", lw=0.8)
    ax_tb.plot([0, 1], [0.44, 0.44], color="#222222", lw=0.8)
    ax_tb.plot([0, 1], [0.22, 0.22], color="#222222", lw=0.8)
    ax_tb.plot([0.5, 0.5], [0.22, 0.72], color="#222222", lw=0.8)
    ax_tb.plot([0.25, 0.25], [0, 0.22], color="#222222", lw=0.8)
    ax_tb.plot([0.5, 0.5], [0, 0.22], color="#222222", lw=0.8)
    ax_tb.plot([0.75, 0.75], [0, 0.22], color="#222222", lw=0.8)

    # Row 1: Title & Document Type
    ax_tb.text(0.03, 0.88, "BENENNUNG / TITEL", fontsize=6.5, color="#666666", va="top")
    ax_tb.text(0.03, 0.78, f"Häcker Besteckeinsatz {key} (Esche dunkelgrau)", fontsize=9.5, fontweight="bold", color="#111111", va="top")
    ax_tb.text(0.70, 0.88, "DOKUMENT-TYP", fontsize=6.5, color="#666666", va="top")
    ax_tb.text(0.70, 0.78, "Fertigungszeichnung", fontsize=8.5, fontweight="bold", color="#111111", va="top")

    # Row 2: Model & Material
    ax_tb.text(0.03, 0.64, "ARTIKELNUMMER / TYP", fontsize=6.5, color="#666666", va="top")
    ax_tb.text(0.03, 0.52, f"Häcker {data['model_no']}", fontsize=8.5, fontweight="bold", color="#111111", va="top")
    ax_tb.text(0.53, 0.64, "WERKSTOFF / MATERIAL", fontsize=6.5, color="#666666", va="top")
    ax_tb.text(0.53, 0.52, "Esche Massivholz, gebeizt/lackiert dunkelgrau", fontsize=7.5, color="#111111", va="top")

    # Row 3: Fit & Dimensions
    ax_tb.text(0.03, 0.36, "PASSEND FÜR KORPUSBREITE", fontsize=6.5, color="#666666", va="top")
    ax_tb.text(0.03, 0.26, f"{data['cabinet']} (Korpustiefe 560 mm)", fontsize=8.0, fontweight="bold", color="#005500", va="top")
    ax_tb.text(0.53, 0.36, "AUSSENMASSE (B × T × H)", fontsize=6.5, color="#666666", va="top")
    ax_tb.text(0.53, 0.26, f"{W:.1f} × {D:.1f} × {HEIGHT:.1f} cm", fontsize=8.0, fontweight="bold", color="#8B0000", va="top")

    # Row 4: Units, Scale, Sheet, Date
    ax_tb.text(0.03, 0.16, "EINHEIT", fontsize=6.0, color="#666666", va="top")
    ax_tb.text(0.03, 0.06, "cm (Zentimeter)", fontsize=7.5, fontweight="bold", color="#111111", va="top")

    ax_tb.text(0.28, 0.16, "MASSSTAB", fontsize=6.0, color="#666666", va="top")
    ax_tb.text(0.28, 0.06, "1:5 / 1:2.5", fontsize=7.5, color="#111111", va="top")

    ax_tb.text(0.53, 0.16, "PROJEKTION", fontsize=6.0, color="#666666", va="top")
    ax_tb.text(0.53, 0.06, "ISO 3rd Angle", fontsize=7.5, color="#111111", va="top")

    ax_tb.text(0.78, 0.16, "BLATT", fontsize=6.0, color="#666666", va="top")
    ax_tb.text(0.78, 0.06, f"1 von 1 (DIN A4)", fontsize=7.5, color="#111111", va="top")

    # Save to all target locations
    for out_dir in OUT_DIRS:
        pdf_path = out_dir / f"{key}_technische_zeichnung.pdf"
        png_path = out_dir / f"{key}_technische_zeichnung.png"
        fig.savefig(pdf_path, format="pdf", bbox_inches='tight')
        fig.savefig(png_path, format="png", dpi=200, bbox_inches='tight')
        print(f"Saved: {pdf_path}")
        print(f"Saved: {png_path}")

    plt.close(fig)

def main():
    print("Generating technical drawings for all 4 Häcker cutlery trays...")
    for key, data in MODELS.items():
        print(f"Processing {key}...")
        generate_technical_drawing(key, data)
    print("All technical drawings successfully generated!")

if __name__ == "__main__":
    main()
