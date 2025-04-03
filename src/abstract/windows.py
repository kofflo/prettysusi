"""
Definition of the abstract window classes supported by the library: frame, dialog and message dialog.
The details of the implementation for each supported GUI type are defined in the concrete subclasses.

Classes:
    FrameStyle: enumeration used to define the style of a frame
    CursorStyle enumeration used to define the style of the cursor
    AbstractFrame: superclass for the frame classes (not to be instantiated)
    AbstractDialog: superclass for the dialog classes (not to be instantiated)
    AbstractMessageDialog: superclass for the message dialog classes (not to be instantiated)
"""
from enum import Enum, auto

import prettysusi

from .. import event_create, BaseClass


class FrameStyle(Enum):
    """Enum class defining the supported frame styles."""
    NORMAL = auto()
    FIXED_SIZE = auto()
    DIALOG = auto()


class CursorStyle(Enum):
    """Enum class defining the supported cursor styles."""
    ARROW = auto()
    SIZING = auto()


class _WindowClass:
    """Superclass for all types of window classes (Frame, Dialog and MessageDialog)."""

    def __init__(self, title=""):
        self.title = title
        self._layout = None

    @property
    def title(self):
        """Return the window title.

        :return: the window title
        """
        return self._title

    @title.setter
    def title(self, title):
        """Set the window title.

        :param title: the new window title
        """
        self._title = title

    @property
    def __panel(self):
        """Return the panel object of the window (necessary to place widgets inside the window).

        :return: the panel object of the window
        """
        return self._panel

    @property
    def __layout_parent(self):
        """Return the layout parent object (necessary to apply a layout to the window).

        :return: the layout parent object of the window
        """
        return self._layout_parent


class AbstractFrame(_WindowClass, BaseClass):
    """
    Base class for Frame. This class should not be instantiated.
    A frame is used to create general-purpose windows.
    """

    _STYLE = FrameStyle.NORMAL
    _close_event = event_create()
    _update_gui_event = event_create()

    def __init__(self, *, parent=None, icon=None, **kwargs):
        """Frame object initialization.

        :param parent: the parent window of the frame; None for a top-level frame
        :param icon: the frame icon
        """
        self.parent = parent
        if parent is not None:
            parent.child_views.append(self)
        self.child_views = []
        self.icon = icon
        self.event_connect(self._close_event, self._on_close_event)
        self.event_connect(self._update_gui_event, self._on_update_gui_event)
        self._default_layout = prettysusi.VBoxLayout()
        super().__init__(**kwargs)

    def set_layout(self, layout):
        """
        Set the layout to be used by the frame. This can be done only once, that is it is not allowed to change the
        layout used by the frame after a layout has already been set.

        :param layout: the layout object to be used by the frame
        """
        if self._layout is not None:
            raise AttributeError("A layout has already been set.")
        self._default_layout.add(layout, align=prettysusi.Align.EXPAND, stretch=1)
        self._layout = self._default_layout._create_layout(self)

    def event_connect(self, event, on_event):
        """Connect an event to a function.

        :param event: the event to connect
        :param on_event: the function to execute when the event is triggered
        """
        raise NotImplementedError

    def event_trigger(self, event, **kwargs):
        """Trigger an event.

        :param event: the event to trigger
        :param kwargs: the parameters to pass to the connected function
        """
        raise NotImplementedError

    @property
    def icon(self):
        """Return the frame icon.

        :return: the frame icon
        """
        return self._icon

    @icon.setter
    def icon(self, icon):
        """Set the frame icon.

        :param icon: the new frame icon
        """
        self._icon = icon

    def show(self):
        """Show the frame."""
        raise NotImplementedError

    def hide(self):
        """Hide the frame."""
        raise NotImplementedError

    def _command_close(self):
        """Command the frame to close."""
        raise NotImplementedError

    def _command_update_gui(self, data):
        """
        Command the update of the content of the frame and of its child views recursively,
        using the data provided as input.

        :param data: the data to use for the content update
        """
        self.on_update_gui(data)
        for child_view in self.child_views:
            child_view.update_gui(data)

    def _close_operations(self):
        """
        Perform the necessary operations when closing the frame (detach from parent's child list,
        close all child windows, call the on_close function.
        """
        if self.parent is not None:
            self.parent.child_views.remove(self)
        for child in self.child_views:
            child.close()
        self.on_close()

    def on_close(self):
        """User-defined function executed when the frame is being closed."""
        pass

    def on_update_gui(self, data):
        """User-defined function executed when the frame content is being updated.

        :param data: the data to use for the content update
        """
        pass

    def set_menubar(self, menu):
        """Set a menu as main menubar of the frame.

        :param menu: the menu to set as menubar
        """
        raise NotImplementedError

    def set_focus(self):
        """Set the focus on the frame."""
        raise NotImplementedError

    def set_cursor(self, cursor):
        """Set the cursor shape when the cursor is on the frame.

        :param cursor: the new cursor shape
        """
        raise NotImplementedError

    def _on_close_event(self):
        """Function executed when the close event is triggered."""
        self._command_close()

    def _on_update_gui_event(self, data):
        """Function executed when the update GUI event is triggered."""
        self._command_update_gui(data)

    def close(self):
        """Trigger the close event, that starts the chain of operations leading to the frame being closed."""
        self.event_trigger(self._close_event)

    def update_gui(self, data):
        """Trigger the update GUI event, that starts the chain of operations leading to the frame content being updated.

        :param data: the data to use for the content update
        """
        self.event_trigger(self._update_gui_event, data=data)


