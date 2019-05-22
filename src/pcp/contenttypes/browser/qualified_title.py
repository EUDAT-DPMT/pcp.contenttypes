
from Products.Five.browser import BrowserView



class QualifiedTitleView(BrowserView):
    """ Prefixes the title with teh portal type for non-standard types"""

    def qualifiedTitle(self):
        """Portal type plus title"""
        type_info = self.context.getTypeInfo()
        title = self.context.Title()
        if type_info.Title() in ['Folder', 'Page', 'Document', 'Topic', 'Image', 'File', 'Event', 'Link']:
            return title
        return "%s: %s" % (type_info.Title(), title)

