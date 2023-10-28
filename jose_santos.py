import pymaps
import os
import webbrowser
import csv
import math
import matplotlib.pyplot as plt


def project():
    if (VerificaIntegridadeFile(file_FactSelec) == -1 or len(list(csv.reader(open(file_FactSelec)))[0]) != 7):
        print("ERRO: Ficheiro  " + file_FactSelec + " corrupto!")
        return
    if (VerificaIntegridadeFile(file_coords) == -1 or len(list(csv.reader(open(file_coords)))[0]) != 3):
        print("ERRO: Ficheiro  " + file_coords + " corrupto!")
        return

    clear()
    print("----------MODELO DE APOIO A DECISAO PARA LOCALIZACAO DE HUB----------")
    print("\n")
    print("1 -> Pontos de Rede de Distribuicao")
    print("2 -> Score Relativo/Global de Localizacoes")
    print("3 -> Gerar Visualizacao Grafica de Localizacoes")
    print("4 -> Salvaguardar Informacao do Site seleccionado pelo WSC")
    print("5 -> Criar Novo Factor de Seleccao de Localizacao")
    print("6 -> Eliminar Novo Factor de Seleccao de Localizacao")
    print("0 -> Terminar")

    op = int(input("Seleccione uma opcao: "))
    while (op < 0 or op > 6):
        print("ERRO: Opcao Invalida")
        print("\n")
        op = int(input("Seleccione uma opcao: "))

    if (op == 0):
        return
    if (op == 1):
        return menu1(file_FactSelec)
    if (op == 2):
        return menu2(file_FactSelec)
    if (op == 3):
        return menu3(file_FactSelec, file_coords)
    if (op == 4):
        return menu4(file_FactSelec)
    if (op == 5):
        return menu5(file_FactSelec)
    if (op == 6):
        return menu6(file_FactSelec)


def menu1(file_FactSelec):
    clear()
    file = open(file_FactSelec, 'r')  # Abre ficheiro em modo leitura
    for line in file:
        print(line)  # Apresenta o ficheiro linha a linha
    print("\n")

    op = int(input("-> Seleccionar 0 para voltar ao menu principal: "))
    while (op != 0):
        print("ERRO: Opcao Invalida")
        op = int(input("-> Seleccionar 0 para voltar ao menu principal: "))

    file.close()  # Encerra o ficheiro
    return project()


def menu2(file_FactSelec):
    clear()

    if (len(list(csv.reader(
            open(file_FactSelec)))) == 1):  # Se o ficheiro s� tiver uma 1 linha (ou seja, o header) retorna ao menu do projecto
        print("ERRO: Nao Existem Criterios de Selec�ao")
        op = int(input("-> Seleccionar 0 para voltar ao menu principal: "))
        while (op != 0):
            print("ERRO: Opcao Invalida")
            op = int(input("-> Seleccionar 0 para voltar ao menu principal: "))
        return project()

    crit, scores_iniciais, localizacoes = SaveCritScoresLocal(
        file_FactSelec)  # Vai buscar valores de crit�rios, scores iniciais e nome das localiza��es
    scores_relativos, scores_global = CalcScores(crit, scores_iniciais)  # Vai calcular os scores relativos e global

    print(localizacoes)
    print("\n")
    print("Scores Relativos")
    for a in scores_relativos:
        print(a)
    print("\n")
    print("Scores Global")
    print(scores_global)
    print("\n")

    op = int(input("-> Seleccionar 0 para voltar ao menu principal: "))
    while (op != 0):
        print("ERRO: Opcao Invalida")
        op = int(input("-> Seleccionar 0 para voltar ao menu principal: "))
    return project()


