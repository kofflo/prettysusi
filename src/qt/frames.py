import PySide6
import PySide6.QtWidgets
import PySide6.QtCore
import PySide6.QtGui

from ..abstract.frames import AbstractFrame, FrameStyle, CursorStyle, AbstractDialog, AbstractMessageDialog


class Frame(AbstractFrame, PySide6.QtWidgets.QMainWindow):

    def __init__(self, *, parent=None, pos=None, size=None, **kwargs):

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
        self._parent = PySide6.QtWidgets.QWidget()
        self._size = size
        self.setCentralWidget(self._parent)

        super().__init__(parent=parent, **kwargs)


    def event_connect(self, event, on_event):
        event.connect(lambda kwargs: on_event(**kwargs))

    def event_trigger(self, event, **kwargs):
        event.emit(kwargs)

    def closeEvent(self, event):
        self._close_operations()
        super().closeEvent(event)

    @property
    def title(self):
        return super(Frame, Frame).title.__get__(self)

    @title.setter
    def title(self, title):
        super(Frame, Frame).title.__set__(self, title)
        self.setWindowTitle(title)

    @property
    def icon(self):
        return super(Frame, Frame).icon.__get__(self)

    @icon.setter
    def icon(self, icon):
        super(Frame, Frame).icon.__set__(self, icon)
        if self.icon is not None:
            app_icon = PySide6.QtGui.QIcon(self.icon)
            self.setWindowIcon(app_icon)

    def show(self):
        PySide6.QtWidgets.QMainWindow.show(self)
#        self._refresh_widgets()

    def _command_close(self):
        PySide6.QtWidgets.QMainWindow.close(self)

    def _set_menubar(self, menu):
        menubar = self.menuBar()
        menubar.clear()
        menu._build_menu(menubar=menubar)

    def _set_cursor(self, cursor):
        if cursor is CursorStyle.SIZING:
            PySide6.QtGui.QGuiApplication.setOverrideCursor(PySide6.QtCore.Qt.SizeAllCursor)
        elif cursor is CursorStyle.ARROW:
            PySide6.QtGui.QGuiApplication.setOverrideCursor(PySide6.QtCore.Qt.ArrowCursor)

    def set_focus(self):
        self.activateWindow()


class Dialog(AbstractDialog, PySide6.QtWidgets.QDialog):

    def __init__(self, *, parent, **kwargs):
        PySide6.QtWidgets.QDialog.__init__(self, parent)
        self._panel = self
        self._parent = self
        super().__init__(**kwargs)
        self.setWindowFlags(self.windowFlags() & ~PySide6.QtGui.Qt.WindowContextHelpButtonHint)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.destroy()

    @property
    def title(self):
        return super(Dialog, Dialog).title.__get__(self)

    @title.setter
    def title(self, title):
        super(Dialog, Dialog).title.__set__(self, title)
        self.setWindowTitle(title)

    def show_modal(self):
        self.layout().setSizeConstraint(PySide6.QtWidgets.QLayout.SetFixedSize)
        self.exec()
        return self._return_value

    def _on_ok(self, obj):
        super()._on_ok(obj)
        self.accept()

    def _on_cancel(self, obj):
        super()._on_cancel(obj)
        self.reject()


class MessageDialog(AbstractMessageDialog, PySide6.QtWidgets.QMessageBox):

    def __init__(self, *, parent, **kwargs):
        PySide6.QtWidgets.QMessageBox.__init__(self, parent)
        self.setIcon(PySide6.QtWidgets.QMessageBox.Critical)
        super().__init__(**kwargs)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.destroy()

    @property
    def title(self):
        return super(MessageDialog, MessageDialog).title.__get__(self)

    @title.setter
    def title(self, title):
        super(MessageDialog, MessageDialog).title.__set__(self, title)
        self.setWindowTitle(title)

    @property
    def message(self):
        return super(MessageDialog, MessageDialog).message.__get__(self)

    @message.setter
    def message(self, message):
        super(MessageDialog, MessageDialog).message.__set__(self, message)
        self.setText(message)

    def show_modal(self):
        self.exec()
        return self.result() == PySide6.QtWidgets.QMessageBox.Accepted
