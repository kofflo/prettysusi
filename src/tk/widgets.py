import tkinter
import tkinter.font
import tkinter.ttk
import tkcalendar
from tkinter import DISABLED, NORMAL, END

from PIL import ImageTk
from threading import Timer

from ..abstract.widgets import AbstractWidget, AbstractMouseEventsWidget, AbstractLabelledWidget, \
    AbstractButton, AbstractCheckBox, AbstractRadioBox, AbstractBitmap, \
    AbstractText, AbstractCalendar, AbstractSpinControl, AbstractMenu, TextStyle, AbstractTextTimedMenu

from . import ttk_style


def _rgb2hex(r, g, b):
    """Create and return a color string with RGB components in hexadecimal format."

    :param r: the red component (0-255)
    :param g: the green component (0-255)
    :param b: the blue component (0-255)
    :return: a color string with RGB components in hexadecimal format
    """
    return "#{:02x}{:02x}{:02x}".format(r, g, b)


def _build_font(size, style):
    """Create a font object with the desired size and style.

    :param size: the font size
    :param style: the font style (TextStyle enum)
    :return: the font object
    """
    if style is TextStyle.BOLD:
        font = tkinter.font.Font(size=size, weight='bold')
    elif style is TextStyle.ITALIC:
        font = tkinter.font.Font(size=size, slant='italic')
    elif style is TextStyle.BOLD_ITALIC:
        font = tkinter.font.Font(size=size, weight='bold', slant='italic')
    else:
        font = tkinter.font.Font(size=size)
    return font


class _Widget(AbstractWidget):
    """
    Base class for all widgets based on tkinter. This class should not be instantiated.
    A widget is any element which is displayed in a window and can be organized in a layout.
    """

    def __init__(self, **kwargs):
        """Initialize the widget.

        :param kwargs: additional parameters for superclass
        """
        self._widget = None
        super().__init__(**kwargs)

    def __getattr__(self, attr):
        """Redirect the attribute search to the tkinter wigdet object.

        :param attr: the desired attribute
        :return: the value of the attribute
        """
        if '_widget' in self.__dict__ and self._widget is not None:
            return getattr(self._widget, attr)
        else:
            try:
                return super().__getattr__(attr)
            except AttributeError:
                return None

    def __setattr__(self, attr, value):
        """Redirect the attribute setting to the tkinter wigdet object.

        :param attr: the desired attribute
        :param value: the new value of the attribute
        """
        if hasattr(self, attr) or self._widget is None:
            super().__setattr__(attr, value)
        else:
            setattr(self._widget, attr, value)

    def enable(self, is_enabled):
        """Set the enabled status of the widget. If not enabled, the user cannot interact with the widget.

        :param is_enabled: the new enabled status
        """
        super().enable(is_enabled)
        if self._widget is not None:
            if self._is_enabled:
                self.configure(state=NORMAL)
            else:
                self.configure(state=DISABLED)

    def hide(self, is_hidden):
        """Set the hidden status of the widget. If hidden, the widget is not displayed.

        :param is_hidden: the new hidden status
        """
        super().hide(is_hidden)
        if self._widget is not None:
            if self._is_hidden:
                self.grid_remove()
            else:
                self.grid()

    def _set_frame(self, frame):
        """Create the widget in the provided frame.

        :param frame: the frame where the widget has to be create.
        """
        if self._is_enabled:
            self.configure(state=NORMAL)
        else:
            self.configure(state=DISABLED)

    def grid(self, **kwargs):
        """Show the tkinter widget.

        :param kwargs: additional parameters for the tkinter grid function
        """
        if self._widget is not None and not self._is_hidden:
            self._widget.grid(**kwargs)


