import PySide6
import PySide6.QtWidgets
import PySide6.QtCore
import PySide6.QtGui

from PIL.ImageQt import ImageQt

from ..abstract.widgets import AbstractWidget, AbstractMouseEventsWidget, AbstractLabelledWidget, \
    AbstractButton, AbstractCheckBox, AbstractRadioBox, AbstractBitmap, \
    AbstractText, AbstractCalendar, AbstractSpinControl, AbstractMenu, TextStyle, AbstractTextTimedMenu


def _build_font(size, style):
    """Create a font object with the desired size and style.

    :param size: the font size
    :param style: the font style (TextStyle enum)
    :return: the font object
    """
    font = PySide6.QtGui.QFont('Helvetica', size)
    if style is TextStyle.BOLD:
        font.setBold(True)
    elif style is TextStyle.ITALIC:
        font.setItalic(True)
    elif style is TextStyle.BOLD_ITALIC:
        font.setBold(True)
        font.setItalic(True)
    return font


def _rgb2hex(r, g, b):
    """Create and return a color string with RGB components in hexadecimal format."

    :param r: the red component (0-255)
    :param g: the green component (0-255)
    :param b: the blue component (0-255)
    :return: a color string with RGB components in hexadecimal format
    """
    return "#{:02x}{:02x}{:02x}".format(r, g, b)


class _Widget(AbstractWidget):
    """
    Base class for all widgets based on PySide6. This class should not be instantiated.
    A widget is any element which is displayed in a window and can be organized in a layout.
    """

    def __init__(self, **kwargs):
        """Initialize the widget.

        :param kwargs: additional parameters for superclass
        """
        super().__init__(**kwargs)
        self.setMouseTracking(True)

    def enable(self, is_enabled):
        """Set the enabled status of the widget. If not enabled, the user cannot interact with the widget.

        :param is_enabled: the new enabled status
        """
        super().enable(is_enabled)
        self.setEnabled(self._is_enabled)

    def hide(self, is_hidden):
        """Set the hidden status of the widget. If hidden, the widget is not displayed.

        :param is_hidden: the new hidden status
        """
        super().hide(is_hidden)
        self.setVisible(not self._is_hidden)


class _MouseEventsWidget(AbstractMouseEventsWidget, _Widget):
    """
    Base class for all widgets based on PySide6 managing raw mouse events. This class should not be instantiated.
    The events supported are left and right mouse button down or up; wheel movement; mouse movement;
    mouse entering or leaving the widget.
    """

    def mousePressEvent(self, event):
        """Executed following a mouse press event.

        :param event: the mouse event
        """
        super().mousePressEvent(event)
        q_position = event.localPos()
        position = q_position.x(), q_position.y()
        # corrects using current curson position due to error in qt6 that does not update mouse event position
        q_global_position = event.globalPos()
        cursor_position = PySide6.QtGui.QCursor.pos()
        position = (position[0] + cursor_position.x() - q_global_position.x(),
                    position[1] + cursor_position.y() - q_global_position.y())
        # end of correction
        button = event.button()
        if button is PySide6.QtCore.Qt.LeftButton:
            self.on_left_down(self, position)
        elif button is PySide6.QtCore.Qt.RightButton:
            self.on_right_down(self, position)

    def mouseReleaseEvent(self, event):
        """Executed following a mouse release event.

        :param event: the mouse event
        """
        super().mouseReleaseEvent(event)
        q_position = event.localPos()
        position = q_position.x(), q_position.y()
        button = event.button()
        if button is PySide6.QtCore.Qt.LeftButton:
            self.on_left_up(self, position)
        elif button is PySide6.QtCore.Qt.RightButton:
            self.on_right_up(self, position)

    def mouseMoveEvent(self, event):
        """Executed following a mouse move event.

        :param event: the mouse event
        """
        super().mouseMoveEvent(event)
        q_position = event.localPos()
        position = q_position.x(), q_position.y()
        self.on_mouse_motion(self, position)

    def wheelEvent(self, event):
        """Executed following a mouse wheel event.

        :param event: the mouse event
        """
        super().wheelEvent(event)
        q_position = event.position()
        position = q_position.x(), q_position.y()
        q_rotation = event.angleDelta()
        rotation = q_rotation.y()
        self.on_wheel(self, position, rotation)

    def enterEvent(self, event):
        """Executed when the mouse cursor enters the widget.

        :param event: the mouse event
        """
        super().enterEvent(event)
        self.on_mouse_enter(self)

    def leaveEvent(self, event):
        """Executed when the mouse cursor leaves the widget.

        :param event: the mouse event
        """
        super().leaveEvent(event)
        self.on_mouse_leave(self)


