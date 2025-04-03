import PySide6.QtWidgets
import PySide6.QtCore
import PySide6.QtGui

from ..abstract.tables import Align, TextStyle, Renderer, AbstractTable
from .widgets import _Widget, _rgb2hex

_UNCHECKED_BOX_SYMBOL = '\u2610'
_CHECKED_BOX_SYMBOL = '\u2611'


class _GridTable(PySide6.QtCore.QAbstractTableModel):
    """Class defining the table model whose data is used to fill the table."""

    def __init__(self, get_row_count, get_column_count, get_data, get_header_data):
        """
        Initialize the grid table, linking the table functions (which in turn are linked to the user-defined functions)
        to the grid table.

        :param get_row_count: function providing the number of rows of the table
        :param get_column_count:  function providing the number of columns of the table
        :param get_data: function providing the data of the table
        :param get_header_data: function providing the data of the table header
        """
        super().__init__()
        self.rowCount = get_row_count
        self.columnCount = get_column_count
        self.data = get_data
        self.headerData = get_header_data


class _TableHeader(PySide6.QtWidgets.QHeaderView):
    """Class defining the header of the table."""

    def mousePressEvent(self, event):
        """Manage the mouse press event on the table header.

        :param event: the mouse event object
        """
        button = event.button()
        index = self.logicalIndexAt(event.pos())
        if self.orientation() is PySide6.QtGui.Qt.Horizontal:
            row = -1
            col = index
        else:
            row = index
            col = -1
        if button is PySide6.QtCore.Qt.LeftButton:
            self.parent().on_header_left_click(self.parent(), row, col)
        elif button is PySide6.QtCore.Qt.RightButton:
            self.parent().on_header_right_click(self.parent(), row, col)

    def mouseDoubleClickEvent(self, event):
        """Manage the mouse double click event on the table header.

        :param event: the mouse event object
        """
        button = event.button()
        index = self.indexAt(event.pos())
        row = index.row()
        col = index.column()
        if button is PySide6.QtCore.Qt.LeftButton:
            self.parent().on_header_left_double_click(self.parent(), row, col)
        elif button is PySide6.QtCore.Qt.RightButton:
            self.parent().on_header_right_double_click(self.parent(), row, col)


