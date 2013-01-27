python-datemath
===============

Simple expression language implementing date arithmetic for Python.

Sure, ``datetime.timedelta`` is nice, but code to do simple date arithmetic
shouldn't be that hard. Further, the logic for implementing date math "with
rounding" (e.g. ``NOW/DAY - 14DAYS``, meaning 14 days since the start of today)
is a little bit tricky, and reads much better as a string.

This module is implemented using PLY. It therefore has some basic syntax
checking and the beginnings of a REPL for testing. It also means that it uses a
LALR table-based parser which is auto-generated in memory from some definitions
in ``datemath_yacc.py``. 

Usage::

    >>> from datemath import datemath
    >>> datemath("NOW")
    datetime.datetime(2012, 2, 26, 21, 56, 52, 489700)
    >>> datemath("NOW - 1MONTH")
    datetime.datetime(2012, 1, 26, 21, 57, 41, 142164)
    >>> datemath("NOW/MONTH - 7DAYS")
    datetime.datetime(2012, 12, 25, 0, 0, 0)


References
----------

* `Solr Date Format`_ used as inspiration
* `PLY` used for the lexer and parser

.. _Solr Date Format: http://lucidworks.lucidimagination.com/display/lweug/Solr+Date+Format
.. _PLY: http://www.dabeaz.com/ply/