class _LabelledWidget(AbstractLabelledWidget, _Widget):
    """Base class for all widgets baed on PySide6 which display a label. This class should not be instantiated."""

    @property
    def label(self):
        """Return the current value of the label.

        :return: the current value of the label
        """
        return super(_LabelledWidget, _LabelledWidget).label.__get__(self)

    @label.setter
    def label(self, label):
        """Set the value of the label.

        :param label: the new value of the label (string)
        """
        super(_LabelledWidget, _LabelledWidget).label.__set__(self, label)
        self.setText(super(_LabelledWidget, _LabelledWidget).label.__get__(self))


class Button(AbstractButton, _LabelledWidget, PySide6.QtWidgets.QPushButton):
    """Button widget based on PySide6."""

    def __init__(self, **kwargs):
        """Initialize the button.

        :param kwargs: additional parameters for superclass
        """
        PySide6.QtWidgets.QPushButton.__init__(self, parent=kwargs['parent']._WindowClass__panel)
        super().__init__(**kwargs)
        self.clicked.connect(self._on_click)

    def _on_click(self):
        """Executed when the button is clicked."""
        self.on_click(self)


class CheckBox(AbstractCheckBox, _LabelledWidget, PySide6.QtWidgets.QCheckBox):
    """Checkbox widget based on PySide6."""

    def __init__(self, **kwargs):
        """Initialize the checkbox.

        :param kwargs: additional parameters for superclass
        """
        PySide6.QtWidgets.QCheckBox.__init__(self, parent=kwargs['parent']._WindowClass__panel)
        super().__init__(**kwargs)
        self.stateChanged.connect(self._on_click)

    def _on_click(self):
        """Executed when the checkbox is clicked."""
        self.on_click(self)

    @property
    def value(self):
        """Return the current status value of the checkbox.

        :return: the current status value of the checkbox
        """
        super(CheckBox, CheckBox).value.__set__(self, self.isChecked())
        return super(CheckBox, CheckBox).value.__get__(self)

    @value.setter
    def value(self, value):
        """Set the status value of the checkbox.

        :param value: the new status value (boolean)
        """
        super(CheckBox, CheckBox).value.__set__(self, value)
        self.blockSignals(True)
        self.setChecked(super(CheckBox, CheckBox).value.__get__(self))
        self.blockSignals(False)


class RadioBox(AbstractRadioBox, PySide6.QtWidgets.QGroupBox):
    """Radiobox widget based on PySide6."""

    def __init__(self, **kwargs):
        """Initialize the radiobox.

        :param kwargs: additional parameters for superclass
        """
        PySide6.QtWidgets.QGroupBox.__init__(self, parent=kwargs['parent']._WindowClass__panel)
        super().__init__(**kwargs)
        self._button_group = PySide6.QtWidgets.QButtonGroup(parent=kwargs['parent']._WindowClass__panel)

        vbox = PySide6.QtWidgets.QVBoxLayout()
        for choice in self._choices:
            button = PySide6.QtWidgets.QRadioButton(choice, parent=kwargs['parent']._WindowClass__panel)
            self._button_group.addButton(button)
            vbox.addWidget(button)
        self.selection = 0

        self.setLayout(vbox)
        self._button_group.buttonClicked.connect(self._on_click)

    def _on_click(self):
        """Executed when the radiobox is clicked."""
        self.on_click(self)

    @property
    def label(self):
        """Return the current value of the label.

        :return: the current value of the label
        """
        return super(RadioBox, RadioBox).label.__get__(self)

    @label.setter
    def label(self, label):
        """Set the value of the label.

        :param label: the new value of the label (string)
        """
        super(RadioBox, RadioBox).label.__set__(self, label)
        self.setTitle(super(RadioBox, RadioBox).label.__get__(self))

    @property
    def selection(self):
        """Return the current selected choice.

        :return: the current selected choice (0-based)
        """
        for index, button in enumerate(self._button_group.buttons()):
            if button.isChecked():
                break
        super(RadioBox, RadioBox).selection.__set__(self, index)
        return super(RadioBox, RadioBox).selection.__get__(self)

    @selection.setter
    def selection(self, selection):
        """Set the selected choice.

        :param selection: the new selected choice (0-based)
        """
        super(RadioBox, RadioBox).selection.__set__(self, selection)
        self._button_group.buttons()[super(RadioBox, RadioBox).selection.__get__(self)].setChecked(True)

    def set_choice(self, index, string):
        """Set the string to display for a choice.

        :param index: the index of the choice (0-based)
        :param string: the new string to display for the choice
        """
        super().set_choice(index, string)
        self._button_group.buttons()[index].setText(self._choices[index])


