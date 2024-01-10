import wx
import wx.adv
import wx.lib.newevent

from ..abstract.frames import AbstractIconFrame
from ..abstract.frames import FrameStyle, CursorStyle, AbstractDialog, AbstractMessageDialog


class Frame(AbstractIconFrame, wx.Frame):

    def __init__(self, *, parent, pos=None, size=None, **kwargs):

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
        self._frame_sizer = wx.BoxSizer(wx.VERTICAL)
        self._frame_sizer.Add(self._panel)
        super().__init__(parent=parent, **kwargs)
        self._create_widgets(self._panel)
        self._create_gui().create_layout(self._panel)
        self._create_menu()

    def event_connect(self, event, on_event):
        self.Bind(event['binder'], lambda e: on_event(**e._getAttrDict()))

    def event_trigger(self, event, **kwargs):
        event = event['class'](**kwargs)
        wx.CallAfter(wx.PostEvent, self, event)

    def _create_menu(self):
        #
        pass

    def _create_gui(self):
        raise NotImplementedError

    @property
    def title(self):
        return super(Frame, Frame).title.__get__(self)

    @title.setter
    def title(self, title):
        super(Frame, Frame).title.__set__(self, title)
        self.SetTitle(title)

    @property
    def icon(self):
        return super(Frame, Frame).icon.__get__(self)

    @icon.setter
    def icon(self, icon):
        super(Frame, Frame).icon.__set__(self, icon)
        if self.icon is not None:
            self.SetIcon(wx.Icon(self.icon))

    def show(self):
        self.Show()

    def close(self):
        self.Close()

    def _on_close(self, event):
        self.detach()
        self.on_close(self)
        event.Skip()

    def _set_menubar(self, menu):
        menubar = wx.MenuBar()
        self.SetMenuBar(menubar)
        menu.build_menu(menubar=menubar)

    def _fit_frame(self):
        self.Layout()
        self.SetSizerAndFit(self._frame_sizer)

    def _set_cursor(self, cursor):
        if cursor is CursorStyle.SIZING:
            self.SetCursor(wx.Cursor(wx.CURSOR_SIZING))
        elif cursor is CursorStyle.ARROW:
            self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))

    def set_focus(self):
        self.SetFocus()


class Dialog(AbstractDialog, wx.Dialog):

    def __init__(self, parent, **kwargs):
        wx.Dialog.__init__(self, parent)
        super().__init__(**kwargs)
        self._create_widgets(self)
        self._create_gui().create_layout(self)
        self.Fit()
        self.SetSizeHints(self.GetSize().x, self.GetSize().y, self.GetMaxWidth(), self.GetMaxHeight())
        self.SetIcon(wx.Icon(parent.icon))

    def _create_gui(self):
        raise NotImplementedError

    @property
    def title(self):
        return super(Dialog, Dialog).title.__get__(self)

    @title.setter
    def title(self, title):
        super(Dialog, Dialog).title.__set__(self, title)
        self.SetTitle(title)

    def show_modal(self):
        self.update_gui({})
        self.Fit()
        return self.ShowModal() == 1

    def _on_ok(self, obj):
        super()._on_ok(obj)
        self.EndModal(self._return_value)

    def _on_cancel(self, obj):
        super()._on_cancel(obj)
        self.EndModal(self._return_value)


class MessageDialog(AbstractMessageDialog, wx.MessageDialog):

    def __init__(self, parent, message, title):
        wx.MessageDialog.__init__(self, parent, "", "", wx.OK | wx.ICON_ERROR)
        super().__init__(message, title=title)

    @property
    def title(self):
        return super(MessageDialog, MessageDialog).title.__get__(self)

    @title.setter
    def title(self, title):
        super(MessageDialog, MessageDialog).title.__set__(self, title)
        self.SetTitle(title)

    @property
    def message(self):
        return super(MessageDialog, MessageDialog).message.__get__(self)

    @message.setter
    def message(self, message):
        super(MessageDialog, MessageDialog).message.__set__(self, message)
        self.SetMessage(message)

    def show_modal(self):
        self.update_gui({})
        return self.ShowModal() == wx.ID_OK
