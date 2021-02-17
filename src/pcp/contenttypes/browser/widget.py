"""
Example use in a template:
<div tal:define="widget_view nocall:context/@@widget_view">
  <div class="field"
       tal:define="widget python:widget_view.get_widget(obj, 'projects_involved')"
       tal:condition="python:widget">
      <label tal:content="widget/label" />
      <br />
      <div tal:content="structure widget/render" />
  </div>
</div>

For behaviors pass interface and fieldname,
e.g. get_widget(obj, 'IRichTextBehavior.text')
"""
from plone import api
from plone.app.contentlisting.interfaces import IContentListing
from plone.dexterity.browser.view import DefaultView
from Products.Five.browser import BrowserView


class WidgetView(BrowserView):
    """Get the widget for any field on a content object.
    Useful to get the default-rendering as configured in the schema.
    """

    def get_widget(self, obj, fieldname):
        default_view = DefaultView(obj, self.request)
        default_view.update()
        if fieldname in default_view.w:
            return default_view.w[fieldname]


class RelationFieldHelper(BrowserView):

    def items(self, widget):
        """Return item for the widget values for the display template.

        Query the catalog for the widget-value (uuids) to only display items
        that the user is allowed to see. Accessing the value with e.g.
        getattr(self.context, self.__name__) would yield the items unfiltered.
        Uses IContentListing for easy access to MimeTypeIcon and more.

        Same as plone.app.z3cform.widget.RelatedItemsWidget.items but for SelectFields
        Used to help display the values of a RelationField that uses a SelectWidget.
        The template that uses this is pcp/contenttypes/select_relation_display.pt
        """
        results = []
        if not widget.value:
            return results
        if isinstance(widget.value, str):
            separator = getattr(widget, 'separator', ';')
            uuids = widget.value.split(separator)
        else:
            uuids = widget.value

        brains = api.content.find(UID=uuids)
        # restore original order
        results = sorted(brains, key=lambda brain: uuids.index(brain.UID))
        return IContentListing(results)