def menu3(file_FactSelec, file_coords):
    clear()

    if (len(list(csv.reader(
            open(file_FactSelec)))) == 1):  # Se o ficheiro s� tiver uma 1 linha (ou seja, o header) retorna ao menu do projecto
        print("ERRO: Nao Existem Criterios de Selec�ao")
        op = int(input("-> Seleccionar 0 para voltar ao menu principal: "))
        while (op != 0):
            print("ERRO: Opcao Invalida")
            op = int(input("-> Seleccionar 0 para voltar ao menu principal: "))
        return project()

    crit, scores_iniciais, localizacoes = SaveCritScoresLocal(
        file_FactSelec)  # Vai buscar valores de crit�rios, scores iniciais e nome das localiza��es
    scores_relativos, scores_global = CalcScores(crit, scores_iniciais)  # Vai calcular os scores relativos e global
    coords = SaveCoords(file_coords)  # Vai buscar os valores de coordenadas de cada localiza��o

    index_best_local = [scores_global.index(
        max(scores_global))]  # Cria uma lista com o �ndice da localiza��o com melhor score global na lista scores_global

    save = scores_global.index(max(scores_global))
    while (len(index_best_local) != scores_global.count(
            max(scores_global))):  # Descobre os �ndices das localiza��es com melhor scores, se existir mais que um
        procura_novo_max = scores_global.index(max(scores_global), save + 1)
        index_best_local.append(procura_novo_max)
        save = procura_novo_max

    mapa = pymaps.PyMap()
    mapa.key = 'AIzaSyCj-UAqhnY-fhkeCEayjALakrGJMgcaQ6A'
    mapa.maps[0].zoom = 4  # Zoom Padr�o da p�gina PyMaps

    blue_icon = pymaps.Icon(
        'blue_icon')  # Nome de Novo �cone (Nota: blue_icon corresponde a localiza��o com melhor score global)
    blue_icon.image = "http://maps.gstatic.com/mapfiles/ms2/micons/blue-dot.png"  # URL de �cone
    blue_icon.iconSize = (32, 32)  # Tamanho do �cone
    mapa.addicon(blue_icon)  # Adiciona o �cone

    red_icon = pymaps.Icon('red_icon')
    red_icon.image = "http://maps.google.com/mapfiles/ms/icons/red-dot.png"
    red_icon.iconSize = (32, 32)
    mapa.addicon(red_icon)

    for a in range(len(coords)):  # Adiciona os pontos no mapa
        for b in index_best_local:
            if a == b:
                mapa.maps[0].setpoint([coords[a][1], coords[a][2], coords[a][0],
                                       'blue_icon'])  # Adiciona no mapa o ponto (Latitude, Longitude, Nome) com melhor score global e com blue_icon
                mapa.maps[0].center = (
                [coords[a][1], coords[a][2]])  # Centra o PyMaps nas coordenadas da localiza��o com melhor score global
                break
            mapa.maps[0].setpoint([coords[a][1], coords[a][2], coords[a][0],
                                   'red_icon'])  # Adiciona o ponto no mapa (Latitude, Longitude, Nome) e com red_icon

    f = open('mymap.html', 'wb')
    f.write(mapa.showhtml().encode('utf-8'))
    f.close()

    filepath = os.path.abspath('mymap.html')
    webbrowser.open('file://' + filepath)

    return project()


