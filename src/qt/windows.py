import PySide6
import PySide6.QtWidgets
import PySide6.QtCore
import PySide6.QtGui

from ..abstract.windows import AbstractFrame, FrameStyle, CursorStyle, AbstractDialog, AbstractErrorMessageDialog


class Frame(AbstractFrame, PySide6.QtWidgets.QMainWindow):
    """Frame based on PySide6: a frame is used to create general-purpose windows."""

    def __init__(self, *, parent=None, pos=None, size=None, **kwargs):
        """Frame object initialization.

        :param parent: the parent window of the frame; None for a top-level frame
        :param pos: the desired position of the frame on the screen in pixel
        :param size: the desired size of the frame in pixel
        :param kwargs: additional parameters for superclass
        """
        PySide6.QtWidgets.QMainWindow.__init__(self)

        if self._STYLE is FrameStyle.FIXED_SIZE:
            self.layout().setSizeConstraint(PySide6.QtWidgets.QLayout.SetFixedSize)
            self.setWindowFlags(self.windowFlags() | PySide6.QtCore.Qt.CustomizeWindowHint)
            self.setWindowFlags(self.windowFlags() | PySide6.QtCore.Qt.WindowMinimizeButtonHint)
            self.setWindowFlags(self.windowFlags() & ~PySide6.QtCore.Qt.WindowMaximizeButtonHint)
            self.setWindowFlags(self.windowFlags() | PySide6.QtCore.Qt.WindowCloseButtonHint)
        elif self._STYLE is FrameStyle.DIALOG:
            self.setWindowFlags(self.windowFlags() | PySide6.QtCore.Qt.CustomizeWindowHint)
            self.setWindowFlags(self.windowFlags()
                                & ~PySide6.QtCore.Qt.WindowMinimizeButtonHint
                                & ~PySide6.QtCore.Qt.WindowMaximizeButtonHint
                                & ~PySide6.QtCore.Qt.WindowCloseButtonHint)

        if size is not None:
            self.resize(*size)

        if pos is not None:
            self.move(*pos)

        self._panel = self
        self._layout_parent = PySide6.QtWidgets.QWidget()
        self._size = size
        self.setCentralWidget(self._layout_parent)

        super().__init__(parent=parent, **kwargs)

    def event_connect(self, event, on_event):
        """Connect an event to a function.

        :param event: the event to connect
        :param on_event: the function to execute when the event is triggered
        """
        event.connect(lambda kwargs: on_event(**kwargs))

    def event_trigger(self, event, **kwargs):
        """Trigger an event.

        :param event: the event to trigger
        :param kwargs: the parameters to pass to the connected function
        """
        event.emit(kwargs)

    def closeEvent(self, event):
        """Function executed when the PySide6 QMainWindow object is closed.

        :param event: the close event
        """
        self._close_operations()
        super().closeEvent(event)

    @property
    def title(self):
        """Return the frame title.

        :return: the frame title
        """
        return super(Frame, Frame).title.__get__(self)

    @title.setter
    def title(self, title):
        """Set the frame title.

        :param title: the new frame title
        """
        super(Frame, Frame).title.__set__(self, title)
        self.setWindowTitle(title)

    @property
    def icon(self):
        """Return the frame icon.

        :return: the frame icon
        """
        return super(Frame, Frame).icon.__get__(self)

    @icon.setter
    def icon(self, icon):
        """Set the frame icon.

        :param icon: the new frame icon
        """
        super(Frame, Frame).icon.__set__(self, icon)
        if self.icon is not None:
            app_icon = PySide6.QtGui.QIcon(self.icon)
            self.setWindowIcon(app_icon)

    def show(self):
        """Show the frame."""
        PySide6.QtWidgets.QMainWindow.show(self)

    def hide(self):
        """Hide the frame."""
        PySide6.QtWidgets.QMainWindow.hide(self)

    def _command_close(self):
        """Command the frame to close."""
        PySide6.QtWidgets.QMainWindow.close(self)

    def set_menubar(self, menu):
        """Set a menu as main menubar of the frame.

        :param menu: the menu to set as menubar
        """
        menubar = self.menuBar()
        menubar.clear()
        menu.attach_menubar(menubar)

    def set_cursor(self, cursor):
        """Set the cursor shape when the cursor is on the frame.

        :param cursor: the new cursor shape
        """
        if cursor is CursorStyle.SIZING:
            PySide6.QtGui.QGuiApplication.setOverrideCursor(PySide6.QtCore.Qt.SizeAllCursor)
        elif cursor is CursorStyle.ARROW:
            PySide6.QtGui.QGuiApplication.setOverrideCursor(PySide6.QtCore.Qt.ArrowCursor)

    def set_focus(self):
        """Set the focus on the frame."""
        self.activateWindow()


