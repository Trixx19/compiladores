import os
from expressaoRegular import tokens
from geradorNFA import construir_nfa_global, coletar_todos_estados, resetar_contador
from geradorDFA import nfa_para_dfa


def construir_dfa():
    resetar_contador()
    nfa_global = construir_nfa_global(tokens)
    todos_estados_nfa = coletar_todos_estados(nfa_global)
    estados_dfa, transicoes_dfa, estado_inicial_dfa, estados_finais_dfa = nfa_para_dfa(nfa_global, todos_estados_nfa)

    # Transforma os estados finais do DFA num dicionário para busca
    finais_dict = dict(estados_finais_dfa)
    return estado_inicial_dfa, transicoes_dfa, finais_dict


def analisador_lexico(codigo, estado_inicial, transicoes, finais_dict):
    # Percorrendo o código fornecido na main
    resultado = []
    linhas = codigo.strip().split('\n')

    for linha in linhas:
        if not linha.strip():
            continue

        pos = 0
        tamanho = len(linha)
        tokens_linha = []
        erro_na_linha = False

        while pos < tamanho:
            # Pula espaços em branco
            while pos < tamanho and linha[pos].isspace():
                pos += 1

            if pos == tamanho:
                break

            # Inicia busca
            estado_atual = estado_inicial
            ultimo_estado_final = None
            pos_ultimo_final = -1
            token_encontrado = None

            pos_atual = pos
            while pos_atual < tamanho:
                char = linha[pos_atual]
                # Verifica se existe transição com o caractere atual
                if char in transicoes.get(estado_atual, {}):
                    estado_atual = transicoes[estado_atual][char]

                    # Se o novo estado for um estado de aceitação, salva como o melhor até agora
                    if estado_atual in finais_dict:
                        ultimo_estado_final = estado_atual
                        pos_ultimo_final = pos_atual
                        token_encontrado = finais_dict[estado_atual]

                    pos_atual += 1
                else:
                    # Sem mais transições possíveis
                    break

            # Checa se o token é reconhecido
            if ultimo_estado_final is not None:
                lexema = linha[pos:pos_ultimo_final + 1]

                # validação de tamanho para VAR
                if token_encontrado == "VAR" and len(lexema) > 30:
                    erro_na_linha = True
                    break

                tokens_linha.append(token_encontrado)
                pos = pos_ultimo_final + 1

            else:
                # Não levou a nenhum estado final
                erro_na_linha = True
                break

        # Se houve falha na checagem, a linha inteira resulta em erro
        if erro_na_linha:
            resultado.append("ERRO")
        else:
            resultado.append(" ".join(tokens_linha))

    return resultado