class AbstractDialog(_WindowClass, BaseClass):
    """
    Base class for Dialog. This class should not be instantiated.
    A dialog is used to create a window that allows the user to choose between two options: OK or Cancel.
    A dialog can be shown only once; a new instance have to be created if the same dialog needs to be shown again.
    """

    def __init__(self, **kwargs):
        """Initialize the dialog object.

        :param kwargs: additional paremeters for superclass
        """
        self._return_value = False
        self._shown = False
        super().__init__(**kwargs)

    def set_layout(self, layout):
        """
        Set the layout to be used by the dialog. This can be done only once, that is it is not allowed to change the
        layout used by the dialog after a layout has already been set.

        :param layout: the layout object to be used by the dialog
        """
        if self._layout is not None:
            raise AttributeError("A layout has already been set.")
        self._layout = layout._create_layout(self)

    def show_modal(self):
        """
        Show the dialog window as a modal (on top of all other windows; the user must interact with the dialog)
        and return a boolean value based on the user choice (True for OK, False for Cancel or no response).
        Can be executed only once.

        :return: a boolean value based on the user choice
        """
        if self._shown:
            raise Exception("A dialog cannot be shown more than once.")
        self._shown = True
        self._show_dialog()
        return self._return_value

    def _show_dialog(self):
        """Show the dialog window (implementation depends on the specific GUI)."""
        raise NotImplementedError

    def _create_ok_button(self, label='OK'):
        """Create the button to the used for the OK choice.

        :param label: the label of the button
        :return: the button object
        """
        from prettysusi.widgets import Button
        return Button(parent=self, label=label, on_click=self._on_ok)

    def _create_cancel_button(self, label='Cancel'):
        """Create the button to the used for the Cancel choice.

        :param label: the label of the button
        :return: the button object
        """
        from prettysusi.widgets import Button
        return Button(parent=self, label=label, on_click=self._on_cancel)

    def _on_ok(self, obj):
        """Executed when the OK choice is selected. The return value is set to True.

        :param obj: the obj
        """
        self.on_ok()
        self._return_value = True

    def _on_cancel(self, obj):
        """Executed when the Cancel choice is selected. The return value is set to False."""
        self.on_cancel()
        self._return_value = False

    def on_ok(self):
        """User-defined function executed when the OK choice is selected."""
        pass

    def on_cancel(self):
        """User-defined function executed when the Cancel choice is selected."""
        pass


class AbstractErrorMessageDialog(_WindowClass, BaseClass):
    """
    Base class for ErrorMessageDialog. This class should not be instantiated.
    An error message dialog is used to display a simple error message to the user and wait for a click on the OK button.
    An error message dialog can be shown only once; a new instance have to be created if it needs to be shown again.
    No widgets or layout can be used in an error message dialog.
    """

    def __init__(self, *, message="", **kwargs):
        """Initialize the error message dialog.

        :param message: the message to display
        :param kwargs: additional parameters for the superclass
        """
        self.message = message
        self._shown = False
        super().__init__(**kwargs)

    @property
    def message(self):
        """Return the message to display in the error message dialog.

        :return: the message to display
        """
        return self._message

    @message.setter
    def message(self, message):
        """Set the message to display in the error message dialog.

        :param message: the new message
        """
        self._message = message

    def show_modal(self):
        """
        Show the error message dialog as a modal (on top of all other windows; the user must interact with the dialog).
        Can be executed only once.
        """
        if self._shown:
            raise Exception("An error message dialog cannot be shown more than once.")
        self._shown = True
