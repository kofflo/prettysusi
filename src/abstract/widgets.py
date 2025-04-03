"""
Definition of the abstract widget classes supported by the library.
The details of the implementation for each supported widget type are defined in the concrete subclasses.

Classes:
    TextStyle: enumeration used to define the style of texts
    AbstractWidget: superclass for the all widget classes, including Table (not to be instantiated)
    AbstractMouseEventsWidget: superclass for all the widgets which manage raw mouse events (not to be instantiated)
    AbstractLabelledWidget: superclass for all the widgets which display a label (not to be instantiated)
    AbstractButton: superclass for all the button-like widgets (not to be instantiated)
    AbstractCheckBox: superclass for checkbox widgets (not to be instantiated)
    AbstractRadioBox: superclass for radiobox widgets (not to be instantiated)
    AbstractBitmap: superclass for bitmap widgets (not to be instantiated)
    AbstractText: superclass for text widgets (not to be instantiated)
    AbstractCalendar: superclass for calendar widgets (not to be instantiated)
    AbstractSpinControl: superclass for spin control widgets (not to be instantiated)
    AbstractMenu: superclass for menu widgets (not to be instantiated)
    AbstractTimedMenu: superclass for all menu widgets which persist for a defined time (not to be instantiated)
    AbstractTextTimedMenu: superclass for menu widgets implemented with text widgets (not to be instantiated)
"""
from enum import Enum, auto
import datetime
from threading import Timer

from .. import BaseClass


class TextStyle(Enum):
    """Enum class defining the supported text styles."""
    NORMAL = auto()
    BOLD = auto()
    ITALIC = auto()
    BOLD_ITALIC = auto()


class AbstractWidget(BaseClass):
    """
    Base class for all widgets. This class should not be instantiated.
    A widget is any element which is displayed in a window and can be organized in a layout.
    """

    def __init__(self, *, parent, is_enabled=True, is_hidden=False):
        """Initialize the widget.

        :param parent: window object in which the widget is contained
        :param is_enabled: boolean defining if the widget is enabled
        :param is_hidden: boolean defining if the widget is hidden
        """
        self._parent = parent
        self._is_enabled = is_enabled
        self._is_hidden = is_hidden

    @property
    def is_enabled(self):
        """Return the current enabled status of the widget. If not enabled, the user cannot interact with the widget.

        :return: the enabled status of the widget
        """
        return self._is_enabled

    def enable(self, is_enabled):
        """Set the enabled status of the widget. If not enabled, the user cannot interact with the widget.

        :param is_enabled: the new enabled status
        """
        self._is_enabled = is_enabled

    @property
    def is_hidden(self):
        """Return the current hidden status of the widget. If hidden, the widget is not displayed.

        :return: the hidden status of the widget
        """
        return self._is_hidden

    def hide(self, is_hidden):
        """Set the hidden status of the widget. If hidden, the widget is not displayed.

        :param is_hidden: the new hidden status
        """
        self._is_hidden = is_hidden


class AbstractMouseEventsWidget(AbstractWidget):
    """
    Base class for all widgets managing raw mouse events. This class should not be instantiated.
    The events supported are left and right mouse button down or up; wheel movement; mouse movement;
    mouse entering or leaving the widget.
    """

    def on_left_down(self, obj, position):
        """User-defined function executed when the left button is pressed on the widget.

        :param obj: the widget where the event has occurred
        :param position: the local position of the mouse cursor on the widget where the left button has been pressed
        """
        pass

    def on_left_up(self, obj, position):
        """User-defined function executed when the left button is released on the widget.

        :param obj: the widget where the event has occurred
        :param position: the local position of the mouse cursor on the widget where the left button has been released
        """
        pass

    def on_right_down(self, obj, position):
        """User-defined function executed when the right button is pressed on the widget.

        :param obj: the widget where the event has occurred
        :param position: the local position of the mouse cursor on the widget where the right button has been pressed
        """
        pass

    def on_right_up(self, obj, position):
        """User-defined function executed when the right button is released on the widget.

        :param obj: the widget where the event has occurred
        :param position: the local position of the mouse cursor on the widget where the right button has been released
        """
        pass

    def on_wheel(self, obj, position, rotation):
        """User-defined function executed when the wheel is scrolled on the widget.

        :param obj: the widget where the event has occurred
        :param position: the local position of the mouse cursor on the widget where the wheel has been scrolled
        :param rotation: the wheel rotation in units (usually multiple of 120; positive for an upward rotation)
        """
        pass

    def on_mouse_motion(self, obj, position):
        """User-defined function executed when the mouse cursor is moved on the widget.

        :param obj: the widget where the event has occurred
        :param position: the local position of the mouse cursor on the widget
        """
        pass

    def on_mouse_enter(self, obj):
        """User-defined function executed when the mouse cursor enters the widget.

        :param obj: the widget where the event has occurred
        """
        pass

    def on_mouse_leave(self, obj):
        """User-defined function executed when the mouse cursor leaves the widget.

        :param obj: the widget where the event has occurred
        """
        pass


