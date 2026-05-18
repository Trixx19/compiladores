tokens = {
    # Palavras reservadas
    "NUM"       : r"(num)",
    "TEXT"      : r"(text)",
    "BOOL"      : r"(bool)",
    "SHOW"      : r"(show)",
    "TRUE"      : r"(true)",
    "FALSE"     : r"(false)",

    # Literais
    "NUM_LIT"   : r"([0-9]+)", # Representa números.
    "CONST"     : r'("[^"]*")',

    # Identificador de variável: começa com letra ou _, seguido de letras/dígitos/_
    "VAR"       : r"([a-zA-Z_][a-zA-Z0-9_]*)",

    # Operadores
    "EQ_EQ"     : r"(==)",
    "EQ"        : r"(=)",
    "ADD"       : r"(\+)",
    "SUB"       : r"(-)",
    "MUL"       : r"(\*)",
    "DIV"       : r"(/)",
    "GT"        : r"(>)",
    "LT"        : r"(<)",

    # Delimitadores
    "SEMICOLON" : r"(;)",
    "LPAREN"    : r"(\()",
    "RPAREN"    : r"(\))",
}