class Table(AbstractTable, _Widget, PySide6.QtWidgets.QTableView):
    """Table based on PySide6. A table is a widget used to display data in a two dimensional grid."""

    def __init__(self, **kwargs):
        """Initialize the table.

        :param kwargs: additional parameters for superclass
        """
        PySide6.QtWidgets.QTableView.__init__(self, kwargs['parent']._WindowClass__panel)
        super().__init__(**kwargs)
        self.setHorizontalHeader(_TableHeader(PySide6.QtGui.Qt.Horizontal, self))
        self.setVerticalHeader(_TableHeader(PySide6.QtGui.Qt.Vertical, self))

        self._qt_font = PySide6.QtGui.QFont('Helvetica', self._FONT_SIZE)
        self._qt_font_bold = PySide6.QtGui.QFont('Helvetica', self._FONT_SIZE)
        self._qt_font_bold.setBold(True)
        self._qt_font_italic = PySide6.QtGui.QFont('Helvetica', self._FONT_SIZE)
        self._qt_font_italic.setItalic(True)
        self._qt_font_bold_italic = PySide6.QtGui.QFont('Helvetica', self._FONT_SIZE)
        self._qt_font_bold_italic.setBold(True)
        self._qt_font_bold_italic.setItalic(True)

        self._font_dict = {
            TextStyle.NORMAL: self._qt_font,
            TextStyle.BOLD: self._qt_font_bold,
            TextStyle.ITALIC: self._qt_font_italic,
            TextStyle.BOLD_ITALIC: self._qt_font_bold_italic
        }

        self._align_dict = {
            Align.LEFT: int(PySide6.QtCore.Qt.AlignLeft | PySide6.QtCore.Qt.AlignVCenter),
            Align.CENTER: int(PySide6.QtCore.Qt.AlignCenter),
            Align.RIGHT: int(PySide6.QtCore.Qt.AlignRight | PySide6.QtCore.Qt.AlignVCenter),
        }
        self._grid_table = _GridTable(self._get_row_count, self._get_column_count,
                                      self._get_data, self._get_header_data)

        color_string = _rgb2hex(*self._get_header_color()[1])
        header_stylesheet = "::section{Background-color : %s}" % color_string
        self.horizontalHeader().setStyleSheet(header_stylesheet)
        self.verticalHeader().setStyleSheet(header_stylesheet)
        corner_stylesheet = "QTableCornerButton::section{Background-color : %s}" % color_string
        self.setStyleSheet(corner_stylesheet)
        self.setCornerButtonEnabled(False)

        self.horizontalHeader().setSectionResizeMode(PySide6.QtWidgets.QHeaderView.Fixed)
        self.verticalHeader().setSectionResizeMode(PySide6.QtWidgets.QHeaderView.Fixed)
        self.setSelectionMode(self.SelectionMode.NoSelection)
        self.setEditTriggers(self.EditTrigger.NoEditTriggers)
        self.setFocusPolicy(PySide6.QtCore.Qt.NoFocus)
        self.setSizePolicy(PySide6.QtWidgets.QSizePolicy.Minimum, PySide6.QtWidgets.QSizePolicy.Minimum)

    def _get_row_count(self, _index):
        """Return the number of rows by calling the user-defined function.

        :return: the number of rows of the table
        """
        return self._get_number_rows()

    def _get_column_count(self, _index):
        """Return the number of columns by calling the user-defined function.

        :return: the number of columns of the table
        """
        return self._get_number_cols()

    def _get_data(self, index, role):
        """
        Return different information used to fill the table; the cell is given by the index and the specific
        information to be provided as output depends on the role.

        :param index: object which allow to determine the cell whose data is required
        :param role: enum which determines the specific information to return (value, color, alignment, font)
        :return: the desired information for the specified cell
        """
        row = index.row()
        column = index.column()
        renderer = self._get_renderer(row, column)
        if role == PySide6.QtCore.Qt.DisplayRole:
            value = self._get_value(row, column)
            if renderer is Renderer.BOOLEAN:
                return (_UNCHECKED_BOX_SYMBOL, _CHECKED_BOX_SYMBOL)[bool(int(value))]
            else:
                return value
        elif role == PySide6.QtCore.Qt.FontRole:
            return self._font_dict[self._get_style(row, column)]
        elif role == PySide6.QtCore.Qt.ForegroundRole:
            return PySide6.QtGui.QColor.fromRgb(*self._get_color(row, column)[0])
        elif role == PySide6.QtCore.Qt.BackgroundRole:
            return PySide6.QtGui.QColor.fromRgb(*self._get_color(row, column)[1])
        elif role == PySide6.QtCore.Qt.TextAlignmentRole:
            if renderer is Renderer.BOOLEAN:
                return self._align_dict[Align.CENTER]
            else:
                return self._align_dict[self._get_align(row, column)]
        if renderer is Renderer.AUTO_WRAP:
            self._set_col_size(column, self._MAX_COL_WIDTH)

    def _get_header_data(self, index, orientation, role):
        """
        Return different information used to fill the table header; the cell is given by the index and the specific
        information to be provided as output depends on the role.

        :param index: index of the header cell whose data is required
        :param orientation: enum which determines if the desired header is the horizontal or the vertical one
        :param role: enum which determines the specific information to return (value, color, font)
        :return: the desired information for the specified header cell
        """
        if role == PySide6.QtCore.Qt.DisplayRole:
            if orientation == PySide6.QtCore.Qt.Horizontal:
                return self._get_col_header_value(index)
            elif orientation == PySide6.QtCore.Qt.Vertical:
                return self._get_row_header_value(index)
        elif role == PySide6.QtCore.Qt.FontRole:
            return self._qt_font_bold
        elif role == PySide6.QtCore.Qt.ForegroundRole:
            return PySide6.QtGui.QColor.fromRgb(*self._get_header_color()[0])

    def mousePressEvent(self, event):
        """Manage the mouse press event on the table.

        :param event: the mouse event object
        """
        button = event.button()
        index = self.indexAt(event.pos())
        row = index.row()
        col = index.column()
        if row == -1 or col == -1:
            return
        if button is PySide6.QtCore.Qt.LeftButton:
            self.on_cell_left_click(self, row, col)
        elif button is PySide6.QtCore.Qt.RightButton:
            self.on_cell_right_click(self, row, col)

    def mouseDoubleClickEvent(self, event):
        """Manage the mouse double click event on the table.

        :param event: the mouse event object
        """
        button = event.button()
        index = self.indexAt(event.pos())
        row = index.row()
        col = index.column()
        if row == -1 or col == -1:
            return
        if button is PySide6.QtCore.Qt.LeftButton:
            self.on_cell_left_double_click(self, row, col)
        elif button is PySide6.QtCore.Qt.RightButton:
            self.on_cell_right_double_click(self, row, col)

    def refresh(self):
        """Refresh the display of the table."""
        self.setModel(self._grid_table)
        self._grid_table.layoutChanged.emit()

        if self._hide_row_headers:
            self.verticalHeader().hide()
        elif not self._auto_size_row_headers:
            self.verticalHeader().setFixedWidth(self._ROW_HEADERS_WIDTH)
        if self._hide_col_headers:
            self.horizontalHeader().hide()
        elif not self._auto_size_col_headers:
            self.horizontalHeader().setFixedHeight(self._COL_HEADERS_HEIGHT)
        if self._auto_size_rows:
            self.resizeRowsToContents()
        else:
            self._set_row_sizes(self._ROW_HEIGHT)
        if self._col_widths is not None:
            self._set_frozen_cols_width()
        elif self._auto_size_cols:
            self.resizeColumnsToContents()
        else:
            self._set_row_sizes(self._COL_WIDTH)

        height = 0
        width = 0

        if self._AVOID_HORIZONTAL_SCROLL:
            self.setHorizontalScrollBarPolicy(PySide6.QtGui.Qt.ScrollBarAlwaysOff)
            width = self.horizontalHeader().length()
            if not self.verticalHeader().isHidden():
                width += self.verticalHeader().width()
            if self._MAXIMUM_WIDTH is not None and width > self._MAXIMUM_WIDTH:
                width = self._MAXIMUM_WIDTH
                self.setHorizontalScrollBarPolicy(PySide6.QtGui.Qt.ScrollBarAsNeeded)
                height += self.horizontalScrollBar().height()

        if self._AVOID_VERTICAL_SCROLL:
            self.setVerticalScrollBarPolicy(PySide6.QtGui.Qt.ScrollBarAlwaysOff)
            height = self.verticalHeader().length()
            if not self.horizontalHeader().isHidden():
                height += self.horizontalHeader().height()
            if self._MAXIMUM_HEIGHT is not None and height > self._MAXIMUM_HEIGHT:
                height = self._MAXIMUM_HEIGHT
                self.setVerticalScrollBarPolicy(PySide6.QtGui.Qt.ScrollBarAsNeeded)
                width += self.verticalScrollBar().width()

        if self._AVOID_HORIZONTAL_SCROLL:
            self.setFixedWidth(width)
        elif self._MAXIMUM_WIDTH is not None:
            self.setMaximumWidth(self._MAXIMUM_WIDTH)
        if self._MINIMUM_WIDTH is not None:
            self.setMinimumWidth(self._MAXIMUM_WIDTH)
        if self._AVOID_VERTICAL_SCROLL:
            self.setFixedHeight(height)
        elif self._MAXIMUM_HEIGHT is not None:
            self.setMaximumHeight(self._MAXIMUM_HEIGHT)
        if self._MINIMUM_HEIGHT is not None:
            self.setMinimumHeight(self._MINIMUM_HEIGHT)

    def _get_row_size(self, row):
        """Return the size (height) of a row.

        :param row: the index of the row
        :return: the size of the row
        """
        return self.rowHeight(row)

    def _get_col_size(self, col):
        """Return the size (width) of a column.

        :param row: the index of the column
        :return: the size of the column
        """
        return self.columnWidth(col)

    def _set_row_size(self, row, size):
        """Set the size (height) of a row to a specific value.

        :param row: the index of the row
        :param size: the desired new size of the row
        """
        self.setRowHeight(row, size)

    def _set_row_sizes(self, size):
        """Set the size (height) of all rows to a specific value.

        :param size: the desired new size of the rows
        """
        self.verticalHeader().setSectionResizeMode(self.verticalHeader().ResizeMode.Fixed)
        self.verticalHeader().setDefaultSectionSize(size)

    def _set_col_size(self, col, size):
        """Set the size (width) of a column to a specific value.

        :param col: the index of the column
        :param size: the desired new size of the column
        """
        self.setColumnWidth(col, size)

    def _set_col_sizes(self, size):
        """Set the size (width) of all columns to a specific value.

        :param size: the desired new size of the columns
        """
        self.horizontalHeader().setSectionResizeMode(self.horizontalHeader().ResizeMode.Fixed)
        self.horizontalHeader().setDefaultSectionSize(size)
