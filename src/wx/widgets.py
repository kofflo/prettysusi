import wx
import wx.adv
import datetime
from types import SimpleNamespace

from .windows import Frame
from ..abstract.widgets import AbstractWidget, AbstractMouseEventsWidget, AbstractLabelledWidget, \
    AbstractButton, AbstractCheckBox, AbstractRadioBox, AbstractBitmap, \
    AbstractText, AbstractCalendar, AbstractSpinControl, AbstractMenu, TextStyle, AbstractTextTimedMenu


def _build_font(size, style):
    """Create a font object with the desired size and style.

    :param size: the font size
    :param style: the font style (TextStyle enum)
    :return: the font object
    """
    font = wx.Font(wx.FontInfo(size))
    if style is TextStyle.BOLD:
        font = font.Bold()
    elif style is TextStyle.ITALIC:
        font = font.Italic()
    elif style is TextStyle.BOLD_ITALIC:
        font = font.Bold().Italic()
    return font


def _pil_2_wx(image):
    """Convert a PIL image into a wxPython Bitmap image.

    :param image: the PIL image to convert
    :return: the resulting wxPython image
    """
    width, height = image.size
    if image.mode == 'RGBA':
        return wx.Bitmap.FromBufferAndAlpha(width, height, image.tobytes('raw', 'RGB'), image.tobytes('raw', 'A'))
    else:
        return wx.Bitmap.FromBuffer(width, height, image.tobytes())


class _Widget(AbstractWidget):
    """
    Base class for all widgets based on wxPython. This class should not be instantiated.
    A widget is any element which is displayed in a window and can be organized in a layout.
    """

    def enable(self, is_enabled):
        """Set the enabled status of the widget. If not enabled, the user cannot interact with the widget.

        :param is_enabled: the new enabled status
        """
        super().enable(is_enabled)
        self.Enable(self._is_enabled)

    def hide(self, is_hidden):
        """Set the hidden status of the widget. If hidden, the widget is not displayed.

        :param is_hidden: the new hidden status
        """
        super().hide(is_hidden)
        self.Show(not self._is_hidden)
# INVESTIGATE ######################################################################################################
#        self._parent._panel.Layout()
#        self._parent._layout.Fit(self._parent)


class _MouseEventsWidget(AbstractMouseEventsWidget, _Widget):
    """
    Base class for all widgets based on wxPython managing raw mouse events. This class should not be instantiated.
    The events supported are left and right mouse button down or up; wheel movement; mouse movement;
    mouse entering or leaving the widget.
    """

    def __init__(self, **kwargs):
        """Initialize the widget.

        :param kwargs: additional parameters for superclass
        """
        super().__init__(**kwargs)
        self.Bind(wx.EVT_LEFT_DOWN, self._on_left_down)
        self.Bind(wx.EVT_LEFT_UP, self._on_left_up)
        self.Bind(wx.EVT_RIGHT_DOWN, self._on_right_down)
        self.Bind(wx.EVT_RIGHT_UP, self._on_right_up)
        self.Bind(wx.EVT_MOUSEWHEEL, self._on_wheel)
        self.Bind(wx.EVT_MOTION, self._on_mouse_motion)
        self.Bind(wx.EVT_ENTER_WINDOW, self._on_mouse_enter)
        self.Bind(wx.EVT_LEAVE_WINDOW, self._on_mouse_leave)

    def _on_left_down(self, event):
        """Executed following a left mouse press event.

        :param event: the mouse event
        """
        position = event.GetPosition().Get()
        self.on_left_down(self, position)

    def _on_left_up(self, event):
        """Executed following a left mouse release event.

        :param event: the mouse event
        """
        position = event.GetPosition().Get()
        self.on_left_up(self, position)

    def _on_right_down(self, event):
        """Executed following a right mouse press event.

        :param event: the mouse event
        """
        position = event.GetPosition().Get()
        self.on_right_down(self, position)

    def _on_right_up(self, event):
        """Executed following a right mouse release event.

        :param event: the mouse event
        """
        position = event.GetPosition().Get()
        self.on_right_up(self, position)

    def _on_mouse_motion(self, event):
        """Executed following a mouse move event.

        :param event: the mouse event
        """
        position = event.GetPosition().Get()
        self.on_mouse_motion(self, position)

    def _on_wheel(self, event):
        """Executed following a mouse wheel event.

        :param event: the mouse event
        """
        position = event.GetPosition().Get()
        rotation = event.GetWheelRotation()
        self.on_wheel(self, position, rotation)

    def _on_mouse_enter(self, event):
        """Executed when the mouse cursor enters the widget.

        :param event: the mouse event
        """
        self.on_mouse_enter(self)

    def _on_mouse_leave(self, event):
        """Executed when the mouse cursor leaves the widget.

        :param event: the mouse event
        """
        self.on_mouse_leave(self)