class AbstractLabelledWidget(AbstractWidget):
    """Base class for all widgets which display a label. This class should not be instantiated."""

    def __init__(self, *, label="", **kwargs):
        """Initialize the labelled widget.

        :param label: the label value (string)
        :param kwargs: additional parameters for superclass
        """
        super().__init__(**kwargs)
        self.label = label

    @property
    def label(self):
        """Return the current value of the label.

        :return: the current value of the label
        """
        return self._label

    @label.setter
    def label(self, label):
        """Set the value of the label.

        :param label: the new value of the label (string)
        """
        self._label = label


class AbstractButton(AbstractLabelledWidget):
    """
    Base class for all button-like widgets. This class should not be instantiated.
    Buttons are widgets which display a label and support a click event; this includes simple buttons,
    as well as checkbox and radiobox widgets and menus.
    """

    def __init__(self, *, on_click=None, **kwargs):
        """Initialize the button.

        :param on_click: the function to be executed when the button is clicked
        :param kwargs: additional parameters for superclass
        """
        super().__init__(**kwargs)
        if on_click is not None:
            self.on_click = on_click

    def on_click(self, obj):
        """User-defined function executed when the button is clicked.

        :param obj: the widget where the event has occurred
        """
        pass


class AbstractCheckBox(AbstractButton):
    """
    Base class for checkbox widgets. This class should not be instantiated.
    Checkbox widgets display a label, support a click event and have a boolean status value.
    """

    def __init__(self, *, value=False, **kwargs):
        """Initialize the checkbox.

        :param value: the initial status value of the checkbox (boolean)
        :param kwargs: additional parameters for the superclass
        """
        super().__init__(**kwargs)
        self.value = value

    @property
    def value(self):
        """Return the current status value of the checkbox.

        :return: the current status value of the checkbox
        """
        return self._value

    @value.setter
    def value(self, value):
        """Set the status value of the checkbox.

        :param value: the new status value (boolean)
        """
        self._value = value


class AbstractRadioBox(AbstractButton):
    """
    Base class for radiobox widgets. This class should not be instantiated.
    Radiobox widgets display a label and one or more choices, support a click event and have a selection status value.
    """

    def __init__(self, *, choices=None, num_choices=1, selection=0,  **kwargs):
        """Initialize the radiobox.

        :param choices: the list of choices to display; if empty, one choice is displayed
        :param num_choices: the number of choices to be displayed (only used if choices is None)
        :param selection: the initial selected choice (0-based; forced to 0 if higher than the number of choices)
        :param kwargs: additional parameters for the superclass
        """
        super().__init__(**kwargs)
        if choices is None:
            self._choices = [''] * max(num_choices, 1)
        elif len(choices) == 0:
            self._choices = ['']
        else:
            self._choices = choices
        if 0 <= selection < len(self._choices):
            self._selection = selection
        else:
            self._selection = 0

    @property
    def selection(self):
        """Return the current selected choice.

        :return: the current selected choice (0-based)
        """
        return self._selection

    @selection.setter
    def selection(self, selection):
        """Set the selected choice.

        :param selection: the new selected choice (0-based)
        """
        if 0 <= selection < len(self._choices):
            self._selection = selection

    def set_choice(self, index, string):
        """Set the string to display for a choice.

        :param index: the index of the choice (0-based)
        :param string: the new string to display for the choice
        """
        if 0 <= index < len(self._choices):
            self._choices[index] = string


