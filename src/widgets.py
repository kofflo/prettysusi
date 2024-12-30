# PrettySUsI library: entry point for import of widget classes (Button, CheckBox, RadioBox, Bitmap, Text,
# Calendar, SpinControl, Menu, TextControl, TextTimedMenu)

from . import gui_type, initialize_error_message

if gui_type is None:
    raise ImportError(initialize_error_message)

from . import Button, CheckBox, RadioBox, Bitmap, Text, Calendar, SpinControl, Menu, TextControl, TextTimedMenu
from .abstract.widgets import TextStyle
