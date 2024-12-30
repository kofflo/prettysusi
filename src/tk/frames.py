import tkinter
import tkinter.ttk
import tkinter.messagebox

from ..abstract.frames import AbstractFrame, FrameStyle, CursorStyle, AbstractDialog, AbstractMessageDialog


class Frame(AbstractFrame):

    def __init__(self, *, parent=None, pos=None, size=None, **kwargs):

        if not isinstance(parent, Frame):
            logical_parent = None
            tk_parent = parent
        else:
            logical_parent = parent
            tk_parent = parent._toplevel
        self._toplevel = tkinter.Toplevel(tk_parent)
        self._toplevel.grid_columnconfigure(0, weight=1)
        self._toplevel.grid_rowconfigure(0, weight=1)

        geometry_string = ''
        if size is not None:
            geometry_string += f'{size[0]}x{size[1]}'
        if pos is not None:
            geometry_string += f'+{pos[0]}+{pos[1]}'
        if geometry_string != '':
            self._toplevel.geometry(geometry_string)

        self._update_gui_data = {}
        self._event_data = {}

        if self._STYLE is FrameStyle.FIXED_SIZE:
            self._toplevel.resizable(0, 0)
            self._toplevel.wm_protocol('WM_DELETE_WINDOW', self._on_close)
        elif self._STYLE is FrameStyle.DIALOG:
            self._toplevel.resizable(0, 0)
            self._toplevel.wm_protocol('WM_DELETE_WINDOW', lambda: None)
        else:
            self._toplevel.wm_protocol('WM_DELETE_WINDOW', self._on_close)

        self._panel = None
        self._parent = self._toplevel
        super().__init__(parent=logical_parent, **kwargs)
        self._layout.grid(row=0, column=0, sticky="nsew")

    def event_connect(self, event, on_event):
        self._toplevel.bind(event, lambda e: on_event(**self._event_data[event]))

    def event_trigger(self, event, **kwargs):
        self._event_data[event] = kwargs
        self._toplevel.event_generate(event)

    @property
    def toplevel(self):
        return self._toplevel

    @property
    def title(self):
        return super(Frame, Frame).title.__get__(self)

    @title.setter
    def title(self, title):
        super(Frame, Frame).title.__set__(self, title)
        self._toplevel.title(self.title)

    @property
    def icon(self):
        return super(Frame, Frame).icon.__get__(self)

    @icon.setter
    def icon(self, icon):
        super(Frame, Frame).icon.__set__(self, icon)
        if self.icon is not None:
            self._toplevel.iconphoto(True, tkinter.PhotoImage(file=self.icon))

    def show(self):
        #
        pass

    def _command_close(self):
        self._on_close()

    def _on_close(self):
        self._toplevel.destroy()
        self._close_operations()
        if self.parent is None:
            self._toplevel.tk.quit()

    def _set_menubar(self, menu):
        menu._build_menu(menubar=menu)
        self._toplevel.config(menu=menu._widget)

    def _set_cursor(self, cursor):
        if cursor is CursorStyle.SIZING:
            self._toplevel.configure(cursor='sb_h_double_arrow')
        elif cursor is CursorStyle.ARROW:
            self._toplevel.configure(cursor='arrow')

    def set_focus(self):
        self._toplevel.lift()


class Dialog(AbstractDialog):

    def __init__(self, *, parent, **kwargs):
        if not isinstance(parent, Frame):
            tk_parent = parent
        else:
            tk_parent = parent._toplevel
        self._toplevel = tkinter.Toplevel(tk_parent)
        self._toplevel.transient(tk_parent)

        self._update_gui_data = {}

        self._toplevel.resizable(0, 0)

        self._panel = self._toplevel
        self._parent = self._toplevel
        super().__init__(**kwargs)
        self._layout.pack()

    @property
    def toplevel(self):
        return self._toplevel

    @property
    def title(self):
        return super(Dialog, Dialog).title.__get__(self)

    @title.setter
    def title(self, title):
        super(Dialog, Dialog).title.__set__(self, title)
        self._toplevel.title(self.title)

    def show_modal(self):
        self._toplevel.grab_set()
        self._toplevel.wait_window()
        return self._return_value

    def _on_ok(self, obj):
        super()._on_ok(obj)
        self._toplevel.destroy()

    def _on_cancel(self, obj):
        super()._on_cancel(obj)
        self._toplevel.destroy()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        #
        pass

class MessageDialog(AbstractMessageDialog):

    def __init__(self, *, parent, **kwargs):
        super().__init__(**kwargs)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        #
        pass

    @property
    def title(self):
        return super(MessageDialog, MessageDialog).title.__get__(self)

    @title.setter
    def title(self, title):
        super(MessageDialog, MessageDialog).title.__set__(self, title)

    @property
    def message(self):
        return super(MessageDialog, MessageDialog).message.__get__(self)

    @message.setter
    def message(self, message):
        super(MessageDialog, MessageDialog).message.__set__(self, message)

    def show_modal(self):
        return_value = tkinter.messagebox.showerror(title=self.title, message=self.message)
        return return_value == tkinter.messagebox.OK