class AbstractBitmap(AbstractMouseEventsWidget):
    """
    Base class for bitmap widgets. This class should not be instantiated.
    Bitmaps support raw mouse events. The image to display must be a PIL Image object.
    """

    def __init__(self, *, bitmap=None, **kwargs):
        """Initialize the bitmap

        :param bitmap: the initial bitmap (PIL Image object)
        :param kwargs: additional parameters for the superclass
        """
        self.bitmap = bitmap
        super().__init__(**kwargs)

    @property
    def bitmap(self):
        """Return the current displayed bitmap.

        :return: the current displayed bitmap
        """
        return self._bitmap

    @bitmap.setter
    def bitmap(self, bitmap):
        """Set the bitmap to display.

        :param bitmap: the bitmap to display (PIL Image object)
        """
        self._bitmap = bitmap


class AbstractText(AbstractLabelledWidget, AbstractMouseEventsWidget):
    """
    Base class for text widgets. This class should not be instantiated.
    Text widgets display a label (with the possibility to change color, size and style) and support raw mouse events.
    """

    def __init__(self, *, text_style=TextStyle.NORMAL, text_size=9,
                 foreground_color=None, background_color=None,
                 **kwargs):
        """Initialize the text widget.

        :param text_style: the initial text style (TextStyle enum)
        :param text_size: the initial text size
        :param foreground_color: the initial foreground color (three-element tuple of RGB values between 0 and 255)
        :param background_color: the initial background color (three-element tuple of RGB values between 0 and 255)
        :param kwargs: additional parameters for the superclass
        """
        super().__init__(**kwargs)
        self._text_size = text_size
        self.text_style = text_style
        self.text_size = text_size
        self._background_color = None
        self.foreground_color = foreground_color
        self.background_color = background_color

    @property
    def text_style(self):
        """Return the current text style.

        :return: the current text style
        """
        return self._text_style

    @text_style.setter
    def text_style(self, text_style):
        """Set the text style.

        :param text_style: the new text style (TextStyle enum)
        """
        self._text_style = text_style

    @property
    def text_size(self):
        """Return the current text size.

        :return: the current text size
        """
        return self._text_size

    @text_size.setter
    def text_size(self, text_size):
        """Set the text size.

        :param text_style: the new text size
        """
        self._text_size = text_size

    @property
    def foreground_color(self):
        """Return the current foreground color.

        :return: the current foreground color
        """
        return self._foreground_color

    @foreground_color.setter
    def foreground_color(self, foreground_color):
        """Set the foreground color.

        :param foreground_color: the new foreground color (three-element tuple of RGB values between 0 and 255)
        """
        self._foreground_color = foreground_color

    @property
    def background_color(self):
        """Return the current background color.

        :return: the current background color
        """
        return self._background_color

    @background_color.setter
    def background_color(self, background_color):
        """Set the background color.

        :param background_color: the new background color (three-element tuple of RGB values between 0 and 255)
        """
        self._background_color = background_color

    def on_change(self, obj):
        """User-defined function executed when the text inside a text widget is changed by the user.

        :param obj: the widget where the event has occurred
        """
        pass


