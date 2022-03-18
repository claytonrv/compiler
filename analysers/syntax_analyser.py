import sys
from os import path
from turtle import left

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from constants import SYMBOLS_TABLE
from models.nodes import (
    AllocExpressionNode,
    AtributeStatementNode,
    ExpressionNode,
    ForStatementNode,
    FunctionListNode,
    FunctionCallNode,
    FunctionDefinitionNode,
    IfStatementNode,
    LValueNode,
    NumberNode,
    ParamerterListCallNode,
    ParamerterListNode,
    ParamerterNode,
    PrintStatementNode,
    ProgramNode,
    ReadStatementNode,
    ReturnStatementNode,
    StatementListNode,
    StatementNode,
    StringNode,
    NullNode,
    TermNode,
    UnaryOperationNode,
    BinaryOperationNode,
    VariableDeclarationNode,
)


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_index = -1
        self.advance()

    def advance(self):
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        return self.current_token

    def factor(self):
        token = self.current_token()
        factor = None

        if token.type == SYMBOLS_TABLE.index(
            "int_constant"
        ) or token.type == SYMBOLS_TABLE.index("float_constant"):
            factor = NumberNode(token)
        elif token.type == SYMBOLS_TABLE.index("string_constant"):
            factor = StringNode(token)
        elif token.type == SYMBOLS_TABLE.index("null"):
            factor = NullNode(token)
        elif token.type == SYMBOLS_TABLE.index("identifier"):
            factor = self.lvalue()
        else:
            factor = self.numerical_expression()

        if factor:
            self.advance()
            return factor

    def unary_expression(self):
        left = self.current_token()
        self.advance()
        factor = self.factor()
        return UnaryOperationNode(left, factor)

    def term(self):
        left = self.unary_expression()
        operation_token = None
        right = None
        self.advance()
        token = self.current_token

        while token.type in [
            SYMBOLS_TABLE.index("multiplication"),
            SYMBOLS_TABLE.index("division"),
            SYMBOLS_TABLE.index("modulus"),
        ]:
            operation_token = self.current_token
            self.advance()
            right = self.unary_expression()
            left = TermNode(left, operation_token, right)
        return left

    def numerical_expression(self):
        left = self.term()
        operation_token = None
        right = None
        self.advance()
        token = self.current_token

        while token.type in [
            SYMBOLS_TABLE.index("addition"),
            SYMBOLS_TABLE.index("subtraction"),
        ]:
            operation_token = token
            self.advance()
            right = self.current_token
            left = BinaryOperationNode(left, operation_token, right)
        return left

    def expression(self):
        left = self.numerical_expression()
        operation_token = None
        right = None
        self.advance()
        token = self.current_token

        if token.type in [
            SYMBOLS_TABLE.index("less_than"),
            SYMBOLS_TABLE.index("greater_than"),
            SYMBOLS_TABLE.index("less_or_equal_to"),
            SYMBOLS_TABLE.index("greater_or_equal_to"),
            SYMBOLS_TABLE.index("equals"),
            SYMBOLS_TABLE.index("different"),
        ]:
            operation_token = token
            self.advance()
            right = self.numerical_expression()

        return ExpressionNode(left, operation_token, right)

    def lvalue(self):
        identifier = self.current_token
        self.advance()
        open_parentheses = self.current_token
        self.advance()
        open_bracket = self.current_token
        self.advance()
        num_expression = self.numerical_expression()
        self.advance()
        close_parentheses = self.current_token
        self.advance()
        close_bracket = self.current_token
        return LValueNode(
            identifier,
            open_parentheses,
            open_bracket,
            num_expression,
            close_parentheses,
            close_bracket,
        )

    def alloc_expression(self):
        allocation_token = self.current_token
        self.advance()
        operator = self.current_token
        self.advance()
        expression = self.expression()
        return AllocExpressionNode(allocation_token, operator, expression)

    def param_list_call(self):
        open_parentheses = self.current_token
        identifiers = []
        self.advance()

        while self.current_token.type != SYMBOLS_TABLE.index("close_parentheses"):
            next_identifier = self.current_token
            self.advance()
            identifiers.append(next_identifier)
        close_parentheses = self.current_token
        return ParamerterListCallNode(open_parentheses, identifiers, close_parentheses)

    def param_list(self):
        params = []
        open_parentheses = self.current_token
        self.advance()

        while self.current_token.type != SYMBOLS_TABLE.index("close_parentheses"):
            token = self.current_token
            if token.type == SYMBOLS_TABLE.index(
                "int"
            ) or token.type == SYMBOLS_TABLE.index("float"):
                factor = NumberNode(token)

            if token.type == SYMBOLS_TABLE.index("string"):
                factor = StringNode(token)

            if token.type == SYMBOLS_TABLE.index("null"):
                factor = NullNode(token)
            self.advance()
            identifier = self.current_token
            params.append(ParamerterNode(factor, identifier))
        close_parentheses = self.current_token
        return ParamerterListNode(open_parentheses, params, close_parentheses)

    def return_statement(self):
        return_token = self.current_token
        self.advance()
        return ReturnStatementNode(return_token)

    def print_statement(self):
        print_token = self.current_token
        self.advance()
        expression = self.expression()
        return PrintStatementNode(print_token, expression)

    def read_statement(self):
        read_token = self.current_token
        self.advance()
        lvalue = self.lvalue()
        return ReadStatementNode(read_token, lvalue)

    def function_call(self):
        identifier = self.current_token
        self.advance()
        parameter_list = self.param_list_call()
        return FunctionCallNode(identifier, parameter_list)

    def atribute_statement(self):
        left = self.lvalue()
        self.advance()
        assign_token = self.current_token
        self.advance()
        token = self.current_token

        if token.type == SYMBOLS_TABLE.index("new"):
            right = self.alloc_expression()
        elif token.type == SYMBOLS_TABLE.index("identifier"):
            right = self.function_call()
        else:
            right = self.expression()
        return AtributeStatementNode(left, assign_token, right)

    def variable_declaration(self):
        constants = []
        factor = self.current_token
        self.advance()
        identifier = self.current_token
        self.advance()

        while self.current_token.type == SYMBOLS_TABLE.index("int_constant"):
            constants.append(self.current_token)
            self.advance()
        return VariableDeclarationNode(factor, identifier, constants)

    def statement(self):
        if self.current_token.type in [
            SYMBOLS_TABLE.index("int"),
            SYMBOLS_TABLE.index("float"),
            SYMBOLS_TABLE.index("string"),
        ]:
            statement = self.variable_declaration()
            self.advance()
            semicolon = self.current_token
            return StatementNode(statement, semicolon)
        elif self.current_token.type == SYMBOLS_TABLE.index("identifier"):
            statement = self.lvalue()
            self.advance()
            semicolon = self.current_token
            return StatementNode(statement, semicolon)
        elif self.current_token.type == SYMBOLS_TABLE.index("print"):
            statement = self.print_statement()
            self.advance()
            semicolon = self.current_token
            return StatementNode(statement, semicolon)
        elif self.current_token.type == SYMBOLS_TABLE.index("read"):
            statement = self.read_statement()
            self.advance()
            semicolon = self.current_token
            return StatementNode(statement, semicolon)
        elif self.current_token.type == SYMBOLS_TABLE.index("return"):
            statement = self.return_statement
            self.advance()
            semicolon = self.current_token
            return StatementNode(statement, semicolon)
        elif self.current_token.type == SYMBOLS_TABLE.index("if"):
            statement = self.if_statement()
            return StatementNode(statement)
        elif self.current_token.type == SYMBOLS_TABLE.index("for"):
            statement = self.for_statement()
            return StatementNode(statement)
        elif self.current_token.type == SYMBOLS_TABLE.index("break"):
            statement = self.current_token
            self.advance()
            semicolon = self.current_token
            return StatementNode(statement, semicolon)
        elif self.current_token.type == SYMBOLS_TABLE.index("semicolon"):
            statement = self.current_token
            return StatementNode(statement)
        else:
            statement = self.statement_list()
            return StatementNode(statement)

    def statement_list(self):
        left = self.statement()
        self.advance()

        while self.current_token.type != SYMBOLS_TABLE.index("semicolon"):
            right = self.current_token
            self.advance()
            left = StatementListNode(left, right)
        return left

    def if_statement(self):
        if_token = self.current_token
        self.advance()
        open_parentheses = self.current_token
        self.advance()
        expression = self.expression()
        self.advance()
        close_parentheses = self.current_token
        self.advance()
        primary_statement = self.statement()
        self.advance()
        if self.current_token.type == SYMBOLS_TABLE.index("else"):
            else_statement = self.current_token
            self.advance()
            secondary_statement = self.statement()
        return IfStatementNode(
            if_token,
            open_parentheses,
            expression,
            close_parentheses,
            primary_statement,
            else_statement,
            secondary_statement,
        )

    def for_statement(self):
        for_token = self.current_token
        self.advance()
        open_parentheses = self.current_token
        self.advance()
        atribute_statement = self.atribute_statement()
        self.advance()
        first_semicolon = self.current_token
        self.advance()
        expression = self.expression()
        self.advance()
        second_semicolon = self.current_token
        self.advance()
        atribute_statement = self.atribute_statement()
        self.advance()
        close_parentheses = self.current_token
        self.advance()
        statement = self.statement()
        return ForStatementNode(
            for_token,
            open_parentheses,
            atribute_statement,
            first_semicolon,
            expression,
            second_semicolon,
            close_parentheses,
            statement,
        )

    def function_definition(self):
        def_token = self.current_token
        self.advance()
        identifier = self.current_token
        self.advance()
        param_list = self.param_list()
        self.advance()
        open_brace = self.current_token
        self.advance()
        statement_list = self.statement_list()
        self.advance()
        close_brace = self.current_token
        return FunctionDefinitionNode(
            def_token, identifier, param_list, open_brace, statement_list, close_brace
        )

    def function_list(self):
        functions = [self.function_definition()]
        self.advance()

        while self.current_token.type == SYMBOLS_TABLE.index("def"):
            functions.append(self.function_definition())
        return FunctionListNode(functions)

    def program(self):
        if self.current_token.type == SYMBOLS_TABLE.index("def"):
            functions = self.function_list()
            self.advance()
        else:
            statement = self.statement()
            self.advance()
        return ProgramNode(functions, statement)

    def parse(self):
        return self.program()
