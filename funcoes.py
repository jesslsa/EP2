#funções do jogo
from audioop import reverse
import math
import random
import dados 
import operator

# Normalizando Base de Países - transforma banco de dados em dicionario cujas chave são paises
def normaliza(DADOS):
    saida = {}
    for continente in DADOS.keys():
        for pais in DADOS[continente]:
            
            conteudo = DADOS[continente][pais]
            
            saida[pais] = conteudo
            saida[pais]['continente'] = continente

    return saida



# Distância de Haversine - calcula distancia entre país selecinado e o sorteado 
def haversine(fi1, l1, fi2, l2):
    latitude1_rad = fi1*math.pi/180
    latitude2_rad = fi2*math.pi/180
    longitude1_rad = l1*math.pi/180
    longitude2_rad = l2*math.pi/180

    dif1 = (latitude2_rad-latitude1_rad)/2
    dif2 = (longitude2_rad-longitude1_rad)/2

    a = (math.sin(dif1))**2
    b = (math.sin(dif2))**2

    c = math.cos(latitude1_rad)*math.cos(latitude2_rad)
    angulo = math.sqrt(a+c*b)
    distancia = 2 * dados.EARTH_RADIUS * math.asin(angulo)
    
    #return (f'{int(distancia):,}').replace(',','.')
    return distancia


# Sorteando Países - Escolhe país que deve ser adivinhado 
#dar .lower() no pais esolhido pelo jogador 
def sorteia_pais(dic):
    sorteio = random.choice(list(dic.keys()))
    return sorteio 



# Está na Lista? - verifica se o pais escolhido pelo user está no dicionario 
# tem que criar lista com os nomes dos paises
def esta_na_lista(pais, listas):
    pais=pais.lower()
    for lista in listas:
        if pais == lista:
            return True
    return False


# Adicionando em uma Lista Ordenada - retorna uma lista crescente com as distancias dos paises ja selecionados pelo jogador 
def adiciona_em_ordem(nome, distancia, lista):
    lista_1=[nome, distancia]
    lista_ordenada=[]
    contador=0
    if lista==[]:
        lista_ordenada.append(lista_1)
    else:
        for h in range(len(lista)):
            if nome==lista[h][0]:
                return lista
                break
    
        for i in range(len(lista)):
            if distancia<=lista[i][1]:
                lista_ordenada.append(lista_1)
                lista_ordenada.append([lista[i][0], lista[i][1]])
                contador=i
                break
    
            else:
                lista_ordenada.append([lista[i][0], lista[i][1]])
        if distancia>=lista[len(lista)-1][1]:
            lista_ordenada.append(lista_1)
        elif contador+1<len(lista):
            for k in range(contador+1,len(lista)):
                lista_ordenada.append([lista[k][0], lista[k][1]])
        
    return lista_ordenada


# Sorteia Letra com Restrições - sorteia uma letra da capital
#  Colocar letras ja sorteadas na lista de restrições
def sorteia_letra_capital(palavra, lista_restrita,dicas_permitidas,quantidade_tentativas):
    especiais = ['.', ',', '-', ';', ' ', '@', '!', '$', '%', '*', '(', ')', '{', '}', '[', ']', ':']
    saida = ''
    palavra = palavra.lower()
    palavra_lista = []
    continua = False

    for letra in palavra:

        if letra not in especiais and letra not in lista_restrita and letra not in palavra_lista:
            palavra_lista.append(letra)
            continua = True

    if(continua==False):
        atualiza_dicas_permitidas(dicas_permitidas,quantidade_tentativas,'2')

    while continua:
        saida = random.choice(palavra_lista)
        continua = False

    return saida

# Sorteia uma cor da bandeira
# Colocar tbm lista de restrição com as cores ja sorteadas
def cor_bandeira(bandeira, lista_restrita):
    cores_possiveis = []
    saida = ''

    for cor, quant in bandeira.items():
        if quant > 0:
            cores_possiveis.append(cor)

    saida = random.choice(cores_possiveis)
    
    if saida == 'outras' or saida in lista_restrita:
        while saida == 'outras' or saida in lista_restrita:
            saida = random.choice(cores_possiveis)

    return saida
# se ele ja sorteou todas as cores possiveis, retorna uma lista vazia