class AbstractCalendar(AbstractWidget):
    """
    Base class for calendar widgets. This class should not be instantiated.
    Calendars support a date-changed event and have a selection status value.
    Different languages are also supported depending on the specific GUI.
    """

    def __init__(self, *, lower_date=None, upper_date=None, selected_date=None, on_date_changed=None, **kwargs):
        """Initialize the calendar.

        :param lower_date: the initial first allowed date for selection
        :param upper_date: the initial last allowed date for selection
        :param selected_date: the initial selected date
        :param on_date_changed: the function to be executed when the selected date is changed
        :param kwargs: additional parameters for the superclass
        """
        super().__init__(**kwargs)
        if selected_date is None:
            selected_date = datetime.date.today()
        self._selected_date = selected_date
        self._upper_date = upper_date
        self.lower_date = lower_date
        self.upper_date = upper_date
        self.selected_date = selected_date
        if on_date_changed is not None:
            self.on_date_changed = on_date_changed

    @property
    def lower_date(self):
        """Return the current first allowed date for selection.

        :return: the current first allowed date for selection
        """
        return self._lower_date

    @lower_date.setter
    def lower_date(self, lower_date):
        """Set the first allowed date for selection.

        :param lower_date: the new first allowed date for selection
        """
        if lower_date is None or self._upper_date is None or lower_date <= self._upper_date:
            self._lower_date = lower_date
        if self._lower_date is not None and self.selected_date < self._lower_date:
            self.selected_date = self._lower_date

    @property
    def upper_date(self):
        """Return the current last allowed date for selection.

        :return: the current last allowed date for selection
        """
        return self._upper_date

    @upper_date.setter
    def upper_date(self, upper_date):
        """Set the last allowed date for selection.

        :param upper_date: the new last allowed date for selection
        """
        if upper_date is None or self._lower_date is None or upper_date >= self._lower_date:
            self._upper_date = upper_date
        if self._upper_date is not None and self.selected_date > self._upper_date:
            self.selected_date = self._upper_date

    @property
    def selected_date(self):
        """Return the current selected date.

        :return: the current selected date
        """
        return self._selected_date

    @selected_date.setter
    def selected_date(self, date):
        """Set the selected date.

        :param date: the new selected date
        """
        if (self._lower_date is None or date >= self._lower_date) and \
           (self._upper_date is None or date <= self._upper_date):
            self._selected_date = date

    def on_date_changed(self, obj):
        """User-defined function executed when the selected date is changed.

        :param obj: the widget where the event has occurred
        """
        pass

    def set_language(self, language_code):
        """Set the language of the calender (as supported by the GUI)

        :param language_code: the new language to use (code according to ISO639)
        """
        raise NotImplementedError


class AbstractSpinControl(AbstractWidget):
    """
    Base class for spin control widgets. This class should not be instantiated.
    Spin controls support a value-changed event and have a status value.
    """

    _DEFAULT_MIN_VALUE = 0
    _DEFAULT_MAX_VALUE = 99

    def __init__(self, *, min_value=None, max_value=None, value=0, on_value_changed=None, **kwargs):
        """Initialize the spin control.

        :param min_value: the initial minimum allowed value
        :param max_value: the initial maximum allowed value
        :param value: the initial value
        :param on_value_changed: function to execute when the value is changed
        :param kwargs: additional parameters for the superclass
        """
        super().__init__(**kwargs)
        self._value = value
        self._max_value = max_value
        self.min_value = min_value
        self.max_value = max_value
        self.value = value
        if on_value_changed is not None:
            self.on_value_changed = on_value_changed

    @property
    def min_value(self):
        """Return the current minimum allowed value.

        :return: the current minimum allowed value
        """
        return self._min_value

    @min_value.setter
    def min_value(self, min_value):
        """Set the minimum allowed value.

        :param min_value: the new minimum allowed value
        """
        if min_value is None or self._max_value is None or min_value <= self._max_value:
            self._min_value = min_value
        if self._min_value is not None and self.value < self._min_value:
            self.value = self._min_value

    @property
    def max_value(self):
        """Return the current maximum allowed value.

        :return: the current maximum allowed value
        """
        return self._max_value

    @max_value.setter
    def max_value(self, max_value):
        """Set the maximum allowed value.

        :param max_value: the new maximum allowed value
        """
        if max_value is None or self._min_value is None or max_value >= self._min_value:
            self._max_value = max_value
        if self._max_value is not None and self.value > self._max_value:
            self.value = self._max_value

    @property
    def value(self):
        """Return the current value.

        :return: the current value
        """
        return self._value

    @value.setter
    def value(self, value):
        """Set the value (clipping between minimum and maximum allowed values if necessary).

        :param value: the new value
        """
        if self._min_value is not None and value < self._min_value:
            value = self._min_value
        if self._max_value is not None and value > self._max_value:
            value = self._max_value
        self._value = value

    def on_value_changed(self, obj):
        """User-defined function executed when the spin control value is changed.

        :param obj: the widget where the event has occurred
        """
        pass