class Bitmap(AbstractBitmap, _MouseEventsWidget, PySide6.QtWidgets.QLabel):
    """Bitmap widget based on PySide6."""

    def __init__(self, **kwargs):
        """Initialize the bitmap.

        :param kwargs: additional parameters for superclass
        """
        PySide6.QtWidgets.QLabel.__init__(self, kwargs['parent']._WindowClass__panel)
        self._image_qt = None
        super().__init__(**kwargs)

    @property
    def bitmap(self):
        """Return the current displayed bitmap.

        :return: the current displayed bitmap
        """
        return super(Bitmap, Bitmap).bitmap.__get__(self)

    @bitmap.setter
    def bitmap(self, bitmap):
        """Set the bitmap to display.

        :param bitmap: the bitmap to display (PIL Image object)
        """
        super(Bitmap, Bitmap).bitmap.__set__(self, bitmap)
        if self.bitmap is not None:
            self._image_qt = ImageQt(self.bitmap)
            self.setPixmap(PySide6.QtGui.QPixmap.fromImage(self._image_qt))
            self.setFixedSize(self._image_qt.size())


class _TextWidget(AbstractText):
    """
    Base class for text widgets based on PySide6. This class should not be instantiated.
    Text widgets display a label (with the possibility to change color, size and style) and support raw mouse events.
    """

    @property
    def text_style(self):
        """Return the current text style.

        :return: the current text style
        """
        return super(_TextWidget, _TextWidget).text_style.__get__(self)

    @text_style.setter
    def text_style(self, text_style):
        """Set the text style.

        :param text_style: the new text style (TextStyle enum)
        """
        super(_TextWidget, _TextWidget).text_style.__set__(self, text_style)
        self.setFont(_build_font(self.text_size, self.text_style))

    @property
    def text_size(self):
        """Return the current text size.

        :return: the current text size
        """
        return super(_TextWidget, _TextWidget).text_size.__get__(self)

    @text_size.setter
    def text_size(self, text_size):
        """Set the text size.

        :param text_style: the new text size
        """
        super(_TextWidget, _TextWidget).text_size.__set__(self, text_size)
        self.setFont(_build_font(self.text_size, self.text_style))

    @property
    def foreground_color(self):
        """Return the current foreground color.

        :return: the current foreground color
        """
        return super(_TextWidget, _TextWidget).foreground_color.__get__(self)

    @foreground_color.setter
    def foreground_color(self, foreground_color):
        """Set the foreground color.

        :param foreground_color: the new foreground color (three-element tuple of RGB values between 0 and 255)
        """
        super(_TextWidget, _TextWidget).foreground_color.__set__(self, foreground_color)
        self._set_style_sheet()

    @property
    def background_color(self):
        """Return the current background color.

        :return: the current background color
        """
        return super(_TextWidget, _TextWidget).background_color.__get__(self)

    @background_color.setter
    def background_color(self, background_color):
        """Set the background color.

        :param background_color: the new background color (three-element tuple of RGB values between 0 and 255)
        """
        super(_TextWidget, _TextWidget).background_color.__set__(self, background_color)
        self._set_style_sheet()

    def _set_style_sheet(self):
        """Set the style sheet to the PySide6 widget to apply the current foreground and background colors."""
        if self.foreground_color:
            color_string = _rgb2hex(*self.foreground_color)
            foreground_style = 'color : %s;' % color_string
        else:
            foreground_style = ''
        if self.background_color:
            color_string = _rgb2hex(*self.background_color)
            background_style = 'background-color : %s;' % color_string
        else:
            background_style = ''
        self.setStyleSheet('QLabel { %s %s }' % (foreground_style, background_style))


