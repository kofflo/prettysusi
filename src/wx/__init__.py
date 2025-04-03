import wx.lib.newevent


def event_create():
    """Create and return an event object.

    :return: the created event object
    """
    event_class, event_binder = wx.lib.newevent.NewEvent()
    return {'class': event_class, 'binder': event_binder}
