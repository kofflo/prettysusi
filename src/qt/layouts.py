import PySide6
import PySide6.QtWidgets
import PySide6.QtCore
import PySide6.QtGui

from ..abstract.layouts import AbstractBoxLayout, AbstractGridLayout, Align


class _Layout:
    """Superclass for all types of PySide6 layout classes (box layouts and grid layout)."""

    def _apply_align(self, align, size_policy):
        """Compute the alignment flag for a layout cell and sets the size policy if needed.

        :param align: the desired alignment (Align enum)
        :param size_policy: the widget QSizePolicy object (None for a cell containing another layout)
        :return: the resulting alignment flag
        """
        align_flag = 0
        if align & Align.EXPAND:
            align_flag = -1
            if size_policy is not None:
                size_policy.setHorizontalPolicy(PySide6.QtWidgets.QSizePolicy.Policy.MinimumExpanding)
        return align_flag


class _BoxLayout(AbstractBoxLayout, _Layout):
    """Superclass for PySide6 box layout classes (VBoxLayout and HBoxLayout)."""

    _LAYOUT_CLASS = None
    _BEFORE = None
    _AFTER = None
    _ORTO_LAYOUT_CLASS = None
    _ORTO_BEFORE = None
    _ORTO_AFTER = None

    def _create_layout(self, window):
        """Create and return a PySide6 layout object.

        :param window: the window object to which the layout is applied (None to create a layout inside another layout)
        :return: the PySide6 layout object
        """
        layout = self._LAYOUT_CLASS()
        layout.setSpacing(0)
        for widget_dict in self._widgets:
            widget = widget_dict['type']
            if widget == 'space':
                layout.addSpacing(widget_dict['space'])
            elif widget == 'stretch':
                layout.addStretch(widget_dict['stretch'])
            else:
                widget_border = widget_dict['border']
                if isinstance(widget_border, int):
                    widget_border = [widget_border] * 4

                widget_align = widget_dict['align']
                if isinstance(widget, _Layout):
                    widget_layout = widget._create_layout(None)
                    widget_layout.setContentsMargins(widget_border[3], widget_border[0], widget_border[1], widget_border[2])
                    align_layout = self._ORTO_LAYOUT_CLASS()
                    if widget_align & Align.END or widget_align & Align.CENTER:
                        align_layout.addStretch()
                    align_layout.addLayout(widget_layout)
                    if widget_align & Align.START or widget_align & Align.CENTER:
                        align_layout.addStretch()
                    layout.addLayout(align_layout, stretch=widget_dict['stretch'])
                else:
                    widget_size_policy = widget.sizePolicy()
                    align_flag = self._apply_align(widget_align, widget_size_policy)
                    widget.setSizePolicy(widget_size_policy)
                    layout.addSpacing(widget_border[self._BEFORE])
                    border_layout = self._ORTO_LAYOUT_CLASS()
                    border_layout.addSpacing(widget_border[self._ORTO_BEFORE])
                    if align_flag == -1:
                        border_layout.addWidget(widget, stretch=widget_dict['stretch'])
                    else:
                        border_layout.addWidget(widget, alignment=align_flag, stretch=widget_dict['stretch'])
                    border_layout.addSpacing(widget_border[self._ORTO_AFTER])
                    layout.addLayout(border_layout, stretch=widget_dict['stretch'])
                    layout.addSpacing(widget_border[self._AFTER])

        if window is not None:
            window._WindowClass__layout_parent.setLayout(layout)

        return layout


class VBoxLayout(_BoxLayout):
    """Vertical box layout based on PySide6: allows to place the widgets in a column."""

    _LAYOUT_CLASS = PySide6.QtWidgets.QVBoxLayout
    _BEFORE = 0
    _AFTER = 2
    _ORTO_LAYOUT_CLASS = PySide6.QtWidgets.QHBoxLayout
    _ORTO_BEFORE = 3
    _ORTO_AFTER = 1

    def _apply_align(self, align, size_policy):
        """Compute the alignment flag for a layout cell and sets the size policy if needed.

        :param align: the desired alignment (Align enum)
        :param size_policy: the widget QSizePolicy object (None for a cell containing another layout)
        :return: the resulting alignment flag
        """
        align_flag = super()._apply_align(align, size_policy)
        if align_flag == 0:
            if align & Align.LEFT:
                align_flag = PySide6.QtCore.Qt.AlignLeft
            elif align & Align.HCENTER:
                align_flag = PySide6.QtCore.Qt.AlignHCenter
            elif align & Align.RIGHT:
                align_flag = PySide6.QtCore.Qt.AlignRight
        return align_flag


