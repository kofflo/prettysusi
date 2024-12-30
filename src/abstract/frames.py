from enum import Enum, auto

import prettysusi

from .. import event_create, BaseClass


class FrameStyle(Enum):
    """Enum class defining the allowed frame styles."""
    NORMAL = auto()
    FIXED_SIZE = auto()
    DIALOG = auto()


class CursorStyle(Enum):
    """Enum class defining the allowed cursor styles."""
    ARROW = auto()
    SIZING = auto()


class AbstractFrame(BaseClass):
    """Base class for Frame objects."""

    _STYLE = FrameStyle.NORMAL
    _close_event = event_create()
    _update_gui_event = event_create()

    def __init__(self, *, parent=None, title="", icon=None):
        """Frame object initialization.

        :param parent: the parent of the frame; None for a top-level frame.
        :param title: the frame title
        :param icon: the frame icon
        """
        self.parent = parent
        if parent is not None:
            parent.child_views.append(self)
        self.child_views = []
        self.title = title
        self.icon = icon
        self.event_connect(self._close_event, self._on_close_event)
        self.event_connect(self._update_gui_event, self._on_update_gui_event)
        self._create_widgets(self._panel)
        self._create_menu()
        self._default_sizer = prettysusi.VBoxLayout()
        self._default_sizer.add(self._create_gui(), align=prettysusi.Align.EXPAND, stretch=1)
        self._layout = self._default_sizer._create_layout(self._parent)

    def event_connect(self, event, on_event):
        """Connect an event to a function.

        :param event: the event to connect.
        :param on_event: the function to execute when the event is triggered.
        """
        raise NotImplementedError

    def event_trigger(self, event, **kwargs):
        """Triggers an event.

        :param event: the event to trigger.
        :param kwargs: the parameters to pass to the connected function.
        """
        raise NotImplementedError

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = title

    @property
    def icon(self):
        return self._icon

    @icon.setter
    def icon(self, icon):
        self._icon = icon

    def show(self):
        """Show the frame."""
        raise NotImplementedError

    def _command_close(self):
        """Close the frame."""
        raise NotImplementedError

    def _command_update_gui(self, data):
        """Update the content of the frame and of its child views recursively using the data provided as input.

        :param data: the data to use for the content update.
        """
        self.on_update_gui(data)
        for child_view in self.child_views:
            child_view.update_gui(data)
        self._fit_frame()

    def _close_operations(self):
        if self.parent is not None:
            self.parent.child_views.remove(self)
        for child in self.child_views:
            child.close()
        self.on_close()

    def on_close(self):
        #
        pass

    def _fit_frame(self):
        #
        pass

    def _set_menubar(self, menu):
        raise NotImplementedError

    def set_focus(self):
        raise NotImplementedError

    def _set_cursor(self, cursor):
        raise NotImplementedError

    def _on_close_event(self):
        self._command_close()

    def _on_update_gui_event(self, data):
        self._command_update_gui(data)

    def close(self):
        self.event_trigger(self._close_event)

    def update_gui(self, data):
        self.event_trigger(self._update_gui_event, data=data)

    def _create_menu(self):
        #
        pass

    def _create_widgets(self, panel):
        #
        pass

    def _create_gui(self):
        return prettysusi.VBoxLayout()


class AbstractDialog(BaseClass):

    def __init__(self, *, title=""):
        self.title = title
        self._return_value = False
        self._create_widgets(self._panel)
        self._layout = self._create_gui()._create_layout(self._parent)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = title

    def update_gui(self, data):
        #
        pass

    def show_modal(self):
        raise NotImplementedError

    def _on_ok(self, obj):
        self.on_ok()
        self._return_value = True

    def _on_cancel(self, obj):
        self.on_cancel()
        self._return_value = False

    def on_ok(self):
        #
        pass

    def on_cancel(self):
        #
        pass

    def _create_widgets(self, panel):
        #
        pass

    def _create_gui(self):
        return prettysusi.VBoxLayout()


class AbstractMessageDialog(AbstractDialog):

    def __init__(self, *, message="", **kwargs):
        self.message = message
        self._panel = None
        self._parent = None
        super().__init__(**kwargs)

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, message):
        self._message = message