class AbstractMenu(AbstractLabelledWidget):
    """
    Base class for menu widgets. This class should not be instantiated.
    Menus allow to create a tree of items which the user can click; each item can in turn be a menu.
    """

    SEPARATOR = None

    def __init__(self, *, items=None, on_click=None, inherit_on_click=False, **kwargs):
        """Initialize the menu.

        :param items: list defining the initial menu items; each entry of the list can be a single item or a tuple of
         three elements, representing the item, the enabled flag and the function to be executed if the item is clicked;
         each item can be a string or a menu object
        :param on_click: the function to be executed if the menu is clicked
        :param kwargs: additional parameters for the superclass
        """
        super().__init__(**kwargs)
        self._items = []
        if items is not None:
            for item in items:
                if isinstance(item, list) or isinstance(item, tuple):
                    self._items.append(item)
                else:
                    self._items.append((item, True, None))
        if on_click is not None:
            self.on_click = on_click
        self.inherit_on_click = inherit_on_click
        self._built = False

    @property
    def inherit_on_click(self):
        """Return the "inherit on-click" property. If true, the function executed when the menu is clicked is inherited
        from upper-level in a menu tree.

        :return: the value of the "inherit on-click" property
        """
        return self._inherit_on_click

    @inherit_on_click.setter
    def inherit_on_click(self, inherit_on_click):
        """Set the "inherit on-click" property.

        :param inherit_on_click: the new value of the "inherit on-click" property
        """
        self._inherit_on_click = inherit_on_click

    def append(self, item, enabled=True, on_item_click=None):
        """Append a new item to the menu. Must be called before the menu has been built or else it will have no effect.

        :param item: the item to append; can be a string or a menu object
        :param enabled: flag defining if the item is enabled
        :param on_item_click: the function to be executed if the item is clicked
        """
        self._items.append((item, enabled, on_item_click))

    def pop_up(self):
        """Build and show the menu as a pop-up."""
        self._build_menu()

    def attach_menubar(self, menubar):
        """Build and show the menu as window menubar."""
        self._build_menu(menubar=menubar)

    def on_click(self, obj, item):
        """User-defined function, executed if the menu is clicked.

        :param obj: the menu object where the click occured
        :param item: the clicked item
        """
        pass

    def on_close(self, obj):
        """
        User-defined function, executed when the menu is closed.
        This is not supported by tk when the submenu in a menubar is closed.

        :param obj: the closed menu object
        """
        pass

    def _build_menu(self, menubar=None, inherited_on_click=None):
        """
        Build the menu. A menu can only be built once: a new instance has to be created if the same menu needs to be
        used again.

        :param menubar: frame menubar where the menu have to be built (None to create an independent menu)
        :param inherited_on_click: function to execute when the menu is clicked, if property inherit_on_click is True
        """
        if self._built:
            raise Exception("The menu has already been built once. It is forbidden to built a menu more than once.")
        if self.inherit_on_click is True and inherited_on_click is not None:
            self.on_click = inherited_on_click
        for menu_id, value in enumerate(self._items):
            item, is_enabled, on_item_click = value
            if menubar is not None:
                self._append_item(menubar, item, is_enabled, on_item_click)
            else:
                self._append_item(self, item, is_enabled, on_item_click)
        self._built = True

    def _append_item(self, target, item, is_enabled, on_item_click):
        """
        Append an item to the target, which can be the menu object itself (for pop-up menus or
        branches of a menu tree) or a window menubar.

        :param target: the target where the item has to be appended (menu object itself or window menubar)
        :param item: the item to append; can be a simple string or a menu
        :param is_enabled: boolean defining if the item is enabled
        :param on_item_click: function to be executed if the item is clicked
        """
        if item == AbstractMenu.SEPARATOR:
            self._append_separator(self)
        elif isinstance(item, AbstractMenu):
            self._append_menu(target, item, is_enabled)
        else:
            self._append_simple_item(target, item, is_enabled, on_item_click)

    def _append_menu(self, target, menu, is_enabled):
        """
        Append a menu to the target, which can be the menu object itself (for pop-up menus or
        branches of a menu tree) or a window menubar.

        :param target: the target where the menu has to be appended (menu object itself or window menubar)
        :param item: the menu to append
        :param is_enabled: boolean defining if the menu is enabled
        """
        raise NotImplementedError

    def _append_simple_item(self, target, item, is_enabled, on_item_click):
        """
        Append a simple string item to the target, which can be a the menu object itself (for pop-up menus or
        branches of a menu tree) or a window menubar.

        :param target: the target where the item has to be appended (menu object itself or window menubar)
        :param item: the item to append
        :param is_enabled: boolean defining if the item is enabled
        :param on_item_click: function to be executed if the item is clicked
        """
        raise NotImplementedError

    def _append_separator(self, target):
        """
        Append a separator to the target, which can be the menu object itself (for pop-up menus or
        branches of a menu tree) or a window menubar. Not all GUI support separators for menubars.

        :param target: the target where the menu has to be appended (menu object itself or window menubar)
        """
        raise NotImplementedError


