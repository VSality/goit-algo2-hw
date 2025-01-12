from edmond_karp import edmonds_karp

def create_capacity_matrix():
    #Термінал1: ID = 0
    #Термінал2: ID = 4
    #Склад1: ID = 1
    #Склад2: ID = 2
    #Склад3: ID = 3
    #Склад4: ID = 5
    #Магазин1: ID = 6
    #Магазин2: ID = 7
    #Магазин3: ID = 8
    #Магазин4: ID = 9
    #Магазин5: ID = 10
    #Магазин6: ID = 11
    #Магазин7: ID = 12
    #Магазин8: ID = 13
    #Магазин9: ID = 14
    #Магазин10: ID = 15
    #Магазин11: ID = 16
    #Магазин12: ID = 17
    #Магазин13: ID = 18
    #Магазин14: ID = 19
    num_nodes = 20

    # Создаем матрицу размером 20x20 и заполняем её нулями
    capacity = [[0] * num_nodes for _ in range(num_nodes)]

    capacity[0][1] = 25  # Термінал1 -> Склад1
    capacity[0][2] = 20  # Термінал1 -> Склад2
    capacity[0][3] = 15  # Термінал1 -> Склад3
    capacity[4][3] = 15  # Термінал2 -> Склад3
    capacity[4][5] = 30  # Термінал2 -> Склад4
    capacity[4][2] = 10  # Термінал2 -> Склад2

    capacity[1][6] = 15  # Склад1 -> Магазин1
    capacity[1][7] = 10  # Склад1 -> Магазин2
    capacity[1][8] = 20  # Склад1 -> Магазин3

    capacity[2][9] = 15  # Склад2 -> Магазин4
    capacity[2][10] = 10  # Склад2 -> Магазин5
    capacity[2][11] = 25  # Склад2 -> Магазин6

    capacity[3][12] = 20  # Склад3 -> Магазин7
    capacity[3][13] = 15  # Склад3 -> Магазин8
    capacity[3][14] = 10  # Склад3 -> Магазин9

    capacity[5][15] = 20  # Склад4 -> Магазин10
    capacity[5][16] = 10  # Склад4 -> Магазин11
    capacity[5][17] = 15  # Склад4 -> Магазин12
    capacity[5][18] = 5   # Склад4 -> Магазин13
    capacity[5][19] = 10  # Склад4 -> Магазин14

    return capacity


def get_path(capacity_matrix, source, target):
    # Источник (source) и сток (sink)
    source = source
    sink = target

    # Запускаем алгоритм Эдмондса-Карпа
    return edmonds_karp(capacity_matrix, source, sink)


# Основная программа
def main():
    # Создаем матрицу пропускных способностей
    capacity_matrix = create_capacity_matrix()

    for skladId in [0, 4]:
        for magId in range(6, 20):
            max_flow, flow = get_path(capacity_matrix, skladId, magId)
            all_path = ""
            for u in range(len(flow)):
                for v in range(len(flow[u])):
                    if flow[u][v] > 0:
                        all_path += f"{u} -> {v} -> поток: {flow[u][v]} -> "
                
            #if(len(all_path) > 0):
                #all_path += f"макс. поток: {max_flow}"
                #print(f"{all_path}")
            term_name = 1
            if(skladId == 4):
                term_name = 2
            if(max_flow > 0):
                print(f"Путь Терминал{term_name} -> Магазин{magId - 5}, поток: {max_flow}")
        

if __name__ == "__main__":
    main()
