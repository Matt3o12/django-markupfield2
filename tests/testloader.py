import sys

if sys.version_info[:2] <= (2,6): # pragma: no cover
    import unittest2 as unittest
else: # pragma: no cover
    import unittest

