from Products.Five.browser import BrowserView


class UpdateUID(BrowserView):
    """Provide utility to reset the uid of an item.
    Use case: carry over the uids from EUDATs RCT specifically
    for accounted items, so the records carry over.
    May be useful for other item types as well, e.g. service components
    """

    def reset_uid(self, uid=None):
        """Reset the uid to the value passed in.
        Existing references should survive this operation.
        No checks are perfomed on the new value passed in.
        Use with care ..."""
        if uid is None:
            return
        self.context._setUID(uid)
        self.request.response.redirect(self.context.absolute_url())
