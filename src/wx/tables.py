import wx.grid

from ..abstract.tables import Align, TextStyle, Renderer, AbstractTable
from .widgets import _Widget


class _GridTable(wx.grid.GridTableBase):
    """Class defining the table model whose data is used to fill the table."""

    def __init__(self, get_number_rows, get_number_cols,
                 get_value, get_row_header_value, get_col_header_value, get_attr):
        """
        Initialize the grid table, linking the table functions (which in turn are linked to the user-defined functions)
        to the grid table.

        :param get_number_rows: function providing the number of rows of the table
        :param get_number_cols:  function providing the number of columns of the table
        :param get_value: function providing the data value of the table
        :param get_row_header_value: function providing the data value of the table row header
        :param get_col_header_value: function providing the data value of the table column header
        :param get_attr: function providing the attribute to apply to the table
        """
        super().__init__()
        self.GetNumberRows = get_number_rows
        self.GetNumberCols = get_number_cols
        self.GetValue = get_value
        self.GetRowLabelValue = get_row_header_value
        self.GetColLabelValue = get_col_header_value
        self.GetAttr = get_attr


class Table(AbstractTable, _Widget, wx.grid.Grid):
    """Table based on wxPython. A table is a widget used to display data in a two dimensional grid."""

    def __init__(self, **kwargs):
        """Initialize the table.

        :param kwargs: additional parameters for superclass
        """
        super().__init__(**kwargs)
        wx.grid.Grid.__init__(self, kwargs['parent']._WindowClass__panel)
        self.SetLabelTextColour(wx.Colour(self._get_header_color()[0]))
        self.SetLabelBackgroundColour(wx.Colour(self._get_header_color()[1]))
        self._wx_font = wx.Font(wx.FontInfo(self._FONT_SIZE))
        self._wx_font_bold = wx.Font(wx.FontInfo(self._FONT_SIZE).Bold())
        self._wx_font_italic = wx.Font(wx.FontInfo(self._FONT_SIZE).Italic())
        self._wx_font_bold_italic = wx.Font(wx.FontInfo(self._FONT_SIZE).Bold().Italic())

        self._grid_table = _GridTable(self._get_number_rows, self._get_number_cols,
                                      self._get_value, self._get_row_header_value, self._get_col_header_value,
                                      self._get_attr)

        self.EnableEditing(False)
        self.EnableDragRowSize(False)
        self.EnableDragColSize(False)
        self.SetCellHighlightPenWidth(0)
        self.SetCellHighlightROPenWidth(0)

        self.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK, self._on_cell_left_click)
        self.Bind(wx.grid.EVT_GRID_CELL_LEFT_DCLICK, self._on_cell_left_double_click)
        self.Bind(wx.grid.EVT_GRID_CELL_RIGHT_CLICK, self._on_cell_right_click)
        self.Bind(wx.grid.EVT_GRID_CELL_RIGHT_DCLICK, self._on_cell_right_double_click)
        self.Bind(wx.grid.EVT_GRID_LABEL_LEFT_CLICK, self._on_label_left_click)
        self.Bind(wx.grid.EVT_GRID_LABEL_LEFT_DCLICK, self._on_label_left_double_click)
        self.Bind(wx.grid.EVT_GRID_LABEL_RIGHT_CLICK, self._on_label_right_click)
        self.Bind(wx.grid.EVT_GRID_LABEL_RIGHT_DCLICK, self._on_label_right_double_click)
        self.GetGridWindow().Bind(wx.EVT_MOTION, self._on_motion)

    def _on_cell_left_click(self, event):
        """Manage the left mouse click on a cell.

        :param event: the mouse event object
        """
        row = event.GetRow()
        col = event.GetCol()
        self.on_cell_left_click(self, row, col)

    def _on_cell_left_double_click(self, event):
        """Manage the left mouse double click on a cell.

        :param event: the mouse event object
        """
        row = event.GetRow()
        col = event.GetCol()
        self.on_cell_left_double_click(self, row, col)

    def _on_cell_right_click(self, event):
        """Manage the right mouse click on a cell.

        :param event: the mouse event object
        """
        row = event.GetRow()
        col = event.GetCol()
        self.on_cell_right_click(self, row, col)

    def _on_cell_right_double_click(self, event):
        """Manage the right mouse double click on a cell.

        :param event: the mouse event object
        """
        row = event.GetRow()
        col = event.GetCol()
        self.on_cell_right_double_click(self, row, col)

    def _on_label_left_click(self, event):
        """Manage the left mouse click on a header.

        :param event: the mouse event object
        """
        row = event.GetRow()
        col = event.GetCol()
        self.on_header_left_click(self, row, col)

    def _on_label_left_double_click(self, event):
        """Manage the left mouse double click on a header.

        :param event: the mouse event object
        """
        row = event.GetRow()
        col = event.GetCol()
        self.on_header_left_double_click(self, row, col)

    def _on_label_right_click(self, event):
        """Manage the right mouse click on a header.

        :param event: the mouse event object
        """
        row = event.GetRow()
        col = event.GetCol()
        self.on_header_right_click(self, row, col)

    def _on_label_right_double_click(self, event):
        """Manage the right mouse double click on a header.

        :param event: the mouse event object
        """
        row = event.GetRow()
        col = event.GetCol()
        self.on_header_right_double_click(self, row, col)

    def _on_motion(self, event):
        """Traps the motion event.

        :param event: the motion event
        """
        pass

    def refresh(self):
        """Refresh the display of the table."""
        self._refresh_attributes()
        self.BeginBatch()
        self.SetTable(self._grid_table, False)
        if self._hide_row_headers:
            self.HideRowLabels()
        elif self._auto_size_row_headers:
            self.SetRowLabelSize(wx.grid.GRID_AUTOSIZE)
        else:
            self.SetRowLabelSize(self._ROW_HEADERS_WIDTH)
        if self._hide_col_headers:
            self.HideColLabels()
        elif self._auto_size_col_headers:
            self.SetColLabelSize(wx.grid.GRID_AUTOSIZE)
        else:
            self.SetColLabelSize(self._COL_HEADERS_HEIGHT)
        if self._auto_size_rows:
            self.AutoSizeRows()
        else:
            self._set_row_sizes(self._ROW_HEIGHT)
        if self._col_widths is not None:
            self._set_frozen_cols_width()
        elif self._auto_size_cols:
            self.AutoSizeColumns()
        else:
            self._set_col_sizes(self._COL_WIDTH)
        if self._MINIMUM_HEIGHT is not None:
            self.SetMinSize(wx.Size(width=-1, height=self._MINIMUM_HEIGHT))
        if self._MAXIMUM_HEIGHT is not None:
            self.SetMaxSize(wx.Size(width=-1, height=self._MAXIMUM_HEIGHT))
        if self._MINIMUM_WIDTH is not None:
            self.SetMinSize(wx.Size(width=-1, height=self._MINIMUM_WIDTH))
        if self._MAXIMUM_WIDTH is not None:
            self.SetMaxSize(wx.Size(width=-1, height=self._MAXIMUM_WIDTH))
        self.EndBatch()

    def _refresh_attributes(self):
        """Refresh the attributes of the table."""
        for row in range(self._get_number_rows()):
            for col in range(self._get_number_cols()):
                self.RefreshAttr(row, col)

    def _get_attr(self, row, col, _kind):
        """Return the attribute to apply to a cell.

        :param row: the row of the cell
        :param col: the column of the cell
        :return: the attribute to apply to the cell
        """
        color = self._get_color(row, col)
        style = self._get_style(row, col)
        align = self._get_align(row, col)
        renderer = self._get_renderer(row, col)

        attr = wx.grid.GridCellAttr()
        attr.SetTextColour(wx.Colour(color[0]))
        attr.SetBackgroundColour(wx.Colour(color[1]))

        if style is TextStyle.BOLD:
            attr.SetFont(self._wx_font_bold)
        elif style is TextStyle.ITALIC:
            attr.SetFont(self._wx_font_italic)
        elif style is TextStyle.BOLD_ITALIC:
            attr.SetFont(self._wx_font_bold_italic)
        else:
            attr.SetFont(self._wx_font)

        if align is Align.RIGHT:
            attr.SetAlignment(wx.ALIGN_RIGHT, wx.ALIGN_CENTER)
        elif align is Align.LEFT:
            attr.SetAlignment(wx.ALIGN_LEFT, wx.ALIGN_CENTER)
        else:
            attr.SetAlignment(wx.ALIGN_CENTER, wx.ALIGN_CENTER)

        if renderer is Renderer.BOOLEAN:
            attr.SetRenderer(wx.grid.GridCellBoolRenderer())
            attr.SetAlignment(wx.ALIGN_CENTER, wx.ALIGN_CENTER)
        elif renderer is Renderer.AUTO_WRAP:
            attr.SetRenderer(wx.grid.GridCellAutoWrapStringRenderer())
            self._set_col_size(col, self._MAX_COL_WIDTH)
        return attr

    def _get_row_size(self, row):
        """Return the size (height) of a row.

        :param row: the index of the row
        :return: the size of the row
        """
        return self.GetRowSize(row)

    def _get_col_size(self, col):
        """Return the size (width) of a column.

        :param row: the index of the column
        :return: the size of the column
        """
        return self.GetColSize(col)

    def _set_row_size(self, row, size):
        """Set the size (height) of a row to a specific value.

        :param row: the index of the row
        :param size: the desired new size of the row
        """
        self.SetRowSize(row, size)

    def _set_row_sizes(self, size):
        """Set the size (height) of all rows to a specific value.

        :param size: the desired new size of the rows
        """
        row_sizes = wx.grid.GridSizesInfo()
        row_sizes.m_sizeDefault = size
        self.SetRowSizes(row_sizes)

    def _set_col_size(self, col, size):
        """Set the size (width) of a column to a specific value.

        :param col: the index of the column
        :param size: the desired new size of the column
        """
        self.SetColSize(col, size)

    def _set_col_sizes(self, size):
        """Set the size (width) of all columns to a specific value.

        :param size: the desired new size of the columns
        """
        col_sizes = wx.grid.GridSizesInfo()
        col_sizes.m_sizeDefault = size
        self.SetColSizes(col_sizes)
