python-datemath
===============

Simple expression language implementing date arithmetic for Python.

Sure, `datetime.timedelta` is nice, but code to do simple date arithmetic
shouldn't be that hard. Further, the logic for implementing date math "with
rounding" (e.g. `NOW/DAY - 14DAYS`, meaning 14 days since the start of today)
is a little bit tricky, and reads much better as a string.

This module is implemented using PLY. It therefore has some basic syntax
checking and the beginnings of a REPL for testing. It also means that it uses a
LALR table-based parser which is auto-generated in memory from some definitions
in `datemath_yacc.py`. 

