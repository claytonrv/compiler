import re
from nltk.tokenize import wordpunct_tokenize

OPERATORS = r"<|>|<=|>=|==|!=|=|\+|-|\∗|/|%"

SPECIAL_SYMBOLS = r":|\(|\)|#|,|\."

RESERVED_WORDS = r"class|function|if|for|exit|return|int|float|str|null"

INT_DATA = r"\d(\d)*"
FLOAT_DATA = r"\d(\d)*\.\d(\d)*"
STRING_DATA = r"\"\w*\""

IDENTIFIER = r"[a-zA-Z]"

START_FUNCTION_DELIMITER = r"\)"


SYMBOLS_TABLE = [
    "operator",
    "reserved_word",
    "special_symbol",
    "int_number",
    "float number",
    "string",
    "identifier",
]


def split_function_delimiters(token):
    tokens = re.split(START_FUNCTION_DELIMITER, token)
    if not '(' in tokens:
        tokens.insert(0,')')
    else:
        tokens.append(')')
    return list(filter(None, tokens))

def compile(file):
    program = file.readlines()
    tokens = []
    for index, line in enumerate(program):
        print("Analisando a linha %d -> %s" % (index, line.rstrip('\r\n')))
        lexemes = wordpunct_tokenize(line)
        for lexeme in lexemes:
            if re.findall(START_FUNCTION_DELIMITER, lexeme):
                lexemes.pop()
                [lexemes.append(tk) for tk in split_function_delimiters(lexeme)]
        for lexeme in lexemes:
            if re.search(OPERATORS, lexeme):
                tokens.append((lexeme, SYMBOLS_TABLE.index('operator')))
            elif re.findall(RESERVED_WORDS, lexeme):
                tokens.append((lexeme, SYMBOLS_TABLE.index('reserved_word')))
            elif re.findall(SPECIAL_SYMBOLS, lexeme):
                tokens.append((lexeme, SYMBOLS_TABLE.index('special_symbol')))
            elif re.findall(INT_DATA, lexeme):
                tokens.append((lexeme, SYMBOLS_TABLE.index('int_number')))
            elif re.findall(FLOAT_DATA, lexeme):
                tokens.append((lexeme, SYMBOLS_TABLE.index('float_number')))
            elif re.findall(STRING_DATA, lexeme):
                tokens.append((lexeme, SYMBOLS_TABLE.index('string')))
            elif re.findall(IDENTIFIER, lexeme):
                tokens.append((lexeme, SYMBOLS_TABLE.index('identifier')))
            else:
                print(f"[ERRO] Encontrado um erro de lexico na linha {index}. Lexema invalido encontrado {lexeme}")
                return
    print(f'\nLista de tokens:')
    token_list = ""
    for token in tokens:
        token_list = token_list + f" <{token[0]}, {token[1]}>"
    print(token_list)
    print('\n\n[SUCESSO] Analise lexica concluida com sucesso.')

def show_messages(type):
    if type == 'start':
        print('---------------------------------------------------------')
        print('\n')
        print('     UNIVERSIDADE FEDERAL DE SANTA CATARINA')
        print('     INE5622 - INTRODUCAO A COMPILADORES')
        print('     Analisador Lexico e Sintatico')
        print('\n     Grupo 3:')
        print('       Clayton Veras (14101362)')
        print('       Evandro Machado (16104900)')
        print('       Gabriel Fiorelli (14101376)')
        print('       Jonas Barbosa (17100911)')
        print('\n')
        print('---------------------------------------------------------')
        print('\n')
    elif type == 'finish':
        pass

if __name__ == "__main__":
    show_messages('start')
    # file_path = input("Digite o caminho do arquivo a ser compilado ")
    file_path = "./correct_program.abc"
    if ".abc" not in file_path:
        print("Arquivo invalido! Por favor, envie um arquivo com extensao .abc")
        exit    
    with open(file_path) as file:
        compile(file)   