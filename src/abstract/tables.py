"""
Definition of the abstract table class; a table is a complex widget used to display information in a two dimensional
grid, supporting different colors, rendering and alignment of the content.
The details of the implementation for each supported GUI type are defined in the concrete subclasses.

Classes:
    Align: enumeration used to define the alignement of the content in the table
    Renderer enumeration used to define the renderer used to show the content in the table
    AbstractTable: superclass for the table classes (not to be instantiated)
"""
from enum import Enum, auto

from .widgets import AbstractWidget, TextStyle


class Align(Enum):
    """Enum class defining the supported alignments."""
    LEFT = auto()
    CENTER = auto()
    RIGHT = auto()


class Renderer(Enum):
    """Enum class defining the supported renderers."""
    NORMAL = auto()
    BOOLEAN = auto()
    AUTO_WRAP = auto()


class AbstractTable(AbstractWidget):
    """
    Base class for Table. This class should not be instantiated.
    A table is a widget used to display data in a two dimensional grid.
    """

    _hide_row_headers = False
    _hide_col_headers = False
    _auto_size_rows = False
    _auto_size_cols = False
    _auto_size_row_headers = False
    _auto_size_col_headers = False
    _MAXIMUM_HEIGHT = None
    _MAXIMUM_WIDTH = None
    _MINIMUM_HEIGHT = None
    _MINIMUM_WIDTH = None
    _FONT_SIZE = 10
    _ROW_HEIGHT = 22
    _ROW_HEADERS_WIDTH = 80
    _COL_WIDTH = 80
    _COL_HEADERS_HEIGHT = 32
    _MAX_COL_WIDTH = 400
    # COLOR FOR TABLE ROWS: [foreground, background]
    _NORMAL_COLOR = [(0, 0, 0), (255, 255, 255)]
    _NORMAL_HEADER_COLOR = [(0, 0, 0), (240, 240, 240)]
    _AVOID_HORIZONTAL_SCROLL = False
    _AVOID_VERTICAL_SCROLL = False

    def __init__(self, **kwargs):
        """Initialize the table.

        :param kwargs: additional parameters for the superclass
        """
        self._col_widths = None
        super().__init__(**kwargs)

    def on_cell_left_click(self, obj, row, col):
        """User-defined function executed when a left click is performed on a cell.

        :param obj: the table object on which the left click was performed
        :param row: the row of the cell where the left click was performed (0-based)
        :param col: the column of the cell where the left click was performed (0-based)
        """
        pass

    def on_cell_left_double_click(self, obj, row, col):
        """User-defined function executed when a left double click is performed on a cell.

        :param obj: the table object on which the left double click was performed
        :param row: the row of the cell where the left double click was performed (0-based)
        :param col: the column of the cell where the left double click was performed (0-based)
        """
        pass

    def on_cell_right_click(self, obj, row, col):
        """User-defined function executed when a right click is performed on a cell.

        :param obj: the table object on which the right click was performed
        :param row: the row of the cell where the right click was performed (0-based)
        :param col: the column of the cell where the right click was performed (0-based)
        """
        pass

    def on_cell_right_double_click(self, obj, row, col):
        """User-defined function executed when a right double click is performed on a cell.

        :param obj: the table object on which the right double click was performed
        :param row: the row of the cell where the right double click was performed (0-based)
        :param col: the column of the cell where the right double click was performed (0-based)
        """
        pass

    def on_header_left_click(self, obj, row, col):
        """User-defined function executed when a left click is performed on a header.

        :param obj: the table object on which the left click was performed
        :param row: the row of the header where the left click was performed (0-based, -1 for a column header)
        :param col: the column of the header where the left  click was performed (0-based, -1 for a row header)
        """
        pass

    def on_header_left_double_click(self, obj, row, col):
        """User-defined function executed when a left double click is performed on a header.

        :param obj: the table object on which the left double click was performed
        :param row: the row of the header where the left double click was performed (0-based, -1 for a column header)
        :param col: the column of the header where the left double  click was performed (0-based, -1 for a row header)
        """
        pass

    def on_header_right_click(self, obj, row, col):
        """User-defined function executed when a right click is performed on a header.

        :param obj: the table object on which the right click was performed
        :param row: the row of the header where the right click was performed (0-based, -1 for a column header)
        :param col: the column of the header where the right  click was performed (0-based, -1 for a row header)
        """
        pass

    def on_header_right_double_click(self, obj, row, col):
        """User-defined function executed when a right double click is performed on a header.

        :param obj: the table object on which the right double click was performed
        :param row: the row of the header where the right double click was performed (0-based, -1 for a column header)
        :param col: the column of the header where the right double  click was performed (0-based, -1 for a row header)
        """
        pass

    def freeze_cols_width(self):
        """Freeze the width of all columns of the table to the current value."""
        self._col_widths = []
        for col in range(self._get_number_cols()):
            self._col_widths.append(self._get_col_size(col))

    def set_cols_width_as(self, other_table):
        """Set the width of all columns of the table equal to the corresponding columns of another table."""
        self._col_widths = []
        for col in range(other_table._get_number_cols()):
            self._col_widths.append(other_table._get_col_size(col))

    def unfreeze_cols_width(self):
        """Unfreeze the width of all columns of the table allowing resizing."""
        self._col_widths = None

    def refresh(self):
        """Refresh the content of the table after a change of the table data."""
        raise NotImplementedError

    def _get_number_rows(self):
        """User-defined function. Return the number of rows that the table should display.

        :return: the number of rows of the table
        """
        raise NotImplementedError

    def _get_number_cols(self):
        """User-defined function. Return the number of columns that the table should display.

        :return: the number of columns of the table
        """
        raise NotImplementedError

    def _get_value(self, row, col):
        """User-defined function. Return the value to be displayed in a cell of the table.

        :param row: the row of the cell (0-based)
        :param col: the column of the cell (0-based)
        :return: the value to be displayed in the cell
        """
        raise NotImplementedError

    def _get_row_header_value(self, row):
        """User-defined function. Return the value to be displayed in a row header of the table.

        :param row: the row of the header (0-based)
        :return: the value to be displayed in the header
        """
        return ""

    def _get_col_header_value(self, col):
        """User-defined function. Return the value to be displayed in a column header of the table.

        :param col: the column of the header (0-based)
        :return: the value to be displayed in the header
        """
        return ""

    def _get_color(self, row, col):
        """
        Default implementation, to be overridden by user-defined function if desired.
        Return the color to be used for a cell, as a two-element tuple of RGB values (for foreground and background).
        Each RGB value is a three-element tuple of integer values for red, green and blue between 0 and 255.

        :param row: the row of the cell (0-based)
        :param col: the column of the cell (0-based)
        :return: the two-element tuple of RGB values (for foreground and background)
        """
        return self._NORMAL_COLOR

    def _get_row_color(self, row):
        """
        Default implementation, to be overridden by user-defined function if desired.
        Only used by GUI which don't support different colors for cells in the same row.
        Return the color to be used for a cell, as a two-element tuple of RGB values (for foreground and background).
        Each RGB value is a three-element tuple of integer values for red, green and blue between 0 and 255.

        :param row: the row of the cell (0-based)
        :return: the two-element tuple of RGB values (for foreground and background)
        """
        return self._get_color(row, 0)

    def _get_header_color(self):
        """
        Default implementation, to be overridden by user-defined function if desired.
        Return the color to be used for a the headers.
        Each RGB value is a three-element tuple of integer values for red, green and blue between 0 and 255.

        :return: the two-element tuple of RGB values (for foreground and background)
        """
        return self._NORMAL_HEADER_COLOR

    def _get_style(self, row, col):
        """
        Default implementation, to be overridden by user-defined function if desired.
        Return the style to be used for a cell as a TextStyle enum.

        :param row: the row of the cell (0-based)
        :param col: the column of the cell (0-based)
        :return: the style to be used for the cell as a TextStyle enum
        """
        return TextStyle.NORMAL

    def _get_align(self, row, col):
        """
        Default implementation, to be overridden by user-defined function if desired.
        Return the alignment to be used for a cell as an Align enum.

        :param row: the row of the cell (0-based)
        :param col: the column of the cell (0-based)
        :return: the alignment to be used for a cell as an Align enum
        """
        return Align.LEFT

    def _get_renderer(self, row, col):
        """
        Default implementation, to be overridden by user-defined function if desired.
        Return the renderer to be used for a cell as a Renderer enum.

        :param row: the row of the cell (0-based)
        :param col: the column of the cell (0-based)
        :return: the renderer to be used for a cell as a Renderer enum
        """
        return Renderer.NORMAL

    def _get_row_size(self, row):
        """Return the size (height) of a row.

        :param row: the index of the row
        :return: the size of the row
        """
        raise NotImplementedError

    def _get_col_size(self, col):
        """Return the size (width) of a column.

        :param row: the index of the column
        :return: the size of the column
        """
        raise NotImplementedError

    def _set_row_size(self, row, size):
        """Set the size (height) of a row to a specific value.

        :param row: the index of the row
        :param size: the desired new size of the row
        """
        raise NotImplementedError

    def _set_row_sizes(self, size):
        """Set the size (height) of all rows to a specific value.

        :param size: the desired new size of the rows
        """
        raise NotImplementedError

    def _set_col_size(self, col, size):
        """Set the size (width) of a column to a specific value.

        :param col: the index of the column
        :param size: the desired new size of the column
        """
        raise NotImplementedError

    def _set_col_sizes(self, size):
        """Set the size (width) of all columns to a specific value.

        :param size: the desired new size of the columns
        """
        raise NotImplementedError

    def _set_frozen_cols_width(self):
        """Applies the frozen width to each column (as saved at the moment when the freeze was commanded)."""
        if self._col_widths is not None:
            for col in range(self._get_number_cols()):
                self._set_col_size(col, self._col_widths[col])
