class ProgramNode:
    def __init__(self, functions, statement) -> None:
        self.functions = functions
        self.statement = statement

    def __repr__(self) -> str:
        return f"{self.functions}, {self.statement}"


class FunctionListNode:
    def __init__(self, functions) -> None:
        self.functions = functions

    def __repr__(self) -> str:
        return f"{[function for function in self.functions]}"


class FunctionDefinitionNode:
    def __init__(
        self, def_token, identifier, param_list, open_brace, statement_list, close_brace
    ) -> None:
        self.def_token = def_token
        self.identifier = identifier
        self.param_list = param_list
        self.open_brace = open_brace
        self.statement_list = statement_list
        self.close_brace = close_brace

    def __repr__(self) -> str:
        return f"{self.def_token}, {self.identifier}, {self.param_list}, {self.open_brace}, {self.statement_list}, {self.close_brace}"


class ParamerterNode:
    def __init__(self, factor, identifier):
        self.factor = factor
        self.identifier = identifier

    def __repr__(self) -> str:
        return f"{self.factor}, {self.identifier}"


class ParamerterListNode:
    def __init__(self, funct_start, parameters, funct_end):
        self.open_parentheses = funct_start
        self.parameters = parameters
        self.close_parentheses = funct_end

    def __repr__(self) -> str:
        return f"{self.open_parentheses}, {[parameter + ', ' for parameter in self.parameters]} {self.close_parentheses}"


class StatementNode:
    def __init__(self, statement, semicolon=None) -> None:
        self.statement = statement
        self.semicolon = semicolon

    def __repr__(self) -> str:
        return f"{self.statement}, {self.semicolon}"


class VariableDeclarationNode:
    def __init__(self, factor, identifier, constants) -> None:
        self.factor = factor
        self.identifier = identifier
        self.constants = constants

    def __repr__(self) -> str:
        return f"{self.factor}, {self.identifier}, {self.constants}"


class AtributeStatementNode:
    def __init__(self, right, assign_token, left) -> None:
        self.right = right
        self.assign_token = assign_token
        self.left = left

    def __repr__(self) -> str:
        return f"{self.right}, {self.assign_token}, {self.left}"


class FunctionCallNode:
    def __init__(self, identifier, parameter_list) -> None:
        self.identifier = identifier
        self.parameter_list = parameter_list

    def __repr__(self) -> str:
        return f"{self.identifier}, {self.parameter_list}"


class ParamerterListCallNode:
    def __init__(self, funct_start, identifiers, funct_end):
        self.open_parentheses = funct_start
        self.identifiers = identifiers
        self.close_parentheses = funct_end

    def __repr__(self) -> str:
        return f"{self.open_parentheses}, {[identifier + ', ' for identifier in self.identifiers] if self.identifiers else ''} {self.close_parentheses}"


class PrintStatementNode:
    def __init__(self, print_token, expression):
        self.print_token = print_token
        self.expression = expression

    def __repr__(self) -> str:
        return f"{self.print_token}, {self.expression}"


class ReadStatementNode:
    def __init__(self, read_token, lvalue):
        self.read_token = read_token
        self.lvalue = lvalue

    def __repr__(self) -> str:
        return f"{self.read_token}, {self.lvalue}"


class ReturnStatementNode:
    def __init__(self, return_token):
        self.return_token = return_token

    def __repr__(self) -> str:
        return f"{self.return_token}"


class IfStatementNode:
    def __init__(
        self,
        if_token,
        open_parentheses,
        expression,
        close_parentheses,
        primary_statement,
        else_statement=None,
        secondary_statement=None,
    ) -> None:
        self.if_token = if_token
        self.open_parentheses = open_parentheses
        self.expression = expression
        self.close_parentheses = close_parentheses
        self.primary_statement = primary_statement
        self.else_statement = else_statement
        self.secondary_statement = secondary_statement

    def __repr__(self) -> str:
        return f"{self.if_token}, {self.open_parentheses}, {self.expression}, {self.close_parentheses}, {self.primary_statement} {', ' + self.else_statement if self.else_statement else ''} {', ' + self.secondary_statement if self.secondary_statement else ''}"


class ForStatementNode:
    def __init__(
        self,
        for_token,
        open_parentheses,
        atribute_statement,
        first_semicolon,
        expression,
        second_semicolon,
        close_parentheses,
        statement,
    ) -> None:
        self.for_token = for_token
        self.open_parentheses = open_parentheses
        self.atribute_statement = atribute_statement
        self.first_semicolon = first_semicolon
        self.expression = expression
        self.second_semicolon = second_semicolon
        self.close_parentheses = close_parentheses
        self.statement = statement

    def __repr__(self) -> str:
        return f"{self.for_token}, {self.open_parentheses}, {self.atribute_statement}, {self.first_semicolon}, {self.expression}, {self.second_semicolon}, {self.close_parentheses}, {self.statement}"


class StatementListNode:
    def __init__(self, left, right) -> None:
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f"{self.left}, {self.right}"


class AllocExpressionNode:
    def __init__(self, allocation_token, operation, expression):
        self.allocation_token = allocation_token
        self.operation_token = operation
        self.expression_node = expression

    def __repr__(self) -> str:
        return f"{self.left_node} {self.operation_token + ', ' if self.operation_token else ''} {self.right_node if self.right_node else ''}"


class ExpressionNode:
    def __init__(self, left_node, operation_token=None, right_node=None):
        self.left_node = left_node
        self.operation_token = operation_token
        self.right_node = right_node

    def __repr__(self) -> str:
        return f"{self.left_node} {self.operation_token + ', ' if self.operation_token else ''} {self.right_node if self.right_node else ''}"


class TermNode:
    def __init__(self, left_node, operation_token=None, right_node=None):
        self.left_node = left_node
        self.operation_token = operation_token
        self.right_node = right_node

    def __repr__(self) -> str:
        return f"{self.left_node} {self.operation_token + ', ' if self.operation_token else ''} {self.right_node if self.right_node else ''}"


class UnaryOperationNode:
    def __init__(self, operation_token, right_node):
        self.operation_token = operation_token
        self.right_node = right_node

    def __repr__(self) -> str:
        return f"{self.operation_token}, {self.right_node}"


class LValueNode:
    def __init__(
        self,
        identifier,
        open_parentheses,
        open_bracket,
        num_expression,
        close_parentheses,
        close_bracket,
    ):
        self.identifier = identifier
        self.open_parentheses = open_parentheses
        self.open_bracket = open_bracket
        self.num_expression = num_expression
        self.close_parentheses = close_parentheses
        self.close_bracket = close_bracket

    def __repr__(self) -> str:
        return f"{self.identifier}, {self.open_parentheses}, {self.open_bracket}, {self.num_expression}, {self.close_parentheses}, {self.close_bracket}"


class NumberNode:
    def __init__(self, number):
        self.number = number

    def __repr__(self):
        return f"{self.number}"


class StringNode:
    def __init__(self, string) -> None:
        self.string = string

    def __repr__(self) -> str:
        return f"{self.string}"


class NullNode:
    def __init__(self, null) -> None:
        self.null = null

    def __repr__(self) -> str:
        return f"{self.null}"


class BinaryOperationNode:
    def __init__(self, left_node, operation_token, right_node):
        self.left_node = left_node
        self.operation_token = operation_token
        self.right_node = right_node

    def __repr__(self) -> str:
        return f"{self.left_node}, {self.operation_token}, {self.right_node}"