def menu4(file_FactSelec):
    clear()

    if (len(list(csv.reader(open(file_FactSelec)))) == 1 or len(list(csv.reader(
            open(file_FactSelec)))) == 2):  # Se o ficheiro s� tiver 2 linhas (ou seja, o header e um crit�rio) retorna ao menu do projecto
        print("ERRO: Numero Insuficiente de Criterios de Selec�ao")
        op = int(input("-> Seleccionar 0 para voltar ao menu principal: "))
        while (op != 0):
            print("ERRO: Opcao Invalida")
            op = int(input("-> Seleccionar 0 para voltar ao menu principal: "))
        return project()

    file = open(file_FactSelec, "r")  # Abre o ficheiro FactSelec em modo de leitura
    conta = 0
    for line in file:  # Imprime FactSelec, linha a linha com o n�mero de crit�rio
        print(conta, end=' ')
        print(line)
        conta += 1
    print("\n")

    crit, scores_iniciais, localizacoes = SaveCritScoresLocal(
        "FactSelec.csv")  # Vai buscar valores de crit�rios, scores iniciais e nome das localiza��es
    scores_relativos, scores_global = CalcScores(crit, scores_iniciais)  # Vai calcular os scores relativos e global

    local_wsc = int(input("Numero do Local para WSC: ")) - 1
    while (local_wsc < 0 or local_wsc >= len(localizacoes)):
        local_wsc = int(input("Numero do Local para WSC: ")) - 1

    k_max = int(input("Criterio Maximo para WSC: "))
    while (k_max < 2 or k_max > len(crit)):
        k_max = int(input("Criterio Maximo para WSC: "))

    save_scores_relativos = []
    for a in range(k_max):
        save_scores_relativos.append(scores_relativos[a][
                                         local_wsc])  # Guarda numa lista (save_scores_relativos) os scores relativos da localidade escolhida at� ao crit�rio m�ximo

    wsc, media, desvio_padrao = WSC(
        save_scores_relativos)  # Vai calcular a soma wsc, m�dia e desvio padrao no local escolhido at� ao crit�rio m�ximo
    print("\n")
    print("WSC escolhido para " + localizacoes[local_wsc] + " e criterio " + str(k_max) + ": " + str(wsc))
    print("\n")

    print("Media escolhido para " + localizacoes[local_wsc] + " e criterio " + str(k_max) + ": " + str(media))
    op = input("Gerar Grafico de Media WSC: ")
    if (op == 'sim' or op == 'Sim'):
        plt.plot(list(range(1, len(save_scores_relativos) + 1)), save_scores_relativos, linestyle="dashed", marker="o",
                 color="blue")  # Gera pontos de 1 at� ao n�mero de scores relativos escolhidos, e com o valor de cada um destes.
        plt.axhline(y=media, xmin=0, xmax=len(crit), linewidth=5, color='r')  # Gera uma linha com valor igual � media
        plt.axis([0, len(crit) + 1, 0,
                  max(save_scores_relativos) + 0.25 * max(save_scores_relativos)])  # Gera os eixos x e y do gr�fico
        plt.xlabel("Numero de Criterios")  # Legenda Eixo X
        plt.ylabel("Pontua�ao de Scores Relativos")  # Legenda Eixo Y
        plt.title("Scores Relativos e Media de " + localizacoes[local_wsc])  # Legenda Gr�fico
        plt.grid()  # Torna o Gr�fico quadriculado
        plt.show()  # Mostra o Gr�fico
    print("\n")

    print("Desvio Padrao escolhido para " + localizacoes[local_wsc] + " e criterio " + str(k_max) + ": " + str(
        desvio_padrao))

    op = int(input("-> Seleccionar 0 para voltar ao menu principal: "))
    while (op != 0):
        print("ERRO: Opcao Invalida")
        op = int(input("-> Seleccionar 0 para voltar ao menu principal: "))

    file.close()
    return project()