class AbstractTimedMenu(AbstractMenu):
    """
    Base class for timed menu widgets, which close automatically after a specified time when the mouse cursor leaves.
    This class should not be instantiated.
    Menus allow to create a tree of items which the user can click; each item can in turn be a menu.
    The timed menu manages mouse enter and mouse leave events.
    """

    _TIMER_DURATION = 0.2

    def __init__(self, **kwargs):
        """Initialize the timed menu.

        :param kwargs: additional parameters for superclass
        """
        super().__init__(**kwargs)
        self._timer = None

    def command_close(self):
        """Command the menu to close when the specified time interval has passed."""
        if self._timer is None and not self._mouse_inside_widget():
            self._timer = Timer(self._TIMER_DURATION, self._close)
            self._timer.start()

    def force_close(self):
        """Force the menu to close without waiting for the specified time interval."""
        if self._timer is not None:
            self._timer.cancel()
            self._timer = None
        self._close()

    def prevent_close(self):
        """Prevent the menu from closing and reset the timer."""
        if self._timer is not None:
            self._timer.cancel()
            self._timer = None

    def _close(self):
        """Close the menu."""
        if self._timer is not None:
            self._timer.cancel()
        else:
            self._timer = None

    def _on_mouse_enter(self, obj):
        """Prevent the closing of the menu when the mouse enters the widget and call the user-defined function.

        :param obj: the menu object that the mouse has entered
        """
        self.prevent_close()
        self.on_mouse_enter(obj)

    def _on_mouse_leave(self, obj):
        """Command the closing of the menu when the mouse leaves the widget and call the user-defined function.

        :param obj: the menu object that the mouse has left
        """
        self.command_close()
        self.on_mouse_leave(obj)

    def on_mouse_enter(self, obj):
        """User-defined function executed when the mouse enters the menu.

        :param obj: the widget where the event has occurred
        """
        pass

    def on_mouse_leave(self, obj):
        """User-defined function executed when the mouse leaves the menu.

        :param obj: the widget where the event has occurred
        """
        pass

    def _mouse_inside_widget(self):
        """Return True if the mouse is inside the widget, False otherwise.

        :return: True if the mouse is inside the widget, False otherwise
        """
        raise NotImplementedError


