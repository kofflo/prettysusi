# PrettySUsI library: entry point for library import

import sys

app = None
event_create = None
Button, CheckBox, RadioBox, Bitmap, Text, TextControl, \
    Calendar, SpinControl, Menu, TextTimedMenu = [None] * 10
Grid = None
Frame, Dialog, MessageDialog = [None] * 3
VBoxLayout, HBoxLayout, GridLayout = [None] * 3
Align = None
gui_type = None
supported_gui = ['wx', 'qt', 'tk']
initialize_error_message = "The prettysusi library has not been initialized\nRun prettysusi.initialize(GUI_TYPE)."


class _DummyObject:
    """Class defining a dummy object, to redirect all attribute calls to a GUI type that has not been loaded."""

    def __getattr__(self, key):
        """The dummy object returns an empty lambda for each attribute request.
        All actions performed on the dummy object result in no effect.

        :param key: the attribute key.
        :return: a lambda identically returning None for any argument.
        """
        return lambda *args, **kwargs: None


class BaseClass:
    """Base class for all PrettySUsI objects, allowing the redirection of attribute calls for a specific GUI type."""

    def __getattr__(self, key):
        """Return the object itself if called with the loaded GUI as attribute or a dummy object if called with one
        of the valid but non loaded GUI as attribute.
        Raise an attribute error if the attribute is not a valid GUI.

        :param key: an attribute key not existing in the object.
        :return: the object itself if the attribute key is the loaded GUI,
         or a dummy object if it is one of the non loaded GUI.
        """
        if key not in supported_gui:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{key}'")
        else:
            if key == gui_type:
                return self
            else:
                return _DummyObject()


def initialize(gui_request):
    """Initialize the library and load all necessary features for the requested GUI type.
    Raise an error if the import of the GUI is not successful, if an invalid GUI has been requrested or
    if the library has already initialized with a different GUI.

    :param gui_request: the requested GUI.
    """

    global app, event_create
    global Button, CheckBox, RadioBox, Bitmap, Text, TextControl, Calendar, SpinControl, Menu, TextTimedMenu
    global Grid
    global Frame, Dialog, MessageDialog
    global VBoxLayout, HBoxLayout, GridLayout
    global Align
    global gui_type

    already_initialized_error_message = "The prettysusi library has already been initialized with GUI '%s'"
    import_error_message = "The required GUI '%s' cannot be loaded correctly\n"
    invalid_gui_error_message = "The required GUI '%s' is not valid\nUse one of the following: %s"

    if gui_type and gui_type != gui_request:
        raise ImportError(already_initialized_error_message % gui_type)

    if gui_request == 'wx':
        # Import WxPython GUI
        try:
            from wx import App

            from .wx import event_create
            from .wx.widgets import Button, CheckBox, RadioBox, Bitmap, Text, TextControl, \
                Calendar, SpinControl, Menu, TextTimedMenu
            from .wx.layouts import VBoxLayout, HBoxLayout, GridLayout, Align
            from .wx.frames import Frame, Dialog, MessageDialog
            from .wx.tables import Grid

            app = App()
            app.run = app.MainLoop
            gui_type = 'wx'

        except ImportError as e:
            raise ImportError((import_error_message % gui_request) + str(e))

    elif gui_request == 'qt':
        # Import Qt GUI
        try:
            from PySide6.QtWidgets import QApplication

            from .qt import event_create
            from .qt.widgets import Button, CheckBox, RadioBox, Bitmap, Text, TextControl, \
                Calendar, SpinControl, Menu, TextTimedMenu
            from .qt.tables import Grid
            from .qt.frames import Frame, Dialog, MessageDialog
            from .qt.layouts import VBoxLayout, HBoxLayout, GridLayout, Align

            app = QApplication([])
            app.run = app.exec
            gui_type = 'qt'

        except ImportError as e:
            raise ImportError((import_error_message % gui_request) + str(e))

    elif gui_request == 'tk':
        # Import tkinter GUI
        try:
            from tkinter import Tk, ttk
            app = Tk()

            from .tk import event_create
            from .tk.widgets import Button, CheckBox, RadioBox, Bitmap, Text, TextControl, \
                Calendar, SpinControl, Menu, TextTimedMenu
            from .tk.tables import Grid
            from .tk.frames import Frame, Dialog, MessageDialog
            from .tk.layouts import VBoxLayout, HBoxLayout, GridLayout, Align

            app.withdraw()
            app.run = app.mainloop
            gui_type = 'tk'

        except ImportError as e:
            raise ImportError((import_error_message % gui_request) + str(e))

    else:
        # An invalid GUI has been requested
        raise ImportError(invalid_gui_error_message % (gui_request, str(supported_gui)))


def set_locale(language_code):
    """Set the correct locale for the used GUI (currently only necessary for 'wx').
    If the requested locale is not valid, English is used as default.

    :param language_code: the language code of the desired locale.
    """
    if gui_type is None:
        raise ImportError(initialize_error_message)
    elif gui_type == 'wx':
        from wx import Locale, Language
        li = Locale.FindLanguageInfo(language_code)
        if li is not None:
            app.locale = Locale(li.Language)
        else:
            app.locale = Locale(Language.LANGUAGE_ENGLISH)