class HBoxLayout(_BoxLayout):
    """Horizontal box layout based on PySide6: allows to place the widgets in a row."""

    _LAYOUT_CLASS = PySide6.QtWidgets.QHBoxLayout
    _BEFORE = 3
    _AFTER = 1
    _ORTO_LAYOUT_CLASS = PySide6.QtWidgets.QVBoxLayout
    _ORTO_BEFORE = 0
    _ORTO_AFTER = 2

    def _apply_align(self, align, size_policy):
        """Compute the alignment flag for a layout cell and sets the size policy if needed.

        :param align: the desired alignment (Align enum)
        :param size_policy: the widget QSizePolicy object (None for a cell containing another layout)
        :return: the resulting alignment flag
        """
        align_flag = super()._apply_align(align, size_policy)
        if align_flag == 0:
            if align & Align.TOP:
                align_flag = PySide6.QtCore.Qt.AlignTop
            elif align & Align.VCENTER:
                align_flag = PySide6.QtCore.Qt.AlignVCenter
            elif align & Align.BOTTOM:
                align_flag = PySide6.QtCore.Qt.AlignBottom
        return align_flag


class GridLayout(AbstractGridLayout, _Layout):
    """Grid layout based on PySide6: allows to place the widgets in a two dimensional grid."""

    def _create_layout(self, window):
        """Create and return a PySide6 layout object.

        :param window: the window object to which the layout is applied (None to create a layout inside another layout)
        :return: the PySide6 layout object
        """
        layout = PySide6.QtWidgets.QGridLayout()
        layout.setHorizontalSpacing(self._hgap)
        layout.setVerticalSpacing(self._vgap)

        for row in range(self._rows):
            if self._row_stretch[row] is not None:
                layout.setRowStretch(row, self._row_stretch[row])

        for col in range(self._cols):
            if self._col_stretch[col] is not None:
                layout.setColumnStretch(col, self._col_stretch[col])

        for row, widgets_row in enumerate(self._widgets):
            for col, widget_dict in enumerate(widgets_row):
                widget = widget_dict['type']
                if widget is None:
                    continue
                elif widget == 'space':
                    layout.addItem(PySide6.QtWidgets.QSpacerItem(widget_dict['width'], widget_dict['height']), row, col)
                else:
                    widget_border = widget_dict['border']
                    if isinstance(widget_border, int):
                        widget_border = [widget_border] * 4
                    widget_align = widget_dict['align']

                    if isinstance(widget, _Layout):
                        widget_layout = widget.create_layout(None)
                        widget_layout.setContentsMargins(widget_border[3], widget_border[0], widget_border[1], widget_border[2])
                        align_flag = self._apply_align(widget_align, None)
                        if align_flag == -1:
                            align_flag = 0
                        layout.addLayout(widget_layout, row, col, alignment=align_flag)
                    else:
                        widget_size_policy = widget.sizePolicy()
                        align_flag = self._apply_align(widget_align, widget_size_policy)
                        widget.setSizePolicy(widget_size_policy)

                        border_layout = PySide6.QtWidgets.QGridLayout()
                        border_layout.setHorizontalSpacing(0)
                        border_layout.setVerticalSpacing(0)
                        border_layout.addItem(PySide6.QtWidgets.QSpacerItem(widget_border[3], widget_border[0]), 0, 0)
                        border_layout.addWidget(widget, 1, 1)
                        border_layout.addItem(PySide6.QtWidgets.QSpacerItem(widget_border[1], widget_border[2]), 2, 2)

                        layout.addLayout(border_layout, row, col, alignment=align_flag)

        if window is not None:
            window._WindowClass__layout_parent.setLayout(layout)
        return layout

    def _apply_align(self, align, size_policy):
        """Compute the alignment flag for a layout cell and sets the size policy if needed.

        :param align: the desired alignment (Align enum)
        :param size_policy: the widget QSizePolicy object (None for a cell containing another layout)
        :return: the resulting alignment flag
        """
        align_flag = super()._apply_align(align, size_policy)
        if align_flag == 0:
            if align & Align.TOP:
                align_flag = PySide6.QtCore.Qt.AlignTop
            elif align & Align.VCENTER:
                align_flag = PySide6.QtCore.Qt.AlignVCenter
            elif align & Align.BOTTOM:
                align_flag = PySide6.QtCore.Qt.AlignBottom
            if align & Align.LEFT:
                align_flag |= PySide6.QtCore.Qt.AlignLeft
            elif align & Align.HCENTER:
                align_flag |= PySide6.QtCore.Qt.AlignHCenter
            elif align & Align.RIGHT:
                align_flag |= PySide6.QtCore.Qt.AlignRight
        return align_flag
