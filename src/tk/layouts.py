import tkinter
from types import SimpleNamespace

from ..abstract.layouts import AbstractBoxLayout, AbstractGridLayout, Align
from .tables import Table


class _Layout:
    """Superclass for all types of tkinter layout classes (box layouts and grid layout)."""

    def _apply_align(self, align):
        """Compute the alignment flag for a layout cell.

        :param align: the desired alignment (Align enum)
        :return: the resulting alignment flag
        """
        raise NotImplementedError()

    @staticmethod
    def _get_border(border_tuple):
        """

        :param border_tuple: the tuple of borders
        :return: borders values rearranged in padx and pady as needed by tkinter
        """
        return [border_tuple[3], border_tuple[1]], [border_tuple[0], border_tuple[2]]


class _BoxLayout(AbstractBoxLayout, _Layout):
    """Superclass for tkinter box layout classes (VBoxLayout and HBoxLayout)."""

    _DIRECTION = None

    def _create_layout(self, window):
        """Create and return a tkinter frame object.

        :param window: the window object to which the layout is applied
        :return: the tkinter frame object
        """
        frame = tkinter.Frame(window._WindowClass__layout_parent)
        frame.pack_propagate(0)
        for index, widget_dict in enumerate(self._widgets):
            widget = widget_dict['type']

            if widget == 'space':
                self._create_space(frame, index, widget_dict['space'])
            elif widget == 'stretch':
                self._create_stretch(frame, index, widget_dict['stretch'])
            else:
                row, col = self._get_row_col(index)

                widget_align = widget_dict['align']
                sticky = self._apply_align(widget_align)

                widget_border = widget_dict['border']
                if isinstance(widget_border, int):
                    widget_border = [widget_border] * 4
                padx, pady = self._get_border(widget_border)
                if isinstance(widget, _Layout):
                    parent = SimpleNamespace()
                    parent._WindowClass__layout_parent = frame
                    widget = widget._create_layout(parent)
                    widget.grid(row=row, column=col, padx=padx, pady=pady, sticky=sticky)
                elif isinstance(widget, Table):
                    frame_table = tkinter.Frame(frame)
                    widget._set_frame(frame_table)
                    if not widget._AVOID_HORIZONTAL_SCROLL:
                        pady_grid = 0
                    else:
                        pady_grid = pady[1]
                    if not widget._AVOID_VERTICAL_SCROLL:
                        padx_grid = 0
                    else:
                        padx_grid = padx[1]
                    if not widget._AVOID_HORIZONTAL_SCROLL:
                        widget.xsb.grid(row=1, column=0, padx=(padx[0], padx_grid), pady=(5, pady[1]), sticky='new')
                    if not widget._AVOID_VERTICAL_SCROLL:
                        widget.ysb.grid(row=0, column=1, padx=(5, padx[1]), pady=(pady[0], pady_grid), sticky='nsw')
                    widget.grid(row=0, column=0, padx=(padx[0], padx_grid), pady=(pady[0], pady_grid), sticky=sticky)
                    frame_table.columnconfigure(0, weight=1)
                    frame_table.rowconfigure(0, weight=1)
                    frame_table.grid(row=row, column=col, sticky=sticky)
                else:
                    widget._set_frame(frame)
                    widget.grid(row=row, column=col, padx=padx, pady=pady, sticky=sticky)

                widget_stretch = widget_dict['stretch']
                self._create_stretch(frame, index, widget_stretch)

        return frame

    def _get_row_col(self, index):
        """Return the row and column values of a cell at the specified index.

        :param index: the index of the cell
        :return: the tuple of row and column values
        """
        raise NotImplementedError()

    def _create_space(self, frame, index, space):
        """Create a space of the specified dimension in the cell at the given index.

        :param frame: the tkinter frame object
        :param index: the index of the cell
        :param space: the dimension of the space
        """
        raise NotImplementedError()

    def _create_stretch(self, frame, index, stretch):
        """Create a stretch of the specified weight in the cell at the given index.

        :param frame: the tkinter frame object
        :param index: the index of the cell
        :param space: the weight of the stretch
        """
        raise NotImplementedError()


