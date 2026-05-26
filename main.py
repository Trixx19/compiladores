from expressaoRegular import tokens
from geradorNFA import construir_nfa_global, coletar_todos_estados, resetar_contador


from geradorDFA import nfa_para_dfa, testar_palavra

def main():
    resetar_contador()
    
    
    tokens_teste = {
        "NUM"     : r"(num)",
        "NUM_LIT" : r"([0-9]+)",
        "VAR"     : r"([a-zA-Z_][a-zA-Z0-9_]*)",
        "EQ"      : r"(=)",
    }

    nfa_global = construir_nfa_global(tokens_teste)  
    todos_estados_nfa = coletar_todos_estados(nfa_global)

    estados_dfa, transicoes_dfa, estado_inicial_dfa, estados_finais_dfa = nfa_para_dfa(nfa_global, todos_estados_nfa)

    print(f"O DFA foi criado e tem {len(estados_dfa)} estados no total.\n")
    print("--- INICIANDO TESTES PRÁTICOS ---")

    
    palavras_para_testar = [
        "num",          # Deve ser NUM
        "12345",        # Deve ser NUM_LIT
        "variavel_1",   # Deve ser VAR
        "=",            # Deve ser EQ
        "numeral",      # Deve ser VAR (Começa com num, mas não para por aí)
        "123a"          # Deve dar Erro léxico
    ]

    for palavra in palavras_para_testar:
        resultado = testar_palavra(palavra, estado_inicial_dfa, transicoes_dfa, estados_finais_dfa)
        print(resultado)

if __name__ == "__main__":
    main()