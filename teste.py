from geradorNFA import *

nfa_add = criar_nfa_caractere('+')
nfa_sub = criar_nfa_caractere('-')

meus_tokens = {
    "ADD": nfa_add,
    "SUB": nfa_sub,
}

nfa_final = unificar_nfas_em_unico_nfa(meus_tokens)

print("Inicial:", nfa_final.estado_inicial.id)

todos = coletar_todos_estados(nfa_final)
for e in todos:
    if e.is_final:
        print(f"Estado {e.id} -> token={e.token}, prioridade={e.prioridade}")