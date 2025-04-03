# PrettySUsI library: entry point for import of table classes (Table)

from . import gui_type, initialize_error_message

if gui_type is None:
    raise ImportError(initialize_error_message)

from . import Table
from .abstract.tables import Align, Renderer, TextStyle
