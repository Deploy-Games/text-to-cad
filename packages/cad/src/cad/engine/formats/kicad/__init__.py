"""KiCad board files: read-only parsing and plot geometry, never a live model or cache."""

from cad.engine.errors import UserError

PLOT_SCHEMA_VERSION = 3
PLOT_SUFFIXES = (".kicad_pcb",)


class PlotError(UserError, ValueError):
    """A file that could not be read as a KiCad board."""
