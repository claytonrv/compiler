import re
import sys
from os import path
from sre_constants import LITERAL
from nltk.tokenize import wordpunct_tokenize

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from constants import SYMBOLS_TABLE
from utils.log_utils import show_messages
from models.token import Token

GREATER_THAN_OPERATOR = r">"
LESS_THAN_OPERATOR = r"<"
GREATER_THAN_OR_EQUAL_TO_OPERATOR = r">="
LESS_THAN_OR_EQUAL_TO_OPERATOR = r"<="
EQUAL_OPERATOR = r"=="
DIFFERENT_OPERATOR = r"!="

ADITION_OPERATOR = r"\+"
SUBTRACTION_OPERATOR = r"-"

MULTIPLICATION_OPERATOR = r"\*"
DIVISION_OPERATOR = r"/"
MODULUS_OPERATOR = r"%"

OPERATORS = [
    (GREATER_THAN_OPERATOR, "greater_than"),
    (LESS_THAN_OPERATOR, "less_than"),
    (GREATER_THAN_OR_EQUAL_TO_OPERATOR, "greater_or_equal_to"),
    (LESS_THAN_OR_EQUAL_TO_OPERATOR, "less_or_equal_to"),
    (EQUAL_OPERATOR, "equals"),
    (DIFFERENT_OPERATOR, "different"),
    (ADITION_OPERATOR, "addition"),
    (SUBTRACTION_OPERATOR, "subtraction"),
    (MULTIPLICATION_OPERATOR, "multiplication"),
    (DIVISION_OPERATOR, "division"),
    (MODULUS_OPERATOR, "modulus"),
]

ATTRIBUTION_SYMBOL = r"="
OPEN_PARENTHESES_SYMBOL = r"\("
CLOSE_PARENTHESES_SYMBOL = r"\)"
OPEN_BRACE_SYMBOL = r"{"
CLOSE_BRACE_SYMBOL = r"}"

SEMICOLON_SYMBOL = r";"
COMMA_SYMBOL = r","
QUOTE_SYMBOL = r"\""


SYMBOLS = [
    (ATTRIBUTION_SYMBOL, "attribution"),
    (OPEN_PARENTHESES_SYMBOL, "open_parentheses"),
    (CLOSE_PARENTHESES_SYMBOL, "close_parentheses"),
    (OPEN_BRACE_SYMBOL, "open_brace"),
    (CLOSE_BRACE_SYMBOL, "close_brace"),
    (SEMICOLON_SYMBOL, "semicolon"),
    (COMMA_SYMBOL, "comma"),
    (QUOTE_SYMBOL, "quote"),
]

DEF_RESERVED_WORD = r"def"
IF_RESERVED_WORD = r"if"
ELSE_RESERVED_WORD = r"else"
FOR_RESERVED_WORD = r"for"
BREAK_RESERVED_WORD = r"break"
RETURN_RESERVED_WORD = r"return"
NULL_RESERVED_WORD = r"null"
PRINT_RESERVED_WORD = r"print"
READ_RESERVED_WORD = r"read"
NEW_RESERVED_WORD = r"new"

RESERVED_WORDS = [
    (DEF_RESERVED_WORD, "def"),
    (IF_RESERVED_WORD, "if"),
    (FOR_RESERVED_WORD, "for"),
    (RETURN_RESERVED_WORD, "return"),
    (NULL_RESERVED_WORD, "null"),
    (PRINT_RESERVED_WORD, "print"),
    (READ_RESERVED_WORD, "read"),
    (NEW_RESERVED_WORD, "new"),
]

PRIMITIVE_TYPE_INT = r"int"
PRIMITIVE_TYPE_FLOAT = r"float"
PRIMITIVE_TYPE_STRING = r"string"

PRIMITIVES = [
    (PRIMITIVE_TYPE_INT, "int"),
    (PRIMITIVE_TYPE_FLOAT, "float"),
    (PRIMITIVE_TYPE_STRING, "string"),
]

INT_CONSTANT = r"[0-9]+"
FLOAT_CONSTANT = r"[0-9]+\.[0-9]+"

NUMBERS = [
    (INT_CONSTANT, "int_constant"),
    (FLOAT_CONSTANT, "float_constant"),
]

LITERAL = r"[0-9]?[a-zA-Z]+[0-9]?"

IDENTIFIER = r"[0-9]?[a-zA-Z]+[0-9]?"

START_FUNCTION_DELIMITER = r"\)"