class _MouseEventsWidget(AbstractMouseEventsWidget, _Widget):
    """
    Base class for all widgets based on tkinter managing raw mouse events. This class should not be instantiated.
    The events supported are left and right mouse button down or up; wheel movement; mouse movement;
    mouse entering or leaving the widget.
    """

    def _set_frame(self, frame):
        """Create the widget in the provided frame.

        :param frame: the frame where the widget has to be create.
        """
        self.bind('<Button-1>', self._on_left_down)
        self.bind('<ButtonRelease-1>', self._on_left_up)
        self.bind('<Button-3>', self._on_right_down)
        self.bind('<ButtonRelease-3>', self._on_right_up)
        self.bind('<MouseWheel>', self._on_wheel)
        self.bind('<Motion>', self._on_mouse_motion)
        self.bind('<Enter>', self._on_mouse_enter)
        self.bind('<Leave>', self._on_mouse_leave)
        super()._set_frame(frame)

    def _on_left_down(self, event):
        """Executed following a left mouse press event.

        :param event: the mouse event
        """
        position = event.x, event.y
        self.on_left_down(self, position)

    def _on_left_up(self, event):
        """Executed following a left mouse release event.

        :param event: the mouse event
        """
        position = event.x, event.y
        self.on_left_up(self, position)

    def _on_right_down(self, event):
        """Executed following a right mouse press event.

        :param event: the mouse event
        """
        position = event.x, event.y
        self.on_right_down(self, position)

    def _on_right_up(self, event):
        """Executed following a right mouse release event.

        :param event: the mouse event
        """
        position = event.x, event.y
        self.on_right_up(self, position)

    def _on_mouse_motion(self, event):
        """Executed following a mouse move event.

        :param event: the mouse event
        """
        position = event.x, event.y
        self.on_mouse_motion(self, position)

    def _on_wheel(self, event):
        """Executed following a mouse wheel event.

        :param event: the mouse event
        """
        position = event.x, event.y
        rotation = event.delta
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
    """Base class for all widgets baed on tkinter which display a label. This class should not be instantiated."""

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
        if self._widget is not None:
            self.configure(text=super(_LabelledWidget, _LabelledWidget).label.__get__(self))

    def _set_frame(self, frame):
        """Create the widget in the provided frame.

        :param frame: the frame where the widget has to be create.
        """
        self.configure(text=super(_LabelledWidget, _LabelledWidget).label.__get__(self))
        super()._set_frame(frame)


class Button(AbstractButton, _LabelledWidget):
    """Button widget based on tkinter."""

    def _on_click(self):
        """Executed when the button is clicked."""
        self.on_click(self)

    def _set_frame(self, frame):
        """Create the widget in the provided frame.

        :param frame: the frame where the widget has to be create.
        """
        self._widget = tkinter.ttk.Button(frame, command=self._on_click)
        super()._set_frame(frame)


class CheckBox(AbstractCheckBox, _LabelledWidget):
    """Checkbox widget based on tkinter."""

    def _on_click(self):
        """Executed when the checkbox is clicked."""
        self.on_click(self)

    @property
    def label(self):
        """Return the current value of the label.

        :return: the current value of the label
        """
        return super(CheckBox, CheckBox).label.__get__(self)

    @label.setter
    def label(self, label):
        """Set the value of the label.

        :param label: the new value of the label (string)
        """
        super(CheckBox, CheckBox).label.__set__(self, label)
        if self._widget is not None:
            self.state(['!alternate'])

    def _set_frame(self, frame):
        """Create the widget in the provided frame.

        :param frame: the frame where the widget has to be create.
        """
        self._widget = tkinter.ttk.Checkbutton(frame, command=self._on_click)
        self.state(['!alternate'])
        if super(CheckBox, CheckBox).value.__get__(self):
            self.state(['selected'])
        else:
            self.state(['!selected'])
        super()._set_frame(frame)

    @property
    def value(self):
        """Return the current status value of the checkbox.

        :return: the current status value of the checkbox
        """
        if self._widget is not None:
            state = 'selected' in self.state()
            super(CheckBox, CheckBox).value.__set__(self, state)
        return super(CheckBox, CheckBox).value.__get__(self)

    @value.setter
    def value(self, value):
        """Set the status value of the checkbox.

        :param value: the new status value (boolean)
        """
        super(CheckBox, CheckBox).value.__set__(self, value)
        if self._widget is not None:
            if super(CheckBox, CheckBox).value.__get__(self):
                self.state(['selected'])
            else:
                self.state(['!selected'])