class _LabelledWidget(AbstractLabelledWidget, _Widget):
    """Base class for all widgets baed on wxPython which display a label. This class should not be instantiated."""

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
        self.SetLabel(super(_LabelledWidget, _LabelledWidget).label.__get__(self))


class Button(AbstractButton, _LabelledWidget, wx.Button):
    """Button widget based on wxPython."""

    def __init__(self, **kwargs):
        """Initialize the button.

        :param kwargs: additional parameters for superclass
        """
        wx.Button.__init__(self, kwargs['parent']._WindowClass__panel)
        super().__init__(**kwargs)
        self.Bind(wx.EVT_BUTTON, self._on_click)

    def _on_click(self, _event):
        """Executed when the button is clicked."""
        self.on_click(self)


class CheckBox(AbstractCheckBox, _LabelledWidget, wx.CheckBox):
    """Checkbox widget based on wxPython."""

    def __init__(self, **kwargs):
        """Initialize the checkbox.

        :param kwargs: additional parameters for superclass
        """
        wx.CheckBox.__init__(self, kwargs['parent']._WindowClass__panel)
        super().__init__(**kwargs)
        self.Bind(wx.EVT_CHECKBOX, self._on_click)

    def _on_click(self, _event):
        """Executed when the checkbox is clicked."""
        self.on_click(self)

    @property
    def value(self):
        """Return the current status value of the checkbox.

        :return: the current status value of the checkbox
        """
        super(CheckBox, CheckBox).value.__set__(self, self.GetValue())
        return super(CheckBox, CheckBox).value.__get__(self)

    @value.setter
    def value(self, value):
        """Set the status value of the checkbox.

        :param value: the new status value (boolean)
        """
        super(CheckBox, CheckBox).value.__set__(self, value)
        self.SetValue(super(CheckBox, CheckBox).value.__get__(self))


class RadioBox(AbstractRadioBox, _LabelledWidget, wx.RadioBox):
    """Radiobox widget based on wxPython."""

    def __init__(self, **kwargs):
        """Initialize the radiobox.

        :param kwargs: additional parameters for superclass
        """
        wx.RadioBox.__init__(self)
        self._created = False
        super().__init__(**kwargs)
        self.Create(kwargs['parent']._WindowClass__panel, label=self._label, style=wx.RA_SPECIFY_ROWS, choices=self._choices)
        self._created = True
        self.Bind(wx.EVT_RADIOBOX, self._on_click)

    def _on_click(self, _event):
        """Executed when the radiobox is clicked."""
        self.on_click(self)

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
        if self._created:
            self.SetLabel(super(_LabelledWidget, _LabelledWidget).label.__get__(self))

    @property
    def selection(self):
        """Return the current selected choice.

        :return: the current selected choice (0-based)
        """
        super(RadioBox, RadioBox).selection.__set__(self, self.GetSelection())
        return super(RadioBox, RadioBox).selection.__get__(self)

    @selection.setter
    def selection(self, selection):
        """Set the selected choice.

        :param selection: the new selected choice (0-based)
        """
        super(RadioBox, RadioBox).selection.__set__(self, selection)
        self.SetSelection(super(RadioBox, RadioBox).selection.__get__(self))

    def set_choice(self, index, string):
        """Set the string to display for a choice.

        :param index: the index of the choice (0-based)
        :param string: the new string to display for the choice
        """
        super().set_choice(index, string)
        self.SetString(index, self._choices[index])


class Bitmap(AbstractBitmap, _MouseEventsWidget, wx.StaticBitmap):
    """Bitmap widget based on wxPython."""

    def __init__(self, **kwargs):
        """Initialize the bitmap.

        :param kwargs: additional parameters for superclass
        """
        wx.StaticBitmap.__init__(self, kwargs['parent']._WindowClass__panel)
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
            self.SetBitmap(_pil_2_wx(self.bitmap))


