import wx
import wx.adv
import wx.lib.newevent

from ..abstract.windows import AbstractFrame, AbstractDialog, AbstractErrorMessageDialog
from ..abstract.windows import FrameStyle, CursorStyle


class Frame(AbstractFrame, wx.Frame):
    """Frame based on wxPython: a frame is used to create general-purpose windows."""

    def __init__(self, *, parent=None, pos=None, size=None, **kwargs):
        """Frame object initialization.

        :param parent: the parent window of the frame; None for a top-level frame
        :param pos: the desired position of the frame on the screen in pixel
        :param size: the desired size of the frame in pixel
        :param kwargs: additional parameters for superclass
        """
        if self._STYLE is FrameStyle.FIXED_SIZE:
            style = wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX)
        elif self._STYLE is FrameStyle.DIALOG:
            style = wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.CLOSE_BOX | wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX)
        else:
            style = wx.DEFAULT_FRAME_STYLE
        if pos is None:
            wx_pos = wx.DefaultPosition
        else:
            wx_pos = wx.Point(*pos)
        if size is None:
            wx_size = wx.DefaultSize
        else:
            wx_size = wx.Size(*size)
        wx.Frame.__init__(self, parent, style=style, pos=wx_pos, size=wx_size)
        self.Bind(wx.EVT_CLOSE, self._on_close)
        self._panel = wx.Panel(self)
        self._layout_parent = self._panel
        self._frame_sizer = wx.BoxSizer(wx.VERTICAL)
        self._frame_sizer.Add(self._panel)
        super().__init__(parent=parent, **kwargs)

    def event_connect(self, event, on_event):
        """Connect an event to a function.

        :param event: the event to connect
        :param on_event: the function to execute when the event is triggered
        """
        self.Bind(event['binder'], lambda e: on_event(**e._getAttrDict()))

    def event_trigger(self, event, **kwargs):
        """Trigger an event.

        :param event: the event to trigger
        :param kwargs: the parameters to pass to the connected function
        """
        event = event['class'](**kwargs)
        wx.CallAfter(wx.PostEvent, self, event)

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
        self.SetTitle(title)

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
            self.SetIcon(wx.Icon(self.icon))

    def show(self):
        """Show the frame."""
        self.Show()

    def hide(self):
        """Hide the frame."""
        self.Hide()

    def _command_close(self):
        """Command the frame to close."""
        self.Close()

    def _on_close(self, event):
        """Function executed when the frame is closed."""
        self._close_operations()
        event.Skip()

    def set_menubar(self, menu):
        """Set a menu as main menubar of the frame.

        :param menu: the menu to set as menubar
        """
        menubar = wx.MenuBar()
        self.SetMenuBar(menubar)
        menu.attach_menubar(menubar)

    def _command_update_gui(self, data):
        """
        Command the update of the content of the frame and of its child views recursively,
        using the data provided as input.

        :param data: the data to use for the content update
        """
        super()._command_update_gui(data)
        self.Layout()
        self.SetSizerAndFit(self._frame_sizer)

    def set_cursor(self, cursor):
        """Set the cursor shape when the cursor is on the frame.

        :param cursor: the new cursor shape
        """
        if cursor is CursorStyle.SIZING:
            self.SetCursor(wx.Cursor(wx.CURSOR_SIZING))
        elif cursor is CursorStyle.ARROW:
            self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))

    def set_focus(self):
        """Set the focus on the frame."""
        self.SetFocus()


class Dialog(AbstractDialog, wx.Dialog):
    """
    Dialog based on tkinter: a dialog is used to create a window that allows the user to choose
    between two options: OK or Cancel.
    """

    def __init__(self, *, parent, **kwargs):
        """Initialize the dialog object.

        :param parent: parent window of the dialog
        :param kwargs: additional parameters for superclass
        """
        wx.Dialog.__init__(self, parent)
        self._panel = self
        self._layout_parent = self
        super().__init__(**kwargs)
        self.SetIcon(wx.Icon(parent.icon))

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
        self.SetTitle(title)

    def _show_dialog(self):
        """Show the dialog window."""
        self.Fit()
        self.ShowModal()
        self.Destroy()

    def _on_ok(self, obj):
        """Executed when the OK choice is selected."""
        super()._on_ok(obj)
        self.EndModal(True)

    def _on_cancel(self, obj):
        """Executed when the Cancel choice is selected."""
        super()._on_cancel(obj)
        self.EndModal(False)


class ErrorMessageDialog(AbstractErrorMessageDialog, wx.MessageDialog):
    """
    Error message dialog based on wxPython: it is used to display a simple error message to the user and wait for a click
    on the OK button.
    """

    def __init__(self, *, parent, **kwargs):
        """Initialize the error message dialog object.

        :param parent: parent window of the error message dialog
        :param kwargs: additional parameters for superclass
        """
        wx.MessageDialog.__init__(self, parent, "", "", wx.OK | wx.ICON_ERROR)
        super().__init__(**kwargs)

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
        self.SetTitle(title)

    @property
    def message(self):
        """Return the message to display in the message dialog.

        :return: the message to display
        """
        return super(ErrorMessageDialog, ErrorMessageDialog).message.__get__(self)

    @message.setter
    def message(self, message):
        """Set the message to display in the message dialog.

        :param message: the new message
        """
        super(ErrorMessageDialog, ErrorMessageDialog).message.__set__(self, message)
        self.SetMessage(message)

    def show_modal(self):
        """
        Show the error message dialog as a modal (on top of all other windows; the user must interact with the dialog).
        Can be executed only once.
        """
        super().show_modal()
        self.ShowModal()
        self.Destroy()
