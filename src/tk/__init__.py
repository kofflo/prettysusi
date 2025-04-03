import uuid
from tkinter import ttk


def event_create():
    """Create and return an event object.

    :return: the created event object
    """
    event_id = uuid.uuid4()
    return '<<' + str(event_id) + '>>'


ttk_style = ttk.Style()
