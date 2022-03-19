import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from analysers.syntax_analyser import Parser
from analysers.lexical_analyser import Lexer
from utils.log_utils import show_messages


def run(program_file):
    print("\n\n[INFO] Iniciando Analise lexica do arquivo.")
    lexer = Lexer(program_file)
    tokens, errors = lexer.get_tokens()

    if errors:
        print("\n\n[INFO] Analise lexica concluida com erros.")
        [print(error) for error in errors]
        return None
    else:
        print(f"\nLista de tokens:")
        token_list = ""
        for token in tokens:
            token_list = token_list + f" <{token.lexeme}, {token.type}>"
        print(token_list)
        print("\n\n[INFO] Analise lexica concluida com sucesso.")

    print("\n\n[INFO] Iniciando Analise sintatica dos tokens.")
    parser = Parser(tokens)
    ast, errors = parser.parse()
    if errors:
        print("\n\n[INFO] Analise sintatica concluida com erros.")
        [print(error) for error in errors]
    else:
        print(repr(ast))
        print("\n\n[INFO] Analise sintatica concluida com sucesso.")


if __name__ == "__main__":
    show_messages("start")
    import sys

    # file_path = "test_files/correct_program.llc"
    file_path = sys.argv[1]
    if not file_path:
        print(
            "[ERRO] Informe o caminho para o arquivo .llc para iniciar a analise lexica"
        )
    if ".llc" not in file_path:
        print("[ERRO] Arquivo invalido! Por favor, envie um arquivo com extensao .llc")
        exit
    if ".llc" not in file_path:
        print("Arquivo invalido! Por favor, envie um arquivo com extensao .abc")
        exit
    with open(file_path) as file:
        run(file)
