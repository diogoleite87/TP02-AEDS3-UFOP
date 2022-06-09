import pandas as pd

class Grafo:

    def __init__(self, num_vert=0, num_arestas=0, lista_adj=None, mat_adj=None):
        self.num_vert = num_vert
        self.num_arestas = num_arestas

        self.num_super_oferta = 0
        self.num_super_demanda = 0

        self.professores = []
        self.num_disciplinas_professores = []

        self.disciplinas = []
        self.nome_disciplinas = []
        self.num_turmas_disciplinas = []

        self.dicionario_professores = {}
        self.dicionario_disciplinas = {}

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

        print("Lendo arquivo...")

        try:
            self.arqProf = pd.read_csv(
                'data/' + professores_CSV, sep=';', encoding='utf-8')
            self.arqDisc = pd.read_csv(
                'data/' + disciplinas_CSV, sep=';', encoding='utf-8')

        except:
            print('Erro ao abrir o arquivo!')

    def define_professores(self):
        print('\nPreenchendo dados dos professores...')

        for i in range(len(self.arqProf['Professor'])):
            self.professores.append(self.arqProf['Professor'][i])

        for i in range(len(self.arqProf['# Disciplinas'])):
            self.num_disciplinas_professores.append(
                self.arqProf['# Disciplinas'][i])

        print(self.professores)
        print(self.num_disciplinas_professores)

    def define_disciplinas(self):
        print('\nPreenchendo dados das disciplinas ofertadas...')

        for i in range(len(self.arqDisc['Disciplina'])):
            self.disciplinas.append(self.arqDisc['Disciplina'][i])

        for i in range(len(self.arqDisc['Nome'])):
            self.nome_disciplinas.append(self.arqDisc['Nome'][i])

        for i in range(len(self.arqDisc['# Turmas'])):
            self.num_turmas_disciplinas.append(self.arqDisc['# Turmas'][i])

        print(self.disciplinas)
        print(self.nome_disciplinas)
        print(self.num_turmas_disciplinas)

    def super_demanda(self):
        self.num_super_demanda = self.arqDisc['# Turmas'].sum()
        print('Super demanda:', + self.num_super_demanda)

    def super_oferta(self):
        self.num_super_oferta = self.arqDisc['# Turmas'].sum()
        print('Super oferta:', + self.num_super_oferta)

    def add_aresta(self, u, v, capacidade = float('inf'), peso = int):

        self.num_arestas += 1
        if u < self.num_vert and v < self.num_vert:
            self.mat_adj[u][v] = [capacidade, peso]
        else:
            print("Aresta invalida!")

    def remove_aresta(self, u, v):

        if u < self.num_vert and v < self.num_vert:
            if self.mat_adj[u][v] != 0:
                self.num_arestas -= 1
                self.mat_adj[u][v] = 0
                for (v2, w2) in self.lista_adj[u]:
                    if v2 == v:
                        self.lista_adj[u].remove((v2, w2))
                        break
            else:
                print("Aresta inexistente!")
        else:
            print("Aresta invalida!")
    
    def add_matriz_superOferta(self):

        # adicionando inicialmente vertice de super demanda
        # self.add_aresta(0, 0, self.num_super_oferta, 0)
        self.mat_adj[0][0] = 0

        for i in range (len(self.professores)):
            self.add_aresta(0, i + 1, 0, self.dicionario_professores[i][1])

        # print(self.mat_adj)

    def add_matriz_professores(self) :

        preferencia = [0, 3, 5, 8, 10]

        for i in range (len(self.dicionario_professores)) :
            for j in range (len(self.dicionario_professores[i][2])) :
                for k in range (len(self.disciplinas)) :
                    if self.dicionario_professores[i][2][j] == self.disciplinas[k]:
                        self.add_aresta(i + 1, k + 1 + len(self.professores), preferencia[j], 2)
                        break

        print(self.mat_adj)

    def add_matriz_disciplinas(self):

        for i in range (len(self.disciplinas)):
            self.add_aresta(i + 1 + len(self.professores), self.num_vert - 1, 0, self.dicionario_disciplinas[i][2])

        print('\n\n\n\n', self.mat_adj)

    def matriz_adj(self):
        print('\nCriando matriz adjacendias...')

        # 2 vertices adicionais que sao o super demanda e o super oferta
        # + len(numero de professores) vertices  e len(numero de turmas) vertices
        self.num_vert = 2 + len(self.professores) + len(self.num_turmas_disciplinas)

        # cria uma matriz preenchida com zeros
        self.mat_adj = [[0 for j in range(self.num_vert)]
                        for i in range(self.num_vert)]

    def cria_dicionario(self):

        print('\nCriando dicionario...')

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

        print(self.dicionario_disciplinas)
        print(self.dicionario_professores)
    
    def teste(self):
        print('testee')
        
    def iniciar(self):
        self.define_professores()
        self.define_disciplinas()
        self.super_oferta()
        self.super_demanda()
        self.cria_dicionario()
        self.matriz_adj()
        self.add_matriz_superOferta()
        self.add_matriz_professores()
        self.add_matriz_disciplinas()
        self.teste()