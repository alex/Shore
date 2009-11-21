from collections import deque
from copy import copy

from ply import yacc

from shore.lexer import Lexer
from shore.utils import PLYCompatLexer


class ParseError(object):
    pass

class Parser(object):
    precedence = (
        ("right", "UNARY"),
        ("left", "POWER"),
    )
    
    def __init__(self, text):
        self.text = text
        self.tokens = Lexer.tokens
        self.parser = yacc.yacc(module=self)
    
    def parse(self):
        return self.parser.parse(lexer=PLYCompatLexer(self.text))
    
    def p_error(self, t):
        raise ParseError
    
    def p_input(self, t):
        """
        input : NEWLINE
              | statement
              | NEWLINE input
              | statement input
        """
    
    def p_statement(self, t):
        """
        statement : simple_statement
                  | compound_statement
        """
    
    def p_simple_statement(self, t):
        """
        simple_statement : expression
                         | declaration
                         | assignment_statement
                         | flow_statement
                         | import_statement
        """
    
    def p_expression_constant(self, t):
        """
        expression : TRUE
                   | FALSE
                   | NONE
                   | STRING
                   | number
        """
    
    def p_expression_binop(self, t):
        """
        expression : expression PLUS expression
                   | expression MINUS expression
                   | expression STAR expression
                   | expression SLASH expression
                   | expression VBAR expression
                   | expression AMPER expression
                   | expression CIRCUMFLEX expression
                   | expression PERCENT expression
                   | expression AND expression
                   | expression OR expression
        """
    
    def p_expression_comp(self, t):
        """
        expression : expression EQUAL EQUAL expression
                   | expression EXCL EQUAL expression
                   | expression LESS expression
                   | expression GREATER expression
                   | expression LESS EQUAL expression
                   | expression GREATER EQUAL expression
                   | expression IS expression
                   | expression IS NOT expression
        """
    
    def p_expression_in(self, t):
        """
        expression : expression IN expression
                   | expression NOT IN expression
        """
    
    def p_expression_power(self, t):
        """
        expression : expression STAR STAR expression %prec POWER
        """
    
    def p_expression_unop(self, t):
        """
        expression : NOT expression %prec UNARY
                   | TILDE expression %prec UNARY
                   | PLUS expression %prec UNARY
                   | MINUS expression %prec UNARY
        """
    
    def p_expression_par(self, t):
        """
        expression : LPAR expression RPAR
        """
    
    def p_expression_subscript(self, t):
        """
        expression : expression LSQB expression RSQB
        """
    
    def p_expression_name(self, t):
        """
        expression : NAME
        """

    def p_expression_function_call(self, t):
        """
        expression : expression LPAR arglist RPAR
        """
    
    def p_number(self, t):
        """
        number : NUMBER
               | NUMBER DOT NUMBER
               | NUMBER DOT
               | DOT NUMBER
        """
    
    def p_declaration(self, t):
        """
        declaration : expression NAME EQUAL expression
        """
    
    def p_expression_type(self, t):
        """
        expression : NAME LESS expressions GREATER
        """
    
    def p_expressions(self, t):
        """
        expressions : expression
                    | expressions COMMA expression
        """
    
    def p_assigment_statement(self, t):
        """
        assignment_statement : NAME EQUAL expression
        """
        # TODO: extend do support i[j] = k, i.j = k, and anything else needed.
    
    def p_flow_statement(self, t):
        """
        flow_statement : BREAK
                       | PASS
                       | CONTINUE
                       | return_statement
                       | raise_statement
                       | yield_statement
        """
    
    def p_return_statement(self, t):
        """
        return_statement : RETURN expression
        """
    
    def p_raise_statement(self, t):
        """
        raise_statement : RAISE
                        | RAISE expression
        """
    
    def p_yield_statement(self, t):
        """
        yield_statement : YIELD expression
        """
    
    def p_import_statement(self, t):
        """
        import_statement : FROM dotted_name IMPORT NAME
                         | IMPORT dotted_name
        """
        # TODO: Extend to support from a import b, c as well as the add statement
    
    def p_dotted_name(self, t):
        """
        dotted_name : NAME
                    | dotted_name DOT NAME
        """
    
    def p_compound_statement(self, t):
        """
        compound_statement : if_statement
                           | try_statement
                           | while_statement
                           | for_statement
                           | function_definition
                           | class_definition
                           | decorated
        """
    
    def p_if_statement(self, t):
        """
        if_statement : IF expression COLON suite
                     | IF expression COLON suite ELSE COLON suite
                     | IF expression COLON suite elifs
                     | IF expression COLON suite elifs ELSE COLON suite
        """
    
    def p_elifs(self, t):
        """
        elifs : ELIF expression COLON suite
              | elifs ELIF expression COLON suite
        """
    
    def p_try_statement(self, t):
        """
        try_statement : TRY COLON suite EXCEPT COLON suite
                      | TRY COLON suite EXCEPT FINALLY COLON suite
        """
    
    def p_while_statement(self, t):
        """
        while_statement : WHILE expression COLON suite
        """
    
    def p_for_statement(self, t):
        """
        for_statement : FOR NAME IN expression COLON suite
        """
    
    def p_suite(self, t):
        """
        suite : NEWLINE INDENT statements DEDENT
        """
    
    def p_statements(self, t):
        """
        statements : statement
                   | statements statement
        """
    
    def p_function_definition(self, t):
        """
        function_definition : expression DEF LESS expression GREATER NAME parameters COLON suite
                            | DEF NAME parameters COLON suite
        """
        # TODO: This is way too restrictive, it requires a return type to be
        # templated, and templating only allows a single type
    
    def p_class_definition(self, t):
        """
        class_definition : CLASS LESS expression GREATER NAME parameters COLON suite
                         | CLASS NAME parameters COLON suite
        """
        # TODO: This only allows templating over a single type.
    
    def p_decorated(self, t):
        """
        decorated : decorators class_definition
                  | decorators function_definition
        """
    
    def p_decorators(self, t):
        """
        decorators : decorator
                   | decorators decorator
        """
    
    def p_decorator(self, t):
        """
        decorator : AT dotted_name NEWLINE
                  | AT dotted_name LPAR arglist RPAR NEWLINE
        """
    
    def p_parameters(self, t):
        """
        parameters : LPAR RPAR
                   | LPAR expression NAME RPAR
        """
        # TODO: This supports taking 0 or 1 params now, and doesn't allow
        # default arguments
    
    def p_arglist(self, t):
        """
        arglist : argument
                | arglist COMMA argument
        """
        # TODO: Trailing commas should be allowed
    
    def p_argument(self, t):
        """
        argument : expression 
                 | NAME EQUAL expression
        """
    
    # TODO: Support atoms (tuple, list, dict, set)
