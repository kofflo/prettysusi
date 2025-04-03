import tkinter
import tkinter.ttk
import tkinter.font

from ..abstract.tables import Align, TextStyle, Renderer, AbstractTable
from .widgets import _Widget, _rgb2hex
from . import ttk_style

_UNCHECKED_BOX_SYMBOL = '\u2610'
_CHECKED_BOX_SYMBOL = '\u2611'


def _fixed_map(style, option):
    """Return the style map for an option with any styles starting with ("!disabled", "!selected", ...) filtered out.

    :param style: the ttk style
    :param option: the option for specific stlye map
    :return: the style map for the option with any styles starting with ("!disabled", "!selected", ...) filtered out
    """
    return [element for element in style.map("Treeview", query_opt=option) if element[:2] != ("!disabled", "!selected")]


class Table(AbstractTable, _Widget):
    """Table based on tkinter. A table is a widget used to display data in a two dimensional grid."""

    _FONT_FAMILY = 'Helvetica'
    _COL_WIDTH = 100
    _COL_HEADERS_HEIGHT = 42
    _MAX_COL_WIDTH = 600
    _MAX_ROW_HEADERS_WIDTH = 200
    _TABLE_ROWS_NUMBER = 10
    _FIXED_ROWS_NUMBER = True
    _AVOID_HORIZONTAL_SCROLL = False
    _AVOID_VERTICAL_SCROLL = False

    ttk_style.map("Treeview",
                  foreground=_fixed_map(ttk_style, "foreground"),
                  background=_fixed_map(ttk_style, "background"),
                  rowheight=_fixed_map(ttk_style, "rowheight"))

    def __init__(self, **kwargs):
        """Initialize the table.

        :param kwargs: additional parameters for superclass
        """
        super().__init__(**kwargs)
        self._row_ids = []

        self._tk_font = (self._FONT_FAMILY, self._FONT_SIZE)
        self._tk_font_bold = (self._FONT_FAMILY, self._FONT_SIZE, 'bold')
        self._tk_font_italic = (self._FONT_FAMILY, self._FONT_SIZE, 'italic')
        self._tk_font_bold_italic = (self._FONT_FAMILY, self._FONT_SIZE, 'bold italic')

        ttk_style.element_create(str(id(self)) + '.Treeheading.border', 'from', 'default')
        ttk_style.layout(
            str(id(self)) + '.Treeview.Heading', [
                (str(id(self)) + '.Treeheading.cell', {'sticky': 'nswe'}),
                (str(id(self)) + '.Treeheading.border', {
                    'sticky': 'nswe', 'children': [
                        (str(id(self)) + '.Treeheading.padding', {
                            'sticky': 'nswe', 'children': [
                                (str(id(self)) + '.Treeheading.image', {'side': 'right', 'sticky': ''}),
                                (str(id(self)) + '.Treeheading.text', {'sticky': 'we'})
                            ]
                        })
                    ]
                }),
            ]
        )
        ttk_style.configure(str(id(self)) + '.Treeview.Heading',
                            font=(self._FONT_FAMILY, self._FONT_SIZE, 'bold'),
                            padding=(self._COL_HEADERS_HEIGHT - self._ROW_HEIGHT) // 2,
                            foreground=_rgb2hex(*self._get_header_color()[0]),
                            background=_rgb2hex(*self._get_header_color()[1]))
        self._current_xview = None
        self._current_yview = None
        self._frame = None

    def hide(self, is_hidden):
        """Set the hidden status of the table. If hidden, the widget is not displayed.

        :param is_hidden: the new hidden status
        """
        super().hide(is_hidden)
        if self._widget is not None:
            if self._is_hidden:
                if not self._AVOID_HORIZONTAL_SCROLL:
                    self.xsb.grid_remove()
                if not self._AVOID_VERTICAL_SCROLL:
                    self.ysb.grid_remove()
            else:
                if not self._AVOID_HORIZONTAL_SCROLL:
                    self.xsb.grid()
                if not self._AVOID_VERTICAL_SCROLL:
                    self.ysb.grid()

    def _create_widget(self, rows_number):
        """Crete the Treeview widget which implements the table.

        :param rows_number: the number of rows
        """
        self._widget = tkinter.ttk.Treeview(self._frame, height=rows_number,
                                            selectmode="none", style=str(id(self)) + '.Treeview')
        self._widget.bind("<Button-1>", self._on_left_click)
        self._widget.bind("<ButtonRelease-1>", self._on_left_release)
        self._widget.bind("<Double-1>", self._on_left_double_click)
        self._widget.bind("<Button-3>", self._on_right_click)
        self._widget.bind("<Double-3>", self._on_right_double_click)
        self._widget.bind("<Motion>", self._on_motion)
        if not self._AVOID_HORIZONTAL_SCROLL:
            self.xsb = tkinter.ttk.Scrollbar(self._frame, orient='horizontal', command=self.xview)
            self.configure(xscrollcommand=self.xsb.set)
        if not self._AVOID_VERTICAL_SCROLL:
            self.ysb = tkinter.ttk.Scrollbar(self._frame, orient='vertical', command=self.yview)
            self.configure(yscrollcommand=self.ysb.set)

    def _set_frame(self, frame):
        """Create the table widget in the provided frame.

        :param frame: the frame where the table widget has to be create.
        """
        self._frame = frame
        self._font_for_measure = tkinter.font.Font(family=self._FONT_FAMILY, size=self._FONT_SIZE, weight='bold')
        self._dummy_text = tkinter.Text(self._frame, font=self._font_for_measure)
        self._create_widget(self._TABLE_ROWS_NUMBER)

    def _on_motion(self, event):
        """Trap the motion event.

        :param event: the mouse event
        :return: the string to trap the event
        """
        if self._widget.identify_region(event.x, event.y) in ['separator', 'heading']:
            return "break"

    def _on_left_release(self, event):
        """Trap the left mouse release event.

        :param event: the mouse event
        :return: the string to trap the event
        """
        return "break"

    def _identify_click(self, event):
        """Determine where the mouse click has occured.

        :param event: the mouse event
        :return: the row and column where the click has occured (0-based)
        """
        if self._widget.identify_region(event.x, event.y) == 'separator':
            return None, None

        if self._widget.identify_region(event.x, event.y) == 'heading':
            row = -1
        else:
            row_id = self._widget.identify_row(event.y)
            if row_id == '':
                return None, None
            row = self._row_ids.index(row_id)
        col = int(self._widget.identify_column(event.x)[1:]) - 1
        return row, col

    def _on_left_click(self, event):
        """Manage the left mouse click event.

        :param event: the mouse event
        :return:  the string to trap the event
        """
        row, col = self._identify_click(event)
        if row is not None:
            if row == -1 or col == -1:
                self.on_header_left_click(self, row, col)
            else:
                self.on_cell_left_click(self, row, col)
        return "break"

    def _on_left_double_click(self, event):
        """Manage the left mouse double click event.

        :param event: the mouse event
        :return:  the string to trap the event
        """
        row, col = self._identify_click(event)
        if row is not None:
            if row == -1 or col == -1:
                self.on_header_left_double_click(self, row, col)
            else:
                self.on_cell_left_double_click(self, row, col)
        return "break"

    def _on_right_click(self, event):
        """Manage the right mouse click event.

        :param event: the mouse event
        :return:  the string to trap the event
        """
        row, col = self._identify_click(event)
        if row is not None:
            if row == -1 or col == -1:
                self.on_header_right_click(self, row, col)
            else:
                self.on_cell_right_click(self, row, col)
        return "break"

    def _on_right_double_click(self, event):
        """Manage the right mouse double click event.

        :param event: the mouse event
        :return:  the string to trap the event
        """
        row, col = self._identify_click(event)
        if row is not None:
            if row == -1 or col == -1:
                self.on_header_right_double_click(self, row, col)
            else:
                self.on_cell_right_double_click(self, row, col)
        return "break"

    def _refresh_rows_number(self):
        """Refresh the number of rows shown in the table."""
        if not self._FIXED_ROWS_NUMBER:
            grid_params = self._widget.grid_info()
            self._widget.grid_forget()
            if not self._AVOID_HORIZONTAL_SCROLL:
                grid_params_xsb = self.xsb.grid_info()
                self.xsb.grid_forget()
            if not self._AVOID_VERTICAL_SCROLL:
                grid_params_ysb = self.ysb.grid_info()
                self.ysb.grid_forget()
            row_numbers = min(self._get_number_rows(), self._TABLE_ROWS_NUMBER)
            self._create_widget(row_numbers)
            if grid_params:
                self._widget.grid(**grid_params)
                if not self._AVOID_HORIZONTAL_SCROLL:
                    self.xsb.grid(**grid_params_xsb)
                if not self._AVOID_VERTICAL_SCROLL:
                    self.ysb.grid(**grid_params_ysb)

    def _refresh_columns(self):
        """Refresh the columns of the table."""
        columns = []
        for col in range(self._get_number_cols()):
            columns.append(f"#{col + 1}")
        self._widget['columns'] = columns
        for col in range(self._get_number_cols()):
            if self._get_number_rows() > 0:
                align = self._get_align(0, col)
                renderer = self._get_renderer(0, col)
                if align is Align.LEFT:
                    anchor = tkinter.W
                elif align is Align.RIGHT:
                    anchor = tkinter.E
                else:
                    anchor = tkinter.CENTER
                if renderer is Renderer.BOOLEAN:
                    anchor = tkinter.CENTER
            else:
                anchor = tkinter.W
            self._widget.column(f"#{col + 1}", anchor=anchor, stretch=False)

    def _refresh_col_headers(self):
        """Refresh the column header of the table.

        :return: a list containing the width of each column as automatically computed
        """
        col_auto_width = [0] * (self._get_number_cols() + 1)

        if not self._hide_col_headers:
            max_headers_height = 0
            for col in range(self._get_number_cols()):
                header = self._get_col_header_value(col)
                self._widget.heading(f"#{col + 1}", text=header)
                max_headers_height = max(max_headers_height, header.count('\n'))
                header_rows = header.split('\n')
                if self._auto_size_cols and not self._col_widths:
                    header_width = 0
                    for header_row in header_rows:
                        header_width = max(header_width, self._font_for_measure.measure(header_row))
                    col_auto_width[col + 1] = max(col_auto_width[col + 1], header_width + 20)
            if self._auto_size_col_headers:
                self._widget.heading("#0", text='\n' * max_headers_height)
        else:
            self._widget.configure(show='tree')
        return col_auto_width

    def _refresh_rows(self, col_auto_width):
        """Refresh the rows of the table.

        :param col_auto_width: a list containing the width of each column as automatically computed
        :return: a list containing the updated width of each column as automatically computed
        """
        for child in self._widget.get_children():
            self._widget.delete(child)
        self._row_ids.clear()

        for row in range(self._get_number_rows()):
            row_values = []
            for col in range(self._get_number_cols()):
                value = self._get_value(row, col)
                renderer = self._get_renderer(row, col)
                if renderer is Renderer.BOOLEAN:
                    value = (_UNCHECKED_BOX_SYMBOL, _CHECKED_BOX_SYMBOL)[bool(int(value))]
                row_values.append(value)
                if self._auto_size_cols and not self._col_widths:
                    col_auto_width[col + 1] = max(col_auto_width[col + 1], self._font_for_measure.measure(value))

            foreground_color, background_color = self._get_row_color(row)
            fg_string = _rgb2hex(*foreground_color)
            bg_string = _rgb2hex(*background_color)

            text_style = self._get_style(row, 0)
            if text_style is TextStyle.BOLD:
                font = self._tk_font_bold
            elif text_style is TextStyle.ITALIC:
                font = self._tk_font_italic
            elif text_style is TextStyle.BOLD_ITALIC:
                font = self._tk_font_bold_italic
            else:
                font = self._tk_font

            tag = fg_string + bg_string + str(font)
            self._widget.tag_configure(tag, foreground=fg_string, background=bg_string, font=font)
            row_header = self._get_row_header_value(row)
            row_id = self._widget.insert('', 'end', text=row_header, values=row_values, tags=(tag,))
            if self._auto_size_row_headers:
                col_auto_width[0] = max(col_auto_width[0], self._font_for_measure.measure(row_header))
            self._row_ids.append(row_id)
        return col_auto_width

    def refresh(self):
        """Refresh the display of the table."""
        self._refresh_rows_number()

        self._refresh_columns()

        col_auto_width = self._refresh_col_headers()

        col_auto_width = self._refresh_rows(col_auto_width)

        if self._hide_row_headers:
            self._widget.column('#0', minwidth=0, width=0)
        elif self._auto_size_row_headers:
            self._widget.column('#0', width=min(col_auto_width[0] + 25, self._MAX_ROW_HEADERS_WIDTH))
        else:
            self._widget.column('#0', width=self._ROW_HEADERS_WIDTH)

        if self._col_widths is not None:
            self._set_frozen_cols_width()
        elif self._auto_size_cols:
            for col in range(self._get_number_cols()):
                self._set_col_size(col, min(col_auto_width[col + 1] + 10, self._MAX_COL_WIDTH))
        else:
            self._set_col_sizes(self._COL_WIDTH)

        # Treeview has no possibility to set the row height individually for each row
        # Therefore "_auto_size_rows" cannot be implemented
        # Similarly, there is no autowrap available and "Renderer.AUTO_WRAP" cannot be implemented
        ttk_style.configure(str(id(self)) + '.Treeview', rowheight=self._ROW_HEIGHT)

    def _get_row_size(self, row):
        """Return the size (height) of a row.

        :param row: the index of the row
        :return: the size of the row
        """
        return ttk_style.lookup('prettysusi.Treeview', 'rowheight')

    def _get_col_size(self, col):
        """Return the size (width) of a column.

        :param row: the index of the column
        :return: the size of the column
        """
        return self._widget.column(f"#{col + 1}")['width']

    def _set_row_size(self, row, size):
        """Set the size (height) of a row to a specific value.

        :param row: the index of the row
        :param size: the desired new size of the row
        """
        self._set_row_sizes(size)

    def _set_row_sizes(self, size):
        """Set the size (height) of all rows to a specific value.

        :param size: the desired new size of the rows
        """
        self._style.configure('prettysusi.Treeview', rowheight=size)

    def _set_col_size(self, col, size):
        """Set the size (width) of a column to a specific value.

        :param col: the index of the column
        :param size: the desired new size of the column
        """
        self._widget.column(f"#{col + 1}", width=size)

    def _set_col_sizes(self, size):
        """Set the size (width) of all columns to a specific value.

        :param size: the desired new size of the columns
        """
        for col in range(self._get_number_cols()):
            self._widget.column(f"#{col + 1}", width=size)