class RadioBox(AbstractRadioBox, _Widget):
    """Radiobox widget based on tkinter."""

    def __init__(self, **kwargs):
        """Initialize the radiobox.

        :param kwargs: additional parameters for superclass
        """
        super().__init__(**kwargs)
        self._var = tkinter.IntVar()
        self._rb = []

    def _set_frame(self, frame):
        """Create the widget in the provided frame.

        :param frame: the frame where the widget has to be create.
        """
        self._widget = tkinter.Frame(frame)
        for index, choice in enumerate(self._choices):
            rb = tkinter.ttk.Radiobutton(self._widget, text=choice, value=index, variable=self._var,
                                         command=self._on_click)
            rb.pack(fill='x')
            self._rb.append(rb)
        self._var.set(super(RadioBox, RadioBox).selection.__get__(self))
        for index in range(len(self._choices)):
            self._rb[index].configure(text=self._choices[index])
        super()._set_frame(frame)

    def _on_click(self):
        """Executed when the radiobox is clicked."""
        self.on_click(self)

    @property
    def selection(self):
        """Return the current selected choice.

        :return: the current selected choice (0-based)
        """
        if self._widget is not None:
            super(RadioBox, RadioBox).selection.__set__(self, self._var.get())
        return super(RadioBox, RadioBox).selection.__get__(self)

    @selection.setter
    def selection(self, selection):
        """Set the selected choice.

        :param selection: the new selected choice (0-based)
        """
        super(RadioBox, RadioBox).selection.__set__(self, selection)
        if self._widget is not None:
            self._var.set(super(RadioBox, RadioBox).selection.__get__(self))

    def set_choice(self, index, string):
        """Set the string to display for a choice.

        :param index: the index of the choice (0-based)
        :param string: the new string to display for the choice
        """
        super().set_choice(index, string)
        if self._widget is not None:
            self._rb[index].configure(text=self._choices[index])

    def configure(self, *args, **kwargs):
        """Propagate the configure command to all radiobuttons.

        :param args: positional parameters for the configure function
        :param kwargs: keyword parameters for the configure function
        """
        for rb in self._rb:
            rb.configure(*args, **kwargs)


class Bitmap(AbstractBitmap, _MouseEventsWidget):
    """Bitmap widget based on tkinter."""

    def __init__(self, **kwargs):
        """Initialize the bitmap.

        :param kwargs: additional parameters for superclass
        """
        super().__init__(**kwargs)
        self._tk_image = None

    def _set_frame(self, frame):
        """Create the widget in the provided frame.

        :param frame: the frame where the widget has to be create.
        """
        self._widget = tkinter.ttk.Label(frame)
        if self.bitmap is not None:
            self._tk_image = ImageTk.PhotoImage(self.bitmap)
            self.configure(image=self._tk_image)
        super()._set_frame(frame)

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
            self._tk_image = ImageTk.PhotoImage(self.bitmap)
            if self._widget is not None:
                self.configure(image=self._tk_image)


class _TextWidget(AbstractText, _Widget):
    """
    Base class for text widgets based on tkinter. This class should not be instantiated.
    Text widgets display a label (with the possibility to change color, size and style) and support raw mouse events.
    """

    def _get_style_id(self):
        """Return the string id of the tkinter style for the specific widget."""
        if self._widget is not None:
            if isinstance(self._widget, tkinter.ttk.Label):
                return 'TLabel'
            elif isinstance(self._widget, tkinter.ttk.Entry):
                return 'TEntry'
            else:
                raise TypeError('Widget does not support TTK style')
        else:
            return None

    def _set_frame(self, frame):
        """Create the widget in the provided frame.

        :param frame: the frame where the widget has to be create.
        """
        self.configure(font=_build_font(self.text_size, self.text_style))
        self.configure(font=_build_font(self.text_size, self.text_style))
        if self.foreground_color:
            ttk_style.configure(str(id(self)) + '.' + self._get_style_id(), foreground=_rgb2hex(*self.foreground_color))
        else:
            default_fg = ttk_style.lookup(self._get_style_id(), 'foreground')
            ttk_style.configure(str(id(self)) + '.' + self._get_style_id(), foreground=default_fg)
        if self.background_color:
            ttk_style.configure(str(id(self)) + '.' + self._get_style_id(), background=_rgb2hex(*self.background_color))
        else:
            default_bg = ttk_style.lookup(self._get_style_id(), 'background')
            ttk_style.configure(str(id(self)) + '.' + self._get_style_id(), background=default_bg)
        self.configure(style=str(id(self)) + '.' + self._get_style_id())
        super()._set_frame(frame)

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
        if self._widget is not None:
            self.configure(font=build_font(self.text_size, self.text_style))

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
        if self._widget is not None:
            self.configure(font=build_font(self.text_size, self.text_style))

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
        if self._widget is not None:
            if self.foreground_color:
                ttk_style.configure(str(id(self)) + '.' + self._get_style_id(),
                                    foreground=_rgb2hex(*self.foreground_color))
            else:
                default_fg = ttk_style.lookup(self._get_style_id(), 'foreground')
                ttk_style.configure(str(id(self)) + '.' + self._get_style_id(), foreground=default_fg)
            self.configure(style=str(id(self)) + '.' + self._get_style_id())

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
        if self._widget is not None:
            if self.background_color:
                ttk_style.configure(str(id(self)) + '.' + self._get_style_id(),
                                    background=_rgb2hex(*self.background_color))
            else:
                default_bg = ttk_style.lookup(self._get_style_id(), 'background')
                ttk_style.configure(str(id(self)) + '.' + self._get_style_id(), background=default_bg)
            self.configure(style=str(id(self)) + '.' + self._get_style_id())