class TextControl(_TextWidget, _LabelledWidget, PySide6.QtWidgets.QLineEdit):
    """TextControl widget based on PySide6. Allows the user to enter a text."""

    def __init__(self, **kwargs):
        """Initialize the text control.

        :param kwargs: additional parameters for superclass
        """
        PySide6.QtWidgets.QLineEdit.__init__(self, kwargs['parent']._WindowClass__panel)
        self.textChanged.connect(self._on_change)
        super().__init__(**kwargs)

    @property
    def label(self):
        """Return the current value of the label.

        :return: the current value of the label
        """
        super(TextControl, TextControl).label.__set__(self, self.text())
        return super(TextControl, TextControl).label.__get__(self)

    @label.setter
    def label(self, label):
        """Set the value of the label.

        :param label: the new value of the label (string)
        """
        super(_LabelledWidget, _LabelledWidget).label.__set__(self, label)
        self.blockSignals(True)
        self.setText(super(TextControl, TextControl).label.__get__(self))
        self.blockSignals(False)

    def _on_change(self, _text):
        """Executed when the text is changed by the user."""
        self.on_change(self)


class Text(_TextWidget, _LabelledWidget, _MouseEventsWidget, PySide6.QtWidgets.QLabel):
    """Text widget based on PySide6. Displays a text."""

    def __init__(self, **kwargs):
        """Initialize the text.

        :param kwargs: additional parameters for superclass
        """
        PySide6.QtWidgets.QLabel.__init__(self, kwargs['parent']._WindowClass__panel)
        super().__init__(**kwargs)


class Calendar(AbstractCalendar, _Widget, PySide6.QtWidgets.QCalendarWidget):
    """
    Calendar widget based on PySide6.
    Calendars support a date-changed event and have a selection status value. Different languages are supported.
    """

    def __init__(self, **kwargs):
        """Initialize the calendar.

        :param kwargs: additional parameters for superclass
        """
        PySide6.QtWidgets.QCalendarWidget.__init__(self, kwargs['parent']._WindowClass__panel)
        self.setFirstDayOfWeek(PySide6.QtCore.Qt.Monday)
        self.clicked.connect(self._on_date_changed)
        self.setHorizontalHeaderFormat(self.HorizontalHeaderFormat.SingleLetterDayNames)
        self.setVerticalHeaderFormat(self.VerticalHeaderFormat.NoVerticalHeader)
        self.setGridVisible(True)
        super().__init__(**kwargs)

    def _on_date_changed(self, _event):
        """Executed when the date is changed by the user."""
        self.on_date_changed(self)

    def paintCell(self, painter, rect, date):
        """Paint the calendar cells in different colors based on the fact that the date is available or not.

        :param painter: painter object used to paint the calendar cells
        :param rect: rectangle object used to paint the calendard cells
        :param date: date corresponding to the cell to paint
        """
        if not self.minimumDate() <= date <= self.maximumDate():
            painter.setBrush(PySide6.QtGui.QBrush(PySide6.QtCore.Qt.lightGray))
            painter.setPen(PySide6.QtGui.QPen(PySide6.QtCore.Qt.lightGray))
            painter.drawRect(rect)
            painter.setPen(PySide6.QtGui.QPen(PySide6.QtCore.Qt.gray))
            painter.drawText(rect, PySide6.QtCore.Qt.AlignHCenter | PySide6.QtCore.Qt.AlignVCenter, str(date.day()))
        else:
            super().paintCell(painter, rect, date)

    @property
    def lower_date(self):
        """Return the current first allowed date for selection.

        :return: the current first allowed date for selection
        """
        return super(Calendar, Calendar).lower_date.__get__(self)

    @lower_date.setter
    def lower_date(self, lower_date):
        """Set the first allowed date for selection.

        :param lower_date: the new first allowed date for selection
        """
        super(Calendar, Calendar).lower_date.__set__(self, lower_date)
        self._set_date_range()

    @property
    def upper_date(self):
        """Return the current last allowed date for selection.

        :return: the current last allowed date for selection
        """
        return super(Calendar, Calendar).upper_date.__get__(self)

    @upper_date.setter
    def upper_date(self, upper_date):
        """Set the last allowed date for selection.

        :param upper_date: the new last allowed date for selection
        """
        super(Calendar, Calendar).upper_date.__set__(self, upper_date)
        self._set_date_range()

    def _set_date_range(self):
        """Set the available date range in the widget based on the current lower and upper date."""
        if self.lower_date is not None:
            date_as_tuple = self.lower_date.timetuple()
            qt_lower_date = PySide6.QtCore.QDate(date_as_tuple[0], date_as_tuple[1], date_as_tuple[2])
        else:
            qt_lower_date = PySide6.QtCore.QDate(1, 1, 1)
        if self.upper_date is not None:
            date_as_tuple = self.upper_date.timetuple()
            qt_upper_date = PySide6.QtCore.QDate(date_as_tuple[0], date_as_tuple[1], date_as_tuple[2])
        else:
            qt_upper_date = PySide6.QtCore.QDate(10000, 1, 1)
        self.setDateRange(qt_lower_date, qt_upper_date)

    @property
    def selected_date(self):
        """Return the current selected date.

        :return: the current selected date
        """
        qt_date = self.selectedDate()
        datetime_date = qt_date.toPython()
        super(Calendar, Calendar).selected_date.__set__(self, datetime_date)
        return super(Calendar, Calendar).selected_date.__get__(self)

    @selected_date.setter
    def selected_date(self, date):
        """Set the selected date.

        :param date: the new selected date
        """
        super(Calendar, Calendar).selected_date.__set__(self, date)
        date_as_tuple = super(Calendar, Calendar).selected_date.__get__(self).timetuple()
        self.setSelectedDate(PySide6.QtCore.QDate(date_as_tuple[0], date_as_tuple[1], date_as_tuple[2]))

    def set_language(self, language_code):
        """Set the language of the calender (as supported by the GUI).

        :param language_code: the new language to use (code according to ISO639); defaults to English
        """
        language = PySide6.QtCore.QLocale.codeToLanguage(language_code)
        if language is not PySide6.QtCore.QLocale.Language.AnyLanguage:
            self.setLocale(language)
        else:
            self.setLocale(PySide6.QtCore.QLocale.Language.English)


