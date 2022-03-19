# compiler

Trabalho final da materia INE5622 - Introducao a Compiladore INE - UFSC

Linguagem usada: Python
Versao testada: 3.9.7

Alunos: - Clayton Veras, Evandro Machado, Gabriel Fiorelli, Jonas Barbosa

## Configurando o projeto

Para configurar o projeto e installar as dependencias necessarias para o funcionamento, execute o seguinte comando:

```bash
    make build
```

## Executando o analisador lexico

Para executar o analisador lexico sozinho, execute o seguinte comando:

```bash
    make lexer file=<path_para_o_arquivo>
    # exemplo: make lexer file=~/Documents/meu_programa.llc
```

Importante: Apenas arquivos com a extensao .llc sao aceitos.

## Executando os analisadores lexico e sintatico

Para executar os dois analisadores (lexico e sintatico), execute o seguinte comando:

```bash
    make compile file=<path_para_o_arquivo>
    # exemplo: make compile file=~/Documents/meu_programa.llc
```

Este comando ira executar o analisador lexico para a geracao dos tokens e na sequencia a inciara a analise sintatica.

Importante: Apenas arquivos com a extensao .llc sao aceitos.
