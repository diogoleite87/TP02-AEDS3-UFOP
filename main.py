from grafo import Grafo

grafo = Grafo()

aux = int(input("Deseja ler o conjunto de arquivo:\n 1 - professores_toy.csv / disciplinas_toy.csv\n 2 - professores.csv / disciplinas.csv\n  --> "))

if aux == 1 :
    grafo.ler_arquivo_csv('professores_toy.csv', 'disciplinas_toy.csv')
else :
    grafo.ler_arquivo_csv('professores.csv', 'disciplinas.csv')

grafo.iniciar()
