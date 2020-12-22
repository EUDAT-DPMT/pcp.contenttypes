from Products.Five.browser import BrowserView


hidden_fields = (
    'id',
    'title',
    'description',
    'constrainTypesMode',
    'locallyAllowedTypes',
    'immediatelyAddableTypes',
    'location',
    'language',
    'effectiveDate',
    'creation_date',
    'modification_date',
    'creators',
    'excludeFromNav',
    'nextPreviousEnabled',
)

hidden_fields = dict([(f, 0) for f in hidden_fields])


class TableView(BrowserView):
    """ Custom view (replaces base_view of Archetypes) ignoring most empty values """

    def data(self):
        result = list()
        for field in self.context.Schema().fields():
            if field.getName() in hidden_fields:
                continue
            if field.widget.isVisible(self.context) in ['invisible', 'hidden']:
                continue
            value = field.get(self.context)
            if value in (None, '', [], ()):
                continue
            result.append(
                dict(
                    field=field.getName(),
                    title=field.widget.Label(self.context),
                    value=value,
                )
            )
        return result