class SpinControl(AbstractSpinControl, _Widget, PySide6.QtWidgets.QSpinBox):
    """Spin control widget based on PySide6. Spin controls support a value-changed event and have a status value."""

    def __init__(self, **kwargs):
        """Initialize the spin control

        :param kwargs: additional parameters for superclass
        """
        PySide6.QtWidgets.QSpinBox.__init__(self, kwargs['parent']._WindowClass__panel)
        super().__init__(**kwargs)
        self.valueChanged.connect(self._on_value_changed)
        self.lineEdit().setReadOnly(True)

    def _on_value_changed(self):
        """Executed when the spin control value is changed by the user."""
        self.on_value_changed(self)

    @property
    def min_value(self):
        """Return the current minimum allowed value.

        :return: the current minimum allowed value
        """
        return super(SpinControl, SpinControl).min_value.__get__(self)

    @min_value.setter
    def min_value(self, min_value):
        """Set the minimum allowed value.

        :param min_value: the new minimum allowed value
        """
        super(SpinControl, SpinControl).min_value.__set__(self, min_value)
        if self.min_value is not None:
            self.setMinimum(self.min_value)
        else:
            self.setMinimum(self._DEFAULT_MIN_VALUE)

    @property
    def max_value(self):
        """Return the current maximum allowed value.

        :return: the current maximum allowed value
        """
        return super(SpinControl, SpinControl).max_value.__get__(self)

    @max_value.setter
    def max_value(self, max_value):
        """Set the maximum allowed value.

        :param max_value: the new maximum allowed value
        """
        super(SpinControl, SpinControl).max_value.__set__(self, max_value)
        if self.max_value is not None:
            self.setMaximum(self.max_value)
        else:
            self.setMaximum(self._DEFAULT_MAX_VALUE)

    @property
    def value(self):
        """Return the current value.

        :return: the current value
        """
        super(SpinControl, SpinControl).value.__set__(self, PySide6.QtWidgets.QSpinBox.value(self))
        return super(SpinControl, SpinControl).value.__get__(self)

    @value.setter
    def value(self, value):
        """Set the value (clipping between minimum and maximum allowed values if necessary).

        :param value: the new value
        """
        super(SpinControl, SpinControl).value.__set__(self, value)
        self.setValue(super(SpinControl, SpinControl).value.__get__(self))