class _TextWidget(AbstractText):
    """
    Base class for text widgets based on wxPYthon. This class should not be instantiated.
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
        self.SetFont(_build_font(self.text_size, self.text_style))

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
        self.SetFont(_build_font(self.text_size, self.text_style))

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
        if self.foreground_color:
            self.SetForegroundColour(self.foreground_color)
        else:
            self.SetForegroundColour(wx.NullColour)

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
        if self.background_color:
            self.SetBackgroundColour(self.background_color)
        else:
            self.SetBackgroundColour(wx.NullColour)


class TextControl(_TextWidget, _LabelledWidget, wx.TextCtrl):
    """TextControl widget based on wxPython. Allows the user to enter a text."""

    def __init__(self, **kwargs):
        """Initialize the text control.

        :param kwargs: additional parameters for superclass
        """
        wx.TextCtrl.__init__(self, kwargs['parent']._WindowClass__panel)
        super().__init__(**kwargs)
        self.Bind(wx.EVT_TEXT, self._on_change)

    @property
    def label(self):
        """Return the current value of the label.

        :return: the current value of the label
        """
        super(_LabelledWidget, _LabelledWidget).label.__set__(self, self.GetValue())
        return super(TextControl, TextControl).label.__get__(self)

    @label.setter
    def label(self, label):
        """Set the value of the label.

        :param label: the new value of the label (string)
        """
        super(_LabelledWidget, _LabelledWidget).label.__set__(self, label)
        self.ChangeValue(super(TextControl, TextControl).label.__get__(self))

    def _on_change(self, _event):
        """Executed when the text is changed by the user."""
        self.on_change(self)


class Text(_TextWidget, _MouseEventsWidget, _LabelledWidget, wx.StaticText):
    """Text widget based on wxPYthon. Displays a text."""

    def __init__(self, **kwargs):
        """Initialize the text.

        :param kwargs: additional parameters for superclass
        """
        wx.StaticText.__init__(self, kwargs['parent']._WindowClass__panel)
        super().__init__(**kwargs)


class Calendar(AbstractCalendar, _Widget, wx.adv.GenericCalendarCtrl):
    """
    Calendar widget based on PySide6.
    Calendars support a date-changed event and have a selection status value.
    Language setting is not supported by wxPython.
    """

    def __init__(self, **kwargs):
        """Initialize the calendar.

        :param kwargs: additional parameters for superclass
        """
        wx.adv.GenericCalendarCtrl.__init__(self, kwargs['parent']._WindowClass__panel, style=wx.adv.CAL_MONDAY_FIRST)
        super().__init__(**kwargs)
        self.Bind(wx.adv.EVT_CALENDAR_SEL_CHANGED, self._on_date_changed)

    def _on_date_changed(self, _event):
        """Executed when the date is changed by the user."""
        self.on_date_changed(self)

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
            wx_lower_date = wx.DateTime.FromDMY(date_as_tuple[2], date_as_tuple[1] - 1, date_as_tuple[0])
        else:
            wx_lower_date = wx.DefaultDateTime
        if self.upper_date is not None:
            date_as_tuple = self.upper_date.timetuple()
            wx_upper_date = wx.DateTime.FromDMY(date_as_tuple[2], date_as_tuple[1] - 1, date_as_tuple[0])
        else:
            wx_upper_date = wx.DefaultDateTime
        self.SetDateRange(lowerdate=wx_lower_date, upperdate=wx_upper_date)

    @property
    def selected_date(self):
        """Return the current selected date.

        :return: the current selected date
        """
        wx_date = self.GetDate()
        datetime_date = datetime.date(year=wx_date.year, month=wx_date.month + 1, day=wx_date.day)
        super(Calendar, Calendar).selected_date.__set__(self, datetime_date)
        return super(Calendar, Calendar).selected_date.__get__(self)

    @selected_date.setter
    def selected_date(self, date):
        """Set the selected date.

        :param date: the new selected date
        """
        super(Calendar, Calendar).selected_date.__set__(self, date)
        date_as_tuple = super(Calendar, Calendar).selected_date.__get__(self).timetuple()
        self.SetDate(wx.DateTime.FromDMY(date_as_tuple[2], date_as_tuple[1] - 1, date_as_tuple[0]))

    def set_language(self, language_code):
        """Set the language of the calender: NOT supported by wxPython.

        :param language_code: the new language to use (code according to ISO639)
        """
        pass


class SpinControl(AbstractSpinControl, _Widget, wx.SpinCtrl):
    """Spin control widget based on wxPython. Spin controls support a value-changed event and have a status value."""

    def __init__(self, **kwargs):
        """Initialize the spin control

        :param kwargs: additional parameters for superclass
        """
        wx.SpinCtrl.__init__(self, kwargs['parent']._WindowClass__panel, style=wx.SP_ARROW_KEYS)
        super().__init__(**kwargs)
        self.Bind(wx.EVT_CHAR, lambda event: None)
        self.Bind(wx.EVT_SET_FOCUS, lambda event: None)
        self.Bind(wx.EVT_SPINCTRL, self._on_value_changed)

    def _on_value_changed(self, _event):
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
            self.SetMin(self.min_value)
        else:
            self.SetMin(self._DEFAULT_MIN_VALUE)

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
            self.SetMax(self.max_value)
        else:
            self.SetMax(self._DEFAULT_MAX_VALUE)

    @property
    def value(self):
        """Return the current value.

        :return: the current value
        """
        super(SpinControl, SpinControl).value.__set__(self, self.GetValue())
        return super(SpinControl, SpinControl).value.__get__(self)

    @value.setter
    def value(self, value):
        """Set the value (clipping between minimum and maximum allowed values if necessary).

        :param value: the new value
        """
        super(SpinControl, SpinControl).value.__set__(self, value)
        self.SetValue(super(SpinControl, SpinControl).value.__get__(self))


class Menu(AbstractMenu, _Widget, wx.Menu):
    """
    Menu widget based on wxPython.
    Menus allow to create a tree of items which the user can click; each item can in turn be a menu.
    """

    def __init__(self, **kwargs):
        """Initialize the menu.

        :param kwargs: additional parameters for superclass
        """
        wx.Menu.__init__(self)
        super().__init__(**kwargs)
        self.Bind(wx.EVT_MENU_CLOSE, self._on_close)

    def _on_click(self, item):
        """Executed when a menu item is clicked.

        :param item: the string corresponding to the clicked item
        """
        self.on_click(self, item)

    def pop_up(self):
        """Build and show the menu as a pop-up."""
        super().pop_up()
        self._parent.PopupMenu(self)
        self.Destroy()

    def _append_separator(self, target):
        """
        Append a separator to the target, which can be the menu object itself (for pop-up menus or
        branches of a menu tree) or a window menubar.
        Separators are not shown in menubars in wxPython.

        :param target: the target where the menu has to be appended (menu object itself or window menubar)
        """
        if isinstance(target, wx.MenuBar):
            return
        else:
            target.Append(wx.ID_SEPARATOR)

    def _append_menu(self, target, menu, is_enabled):
        """
        Append a menu to the target, which can be the menu object itself (for pop-up menus or
        branches of a menu tree) or a window menubar.

        :param target: the target where the menu has to be appended (menu object itself or window menubar)
        :param item: the menu to append
        :param is_enabled: boolean defining if the menu is enabled
        """
        if isinstance(target, wx.MenuBar):
            menu._build_menu(inherited_on_click=self.on_click)
            target.Append(menu, menu.label)
            target.EnableTop(target.GetMenuCount() - 1, is_enabled)
        else:
            menu._build_menu(inherited_on_click=self.on_click)
            entry = target.AppendSubMenu(menu, menu.label)
            target.Enable(entry.GetId(), is_enabled)

    def _append_simple_item(self, target, item, is_enabled, on_item_click):
        """
        Append a simple string item to the target, which can be a the menu object itself (for pop-up menus or
        branches of a menu tree) or a window menubar.

        :param target: the target where the item has to be appended (menu object itself or window menubar)
        :param item: the item to append
        :param is_enabled: boolean defining if the item is enabled
        :param on_item_click: function to be executed if the item is clicked
        """
        if isinstance(target, wx.MenuBar):
            bridge_menu = wx.Menu()
            target.Append(bridge_menu, item)
            if on_item_click is not None:
                bridge_menu.Bind(wx.EVT_MENU_OPEN, lambda event: on_item_click(self))
            else:
                bridge_menu.Bind(wx.EVT_MENU_OPEN, lambda event, i=item: self._on_click(i))
            target.EnableTop(target.GetMenuCount() - 1, is_enabled)
        else:
            entry = target.Append(wx.ID_ANY, item)
            if on_item_click is not None:
                target.Bind(wx.EVT_MENU, lambda event: on_item_click(self), entry)
            else:
                target.Bind(wx.EVT_MENU, lambda event, i=item: self._on_click(i), entry)
            target.Enable(entry.GetId(), is_enabled)

    def _on_close(self, event):
        """Executed when the menu is closed."""
        self.on_close(self)


class TextTimedMenu(AbstractTextTimedMenu, wx.PopupWindow):
    """
    Text timed menu based on wxPython; these are menus built with text labels, which close automatically after a
    specified time when the mouse cursor leaves.
    """

    def __init__(self, **kwargs):
        """Initialize the timed text menu.

        :param kwargs: additional parameters for superclass
        """
        wx.PopupWindow.__init__(self, kwargs['parent']._WindowClass__panel)
        super().__init__(**kwargs)

        self._panel = wx.Panel(self)
        self._sizer = wx.BoxSizer(wx.VERTICAL)
        self._panel.SetSizer(self._sizer)
        self._frame_sizer = wx.BoxSizer(wx.VERTICAL)
        self._frame_sizer.Add(self._panel)
        self.Bind(wx.EVT_CLOSE, self._on_close)

    def pop_up(self, *, modal=False):
        """Build and show the menu as a pop-up. It can be shown as a modal, forcing interaction from the user.

        :param modal: specifies if the text timed menu should be modal or not
        """
        super().pop_up()
        self.SetSizerAndFit(self._frame_sizer)
        self.Position(wx.GetMousePosition(), (10, 10))
        self.make_modal(modal)
        self.Show()

    def make_modal(self, modal):
        """Make the menu modal or not based on the specified boolean flag.

        :param modal: boolean determining if the menu should be made modal or not
        """
        if modal and not hasattr(self, '_disabler'):
            self._disabler = wx.WindowDisabler(self)
        if not modal and hasattr(self, '_disabler'):
            del self._disabler

    def _create_text(self, label):
        """Create a Text widget with the specified label.

        :param label: the desired text label
        :return: the created Text widget
        """
        if label == self.SEPARATOR:
            label = ""
        # It is necessary to put the Text inside a wx.Panel,
        # because under Linux the wx.StaticText
        # does not receive enter and leave events
        text_parent = SimpleNamespace()
        text_parent._WindowClass__panel = wx.Panel(self._panel)
        text = Text(parent=text_parent, label=label)
        text_parent._WindowClass__panel.Bind(wx.EVT_ENTER_WINDOW, text._on_mouse_enter)
        text_parent._WindowClass__panel.Bind(wx.EVT_LEAVE_WINDOW, text._on_mouse_leave)
        self._sizer.Add(text_parent._WindowClass__panel, flag=wx.EXPAND)
        return text

    def _set_normal_color(self, text):
        """Set the normal color (not selected item) to a Text widget.

        :param text: the text widget to configure
        """
        super()._set_normal_color(text)
        panel = text.GetParent()
        panel.SetForegroundColour(self._FOREGROUND_NORMAL_COLOR)
        panel.SetBackgroundColour(self._BACKGROUND_NORMAL_COLOR)

    def _set_highlight_color(self, text):
        """Set the highlight color (selected item) to a Text widget.

        :param text: the text widget to configure
        """
        super()._set_highlight_color(text)
        panel = text.GetParent()
        panel.SetForegroundColour(self._FOREGROUND_HIGHLIGHT_COLOR)
        panel.SetBackgroundColour(self._BACKGROUND_HIGHLIGHT_COLOR)

    def _set_disabled_color(self, text):
        """Set the disabled color (disabled item, that is not selectable) to a Text widget.

        :param text: the text widget to configure
        """
        super()._set_disabled_color(text)
        panel = text.GetParent()
        panel.SetForegroundColour(self._FOREGROUND_DISABLED_COLOR)
        panel.SetBackgroundColour(self._BACKGROUND_DISABLED_COLOR)

    def _close(self):
        """Close the menu."""
        super()._close()
        self.make_modal(False)
        self.Close()
        wx.CallAfter(self.Destroy)

    def _on_mouse_enter_item(self, obj):
        """
        Executed when the mouse enters an item; change the item to highlight color and call the widget
        _on_mouse_enter function.

        :param obj: the text widget where the event has occurred
        """
        super()._on_mouse_enter_item(obj)
        self.Refresh()

    def _on_mouse_leave_item(self, obj):
        """
        Executed when the mouse leaves an item; change the item to normal color and call the widget
        _on_mouse_leave function if the mouse is no longer in the menu widget.

        :param obj: the text widget where the event has occurred
        """
        super()._on_mouse_leave_item(obj)
        self.Refresh()

    def _on_close(self, _event):
        """Executed when the menu is closed."""
        self.on_close(self)
