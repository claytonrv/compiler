import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from analysers.syntax_analyser import Parser
from analysers.lexical_analyser import Lexer


def run(program_file):
    lexer = Lexer(program_file)
    tokens, errors = lexer.get_tokens()

    if errors:
        return None, errors

    parser = Parser(tokens)
    ast = parser.parse()
    print(ast)


if __name__ == "__main__":
    file_path = "./correct_program.abc"
    if ".abc" not in file_path:
        print("Arquivo invalido! Por favor, envie um arquivo com extensao .abc")
        exit
    with open(file_path) as file:
        run(file)
