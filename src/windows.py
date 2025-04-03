# PrettySUsI library: entry point for import of frame classes (Frame, Diolog, MessageDialog)

from . import gui_type, initialize_error_message

if gui_type is None:
    raise ImportError(initialize_error_message)

from . import Frame, Dialog, ErrorMessageDialog
from .abstract.windows import FrameStyle, CursorStyle
