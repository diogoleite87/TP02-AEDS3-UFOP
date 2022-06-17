from turtle import right
import pandas as pd


class Grafo:

    def __init__(self, num_vert=0, num_arestas=0, lista_adj=None, mat_adj=None, arestas=None, ofertas=None):
        self.num_vert = num_vert
        self.num_arestas = num_arestas
        self.list_b = []
        self.num_super_oferta = 0
        self.num_super_demanda = 0

        self.professores = []
        self.num_disciplinas_professores = []

        self.disciplinas = []
        self.nome_disciplinas = []
        self.num_turmas_disciplinas = []

        self.dicionario_professores = {}
        self.dicionario_disciplinas = {}

        self.list_semAlocacao = []

        if ofertas is None:
            self.ofertas = [[] for i in range(num_vert)]
        else:
            self.ofertas = ofertas
        if arestas is None:
            self.arestas = [[] for _ in range(num_vert)]
        else:
            self.arestas = arestas
        if lista_adj is None:
            self.list_adj = [[] for i in range(num_vert)]
        else:
            self.list_adj = lista_adj
        if mat_adj is None:
            self.mat_adj = [[0 for j in range(num_vert)]
                            for i in range(num_vert)]
        else:
            self.mat_adj = mat_adj

    def ler_arquivo_csv(self, professores_CSV, disciplinas_CSV):

        # função para ler o arquivo CSV e salvar no objeto
        try:
            self.arqProf = pd.read_csv(
                'data/' + professores_CSV, sep=';', encoding='utf-8')
            self.arqDisc = pd.read_csv(
                'data/' + disciplinas_CSV, sep=';', encoding='utf-8')

        except:
            print('Erro ao abrir o arquivo!')

    def define_professores(self):

        # busca no arquivo CSV a coluna de professores
        # salva em um dicionario os nomes dos professores
        for i in range(len(self.arqProf['Professor'])):
            self.professores.append(self.arqProf['Professor'][i])

        # busca no arquivo CSV na coluna de disciplinas
        # salva em um dicionario o numero de disiciplinas correspondentes
        for i in range(len(self.arqProf['# Disciplinas'])):
            self.num_disciplinas_professores.append(
                self.arqProf['# Disciplinas'][i])

    def define_disciplinas(self):

        # busca no arquivo CSV o codigo das disciplinas
        # salva em um dicionario os codigos das disciplinas
        for i in range(len(self.arqDisc['Disciplina'])):
            self.disciplinas.append(self.arqDisc['Disciplina'][i])

        # busca no arquivo CSV o nome das disciplinas
        # salva em um dicionario os nomes das disciplinas
        for i in range(len(self.arqDisc['Nome'])):
            self.nome_disciplinas.append(self.arqDisc['Nome'][i])

        # busca no aquivo CSV na coluna turmas
        # salva em um dicionario o numero de turmas correspondentes
        for i in range(len(self.arqDisc['# Turmas'])):
            self.num_turmas_disciplinas.append(self.arqDisc['# Turmas'][i])

    def super_demanda(self):

        # define a capacidade do vertice super demanda
        self.num_super_demanda = - self.arqDisc['# Turmas'].sum()

    def super_oferta(self):

        # define a capacidade do vertice super oferta
        self.num_super_oferta = self.arqDisc['# Turmas'].sum()

    def add_aresta(self, u, v, capacidade=float('inf'), peso=0):

        # função para adicionar arestas em todas as matrizes e listas
        if u < self.num_vert and v < self.num_vert:
            self.mat_adj[u][v] = [peso, capacidade]
            self.mat_cap[u][v] = capacidade
            self.mat_custo[u][v] = peso
            self.list_adj[u].append((v, [peso, capacidade]))
            self.arestas.append((u, v, peso))
            self.num_arestas += 1
        else:
            print("Aresta invalida!")

    def add_matriz_superOferta(self):

        # funcao que liga vertice super oferta nos professores
        # adicionando inicialmente vertice de super oferta
        self.mat_adj[0][0] = 0

        # ligando vertice super oferta nos professores
        for i in range(len(self.professores)):
            self.add_aresta(0, i + 1, self.dicionario_professores[i][1], 0)

    def add_matriz_professores(self):

        # funcao que liga os professores nas disciplinas com o devido custo/preferencia
        preferencia = [0, 3, 5, 8, 10]

        # ligando os professores nas disciplinas correspondentes
        for i in range(len(self.dicionario_professores)):
            for j in range(len(self.dicionario_professores[i][2])):
                for k in range(len(self.disciplinas)):
                    if self.dicionario_professores[i][2][j] == self.disciplinas[k]:

                        # if para limitar eletiva em 1
                        if self.disciplinas[k] == "CSI000":
                            self.add_aresta(
                                i + 1, k + 1 + len(self.professores), 1, preferencia[j])
                            break
                        else:
                            self.add_aresta(
                                i + 1, k + 1 + len(self.professores), 2, preferencia[j])
                            break

    def add_matriz_disciplinas(self):

        # funcao que liga as disciplinas no vertice super demanda
        # ligando as disicplinas no vertice super demanda
        for i in range(len(self.disciplinas)):
            self.add_aresta(i + 1 + len(self.professores),
                            self.num_vert - 1, self.dicionario_disciplinas[i][2], 0)

    def matriz_adj(self):

        # funcao que cria todas as listas e matrizes com indice inicial 0
        # 2 vertices adicionais que sao o super demanda e o super oferta
        # + len(numero de professores) vertices  e len(numero de turmas) vertices
        self.num_vert = 2 + len(self.professores) + \
            len(self.num_turmas_disciplinas)

        self.mat_adj = [[0 for j in range(self.num_vert)]
                        for i in range(self.num_vert)]

        self.mat_cap = [[0 for j in range(self.num_vert)]
                        for i in range(self.num_vert)]

        self.mat_custo = [[0 for j in range(self.num_vert)]
                          for i in range(self.num_vert)]

        self.list_adj = [[] for i in range(self.num_vert)]

    def cria_dicionario(self):

        # funcao que cria dicionarios com todos os valores contidos no CSV
        for i in range(len(self.disciplinas)):
            self.dicionario_disciplinas[i] = [
                self.disciplinas[i], self.nome_disciplinas[i], self.num_turmas_disciplinas[i]]

        for i in range(len(self.professores)):
            self.dicionario_professores[i] = [self.professores[i], self.num_disciplinas_professores[i], [self.arqProf['Preferência 1'][i],
                                                                                                         self.arqProf['Preferência 2'][i], self.arqProf['Preferência 3'][i], self.arqProf['Preferência 4'][i], self.arqProf['Preferência 5'][i]]]
        # retirar os NaN da lista de preferencias dentro do dicionario
        for i in range(len(self.dicionario_professores)):
            self.dicionario_professores[i][2] = [
                x for x in self.dicionario_professores[i][2] if pd.isnull(x) == False and x != 'nan']

    def criaListaB(self):

        # funcao que cria uma lista auxiliar para usar no SCM
        self.list_b.append((self.num_super_oferta))

        for i in range(len(self.num_disciplinas_professores)):
            self.list_b.append((self.num_disciplinas_professores[i]))

        for i in range(len(self.nome_disciplinas)):
            self.list_b.append((0))

        self.list_b.append((self.num_super_demanda))

    def bellman_ford(self, s, v):

        # funcao que retorna o caminho minimo entra o vertice de origem e destino
        dist = [float("inf") for _ in range(len(self.list_adj))]
        pred = [None for _ in range(len(self.list_adj))]

        dist[s] = 0

        # resgatar os valores dist e pred da logica de Bellma Ford
        for i in range(0, len(self.list_adj) - 1):
            update = False
            for origem, destino, peso in self.arestas:
                if dist[destino] > dist[origem] + peso:
                    dist[destino] = dist[origem] + peso
                    pred[destino] = origem
                    update = True

            if update is False:
                break
        
        # traduz o dist e pred para uma lista contendo o caminho feito
        caminho = [v]
        i = pred[v]
        while i in pred:
            if i is None:
                break
            caminho.append(i)
            i = pred[i]

        if len(caminho) == 1:
            caminho.clear()
            return caminho

        caminho.reverse()

        return caminho

    def scm(self, s, t):

        # funcao que coloca em pratica o SUCESSIVOS-CAMINHOS-MINIMOS
        # utilizando as matrizes e listas criadas anteriormente
        self.mat_final = [
            [0 for i in range(len(self.mat_adj))] for j in range(len(self.mat_adj))]
        C = self.bellman_ford(s, t)

        while len(C) != 0 and self.list_b[s] != 0:

            f = float('inf')
            for i in range(1, len(C)):
                u = C[i - 1]
                v = C[i]
                if self.mat_cap[u][v] < f:
                    f = self.mat_cap[u][v]

            for i in range(1, len(C)):
                u = C[i - 1]
                v = C[i]
                self.mat_final[u][v] += f
                self.mat_cap[u][v] -= f
                self.mat_cap[v][u] += f

                if self.mat_cap[u][v] == 0:
                    self.mat_adj[u][v] = 0
                    self.arestas.remove((u, v, self.mat_custo[u][v]))

                if self.mat_adj[v][u] == 0:
                    self.mat_adj[v][u] = 1
                    self.arestas.append((v, u, -self.mat_custo[u][v]))
                    self.mat_custo[v][u] = -self.mat_custo[u][v]

                # fluxo reverso
                if self.mat_final[v][u] != 0:
                    self.mat_final[v][u] = self.mat_final[v][u] - f

            self.list_b[s] -= f
            self.list_b[t] += f
            C = self.bellman_ford(s, t)

        return self.mat_final

    def imprimeAlocacao(self):

        # funcao que imprime os resultados das alocações feitas
        # percorre a matriz final com os valores finais de alocaçoes
        preferencia = [0, 3, 5, 8, 10]

        print("{:<20} {:<20} {:<40} {:<40} {:<40}".format(
            'Professor', 'Disciplina', 'Nome', 'Classes', 'Custo'))
        for i in range(len(self.professores)):
            if self.dicionario_professores[i][1] == 0 :
                self.list_semAlocacao.append(self.dicionario_professores[i][0])

            for k in range(len(self.mat_final[i]) - 2 - len(self.professores)):
                if self.mat_final[i + 1][k + 1 + len(self.professores)] != 0:
                    for y in range(len(self.dicionario_professores[i][2])):

                        # if que calcula o custo da alocação
                        if self.dicionario_professores[i][2][y] == self.disciplinas[k]:
                            aux = preferencia[y] * (self.mat_final[i + 1]
                                                    [k + 1 + len(self.professores)])
                            break

                    print("{:<20} {:<20} {:<40} {:<40} {:<40}".format(
                        self.professores[i], self.disciplinas[k], self.nome_disciplinas[k], self.mat_final[i + 1][k + 1 + len(self.professores)], aux))
        
        # retorna professores que nao obteram alocações
        if self.list_semAlocacao != []:
            print("\nLista de professores sem alocação: ", self.list_semAlocacao)
        else: 
            print("\nTodos os professores foram alocados em alguma disciplina.")

    def iniciar(self):

        # funcao iniciar, executa uma etapa por vez
        self.define_professores()
        self.define_disciplinas()
        self.super_oferta()
        self.super_demanda()
        self.cria_dicionario()
        self.matriz_adj()
        self.add_matriz_superOferta()
        self.add_matriz_professores()
        self.add_matriz_disciplinas()
        self.criaListaB()
        self.scm(0, self.num_vert - 1)
        self.imprimeAlocacao()