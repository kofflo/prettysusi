import PySide6.QtCore


def event_create():
    """Create and return an event object.

    :return: the created event object
    """
    return PySide6.QtCore.Signal(dict)
