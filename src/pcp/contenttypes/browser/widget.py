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
