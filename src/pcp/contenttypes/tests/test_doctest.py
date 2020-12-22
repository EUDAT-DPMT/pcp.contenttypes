from pcp.contenttypes.testing import PCP_CONTENTTYPES_FUNCTIONAL_TESTING
from plone.testing import layered

import doctest
import unittest


def test_suite():
    return unittest.TestSuite(
        [
            layered(
                doctest.DocFileSuite(
                    'README.txt',
                    package='pcp.contenttypes',
                    optionflags=doctest.ELLIPSIS | doctest.REPORT_ONLY_FIRST_FAILURE,
                ),
                layer=PCP_CONTENTTYPES_FUNCTIONAL_TESTING,
            )
        ]
    )
