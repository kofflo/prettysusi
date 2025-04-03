"""
Definition of the abstract layout classes supported by the library: box layout (vertical and horizontal)
and grid layout.
The details of the implementation for each supported layout type are defined in the concrete subclasses.

Classes:
    Align: enumeration used to define the alignement of the content in the layout
    AbstractBoxLayout: superclass for the box layout classes (not to be instantiated)
    AbstractGridLayout: superclass for the grid layout classes (not to be instantiated)
"""
from enum import Flag, auto

from .. import BaseClass


class Align(Flag):
    """Enum class defining the supported alignments."""
    LEFT = auto()
    HCENTER = auto()
    RIGHT = auto()
    TOP = auto()
    VCENTER = auto()
    BOTTOM = auto()
    START = LEFT | TOP
    CENTER = HCENTER | VCENTER
    END = RIGHT | BOTTOM
    EXPAND = auto()


class _AbstractLayout(BaseClass):
    """Superclass for all types of layout classes (box layouts and grid layout)."""

    def _create_layout(self, window):
        """Create the layout object (concrete implementation depends on the specific GUI).

        :param window: the window object to which the layout is applied
        :return: the layout object (GUI-specific)
        """
        raise NotImplementedError()


class AbstractBoxLayout(_AbstractLayout):
    """
    Base class for VBoxLayout and HBoxLayout. This class should not be instantiated.
    A box layout displays its content in a single column (vertical box layout) or row (horizontal box layout).
    """

    def __init__(self):
        """Initialize the box layout."""
        self._widgets = []

    def add(self, widget, *, align=Align.START, border=0, stretch=0):
        """Add a widget to the box layout, positioning it after all the already added widgets.

        :param widget: the widget to add
        :param align: the desired alignment of the widget in its space
        :param border: the size of the border to be applied around the widget (single value for a uniform border or
        a tuple of four values: top right bottom left)
        :param stretch: the weight of the stretch to be applied to the cell where the widget is placed
        """
        self._widgets.append({'type': widget, 'align': align, 'border': border, 'stretch': stretch})

    def add_space(self, space):
        """Add a space of the specified size to the box layout, positioning it after all the already added widgets.

        :param space: the size of the space to add
        """
        self._widgets.append({'type': 'space', 'space': space})

    def add_stretch(self, stretch=1):
        """Add a cell with a stretch of the specified weight to the box layout, after all the already added widgets.

        :param stretch: the weight of the stretch
        """
        self._widgets.append({'type': 'stretch', 'stretch': stretch})


class AbstractGridLayout(_AbstractLayout):
    """
    Base class for GridLayout. This class should not be instantiated.
    A grid layout displays its content in a two dimensional table with fixed dimensions.
    """

    def __init__(self, *, rows, cols, vgap, hgap):
        """Initialize the grid layout.

        :param rows: number of rows of the layout
        :param cols: number of columns of the layout
        :param vgap: vertical gap between the rows
        :param hgap: horizontal gap between the columns
        """
        self._rows = rows
        self._cols = cols
        self._widgets = [[None] * self._cols for _ in range(self._rows)]
        self._row_stretch = [None] * self._rows
        self._col_stretch = [None] * self._cols
        self._vgap = vgap
        self._hgap = hgap

    def add(self, widget, *, row, col, align=Align.CENTER, border=0):
        """Add a widget to the grid layout in the cell corresponding to the specified row and column.

        :param widget: the widget to add
        :param row: the row of the cell where the widget is added
        :param col: the column of the cell where the widget is added
        :param align: the desired alignment of the widget in its space
        :param border: the size of the border to be applied around the widget (single value for a uniform border or
        a tuple of four values: top right bottom left)
        """
        self._widgets[row][col] = {'type': widget, 'align': align, 'border': border}

    def add_space(self, *, row, col, width, height):
        """
        Add a space of the specified width and height to the grid layout in the cell corresponding to the specified
        row and column.

        :param row: the row of the cell where the widget is added
        :param col: the column of the cell where the widget is added
        :param width: the width of the space to add
        :param height: the height of the space to add
        """
        self._widgets[row][col] = {'type': 'space', 'width': width, 'height': height}

    def row_stretch(self, *, row, stretch):
        """Define the weight of the stretch for the specified row.

        :param row: the row to which the stretch is applied
        :param stretch: the weight of the stretch
        """
        self._row_stretch[row] = stretch

    def col_stretch(self, *, col, stretch):
        """Define the weight of the stretch for the specified column.

        :param col: the column to which the stretch is applied
        :param stretch: the weight of the stretch
        """
        self._col_stretch[col] = stretch