class Menu(AbstractMenu, _Widget, PySide6.QtWidgets.QMenu):
    """
    Menu widget based on PySide6.
    Menus allow to create a tree of items which the user can click; each item can in turn be a menu.
    """

    def __init__(self, **kwargs):
        """Initialize the menu.

        :param kwargs: additional parameters for superclass
        """
        PySide6.QtWidgets.QMenu.__init__(self)
        super().__init__(**kwargs)

    def _on_click(self, item):
        """Executed when a menu item is clicked.

        :param item: the string corresponding to the clicked item
        """
        self.on_click(self, item)

    def pop_up(self):
        """Build and show the menu as a pop-up."""
        super().pop_up()
        self.exec(PySide6.QtGui.QCursor.pos())

    def _append_separator(self, target):
        """
        Append a separator to the target, which can be the menu object itself (for pop-up menus or
        branches of a menu tree) or a window menubar.
        Separators are not shown in menubars in PySide6.

        :param target: the target where the menu has to be appended (menu object itself or window menubar)
        """
        target.addSeparator()

    def _append_menu(self, target, menu, is_enabled):
        """
        Append a menu to the target, which can be the menu object itself (for pop-up menus or
        branches of a menu tree) or a window menubar.

        :param target: the target where the menu has to be appended (menu object itself or window menubar)
        :param item: the menu to append
        :param is_enabled: boolean defining if the menu is enabled
        """
        menu._build_menu(inherited_on_click=self.on_click)
        menu.setTitle(menu.label)
        target.addMenu(menu)
        menu.setEnabled(is_enabled)

    def _append_simple_item(self, target, item, is_enabled, on_item_click):
        """
        Append a simple string item to the target, which can be a the menu object itself (for pop-up menus or
        branches of a menu tree) or a window menubar.

        :param target: the target where the item has to be appended (menu object itself or window menubar)
        :param item: the item to append
        :param is_enabled: boolean defining if the item is enabled
        :param on_item_click: function to be executed if the item is clicked
        """
        entry = PySide6.QtGui.QAction(item, target)
        ampersand = item.find('&')
        if ampersand != -1:
            shortcut_key = item[ampersand + 1]
            entry.setShortcut('Alt+' + shortcut_key)
        target.addAction(entry)
        if on_item_click is not None:
            entry.triggered.connect(lambda checked=False: on_item_click(self))
        else:
            entry.triggered.connect(lambda checked=False, i=item: self._on_click(i))
        entry.setEnabled(is_enabled)

    def closeEvent(self, _event):
        """Executed when the menu is closed."""
        self.on_close(self)


class TextTimedMenu(AbstractTextTimedMenu, PySide6.QtWidgets.QDialog):
    """
    Text timed menu based on PySide6; these are menus built with text labels, which close automatically after a
    specified time when the mouse cursor leaves.
    """

    _close_signal = PySide6.QtCore.Signal()

    def __init__(self, **kwargs):
        """Initialize the timed text menu.

        :param kwargs: additional parameters for superclass
        """
        PySide6.QtWidgets.QDialog.__init__(self, parent=None)
        self._close_signal.connect(self._on_close_signal)
        super().__init__(**kwargs)
        self.setWindowFlag(PySide6.QtCore.Qt.FramelessWindowHint)
        self._layout = PySide6.QtWidgets.QVBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)

    def closeEvent(self, event):
        """Executed when the menu is closed.

        :param event: the close event
        """
        super().closeEvent(event)
        self.on_close(self)

    def pop_up(self, *, modal=False):
        """Build and show the menu as a pop-up. It can be shown as a modal, forcing interaction from the user.

        :param modal: specifies if the text timed menu should be modal or not
        """
        super().pop_up()
        self.setLayout(self._layout)
        delta = PySide6.QtCore.QPoint(10, 10)
        self.move(PySide6.QtGui.QCursor.pos() + delta)
        if modal:
            PySide6.QtWidgets.QDialog.exec(self)
        else:
            PySide6.QtWidgets.QDialog.show(self)

    def _create_text(self, label):
        """Create a Text widget with the specified label.

        :param label: the desired text label
        :return: the created Text widget
        """
        if label == self.SEPARATOR:
            label = ""
        text = Text(parent=self._parent, label=label)
        self._layout.addWidget(text)
        return text

    def _close(self):
        """Close the menu."""
        super()._close()
        for text in self._texts:
            text.leaveEvent = lambda event: None
        self._close_signal.emit()

    def _on_close_signal(self):
        """Executed when the close signal is emitted."""
        PySide6.QtWidgets.QWidget.close(self)