class AbstractTextTimedMenu(AbstractTimedMenu):
    """
    Base class for timed menu widgets created with Text labels.
    Different text foreground and background colors are used to indicate the currently selected item and disabled items.
    Text timed menus cannot be attached as menubars to windows.
    This class should not be instantiated.
    """

    _FOREGROUND_NORMAL_COLOR = (0, 0, 0)
    _BACKGROUND_NORMAL_COLOR = (255, 255, 255)
    _FOREGROUND_HIGHLIGHT_COLOR = (255, 255, 255)
    _BACKGROUND_HIGHLIGHT_COLOR = (0, 120, 215)
    _FOREGROUND_DISABLED_COLOR = (80, 80, 80)
    _BACKGROUND_DISABLED_COLOR = (255, 255, 255)

    def __init__(self, **kwargs):
        """Initialize the text timed menu.

        :param kwargs: additional parameters for superclass
        """
        super().__init__(**kwargs)
        self._mouse_inside = {}
        self._texts = {}

    def attach_menubar(self, menubar):
        """Use as window menubar not supported by text timed menus."""
        raise Exception("Use as window menubar not supported by text timed menus.")

    def _create_text(self, label):
        """Create a Text widget with the specified label.

        :param label: the desired text label
        :return: the created Text widget
        """
        raise NotImplementedError

    def _append_item(self, target, item, is_enabled, on_item_click):
        """
        Append an item to the target, which must be the menu object itself.
        Both simple string items or menus can be appended, but menus are flattened out and all their items are appended
        at the higher level.

        :param target: the target where the item has to be appended (the menu object itself)
        :param item: the item to append; can be a simple string or a menu
        :param is_enabled: boolean defining if the item is enabled
        :param on_item_click: function to be executed if the item is clicked
        """
        if isinstance(item, AbstractMenu):
            for menu_id, value in enumerate(item._items):
                sub_item, sub_is_enabled, sub_on_item_click = value
                self._append_item(target, sub_item, sub_is_enabled and is_enabled, sub_on_item_click)
        else:
            text = self._create_text(label=item)
            self._mouse_inside[text] = False
            self._texts[text] = item
            if item is not AbstractMenu.SEPARATOR and is_enabled:
                if on_item_click is not None:
                    text.on_left_down = lambda obj, pos: (self._close(), on_item_click(self))
                    text.on_right_down = lambda obj, pos: (self._close(), on_item_click(self))
                else:
                    text.on_left_down = lambda obj, pos, i=item: self._on_item_click(i)
                    text.on_right_down = lambda obj, pos, i=item: self._on_item_click(i)
                text.on_mouse_enter = self._on_mouse_enter_item
                text.on_mouse_leave = self._on_mouse_leave_item
                self._set_normal_color(text)
            else:
                text.on_mouse_enter = self._on_mouse_enter_disabled_item
                text.on_mouse_leave = self._on_mouse_leave_disabled_item
                self._set_disabled_color(text)

    def _set_normal_color(self, text):
        """Set the normal color (not selected item) to a Text widget.

        :param text: the text widget to configure
        """
        text.foreground_color = self._FOREGROUND_NORMAL_COLOR
        text.background_color = self._BACKGROUND_NORMAL_COLOR

    def _set_highlight_color(self, text):
        """Set the highlight color (selected item) to a Text widget.

        :param text: the text widget to configure
        """
        text.foreground_color = self._FOREGROUND_HIGHLIGHT_COLOR
        text.background_color = self._BACKGROUND_HIGHLIGHT_COLOR

    def _set_disabled_color(self, text):
        """Set the disabled color (disabled item, that is not selectable) to a Text widget.

        :param text: the text widget to configure
        """
        text.foreground_color = self._FOREGROUND_DISABLED_COLOR
        text.background_color = self._BACKGROUND_DISABLED_COLOR

    def _on_mouse_enter_item(self, obj):
        """
        Executed when the mouse enters an item; change the item to highlight color and call the widget
        _on_mouse_enter function.

        :param obj: the text widget where the event has occurred
        """
        self._mouse_inside[obj] = True
        self._set_highlight_color(obj)
        self._on_mouse_enter(self)

    def _on_mouse_leave_item(self, obj):
        """
        Executed when the mouse leaves an item; change the item to normal color and call the widget
        _on_mouse_leave function if the mouse is no longer in the menu widget.

        :param obj: the text widget where the event has occurred
        """
        self._mouse_inside[obj] = False
        self._set_normal_color(obj)
        if not self._mouse_inside_widget():
            self._on_mouse_leave(self)

    def _on_mouse_enter_disabled_item(self, obj):
        """Executed when the mouse enters a disabled item; call the widget _on_mouse_enter function.

        :param obj: the text widget where the event has occurred
        """
        self._mouse_inside[obj] = True
        self._on_mouse_enter(self)

    def _on_mouse_leave_disabled_item(self, obj):
        """
        Executed when the mouse leaves a disabled item; call the widget _on_mouse_leave function
        if the mouse is no longer in the menu widget.

        :param obj: the text widget where the event has occurred
        """
        self._mouse_inside[obj] = False
        if not self._mouse_inside_widget():
            self._on_mouse_leave(self)

    def _on_item_click(self, item):
        """Executed if one of the item is clicked; close the menu and execute the user-defined function for the item.

        :param item: the clicked item
        """
        self._close()
        self.on_click(self, item)

    def _mouse_inside_widget(self):
        """Return True if the mouse is inside the widget, False otherwise.

        :return: True if the mouse is inside the widget, False otherwise
        """
        return any(self._mouse_inside.values())
