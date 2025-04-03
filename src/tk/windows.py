import tkinter
import tkinter.ttk
import tkinter.messagebox

from ..abstract.windows import AbstractFrame, FrameStyle, CursorStyle, AbstractDialog, AbstractErrorMessageDialog


class Frame(AbstractFrame):
    """Frame based on tkinter: a frame is used to create general-purpose windows."""

    def __init__(self, *, parent=None, pos=None, size=None, **kwargs):
        """Frame object initialization.

        :param parent: the parent window of the frame; None for a top-level frame
        :param pos: the desired position of the frame on the screen in pixel
        :param size: the desired size of the frame in pixel
        :param kwargs: additional parameters for superclass
        """
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
        self._layout_parent = self._toplevel
        super().__init__(parent=logical_parent, **kwargs)

    def set_layout(self, layout):
        """
        Set the layout to be used by the frame. This can be done only once, that is it is not allowed to change the
        layout used by the frame after a layout has already been set.

        :param layout: the layout object to be used by the frame
        """
        super().set_layout(layout)
        self._layout.grid(row=0, column=0, sticky="nsew")

    def event_connect(self, event, on_event):
        """Connect an event to a function.

        :param event: the event to connect
        :param on_event: the function to execute when the event is triggered
        """
        self._toplevel.bind(event, lambda e: on_event(**self._event_data[event]))

    def event_trigger(self, event, **kwargs):
        """Trigger an event.

        :param event: the event to trigger
        :param kwargs: the parameters to pass to the connected function
        """
        self._event_data[event] = kwargs
        self._toplevel.event_generate(event)

    @property
    def toplevel(self):
        """Return the Toplevel object that implements the frame.

        :return: the Toplevel object that implements the frame
        """
        return self._toplevel

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
        self._toplevel.title(self.title)

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
            self._toplevel.iconphoto(True, tkinter.PhotoImage(file=self.icon))

    def show(self):
        """Show the frame."""
        self._toplevel.deiconify()

    def hide(self):
        """Hide the frame."""
        self._toplevel.withdraw()

    def _command_close(self):
        """Command the frame to close."""
        self._on_close()

    def _on_close(self):
        """Function executed when the frame is closed."""
        self._close_operations()
        self._toplevel.destroy()
        if self.parent is None:
            self._toplevel.tk.quit()

    def set_menubar(self, menu):
        """Set a menu as main menubar of the frame.

        :param menu: the menu to set as menubar
        """
        menu.attach_menubar(menu)
        self._toplevel.config(menu=menu._widget)

    def set_cursor(self, cursor):
        """Set the cursor shape when the cursor is on the frame.

        :param cursor: the new cursor shape
        """
        if cursor is CursorStyle.SIZING:
            self._toplevel.configure(cursor='sb_h_double_arrow')
        elif cursor is CursorStyle.ARROW:
            self._toplevel.configure(cursor='arrow')

    def set_focus(self):
        """Set the focus on the frame."""
        self._toplevel.lift()


class Dialog(AbstractDialog):
    """
    Dialog based on tkinter: a dialog is used to create a window that allows the user to choose
    between two options: OK or Cancel.
    """

    def __init__(self, *, parent, **kwargs):
        """Initialize the dialog object.

        :param parent: parent window of the dialog
        :param kwargs: additional parameters for superclass
        """
        if not isinstance(parent, Frame):
            tk_parent = parent
        else:
            tk_parent = parent._toplevel
        self._toplevel = tkinter.Toplevel(tk_parent)
        self._toplevel.transient(tk_parent)

        self._toplevel.resizable(0, 0)

        self._panel = self._toplevel
        self._layout_parent = self._toplevel
        super().__init__(**kwargs)

    def set_layout(self, layout):
        """
        Set the layout to be used by the dialog. This can be done only once, that is it is not allowed to change the
        layout used by the dialog after a layout has already been set.

        :param layout: the layout object to be used by the dialog
        """
        super().set_layout(layout)
        self._layout.pack()

    @property
    def toplevel(self):
        """Return the Toplevel object that implements the dialog.

        :return: the Toplevel object that implements the dialog
        """
        return self._toplevel

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
        self._toplevel.title(self.title)

    def _show_dialog(self):
        """Show the dialog window."""
        self._toplevel.grab_set()
        self._toplevel.focus_force()
        self._toplevel.wait_window()

    def _on_ok(self, obj):
        """Executed when the OK choice is selected."""
        super()._on_ok(obj)
        self._toplevel.destroy()

    def _on_cancel(self, obj):
        """Executed when the Cancel choice is selected."""
        super()._on_cancel(obj)
        self._toplevel.destroy()

    def __enter__(self):
        """Enter function, necessary to correctly manage the with block with the dialog.

        :return: the dialog object itself
        """
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """Exit function, necessary to correctly manage the with block with the dialog.

        :param exc_type: exception type
        :param exc_value: exception value
        :param exc_traceback: exception traceback
        """
        pass

class ErrorMessageDialog(AbstractErrorMessageDialog):
    """
    Error message dialog based on tkinter: it is used to display a simple error message to the user and wait for a click
    on the OK button.
    """

    def __init__(self, *, parent, **kwargs):
        """Initialize the error message dialog object.

        :param parent: parent window of the error message dialog
        :param kwargs: additional parameters for superclass
        """
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

    def show_modal(self):
        """
        Show the error message dialog as a modal (on top of all other windows; the user must interact with the dialog).
        Can be executed only once.
        """
        super().show_modal()
        tkinter.messagebox.showerror(title=self.title, message=self.message)