def menu5(file_FactSelec):
    clear()
    crit, scores_iniciais, localizacoes = SaveCritScoresLocal(
        file_FactSelec)  # Vai buscar valores de crit�rios, scores iniciais e nome das localiza��es

    name_new_crit = input("Nome do Novo Criterio: ")
    peso_new_crit = float(input("Peso do Novo Criterio: "))

    while (peso_new_crit <= 0):
        print("\n")
        print("ERRO: Valor Invalido")
        peso_new_crit = float(input("Peso do Novo Criterio: "))

    save_new_crit = [str(name_new_crit),
                     str(peso_new_crit)]  # Cria uma lista save_new_crit que guarda, convertido para string, o nome e peso do novo crit�rio

    for a in localizacoes:
        new_score = int(input("Score Inicial para " + (name_new_crit) + " em " + a + ": "))
        while (new_score < 0):
            print("\n")
            print("ERRO: Valor Invalido")
            new_score = int(input("Score Inicial para " + (name_new_crit) + " em " + a + ": "))
        save_new_crit.append(
            str(new_score))  # Adiciona � lista save_new_crit, o score inicial de cada localiza��o para o novo crit�rio

    save_new_file = list(csv.reader(open(file_FactSelec)))  # Guarda o ficheiro FactSelec numa nova lista, save_new_file
    save_new_file.append(
        save_new_crit)  # Adiciona a save_new_file a lista save_new_crit (nome de novo crit�rio, peso, score inicial para cada localiza��o)

    file = open(file_FactSelec, 'w', newline='')  # Abre o ficheiro FactSelec em modo de escrita
    writer = csv.writer(file)

    for line in save_new_file:  # Escreve para o ficheiro FactSelec vazio a lista save_new_file, linha a linha, adicionando o novo crit�rio
        writer.writerow(line)

    file.close()
    return project()


def menu6(file_FactSelec):
    clear()

    if (len(list(csv.reader(
            open(file_FactSelec)))) == 1):  # Se o ficheiro s� tiver uma 1 linha (ou seja, o header) retorna ao menu do projecto
        print("ERRO: Impossivel Remover Criterio de Selec�ao")
        op = int(input("-> Seleccionar 0 para voltar ao menu principal: "))
        while (op != 0):
            print("ERRO: Opcao Invalida")
            op = int(input("-> Seleccionar 0 para voltar ao menu principal: "))
        return project()

    file_old = open(file_FactSelec, 'r')  # Abre o ficheiro FactSelec em modo de leitura
    num_crit = 0
    for line in file_old:  # Imprime FactSelec, linha a linha com o n�mero de crit�rio
        print(num_crit, end=' ')
        print(line)
        num_crit += 1

    file_old.seek(0)  # Retorna o ponteiro ao in�cio do ficheiro

    print("\n")
    delete_line = int(input("Escolha o Criterio a Eliminar: "))
    while (delete_line < 1 or delete_line > len(list(csv.reader(
            open(file_FactSelec)))) - 1):  # Conta o numero de linhas e impede de eliminar criterios impossiveis
        delete_line = int(input("Escolha o Criterio a Eliminar: "))

    file_new = open('FactSelec_temp.csv', 'w', newline='')  # Cria um ficheiro FactSelec tempor�rio em modo de escrita

    reader = csv.reader(file_old)
    writer = csv.writer(file_new)

    conta = 0
    for a in reader:  # Percorre o ficheiro FactSelec
        if (conta == delete_line):  # Se o contador for igual � linha a eliminar, passa � frente
            conta += 1
            continue
        writer.writerow([a[0], a[1], a[2], a[3], a[4], a[5],
                         a[6]])  # Escreve para o ficheiro FactSelec_temp, cada coluna da linha de FactSelec
        conta += 1

    file_old.close()
    file_new.close()

    os.remove(file_FactSelec)  # Apaga o ficheiro FactSelec
    os.rename('FactSelec_temp.csv', file_FactSelec)  # Altera o nome de FactSelec tempor�rio, para o nome de FactSelec

    return project()


# FUN��ES

def SaveCritScoresLocal(filename):
    crit = []
    scores_iniciais = []
    with open(filename, 'rU') as f:  # Abre ficheiro file_FactSelec em modo leitura
        reader = csv.reader(f)
        for line in reader:  # Percorre o ficheiro linha a linha
            crit.append(line[1])  # Vai adicionando � lista de crit�rio os elementos da coluna 1 do ficheiro
            scores_iniciais.append(
                line[2:])  # Vai adicionando � lista de scores_iniciais da coluna 2 para a frente, do ficheiro
    localizacoes = scores_iniciais[0]  # Vai buscar as localizacoes ao primeiro elemento da lista de scores_iniciais

    f.close()
    return crit[1:], scores_iniciais[
                     1:], localizacoes  # Retorna ao projecto apenas os valores do crit�rios, apenas os valores dos scores_iniciais e o nome das localiza��es


