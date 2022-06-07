import pandas as pd

class Grafo:

    def __init__(self, num_vert=0, num_arestas=0, lista_adj=None, mat_adj=None):
        self.num_vert = num_vert
        self.num_arestas = num_arestas
        if lista_adj is None:
            self.lista_adj = [[] for i in range(num_vert)]
        else:
            self.lista_adj = lista_adj
        if mat_adj is None:
            self.mat_adj = [[0 for j in range(num_vert)]
                            for i in range(num_vert)]
        else:
            self.mat_adj = mat_adj

    def ler_arquivo_csv (self, professores_CSV, disciplinas_CSV):

        print("Lendo arquivo..")

        arqProf = pd.read_csv('data/' + professores_CSV, sep = ';', encoding = 'utf-8')
        arqDisc = pd.read_csv('data/' + disciplinas_CSV, sep = ';', encoding = 'utf-8')

        print(arqDisc)
        print(arqProf)