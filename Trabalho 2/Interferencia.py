# Q2 - Grafo de Interferência (utilizando a Análise de Longevidade)
import os
import re

from longevidade import ler_entrada, calcular_use_def, analisar_longevidade, extrair_variaveis


class GrafoInterferencia:
    def __init__(self):
        self.vertices = set()
        self.arestas = set()  

    def add_vertice(self, var):
        self.vertices.add(var)

    def add_aresta(self, a, b):
        if a == b:
            return
        self.add_vertice(a)
        self.add_vertice(b)
        self.arestas.add(frozenset((a, b)))

    def vizinhos(self, var):
        viz = set()
        for aresta in self.arestas:
            if var in aresta:
                resto = aresta - {var}
                if resto:
                    viz.add(next(iter(resto)))
        return viz


def eh_instrucao_move(instrucao):
    
    if '=' not in instrucao:
        return False, None, None
    lado_esq, lado_dir = instrucao.split('=', 1)
    destino = lado_esq.strip()
    origem = lado_dir.strip()

    
    if re.fullmatch(r"[a-zA-Z_]\w*", origem):
        return True, destino, origem

    return False, destino, None


def calcular_out_por_instrucao(bloco):
    
    n = len(bloco.instrucoes)
    out_por_instr = [None] * n

    out_seguinte = bloco.out_set  
    for idx in range(n - 1, -1, -1):
        out_por_instr[idx] = out_seguinte

        instrucao = bloco.instrucoes[idx]
        definida, usadas = extrair_variaveis(instrucao)
        def_instr = {definida} if definida else set()

        in_instr = usadas | (out_seguinte - def_instr)
        out_seguinte = in_instr  

    return list(zip(bloco.instrucoes, out_por_instr))


def montar_grafo_interferencia(blocos):
    grafo = GrafoInterferencia()

    for bloco in blocos.values():
        
        grafo.vertices |= bloco.use | bloco.def_

        for instrucao, out_instr in calcular_out_por_instrucao(bloco):
            eh_move, destino, origem = eh_instrucao_move(instrucao)

            if not destino:
                continue

            if eh_move:
                
                for var in out_instr:
                    if var != destino and var != origem:
                        grafo.add_aresta(destino, var)
            else:
                
                for var in out_instr:
                    if var != destino:
                        grafo.add_aresta(destino, var)

    return grafo


def processar(dados):
    blocos = ler_entrada(dados)

    for bloco in blocos.values():
        calcular_use_def(bloco)

    analisar_longevidade(blocos)

    grafo = montar_grafo_interferencia(blocos)
    return grafo


def formatar_saida(grafo):
    linhas_saida = ["Resultado do Grafo de Interferência:"]

    linhas_saida.append(f"Vértices = {sorted(grafo.vertices)}")
    linhas_saida.append("-" * 30)

    for var in sorted(grafo.vertices):
        vizinhos = sorted(grafo.vizinhos(var))
        linhas_saida.append(f"{var}: {vizinhos}")

    linhas_saida.append("-" * 30)
    linhas_saida.append("Arestas:")
    for aresta in sorted(tuple(sorted(a)) for a in grafo.arestas):
        linhas_saida.append(f"({aresta[0]}, {aresta[1]})")

    return "\n".join(linhas_saida)


def main():
    PASTA_ENTRADA = "in"
    PASTA_SAIDA = "out"

    if not os.path.isdir(PASTA_ENTRADA):
        print(f"Erro: pasta '{PASTA_ENTRADA}' nao encontrada.")
        return

    os.makedirs(PASTA_SAIDA, exist_ok=True)

    for nome_arquivo in os.listdir(PASTA_ENTRADA):
        caminho_entrada = os.path.join(PASTA_ENTRADA, nome_arquivo)
        nome_saida = os.path.splitext(nome_arquivo)[0] + "_gi.txt"
        caminho_saida = os.path.join(PASTA_SAIDA, nome_saida)

        with open(caminho_entrada, 'r', encoding='utf-8') as f:
            dados = f.read()

        grafo = processar(dados)
        resultado = formatar_saida(grafo)

        with open(caminho_saida, 'w', encoding='utf-8') as f:
            f.write(resultado)


if __name__ == "__main__":
    main()