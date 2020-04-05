# -*- coding: UTF-8 -*-
from z3c.form.browser.text import TextWidget
from z3c.form.interfaces import ITextWidget
from zope.interface import implementer_only


class ITrustedTextWidget(ITextWidget):
    """Trusted Text widget."""


@implementer_only(ITrustedTextWidget)
class TrustedTextWidget(TextWidget):
    """Same a a TextLine Widget but does not escape code.
    The template uses content="structure view/value" instead of content="view/value"
    """
