import re
from nltk.tokenize import wordpunct_tokenize

# OPERATORS = r"(\++)|(-)|(=)|(\*)|(/)|(%)|(--)|(<=)|(>=)"

OPERATORS = r"<|>|<=|>=|==|!=|=|\+|-|\∗|/|%"

SPECIAL_SYMBOLS = r":|\(|\)|#|,|\."

RESERVED_WORDS = r"class|function|if|for|exit|return|int|float|str|null"

INT_DATA = r"\d(\d)*"
FLOAT_DATA = r"\d(\d)*\.\d(\d)*"
STRING_DATA = r"\"\w*\""

IDENTIFIER = r"[a-zA-Z]"


START_FUNCTION_DELIMITER = r"\)"

def split_function_delimiters(token):
    tokens = re.split(START_FUNCTION_DELIMITER, token)
    if not '(' in tokens:
        tokens.insert(0,')')
    else:
        tokens.append(')')
    return list(filter(None, tokens))

def compile(file):
    program = file.readlines()
    for index, line in enumerate(program):
        print(f"\nAnalisando a linha {index} -> {line}")
        tokens = wordpunct_tokenize(line)
        for token in tokens:
            if re.findall(START_FUNCTION_DELIMITER, token):
                tokens.pop()
                [tokens.append(tk) for tk in split_function_delimiters(token)]
        for token in tokens:
            if re.findall(SPECIAL_SYMBOLS, token):
                print(f"Simbolo especial econtrado: {token}")
            elif re.search(OPERATORS, token):
                print(f"Operador econtrado: {token}")
            elif re.findall(RESERVED_WORDS, token):
                print(f"Palavra reservada encontrada: {token}")
            elif re.findall(INT_DATA, token):
                print(f"Valor inteiro encontrado: {token}")
            elif re.findall(FLOAT_DATA, token):
                print(f"Valor real encontrado: {token}")
            elif re.findall(STRING_DATA, token):
                print(f"Cadeia de caracteres encontrada: {token}")
            elif re.findall(IDENTIFIER, token):
                print(f"Identificador encontrado: {token}")
            else:
                print(f"[ERRO] Encontrado um erro de lexico na linha {index}. Token invalido encontrado {token}")
                return
    print('\n\n[SUCESSO] Analise lexica concluida com sucesso.')

if __name__ == "__main__":
    # file_path = input("Digite o caminho do arquivo a ser compilado ")
    file_path = "./correct_program.abc"
    if ".abc" not in file_path:
        print("Arquivo invalido! Por favor, envie um arquivo com extensao .abc")
        exit    
    with open(file_path) as file:
        compile(file)   