class TextControl(_TextWidget):
    """TextControl widget based on tkinter. Allows the user to enter a text."""

    def _set_frame(self, frame):
        """Create the widget in the provided frame.

        :param frame: the frame where the widget has to be create.
        """
        self._string_var = tkinter.StringVar()
        self._widget = tkinter.ttk.Entry(frame, textvariable=self._string_var)
        self._trace_id = self._string_var.trace_add("write", self._on_change)
        self.insert(0, super(TextControl, TextControl).label.__get__(self))
        super()._set_frame(frame)

    def _on_change(self, *_args):
        """Executed when the text is changed by the user."""
        self.on_change(self)

    @property
    def label(self):
        """Return the current value of the label.

        :return: the current value of the label
        """
        if self._widget is not None:
            super(TextControl, TextControl).label.__set__(self, self.get())
        return super(TextControl, TextControl).label.__get__(self)

    @label.setter
    def label(self, label):
        """Set the value of the label.

        :param label: the new value of the label (string)
        """
        super(TextControl, TextControl).label.__set__(self, label)
        if self._widget is not None:
            self.delete(0, END)
            self._string_var.trace_remove("write", self._trace_id)
            self.insert(0, super(TextControl, TextControl).label.__get__(self))
            self._trace_id = self._string_var.trace_add("write", self._on_change)

class Text(_TextWidget, _MouseEventsWidget, _LabelledWidget):
    """Text widget based on tkinter. Displays a text."""

    def _set_frame(self, frame):
        """Create the widget in the provided frame.

        :param frame: the frame where the widget has to be create.
        """
        self._widget = tkinter.ttk.Label(frame)
        super()._set_frame(frame)


class Calendar(AbstractCalendar, _Widget):
    """
    Calendar widget based on tkinter.
    Calendars support a date-changed event and have a selection status value. Different languages are supported.
    """

    def _set_frame(self, frame):
        """Create the widget in the provided frame.

        :param frame: the frame where the widget has to be create.
        """
        self._widget = tkcalendar.Calendar(frame, firstweekday='monday')
        self.bind('<<CalendarSelected>>', self._on_date_changed)
        self.configure(mindate=super(Calendar, Calendar).lower_date.__get__(self))
        self.configure(maxdate=super(Calendar, Calendar).upper_date.__get__(self))
        super(Calendar, Calendar).selected_date.__set__(self, self.selection_get())
        super()._set_frame(frame)

    def _on_date_changed(self, event):
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
        if self._widget is not None:
            self.configure(mindate=super(Calendar, Calendar).lower_date.__get__(self))

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
        if self._widget is not None:
            self.configure(maxdate=super(Calendar, Calendar).upper_date.__get__(self))

    @property
    def selected_date(self):
        """Return the current selected date.

        :return: the current selected date
        """
        if self._widget is not None:
            super(Calendar, Calendar).selected_date.__set__(self, self.selection_get())
        return super(Calendar, Calendar).selected_date.__get__(self)

    @selected_date.setter
    def selected_date(self, date):
        """Set the selected date.

        :param date: the new selected date
        """
        super(Calendar, Calendar).selected_date.__set__(self, date)
        if self._widget is not None:
            self.selection_set(super(Calendar, Calendar).selected_date.__get__(self))

    def set_language(self, language_code):
        """Set the language of the calender.

        :param language_code: the new language to use (code according to ISO639); defaults to English
        """
        if self._widget is not None:
            try:
                self.configure(locale=language_code)
            except:
                self.configure(locale='en')