class VBoxLayout(_BoxLayout):
    """Vertical box layout based on tkinter: allows to place the widgets in a column."""

    def _create_layout(self, window):
        """Create and return a tkinter frame object.

        :param window: the window object to which the layout is applied
        :return: the tkinter frame object
        """
        frame = super()._create_layout(window)
        frame.grid_columnconfigure(0, weight=1)
        return frame

    def _create_space(self, frame, index, space):
        """Create a space of the specified dimension in the cell at the given index.

        :param frame: the tkinter frame object
        :param index: the index of the cell
        :param space: the dimension of the space
        """
        frame.grid_rowconfigure(index, minsize=space)

    def _create_stretch(self, frame, index, stretch):
        """Create a stretch of the specified weight in the cell at the given index.

        :param frame: the tkinter frame object
        :param index: the index of the cell
        :param space: the weight of the stretch
        """
        frame.grid_rowconfigure(index, weight=stretch)

    def _get_row_col(self, index):
        """Return the row and column values of a cell at the specified index.

        :param index: the index of the cell
        :return: the tuple of row and column values (column always 0 for a vertical box layout)
        """
        return index, 0

    def _apply_align(self, align):
        """Compute the alignment flag for a layout cell.

        :param align: the desired alignment (Align enum)
        :return: the resulting alignment flag
        """
        if align & Align.EXPAND:
            return "ew"
        elif align & Align.LEFT:
            return "w"
        elif align & Align.HCENTER:
            return ""
        elif align & Align.RIGHT:
            return "e"
        return ""


class HBoxLayout(_BoxLayout):
    """Horizontal box layout based on tkinter: allows to place the widgets in a row."""

    def _create_layout(self, window):
        """Create and return a tkinter frame object.

        :param window: the window object to which the layout is applied
        :return: the tkinter frame object
        """
        frame = super()._create_layout(window)
        frame.grid_rowconfigure(0, weight=1)
        return frame

    def _create_space(self, frame, index, space):
        """Create a space of the specified dimension in the cell at the given index.

        :param frame: the tkinter frame object
        :param index: the index of the cell
        :param space: the dimension of the space
        """
        frame.grid_columnconfigure(index, minsize=space)

    def _create_stretch(self, frame, index, stretch):
        """Create a stretch of the specified weight in the cell at the given index.

        :param frame: the tkinter frame object
        :param index: the index of the cell
        :param space: the weight of the stretch
        """
        frame.grid_columnconfigure(index, weight=stretch)

    def _get_row_col(self, index):
        """Return the row and column values of a cell at the specified index.

        :param index: the index of the cell
        :return: the tuple of row and column values (raw always 0 for a horizontal box layout)
        """
        return 0, index

    def _apply_align(self, align):
        """Compute the alignment flag for a layout cell.

        :param align: the desired alignment (Align enum)
        :return: the resulting alignment flag
        """
        if align & Align.EXPAND:
            return "ns"
        elif align & Align.TOP:
            return "n"
        elif align & Align.VCENTER:
            return ""
        elif align & Align.BOTTOM:
            return "s"
        return ""


class GridLayout(AbstractGridLayout, _Layout):
    """Grid layout based on tkinter: allows to place the widgets in a two dimensional grid."""

    def _create_layout(self, window):
        """Create and return a tkinter frame object.

        :param window: the window object to which the layout is applied
        :return: the tkinter frame object
        """
        frame = tkinter.Frame(window._WindowClass__layout_parent)

        for row in range(self._rows):
            if self._row_stretch[row] is not None:
                frame.grid_rowconfigure(row, weight=self._row_stretch[row])

        for col in range(self._cols):
            if self._col_stretch[col] is not None:
                frame.grid_columnconfigure(col, weight=self._col_stretch[col])

        for row, widgets_row in enumerate(self._widgets):
            for col, widget_dict in enumerate(widgets_row):
                widget = widget_dict['type']
                if widget == 'space':
                    frame.grid_rowconfigure(row, minsize=widget_dict['height'])
                    frame.grid_columnconfigure(col, minsize=widget_dict['width'])
                else:
                    widget_align = widget_dict['align']
                    sticky = self._apply_align(widget_align)

                    if isinstance(widget, _Layout):
                        widget = widget.create_layout(frame)
                    else:
                        widget._set_frame(frame)

                    widget_border = widget_dict['border']
                    if isinstance(widget_border, int):
                        widget_border = [widget_border] * 4
                    padx, pady = self._get_border(widget_border)

                    if row != 0:
                        pady[0] += self._vgap / 2
                    if row != self._rows - 1:
                        pady[1] += self._vgap / 2
                    if col != 0:
                        padx[0] += self._hgap / 2
                    if col != self._cols - 1:
                        padx[1] += self._hgap / 2

                    widget.grid(row=row, column=col, padx=padx, pady=pady, sticky=sticky)
        return frame

    def _apply_align(self, align):
        """Compute the alignment flag for a layout cell.

        :param align: the desired alignment (Align enum)
        :return: the resulting alignment flag
        """
        if align & Align.EXPAND:
            return "nsew"
        else:
            sticky=""
            if align & Align.TOP:
                sticky += "n"
            elif align & Align.BOTTOM:
                sticky += "s"
            if align & Align.LEFT:
                sticky += "w"
            elif align & Align.RIGHT:
                sticky += "e"
            return sticky