def CalcScores(crit, scores_iniciais):
    scores_relativos = []
    scores_global = [0] * len(scores_iniciais[
                                  0])  # Cria uma lista para guardar os eventuais scores global com o tamanho das locali��es existentes
    for a in range(len(scores_iniciais)):
        save = []  # Cria lista save para guardar dados / Apaga lista save
        for b in range(len(scores_iniciais[a])):
            save.append(float(scores_iniciais[a][b]) * float(
                crit[a]))  # Guarda na lista save o score relativo resultante do score inicial pelo peso do crit
            scores_global[b] += float(scores_iniciais[a][b]) * float(
                crit[a])  # Vai somando o score relativo de cada localiza��o de forma a calcular o score global
        scores_relativos.append(
            save)  # Vai passando � lista scores_relativos, o score relativo calculado de cada crit�rio

    return scores_relativos, scores_global


def SaveCoords(filename):
    coords = []  # Cria uma lista vazia para eventualmente guardar as coordenadas de cada localiza��o
    with open(filename, 'rU') as f:
        reader = csv.reader(f)
        header = next(reader)

        for line in reader:
            coords.append(line)  # Percorre o ficheiro de coordenadas, linha a linha, e adiciona cada � lista coords

    f.close()
    return coords  # Retorna uma lista de lista contendo cada uma o nome, latitude e longitude da localiza��o


def WSC(save_scores_relativos):
    WSC = 0
    media = 0
    variancia = 0

    for a in save_scores_relativos:  # Calcula o WSC (Soma dos scores relativos at� ao crit�rio dado)
        WSC += float(a)

    media = WSC / (len(save_scores_relativos))

    for a in save_scores_relativos:  # Calcula parte da variancia (Soma ao quadrado da diferen�a entre os scores relativos e a media)
        variancia += (a - media) ** 2

    variancia = variancia / (len(save_scores_relativos) - 1)
    desvio_padrao = math.sqrt(variancia)

    return WSC, media, desvio_padrao


# FUN��ES DE SUPORTE

def VerificaExistFile(filename):  # Verifica a existencia de ficheiros
    try:  # Tenta abrir o ficheiro com o nome padr�o
        open(filename)
        return filename  # Caso exista com o nome padr�o, continua para o projecto
    except IOError:  # N�o encontra o ficheiro com o nome padr�o
        print("ERRO: %s nao encontrado" % filename)
        check = 0
    while (check == 0):  # Pede ao utilizador o novo nome do ficheiro, at� o encontrar
        print("\n")
        filename = input("Nome de Ficheiro a Procurar: ")
        try:
            open(filename)
            check = 1
        except IOError:
            print("ERRO: %s nao encontrado" % filename)
    return filename  # Retorna o novo nome do ficheiro


def VerificaIntegridadeFile(filename):  # Verifica se o ficheiro n�o est� corrupto
    file = open(filename, 'r')
    reader = csv.reader(file)

    num_row = len(list(csv.reader(open(filename)))[0])  # Conta o numero de colunas do ficheiro

    header = next(reader)

    for line in reader:  # Percorre o ficheiro linha a linha
        for a in range(1, num_row):
            try:
                float(line[a])
            except IndexError:  # Caso o ficheiro n�o estiver organizado estruturalmente, retorna erro
                file.close()
                return -1
            except ValueError:  # Caso o ficheiro n�o contenha n�meros a partir da segunda coluna, retorna erro
                file.close()
                return -1
    file.close()
    return 0


def clear():
    print("\n" * 20)


if __name__ == '__main__':
    file_FactSelec = VerificaExistFile("FactSelec.csv")  # Tenta verificar a existencia do ficheiro FactSelec.csv
    file_coords = VerificaExistFile("coords.csv")  # Tenta verificar a existencia do ficheiro coords.csv
    project()
