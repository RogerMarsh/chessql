# __init__.py
# Copyright 2017 Roger Marsh
# Licence: See LICENCE (BSD licence)
"""Chess Query Language (CQL) parser."""


def empty_copy(obj):
    """Return an empty instance of obj's class."""

    class Empty(obj.__class__):
        """Define class as sublass of obj.__class__."""

        def __init__(self):
            pass

    newcopy = Empty()
    # Pylint reports attribute-defined-outside-init for __class__.
    newcopy.__class__ = obj.__class__
    return newcopy
