from expressaoRegular import tokens
from geradorNFA import construir_nfa_global, coletar_todos_estados, resetar_contador

def main():
    resetar_contador()
    
    # Teste só com alguns tokens
    tokens_teste = {
        "NUM"     : r"(num)",
        "NUM_LIT" : r"([0-9]+)",
        "VAR"     : r"([a-zA-Z_][a-zA-Z0-9_]*)",
        "EQ"      : r"(=)",
    }

    nfa_global = construir_nfa_global(tokens_teste)  # passa o dict pro autômato

    todos = coletar_todos_estados(nfa_global)
    finais = [e for e in todos if e.is_final]

    print(f"Estados totais : {len(todos)}")
    print(f"Estado inicial : {nfa_global.estado_inicial.id}")
    for ef in finais:
        print(f"  Estado {ef.id} => token='{ef.token}'")

if __name__ == "__main__":
    main()