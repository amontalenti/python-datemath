
# -----------------------------------------------------------------------------
# datemath.py
#
# A simple calculator with variables -- all in one file -- modified to support
# date math syntax as well. (converts expressions like 1DAY into the # of 
# seconds in a day, likewise for 1MONTH and 5YEARS).
# -----------------------------------------------------------------------------

tokens = (
    'NAME','NUMBER',
    'PLUS','MINUS','ROUND','EQUALS',
    'LPAREN','RPAREN', 'NOW', 'DATE'
    )

# Tokens

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_EQUALS  = r'='
t_ROUND   = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_NAME    = r'[a-zA-Z_][a-zA-Z0-9_]*'

class Units:
    MILLI = 0.001
    MILLISECOND = MILLI
    SECOND = 1
    MINUTE = 60
    HOUR = 60*MINUTE
    DAY = 24*HOUR
    MONTH = 30*DAY
    YEAR = 365*DAY

import datetime

def t_DATE(t):
    r'([0-9]*)(YEAR|MONTH|DAY|HOUR|MINUTE|SECOND|MILLI|MILLISECOND)(S)?'
    # known issue: if doing date math with months or years, we're facing bugs
    # related to end-of-month (e.g. 3/31/2013 - 1MONTH does not equal 1/28/2013)
    # and related to leap year (e.g. 2013/1/1 - 1YEAR does not equal 1/1/2012)
    # these issues are handled in Java by the "Calendar" class, which is able to
    # handle these edge cases by using the "numdays minimum" algorithm. That is,
    # given two operands, dt1 and dt2, you calculate:
    # >>> daymin = min(numdays(dt1.month), numdays(dt2.month))
    # and then say, if dt2.day > daymin then newdt.day = daymin
    # an interesting truth revealed by this math --
    #      3/31/2013 - 1MONTH - 1MONTH = 1/28/2013
    # yet, 3/31/2013 - 2MONTH          = 1/31/2013
    # kind of mind-bending, eh?
    regex = t.lexer.lexmatch.groups()
    if regex[1] == "":
        # round to the specified date
        t.value = regex[2]
    else:
        # get the date value for math purposes
        t.value = datetime.timedelta(seconds=int(regex[1]) * getattr(Units, regex[2]))
    return t

import datetime

def t_NOW(t):
    r'NOW'
    t.value = datetime.datetime.now()
    return t

def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

# Ignored characters
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
# Build the lexer
import ply.lex as lex
lex.lex()

# Parsing rules

precedence = (
    ('left','PLUS','MINUS'),
    ('left','ROUND'),
    ('right','UMINUS'),
    )

# dictionary of names
names = {}

def seconds_rounding(dt=None, roundTo=60):
    if dt == None: 
        dt = datetime.datetime.now()
    seconds = (dt - dt.min).seconds
    # is a floor division, not a comment on following line:
    rounding = (seconds+roundTo/2) // roundTo * roundTo
    rounding = 0
    return dt + datetime.timedelta(0,rounding-seconds,-dt.microsecond)

def date_modulo(dateval, roundval):
    if roundval == "YEAR":
        rounded = seconds_rounding(dateval, Units.DAY)
        rounded = rounded.replace(day=1, month=1)
    elif roundval == "MONTH":
        rounded = seconds_rounding(dateval, Units.DAY)
        rounded = rounded.replace(day=1)
    else:
        rounded = seconds_rounding(dateval, getattr(Units, roundval))
    return rounded
    
def p_statement_assign(t):
    'statement : NAME EQUALS expression'
    names[t[1]] = t[3]

def p_statement_expr(t):
    'statement : expression'
    t[0] = t[1]

def p_expression_binop(t):
    '''expression : expression ROUND expression
                  | expression PLUS expression
                  | expression MINUS expression'''
    if t[2] == '+'  : t[0] = t[1] + t[3]
    elif t[2] == '-': t[0] = t[1] - t[3]
    elif t[2] == '/': t[0] = date_modulo(dateval=t[1], roundval=t[3])

def p_expression_uminus(t):
    'expression : MINUS expression %prec UMINUS'
    t[0] = -t[2]

def p_expression_group(t):
    'expression : LPAREN expression RPAREN'
    t[0] = t[2]

def p_expression_number(t):
    'expression : NUMBER'
    t[0] = t[1]

def p_expressions_now(t):
    'expression : NOW'
    t[0] = t[1]

def p_expression_date(t):
    'expression : DATE'
    t[0] = t[1]

def p_expression_name(t):
    'expression : NAME'
    try:
        t[0] = names[t[1]]
    except LookupError:
        print("Undefined name '%s'" % t[1])
        t[0] = 0

def p_error(t):
    if t is None:
        print("Syntax error with null value")
    else:
        print("Syntax error at '%s'" % t.value)

import ply.yacc as yacc
yacc.yacc(write_tables=0)

if __name__ == "__main__":
    while 1:
        try:
            s = raw_input('calc > ')   # Use raw_input on Python 2
        except EOFError:
            break
        yacc.parse(s)
