from collections import deque
from copy import copy

from ply import yacc

from shore import ast
from shore.lexer import Lexer
from shore.utils import PLYCompatLexer


class ParseError(Exception):
    pass

class Parser(object):
    precedence = (
        ("nonassoc", "AND", "OR"),
        ("right", "NOT"),
        ("nonassoc", "COMPARISON"),
        ("left", "AMPER", "VBAR", "CIRCUMFLEX"),
        ("left", "PLUS", "MINUS"),
        ("left", "STAR", "SLASH", "PERCENT"),
        ("right", "UNARY"),
        ("right", "STARSTAR"),
    )
    
    debug = False
    
    def __init__(self, text):
        self.text = text
        self.tokens = Lexer.tokens
        self.parser = yacc.yacc(module=self, tabmodule="shore.parsetab")
    
    def parse(self):
        return self.parser.parse(lexer=PLYCompatLexer(self.text), debug=self.debug)
    
    def p_error(self, t):
        raise ParseError(t)
    
    def p_input(self, t):
        """
        input : NEWLINE
              | statement
              | input NEWLINE
              | input statement
        """
        if len(t) == 2:
            if t[1] == "\n":
                t[0] = ast.NodeList([])
            else:
                t[0] = ast.NodeList([t[1]])
        else:
            if t[2] == "\n":
                t[0] = t[1]
            else:
                t[0] = ast.NodeList(t[1].nodes + [t[2]])
    
    def p_statement(self, t):
        """
        statement : simple_statement NEWLINE
                  | compound_statement
        """
        t[0] = t[1]
    
    def p_simple_statement(self, t):
        """
        simple_statement : expression
                         | declaration
                         | assignment_statement
                         | flow_statement
                         | import_statement
        """
        t[0] = t[1]
    
    def p_expression_bool(self, t):
        """
        expression : TRUE
                   | FALSE
        """
        val = {
            "True": True,
            "False": False,
        }
        t[0] = ast.BooleanNode(val[t[1]])
    
    def p_expression_none(self, t):
        """
        expression : NONE
        """
        t[0] = ast.NoneNode()
    
    def p_expression_string(self, t):
        """
        expression : STRING
        """
        t[0] = ast.StringNode(t[1])
        
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
                   | expression STARSTAR expression
        """
        t[0] = ast.BinOpNode(t[1], t[3], t[2])
    
    def p_expression_comp(self, t):
        """
        expression : expression EQEQ expression %prec COMPARISON
                   | expression NE expression %prec COMPARISON
                   | expression LESS expression %prec COMPARISON
                   | expression GREATER expression %prec COMPARISON
                   | expression LE expression %prec COMPARISON
                   | expression GE expression %prec COMPARISON
                   | expression IS expression %prec COMPARISON
        """
        t[0] = ast.CompNode(t[1], t[3], t[2])
    
    def p_expression_is_not(self, t):
        """
        expression : expression ISNOT expression %prec COMPARISON
        """
        t[0] = ast.UnaryOpNode(ast.CompNode(t[1], t[3], "is"), "not")
    
    def p_expression_in(self, t):
        """
        expression : expression IN expression %prec COMPARISON
                   | expression NOT IN expression %prec COMPARISON
        """
        if len(t) == 4:
            t[0] = ast.ContainsNode(t[1], t[3])
        else:
            t[0] = ast.UnaryOpNode(ast.ContainsNode(t[1], t[4]), "not")
    
    def p_expression_unop(self, t):
        """
        expression : NOT expression
                   | TILDE expression %prec UNARY
                   | PLUS expression %prec UNARY
                   | MINUS expression %prec UNARY
        """
        t[0] = ast.UnaryOpNode(t[2], t[1])
    
    def p_expression_par(self, t):
        """
        expression : LPAR expression RPAR
        """
        t[0] = t[2]
    
    def p_expression_subscript(self, t):
        """
        expression : expression LSQB expression RSQB
        """
        t[0] = ast.SubscriptNode(t[1], t[3])
    
    def p_expression_name(self, t):
        """
        expression : template
        """
        t[0] = t[1]

    def p_expression_function_call(self, t):
        """
        expression : expression LPAR arglist RPAR
        """
    
    def p_expression_int(self, t):
        """
        expression : NUMBER
        """
        t[0] = ast.IntegerNode(t[1])
    
    def p_expression_float(self, t):
        """
        expression : NUMBER DOT NUMBER
                   | NUMBER DOT
                   | DOT NUMBER
        """
        if len(t) == 4:
            t[0] = ast.FloatNode("%s.%s" % (t[1], t[3]))
        else:
            if t[1] == ".":
                t[0] = ast.FloatNode("0.%s" % t[2])
            else:
                t[0] = ast.FloatNode("%s.0" % t[1])
    
    def p_declaration(self, t):
        """
        declaration : template NAME EQUAL expression
        """
        t[0] = ast.DeclarationNode(t[1], t[2], t[4])
    
    def p_template(self, t):
        """
        template : NAME
                 | NAME LESS templates GREATER
        """
        if len(t) == 2:
            t[0] = ast.NameNode(t[1])
        else:
            t[0] = ast.TemplateNode(ast.NameNode(t[1]), t[3])
    
    def p_templates(self, t):
        """
        templates : template
                  | templates COMMA template
        """
        if len(t) == 2:
            t[0] = [t[1]]
        else:
            t[0] = t[1] + [t[3]]
    
    def p_assigment_statement_name(self, t):
        """
        assignment_statement : NAME EQUAL expression
        """
        t[0] = ast.AssignmentNode(t[1], t[3])
    
    def p_assignment_statement_attr(self, t):
        """
        assignment_statement : expression DOT NAME EQUAL expression
        """
    
    def p_assignment_statement_item(self, t):
        """
        assignment_statement : expression LSQB expression RSQB EQUAL expression
        """
        t[0] = ast.ItemAssignmentNode(t[1], t[3], t[6])
        
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
        # TODO: Extend to support from a import b, c as well as the as statement
    
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
        # TODO: Finally without except.
    
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
        function_definition : template DEF LESS expression GREATER NAME parameters COLON suite
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
