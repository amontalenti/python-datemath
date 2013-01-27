from datemath_yacc import yacc

def datemath(expr):
    return yacc.parse(expr)
