# patches to by applied using collective.monkeypatcher
# follows advice from 
# http://docs.plone.org/develop/plone/misc/monkeypatch.html


#
# patch the diff tool to support some of ATEXtensions' fields 
# (record(s) in particular) in diff view
#

from Products.CMFDiffTool.TextDiff import TextDiff
from Products.CMFDiffTool.TextDiff import AsTextDiff
from Products.CMFDiffTool.FieldDiff import FieldDiff
from Products.CMFDiffTool.BinaryDiff import BinaryDiff
from Products.CMFDiffTool.ListDiff import ListDiff

NEW_AT_FIELD_MAPPING = {'text': 'variable_text',
                        'string': 'variable_text',
                        'datetime': FieldDiff,
                        'file': 'variable_binary',
                        'blob': 'variable_binary',
                        'image': BinaryDiff,
                        'lines': ListDiff,
                        'integer': FieldDiff,
                        'float': FieldDiff,
                        'fixedpoint': FieldDiff,
                        'boolean': FieldDiff,
                        'record': AsTextDiff,
                        'address': AsTextDiff,
                        'records': AsTextDiff,
                        'reference': 'raw:ListDiff'}

patched_field_mapping = lambda : NEW_AT_FIELD_MAPPING  # Now we have a callable method!

def apply_patched_mapping(scope, original, replacement):
    setattr(scope, original, replacement())
    return
