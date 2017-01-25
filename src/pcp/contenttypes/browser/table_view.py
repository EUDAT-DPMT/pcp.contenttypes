
from Products.Five.browser import BrowserView


class TableView(BrowserView):
    """ Custom view (replaces base_view of Archetypes """

    def data(self):

        result = list()
        for field in self.context.Schema().fields():
            value = field.get(self.context)
            if value in (None, '', [], ()):
                continue
            result.append(dict(
                title=field.getName(),
                value=value))
        return result

