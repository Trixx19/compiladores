class Estado:
    """Representa um estado dentro do Autômato Finito Não-Determinístico (NFA)"""
    def __init__(self, id_estado):
        self.id = id_estado
        self.transicoes = {}   
        self.is_final = False
        self.token = None      
        self.prioridade = 0    

    def adicionar_transicao(self, simbolo, estado_destino):
        if simbolo not in self.transicoes:
            self.transicoes[simbolo] = []
        self.transicoes[simbolo].append(estado_destino)


class NFA:
    """Representa um NFA completo com um estado inicial e um estado final"""
    def __init__(self, estado_inicial, estado_final):
        self.estado_inicial = estado_inicial
        self.estado_final = estado_final



class GeradorEstados:
    def __init__(self):
        self._contador = 1

    def novo_estado(self):
        estado = Estado(self._contador)
        self._contador += 1
        return estado

    def resetar(self):
        self._contador = 1

_gerador = GeradorEstados()

def novo_estado():
    return _gerador.novo_estado()

def resetar_contador():
    _gerador.resetar()


# --- OPERAÇÕES DE THOMPSON ---

def criar_nfa_caractere(caractere):
    """Cria um NFA básico que reconhece exatamente um caractere"""
    inicial = novo_estado()
    final = novo_estado()
    inicial.adicionar_transicao(caractere, final)
    return NFA(inicial, final)

def concatenar_nfa(nfa1, nfa2):
    """Concatena dois NFAs: nfa1 seguido de nfa2"""
    nfa1.estado_final.adicionar_transicao('epsilon', nfa2.estado_inicial)
    return NFA(nfa1.estado_inicial, nfa2.estado_final)

def unir_nfa(nfa1, nfa2):
    """União entre dois NFAs (nfa1 | nfa2)"""
    inicial = novo_estado()
    final = novo_estado()
    inicial.adicionar_transicao('epsilon', nfa1.estado_inicial)
    inicial.adicionar_transicao('epsilon', nfa2.estado_inicial)
    nfa1.estado_final.adicionar_transicao('epsilon', final)
    nfa2.estado_final.adicionar_transicao('epsilon', final)
    return NFA(inicial, final)

def fecho_kleene(nfa):
    """Fecho de Kleene: zero ou mais repetições (nfa*)"""
    inicial = novo_estado()
    final = novo_estado()
    inicial.adicionar_transicao('epsilon', nfa.estado_inicial)
    inicial.adicionar_transicao('epsilon', final)
    nfa.estado_final.adicionar_transicao('epsilon', nfa.estado_inicial)
    nfa.estado_final.adicionar_transicao('epsilon', final)
    return NFA(inicial, final)

def mais_kleene(nfa):
    """Um ou mais repetições (nfa+) — açúcar sintático sobre kleene"""
  
    inicial = novo_estado()
    final = novo_estado()
    inicial.adicionar_transicao('epsilon', nfa.estado_inicial)
    nfa.estado_final.adicionar_transicao('epsilon', nfa.estado_inicial)
    nfa.estado_final.adicionar_transicao('epsilon', final)
    return NFA(inicial, final)

def opcional_nfa(nfa):
    inicial = novo_estado()
    final = novo_estado()
    inicial.adicionar_transicao('epsilon', nfa.estado_inicial)
    inicial.adicionar_transicao('epsilon', final)   # caminho vazio
    nfa.estado_final.adicionar_transicao('epsilon', final)
    return NFA(inicial, final)



def unificar_nfas_em_unico_nfa(dicionario_nfas_tokens):
    
    estado_inicial_global = novo_estado()

    for prioridade, (nome_token, nfa_do_token) in enumerate(dicionario_nfas_tokens.items(), start=1):
        estado_inicial_global.adicionar_transicao('epsilon', nfa_do_token.estado_inicial)

        nfa_do_token.estado_final.is_final = True
        nfa_do_token.estado_final.token = nome_token
        nfa_do_token.estado_final.prioridade = prioridade  

    return NFA(estado_inicial_global, None)



def coletar_todos_estados(nfa):
    visitados = set()
    fila = [nfa.estado_inicial]
    estados = []
    while fila:
        s = fila.pop()
        if s.id in visitados:
            continue
        visitados.add(s.id)
        estados.append(s)
        for destinos in s.transicoes.values():
            for d in destinos:
                fila.append(d)
    return estados




