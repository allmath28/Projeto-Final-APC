from operator import *

pedidos_rest = []
areas = []
mesas = []
estoque = []
cardapio = []

"""Definição das funções"""


def fechar_restaurante():
    # Função para fechamento do Restaurante

    if len(pedidos_rest) > 0:
        for indice, mesa in enumerate(pedidos_rest):
            num_pedido = indice + 1
            print(f"{num_pedido}. {mesa}")
    else:
        print('- historico vazio')


def relatorio_pedidos():
    # Função que imprime o relatório de pedidos de cada mesa

    if len(pedidos_rest) > 0:
        lista_mesas = sorted(mesas, key=itemgetter('num'))
        for mesa in lista_mesas:
          if len(mesa['pedidos']) > 0:
            print(f"mesa: {mesa['num']}")
            for pedido in mesa['pedidos']:
                print(f'- {pedido}')
    else:
        print('- nenhum pedido foi realizado')


def remove_item_estoque():
    # Função para fazer a verificação do estoque e remover caso o item chegue ao valor 0

    for item in estoque:
        if item['quantidade'] == 0:
            estoque.remove(item)


def adiciona_pedido(mesa, prato):
    # Função que recebe como parametros a mesa e o prato, e adiciona o pedido a mesa designada

    for item in mesas:
        if item['num'] == mesa:
            item['pedidos'].append(prato)
            item['pedidos'].sort()
            for pedido in pedidos_rest:
                if pedido['mesa'] == mesa:
                    pedido['pedidos'].append(prato)
            else:
                pedidos_rest.append(f"mesa {mesa} pediu {prato}")


def verifica_estoque(prato):
    # Função para verificação do estoque na hora do pedido retornando um valor booleano

    for item in cardapio:
        if item['nome'] == prato:
            for ing in item['ingredientes']:
                total_ing_necessario = item['ingredientes'].count(ing)
                tem_ing = False
                for recurso in estoque:
                    if ing == recurso['nome']:  # Caso haja ingredientes suficientes no estoque, continua a verificação
                        tem_ing = True
                        total_ing_disponivel = recurso['quantidade']
                        if total_ing_necessario <= total_ing_disponivel:
                            recurso['quantidade'] -= total_ing_necessario

                            if recurso['quantidade'] == 0:
                              estoque.remove(recurso)

                            continue
                else:  
                    if not tem_ing: # Caso não haja, retorna o seguinte erro
                        print(f'erro >> ingredientes insuficientes para produzir o item {prato}')
                        return False

    return True  # Retorna verdadeiro caso tenha todos os ingredientes no estoque


def verifica_pedido(num, prato):
    # Função que faz várias verificações na hora de realizar um pedido

    for mesa in mesas:  # Verifica se a mesa existe
        if mesa['num'] == num:
            if mesa['status'] == 'ocupada':  # Verifica se a mesa está ocupada

                for item in cardapio:  # Verifica se o prato pedido existe no cardápio

                    if item['nome'] == prato:  # Caso passe em todas as verificações faz o seguinte comando

                        if verifica_estoque(prato):  # Chama a função de verificação de estoque para o prato
                            return True
                        else: 
                            return False
                else:
                    print(f'erro >> item {prato} nao existe no cardapio')
                    break
            else:
                print(f'erro >> mesa {mesa["num"]} desocupada')
                break
    else:
        print(f'erro >> mesa {num} inexistente')


def adiciona_item(item, qtde):
    # Função para adicionar ou modificar item no estoque

    for coisa in estoque:
        if coisa['nome'] == item:
            coisa['quantidade'] = qtde
            break
    else:
        item_novo = {'nome': item, 'quantidade': qtde}
        estoque.append(item_novo)


def atualiza_estoque():
    # Função para leitura de arquivo para atualização do estoque

    file = input()
    with open(file) as arquivo:
        for linha in arquivo:
            linha = linha.strip('\n')
            linha = linha.split(', ')
            item, qtde = linha[0], int(linha[1])
            adiciona_item(item, qtde)


def adiciona_prato(item, ingredientes):
    # Função para adicionar ou modificar pratos no cardápio

    for prato in cardapio:
        if prato['nome'] == item:
            prato['ingredientes'] = ingredientes
            break
    else:
        prato = {'nome': item, 'ingredientes': ingredientes}
        cardapio.append(prato)


def atualiza_cardapio():
    # Função para leitura de arquivo para atualização do cardápio

    file = input()
    with open(file) as arquivo:
        for linha in arquivo:
            linha = linha.strip('\n')
            linha = linha.split(', ')
            item, ingredientes = linha[0], linha[1:]
            adiciona_prato(item, ingredientes)