class SpinControl(AbstractSpinControl, _Widget):
    """Spin control widget based on tkinter. Spin controls support a value-changed event and have a status value."""

    def _set_frame(self, frame):
        """Create the widget in the provided frame.

        :param frame: the frame where the widget has to be create.
        """
        self._widget = tkinter.ttk.Spinbox(frame, command=self._on_value_changed)
        self.insert(0, super(SpinControl, SpinControl).value.__get__(self))
        self.state(['readonly'])
        if self.min_value is not None:
            self.configure(from_=self.min_value)
        else:
            self.configure(from_=self._DEFAULT_MIN_VALUE)
        if self.max_value is not None:
            self.configure(to=self.max_value)
        else:
            self.configure(to=self._DEFAULT_MAX_VALUE)
        super()._set_frame(frame)

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
        if self._widget is not None:
            if self.min_value is not None:
                self.configure(from_=self.min_value)
            else:
                self.configure(from_=self._DEFAULT_MIN_VALUE)

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
        if self._widget is not None:
            if self.max_value is not None:
                self.configure(to=self.max_value)
            else:
                self.configure(to=self._DEFAULT_MAX_VALUE)

    @property
    def value(self):
        """Return the current value.

        :return: the current value
        """
        if self._widget is not None:
            super(SpinControl, SpinControl).value.__set__(self, int(self.get()))
            self.state(['!readonly'])
            self.delete(0, END)
            self.insert(0, super(SpinControl, SpinControl).value.__get__(self))
            self.state(['readonly'])
        return super(SpinControl, SpinControl).value.__get__(self)

    @value.setter
    def value(self, value):
        """Set the value (clipping between minimum and maximum allowed values if necessary).

        :param value: the new value
        """
        super(SpinControl, SpinControl).value.__set__(self, value)
        if self._widget is not None:
            self.state(['!readonly'])
            self.delete(0, END)
            self.insert(0, super(SpinControl, SpinControl).value.__get__(self))
            self.state(['readonly'])


