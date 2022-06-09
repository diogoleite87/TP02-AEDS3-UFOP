from grafo import Grafo

grafo = Grafo()

# professores_CSV = str(input("Digite o nome do arquivo de professores: "))
# disciplinas_CSV = str(input("Digite o nome do arquivo de disciplinas: "))

# grafo.ler_arquivo_csv(professores_CSV, disciplinas_CSV)

# grafo.ler_arquivo_csv('professores.csv', 'disciplinas.csv')
grafo.ler_arquivo_csv('professores_toy.csv', 'disciplinas_toy.csv')
grafo.iniciar()