def adiciona_mesa(num, area, status):
    # Função para adição ou modificação de mesas no restaurante

    for mesa in mesas:
        if mesa['num'] == num:
            mesa['area'] = area
            mesa['status'] = status
            areas.append(area)
            break
    else:
        mesa = {'num': num, 'area': area, 'status': status, 'pedidos': []}
        mesas.append(mesa)
        areas.append(area)


def atualiza_mesa():
    # Função para leitura de arquivo para atualização de mesas

    file = input()
    with open(file) as arquivo:
        for linha in arquivo:
            linha = linha.strip('\n')
            num, area, status = linha.strip().split(', ')
            adiciona_mesa(int(num), area, status)


def relatorio_mesas():
    # Função para exibição do relatório de mesas do restaurante

    lista_areas = sorted(areas)
    lista_mesas = sorted(mesas, key=itemgetter('area'))

    if len(areas) > 0:  # Verifica se existe alguma área no restaurante

        for area in lista_areas:  # Caso haja, executa o seguinte comando
            print('area:', area)

            for mesa in lista_mesas:  # Caso haja mesas na área, irá mostrar o número e o status da mesa

                if mesa['area'] == area:
                    print(f"- mesa: {mesa['num']}, status: {mesa['status']}")
                    

                else:  # Caso não haja mesas na área, exibe esta mensagem
                    print('- area sem mesas')

    else:  # Caso não haja mesas no restaurante, exibe esta mensagem
        print('- restaurante sem mesas')


def relatorio_cardapio():
    # Função para exibição do relatório do cardápio

    lista_cardapio = sorted(cardapio, key=itemgetter('nome'))

    if len(cardapio) > 0:  # Verifica se há algum item no cardápio

        for prato in lista_cardapio:  # Caso haja, executa os seguintes comandos

            print(f'item: ', prato['nome'])
            for item in prato['ingredientes']:  # Exibe o prato e os ingredientes necessários para cada prato
                print(f"- {item}: {prato['ingredientes'].count(item)}")

    else:  # Caso não tenha nenhum item no cardápio, exibe esta mensagem
        print('- cardapio vazio')


def relatorio_estoque():
    # Função para exibição do relatório do estoque

    lista_estoque = sorted(estoque, key=itemgetter('nome'))

    if len(estoque) > 0:  # Verifica se há algum item no estoque

        for item in lista_estoque:  # Caso haja, exibe o item e a quantidade
            print(f"{item['nome']}: {item['quantidade']}")

    else:  # Caso não haja, exibe esta mensagem
        print('- estoque vazio')


def fazer_pedido():
    # Função para realização de um pedido

    mesa, prato = input().split(',')
    mesa = int(mesa.strip())
    prato = prato.strip()

    if verifica_pedido(mesa, prato):  # Chama a função de verificação com os parametros mesa e prato
        # Caso retorne verdadeiro, chama a função de adicionar pedido
        adiciona_pedido(mesa, prato)
        print(f'sucesso >> pedido realizado: item {prato} para mesa {mesa}')


"""Inicio dos Comandos """

status = True

print('=> restaurante aberto')

while status:

    op = input()

    if op == '+ atualizar mesas':
        """comando Atualizar mesas"""
        atualiza_mesa()

    elif op == '+ atualizar cardapio':
        """comando Atualizar cardapio"""
        atualiza_cardapio()

    elif op == '+ atualizar estoque':
        """comando Atualizar estoque"""
        remove_item_estoque()
        atualiza_estoque()

    elif op == '+ relatorio mesas':
        """comando Relatório de mesas"""
        relatorio_mesas()

    elif op == '+ relatorio cardapio':
        """comando Relatorio do Cardapio"""
        relatorio_cardapio()

    elif op == '+ relatorio estoque':
        """comando Relatorio do Estoque"""
        relatorio_estoque()

    elif op == '+ fazer pedido':
        """comando Fazer Pedido"""
        fazer_pedido()
        remove_item_estoque()

    elif op == '+ relatorio pedidos':
        """comando Relatorio de Pedidos"""
        relatorio_pedidos()

    elif op == '+ fechar restaurante':
        """comando Fechar o Restaurante"""
        status = False
        fechar_restaurante()
        print('=> restaurante fechado')

    else:
        """Caso não seja inserido um comando correto, imprime essa mensagem"""
        print('erro >> comando inexistente')
