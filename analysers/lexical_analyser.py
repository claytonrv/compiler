import re
import sys
from os import path
from sre_constants import LITERAL
from nltk.tokenize import wordpunct_tokenize

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from constants import SYMBOLS_TABLE
from utils.log_utils import show_messages
from models.token import Token

OPERATORS = r"<|>|<=|>=|==|!=|=|\+|-|\∗|/|%"

SPECIAL_SYMBOLS = r":|\(|\)|#|,|\."

QUOTE = r"\""

RESERVED_WORDS = r"class|function|if|for|exit|return|int|float|string|null"

INT_DATA = r"[0-9]+"
FLOAT_DATA = r"[0-9]+\.[0-9]+"

LITERAL = r"[a-zA-Z]+"

IDENTIFIER = r"[a-zA-Z]+"

START_FUNCTION_DELIMITER = r"\)"


class Lexer:
    def __init__(self, file_data):
        self.file = file_data
        self.program_lines = self.file.readlines()

    def split_function_delimiters(self, token):
        tokens = re.split(START_FUNCTION_DELIMITER, token)
        if not "(" in tokens:
            tokens.insert(0, ")")
        else:
            tokens.append(")")
        return list(filter(None, tokens))

    def get_tokens(self):
        tokens = []
        errors = []
        last_token = None
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
                if re.search(OPERATORS, lexeme):
                    tokens.append(Token(lexeme, SYMBOLS_TABLE.index("operator")))
                    last_token = SYMBOLS_TABLE.index("operator")
                elif re.findall(RESERVED_WORDS, lexeme):
                    tokens.append(Token(lexeme, SYMBOLS_TABLE.index("reserved_word")))
                    last_token = SYMBOLS_TABLE.index("reserved_word")
                elif re.findall(SPECIAL_SYMBOLS, lexeme):
                    tokens.append(Token(lexeme, SYMBOLS_TABLE.index("special_symbol")))
                    last_token = SYMBOLS_TABLE.index("special_symbol")
                elif re.findall(INT_DATA, lexeme):
                    tokens.append(Token(lexeme, SYMBOLS_TABLE.index("int_number")))
                    last_token = SYMBOLS_TABLE.index("int_number")
                elif re.findall(FLOAT_DATA, lexeme):
                    tokens.append(Token(lexeme, SYMBOLS_TABLE.index("float_number")))
                    last_token = SYMBOLS_TABLE.index("float_number")
                elif re.findall(LITERAL, lexeme) and (
                    last_token == SYMBOLS_TABLE.index("literal")
                    or last_token == SYMBOLS_TABLE.index("quote")
                ):
                    tokens.append(Token(lexeme, SYMBOLS_TABLE.index("literal")))
                    last_token = SYMBOLS_TABLE.index("literal")
                elif re.findall(QUOTE, lexeme):
                    tokens.append(Token(lexeme, SYMBOLS_TABLE.index("quote")))
                    if last_token == SYMBOLS_TABLE.index("literal"):
                        last_token = None
                    else:
                        last_token = SYMBOLS_TABLE.index("quote")
                elif re.findall(IDENTIFIER, lexeme):
                    tokens.append(Token(lexeme, SYMBOLS_TABLE.index("identifier")))
                    last_token = SYMBOLS_TABLE.index("identifier")
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