class Menu(AbstractMenu, _Widget):
    """
    Menu widget based on tkinter.
    Menus allow to create a tree of items which the user can click; each item can in turn be a menu.
    """

    _TIMER_FORCE_CLOSE = 0.1

    def __init__(self, **kwargs):
        """Initialize the menu.

        :param kwargs: additional parameters for superclass
        """
        super().__init__(**kwargs)
        self._wait_var = tkinter.IntVar()
        self._wait_var.set(0)

    def _on_click(self, item):
        """Executed when a menu item is clicked.

        :param item: the string corresponding to the clicked item
        """
        self.on_click(self, item)

    def _build_menu(self, menubar=None, inherited_on_click=None):
        """
        Build the menu. A menu can only be built once: a new instance has to be created if the same menu needs to be
        used again.

        :param menubar: frame menubar where the menu have to be built (None to create an independent menu)
        :param inherited_on_click: function to execute when the menu is clicked, if property inherit_on_click is True
        """
        if self._widget is None:
            self._widget = tkinter.Menu(self._parent.toplevel, tearoff=0)
        super()._build_menu(menubar, inherited_on_click)

    def pop_up(self):
        """Build and show the menu as a pop-up."""
        if self._widget is not None:
            self.delete(0, END)
        super().pop_up()
        self.tk_popup(self._parent.toplevel.winfo_pointerx(), self._parent.toplevel.winfo_pointery())
        self.on_close(self)
        # Start a timer to force the wait variable to change
        # even if the menu has been closed without clicking on it
        Timer(self._TIMER_FORCE_CLOSE, self._force_close).start()
        # Wait until the item click function has been executed or the timer has expired
        self._widget.wait_variable(self._wait_var)

    def _force_close(self):
        """Force the closing of the menu after a short time has passed."""
        self._wait_var.set(1)

    def _append_separator(self, target):
        """
        Append a separator to the target, which can be the menu object itself (for pop-up menus or
        branches of a menu tree) or a window menubar.
        Separators are not shown in menubars in wxPython.

        :param target: the target where the menu has to be appended (menu object itself or window menubar)
        """
        target.add_separator()

    def _append_menu(self, target, menu, is_enabled):
        """
        Append a menu to the target, which can be the menu object itself (for pop-up menus or
        branches of a menu tree) or a window menubar.

        :param target: the target where the menu has to be appended (menu object itself or window menubar)
        :param item: the menu to append
        :param is_enabled: boolean defining if the menu is enabled
        """
        menu._build_menu(inherited_on_click=self.on_click)
        target.add_cascade(label=menu.label, menu=menu._widget)
        if not is_enabled:
            target.entryconfig(menu, state="disabled")

    def _append_simple_item(self, target, item, is_enabled, on_item_click):
        """
        Append a simple string item to the target, which can be a the menu object itself (for pop-up menus or
        branches of a menu tree) or a window menubar.

        :param target: the target where the item has to be appended (menu object itself or window menubar)
        :param item: the item to append
        :param is_enabled: boolean defining if the item is enabled
        :param on_item_click: function to be executed if the item is clicked
        """
        ampersand = item.find('&')
        if ampersand != -1:
            shortcut_key = item[ampersand + 1].lower()
            item = item[:ampersand] + item[ampersand + 1:]
        else:
            shortcut_key = None
        tab = item.find('\t')
        if tab != -1:
            accelerator = item[tab + 1:]
            item = item[:tab]
        else:
            accelerator = None
        if on_item_click is None:
            def _on_item_click():
                self._on_click(item)
                self._wait_var.set(1)
        else:
            def _on_item_click():
                on_item_click(self)
                self._wait_var.set(1)
        target.add_command(label=item, command=_on_item_click, underline=ampersand, accelerator=accelerator)
        if shortcut_key:
            self._parent.toplevel.bind_all(f'<Alt-{shortcut_key}>', lambda event: _on_item_click())
        if not is_enabled:
            target.entryconfig(item, state="disabled")


class TextTimedMenu(AbstractTextTimedMenu, _Widget):
    """
    Text timed menu based on tkinter; these are menus built with text labels, which close automatically after a
    specified time when the mouse cursor leaves.
    """

    def _set_frame(self, frame):
        """Create the widget in the provided frame.

        :param frame: the frame where the widget has to be create.
        """
        self._widget = tkinter.Toplevel(frame)
        self._widget.overrideredirect(True)
        self._widget.protocol('WM_DELETE_WINDOW', lambda: self.on_close(self))

    def pop_up(self, *, modal=False):
        """Build and show the menu as a pop-up. It can be shown as a modal, forcing interaction from the user.

        :param modal: specifies if the text timed menu should be modal or not
        """
        self._set_frame(self._parent.toplevel)
        if modal:
            self._widget.grab_set()
        super().pop_up()
        x_mouse = self._parent.toplevel.winfo_pointerx()
        y_mouse = self._parent.toplevel.winfo_pointery()
        self._widget.geometry(f"+{x_mouse + 10}+{y_mouse + 10}")
        self._widget.bind('<<CloseWidget>>', self._on_close_signal)

    def _create_text(self, label):
        """Create a Text widget with the specified label.

        :param label: the desired text label
        :return: the created Text widget
        """
        if label == self.SEPARATOR:
            label = ""
        text = Text(parent=None, label=label)
        text._set_frame(self._widget)
        text.label = label
        text.pack(expand=True, fill='x')
        return text

    def _close(self):
        """Close the menu."""
        super()._close()
        self._widget.event_generate('<<CloseWidget>>')

    def _on_close_signal(self, event):
        """Executed when the close event is triggered."""
        self.on_close(self)
        self._widget.destroy()