class Lexer:
    def __init__(self, file_data):
        self.file = file_data
        self.program_lines = self.file.readlines()
        self.current_lexeme_type = None
        self.last_token = None

    def split_function_delimiters(self, token):
        tokens = re.split(START_FUNCTION_DELIMITER, token)
        if not "(" in tokens:
            tokens.insert(0, ")")
        else:
            tokens.append(")")
        return list(filter(None, tokens))

    def _is_operator(self, lexeme):
        operator_type = None
        for operator, op_type in OPERATORS:
            if re.search(operator, lexeme):
                self.current_lexeme_type = op_type
                operator_type = op_type
        return operator_type is not None

    def _is_reserved_word(self, lexeme):
        reserved_word_type = None
        for reserved_word, rw_type in RESERVED_WORDS:
            if re.search(reserved_word, lexeme):
                self.current_lexeme_type = rw_type
                reserved_word_type = rw_type
        return reserved_word_type is not None

    def _is_symbol(self, lexeme):
        symbol_type = None
        for symbol, symb_type in SYMBOLS:
            if re.search(symbol, lexeme):
                self.current_lexeme_type = symb_type
                symbol_type = symb_type
        return symbol_type is not None

    def _is_primitive(self, lexeme):
        primitive_type = None
        for primitive, pmtv_type in PRIMITIVES:
            if re.search(primitive, lexeme):
                self.current_lexeme_type = pmtv_type
                primitive_type = pmtv_type
        return primitive_type is not None

    def _is_literal(self, lexeme):
        literal_type = None
        if re.search(LITERAL, lexeme):
            self.current_lexeme_type = "string_constant"
            literal_type = "string_constant"
        return literal_type is not None

    def _is_identifier(self, lexeme):
        identifier_type = None
        if re.findall(IDENTIFIER, lexeme):
            self.current_lexeme_type = "identifier"
            identifier_type = "identifier"
        return identifier_type is not None

    def _is_number(self, lexeme):
        number_type = None
        for number, nbr_type in NUMBERS:
            if re.search(number, lexeme):
                self.current_lexeme_type = nbr_type
                number_type = nbr_type
        return number_type is not None

    def get_tokens(self):
        tokens = []
        errors = []
        for index, line in enumerate(self.program_lines):
            print("Analisando a linha %d -> %s" % (index, line.rstrip("\r\n")))
            lexemes = wordpunct_tokenize(line)
            for lexeme in lexemes:
                if re.findall(START_FUNCTION_DELIMITER, lexeme):
                    lexemes.pop()
                    [
                        lexemes.append(tk)
                        for tk in self.split_function_delimiters(lexeme)
                    ]
            for lexeme in lexemes:
                if self._is_operator(lexeme):
                    lexeme_type = SYMBOLS_TABLE.index(self.current_lexeme_type)
                    tokens.append(Token(lexeme, lexeme_type))
                    self.last_token = lexeme_type
                elif self._is_reserved_word(lexeme):
                    lexeme_type = SYMBOLS_TABLE.index(self.current_lexeme_type)
                    tokens.append(Token(lexeme, lexeme_type))
                    self.last_token = lexeme_type
                elif self._is_symbol(lexeme):
                    symbol_type = SYMBOLS_TABLE.index(self.current_lexeme_type)
                    if symbol_type == 7:  # QUOTE INDEX ON SYMBOLS_TABLE
                        if self.last_token == 29:  # LITERAL INDEX ON SYMBOLS_TABLE
                            self.last_token = None
                        else:
                            self.last_token = 7  # QUOTE INDEX ON SYMBOLS_TABLE
                    tokens.append(Token(lexeme, symbol_type))
                    self.last_token = symbol_type
                elif self._is_primitive(lexeme):
                    primitive_type = SYMBOLS_TABLE.index(self.current_lexeme_type)
                    tokens.append(Token(lexeme, primitive_type))
                    self.last_token = primitive_type
                elif self._is_literal(lexeme):
                    literal_type = SYMBOLS_TABLE.index(self.current_lexeme_type)
                    tokens.append(Token(lexeme, literal_type))
                    self.last_token = literal_type
                elif self._is_identifier(lexeme):
                    if self.last_token != "literal" or self.last_token != "quote":
                        identifier_type = SYMBOLS_TABLE.index(self.current_lexeme_type)
                        tokens.append(Token(lexeme, identifier_type))
                        self.last_token = identifier_type
                elif self._is_number(lexeme):
                    number_type = SYMBOLS_TABLE.index(self.current_lexeme_type)
                    tokens.append(Token(lexeme, number_type))
                    self.last_token = number_type
                else:
                    errors.append(
                        f"[ERRO] Encontrado um erro de lexico na linha {index}. Lexema invalido encontrado {lexeme}"
                    )
        return tokens, errors


if __name__ == "__main__":
    show_messages("start")
    # file_path = input("Digite o caminho do arquivo a ser compilado ")
    file_path = "./correct_program.abc"
    if ".abc" not in file_path:
        print("Arquivo invalido! Por favor, envie um arquivo com extensao .abc")
        exit
    with open(file_path) as file:
        lexer = Lexer(file)
        tokens, errors = lexer.get_tokens()

        if errors:
            [print(error) for error in errors]
        else:
            print(f"\nLista de tokens:")
            token_list = ""
            for token in tokens:
                token_list = token_list + f" <{token[0]}, {token[1]}>"
            print(token_list)
            print("\n\n[SUCESSO] Analise lexica concluida com sucesso.")