#inicializa os dados do pais sorteado
def cria_dicionario_pais_sorteado(pais,dicionario):
    dicionario_pais_sorteado = {}
    dicionario_pais_sorteado["nome"] = pais
    dicionario_pais_sorteado["latitude"] = dicionario[pais]['geo']['latitude']
    dicionario_pais_sorteado["longitude"] = dicionario[pais]['geo']['longitude']
    dicionario_pais_sorteado["area"] = dicionario[pais]['area']
    dicionario_pais_sorteado["populacao"] = dicionario[pais]['populacao']
    dicionario_pais_sorteado["capital"] = dicionario[pais]['capital']
    dicionario_pais_sorteado["bandeira"] = dicionario[pais]['bandeira']
    dicionario_pais_sorteado["continente"] = dicionario[pais]['continente']
    return dicionario_pais_sorteado


#debita tentativas
def debita_tentativa(total, debito, tentativas, entrada):
    if entrada not in tentativas.keys():
        if(total > debito):
            return total-debito
        return 0
    return total

def adiciona_tentativa(entrada,distancia_tentativa,distancias):
    distancias[entrada]=int(distancia_tentativa)
    distancias = dict(sorted(distancias.items(), key=operator.itemgetter(1),reverse=True))
    return distancias

def atualiza_dicas_permitidas(dicas_permitidas,quantidade_tentativas,dica_bloqueada):
    quantidade_tentativas = int(quantidade_tentativas)
    if(quantidade_tentativas<=4 and dicas_permitidas['1']==True):
        dicas_permitidas['1']=False
    if(quantidade_tentativas<=3 and dicas_permitidas['2']==True):
        dicas_permitidas['2']=False
    if(quantidade_tentativas<=6 and dicas_permitidas['3']==True):
        dicas_permitidas['3']=False
    if(quantidade_tentativas<=5 and dicas_permitidas['4']==True):
        dicas_permitidas['4']=False
    if(quantidade_tentativas<=7 and dicas_permitidas['5']==True):
        dicas_permitidas['5']=False
    if(dica_bloqueada!=''):
        dicas_permitidas[str(dica_bloqueada)]=False
    return dicas_permitidas


def dicas(entrada_dicas, pais_sorteado, lista_restrita_bandeira, lista_restrita_capital,dicas_permitidas,quantidade_tentativas):

    area_pais_sorteado = pais_sorteado['area']
    populacao_pais_sorteado = pais_sorteado['populacao']
    capital_pais_sorteado = pais_sorteado['capital']
    bandeira_pais_sorteado = pais_sorteado['bandeira']
    continente_pais_sorteado = pais_sorteado['continente']

    if(int(entrada_dicas)==1):
        dados = [cor_bandeira(bandeira_pais_sorteado, lista_restrita_bandeira), '4', 'Cor da Bandeira: ']
    if(int(entrada_dicas)==2):
        dados = [sorteia_letra_capital(capital_pais_sorteado, lista_restrita_capital,dicas_permitidas,quantidade_tentativas), '3', 'Letra da capital: ']
    if(int(entrada_dicas)==3):
        dados = [area_pais_sorteado, '6', 'Área: ']
    if(int(entrada_dicas)==4):
        dados = [populacao_pais_sorteado, '5', 'População: ']
    if(int(entrada_dicas)==5):
        dados = [continente_pais_sorteado, '7', 'Continente: ']

    dica = dados[0]
    tentativas_gastas = dados[1]
    identificador = dados[2]

    return dica, tentativas_gastas, identificador


def adiciona_dicas_usadas(nova_dica, dicas_ja_foram, entrada_dicas, dica):
    if entrada_dicas not in dicas_ja_foram.keys():
        dicas_ja_foram[entrada_dicas] = nova_dica

    elif entrada_dicas == '1':
        dicas_ja_foram[entrada_dicas] += ', {}'.format(dica)
    elif entrada_dicas == '2':
        dicas_ja_foram[entrada_dicas] += ', {}'.format(dica)

    return dicas_ja_foram

def normaliza_cores_bandeira(cores_bandeira):
    cores_auxiliar={}
    for cor in cores_bandeira.keys():
        if(cores_bandeira[cor]==0):
            cores_auxiliar[cor]=True
    for cor in cores_auxiliar.keys():
        del cores_bandeira[cor]
    if 'outras' in cores_bandeira:
        del cores_bandeira['outras']
    return cores_bandeira