class Dialog(AbstractDialog, PySide6.QtWidgets.QDialog):
    """
    Dialog based on PySide6: a dialog is used to create a window that allows the user to choose
    between two options: OK or Cancel.
    """

    def __init__(self, *, parent, **kwargs):
        """Initialize the dialog object.

        :param parent: parent window of the dialog
        :param kwargs: additional parameters for superclass
        """
        PySide6.QtWidgets.QDialog.__init__(self, parent)
        self._panel = self
        self._layout_parent = self
        super().__init__(**kwargs)
        self.setWindowFlags(self.windowFlags() & ~PySide6.QtGui.Qt.WindowContextHelpButtonHint)
        self.setAttribute(PySide6.QtCore.Qt.WA_DeleteOnClose)

    def __enter__(self):
        """Enter function, necessary to correctly manage the with block with the dialog.

        :return: the dialog object itself
        """
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """Exit function, necessary to correctly manage the with block with the dialog. Destroy the dialog object.

        :param exc_type: exception type
        :param exc_value: exception value
        :param exc_traceback: exception traceback
        """
        pass

    @property
    def title(self):
        """Return the dialog title.

        :return: the dialog title
        """
        return super(Dialog, Dialog).title.__get__(self)

    @title.setter
    def title(self, title):
        """Set the dialog title.

        :param title: the new dialog title
        """
        super(Dialog, Dialog).title.__set__(self, title)
        self.setWindowTitle(title)

    def _show_dialog(self):
        """Show the dialog window."""
        self.layout().setSizeConstraint(PySide6.QtWidgets.QLayout.SetFixedSize)
        self.exec()

    def _on_ok(self, obj):
        """Executed when the OK choice is selected."""
        super()._on_ok(obj)
        self.accept()
        self.destroy()

    def _on_cancel(self, obj):
        """Executed when the Cancel choice is selected."""
        super()._on_cancel(obj)
        self.reject()
        self.destroy()


class ErrorMessageDialog(AbstractErrorMessageDialog, PySide6.QtWidgets.QMessageBox):
    """
    Error message dialog based on PySide6: it is used to display a simple error message to the user and wait for a click
    on the OK button.
    """

    def __init__(self, *, parent, **kwargs):
        """Initialize the error message dialog object.

        :param parent: parent window of the error message dialog
        :param kwargs: additional parameters for superclass
        """
        PySide6.QtWidgets.QMessageBox.__init__(self, parent)
        self.setIcon(PySide6.QtWidgets.QMessageBox.Critical)
        self.setAttribute(PySide6.QtCore.Qt.WA_DeleteOnClose)
        super().__init__(**kwargs)

    def __enter__(self):
        """Enter function, necessary to correctly manage the with block with the error message dialog.

        :return: the message dialog object itself
        """
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """
        Exit function, necessary to correctly manage the with block with the error message dialog.

        :param exc_type: exception type
        :param exc_value: exception value
        :param exc_traceback: exception traceback
        """
        pass

    @property
    def title(self):
        """Return the dialog title.

        :return: the dialog title
        """
        return super(ErrorMessageDialog, ErrorMessageDialog).title.__get__(self)

    @title.setter
    def title(self, title):
        """Set the message dialog title.

        :param title: the new dialog title
        """
        super(ErrorMessageDialog, ErrorMessageDialog).title.__set__(self, title)
        self.setWindowTitle(title)

    @property
    def message(self):
        """Return the message to display in the error message dialog.

        :return: the message to display
        """
        return super(ErrorMessageDialog, ErrorMessageDialog).message.__get__(self)

    @message.setter
    def message(self, message):
        """Set the message to display in the error message dialog.

        :param message: the new message
        """
        super(ErrorMessageDialog, ErrorMessageDialog).message.__set__(self, message)
        self.setText(message)

    def show_modal(self):
        """
        Show the error message dialog as a modal (on top of all other windows; the user must interact with the dialog).
        Can be executed only once.
        """
        super().show_modal()
        self.exec()
