from collections import deque
from copy import copy

from ply import yacc

from shore.lexer import Lexer
from shore.utils import PLYCompatLexer


class Parser(object):
    def __init__(self, text):
        self.text = text
        self.tokens = Lexer.tokens
        self.parser = yacc.yacc(module=self)
    
    def parse(self):
        return self.parser.parse(lexer=PLYCompatLexer(self.text))
    
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
    
    def p_expression_power(self, t):
        """
        expression : expression STAR STAR expression
        """
    
    def p_expression_unop(self, t):
        """
        expression : NOT expression
                   | TILDE expression
        """
    
    def p_expression_par(self, t):
        """
        expression : LPAR expression RPAR
        """
    
    def p_expression_subscript(self, t):
        """
        expression : expression LSQB expression RSQB
        """
    
    def p_number(self, t):
        """
        number : NUMBER
               | NUMBER DOT NUMBER
               | NUMBER DOT
               | DOT NUMBER
        """
