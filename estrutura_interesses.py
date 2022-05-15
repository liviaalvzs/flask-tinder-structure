database = {} #um dicionário, que tem a chave interesses para o controle
#dos interesses (que pessoa se interessa por que outra), e pessoas para o controle de pessoas (quem sao as pessoas e quais sao os dados pessoais de cada pessoa no sistema)
#voce pode controlar as pessoas de outra forma se quiser, nao precisa mudar nada
#do seu código para usar essa váriavel
database['interesses'] = { 
    100: [101, 102, 103],
    200: [100]
}
database['pessoa'] = [] #esse voce só faz se quiser guardar nessa lista os dicionários das pessoas

#em todo esse codigo que estou compartilhando, as variaveis interessado, alvo de interesse, pessoa, pessoa1 e pessoa2 sao sempre IDs de pessoas

class NotFoundError(Exception):
    pass

def todas_as_pessoas():
    return database['pessoa']

def adiciona_pessoa(dic_pessoa):
    database['pessoa'].append(dic_pessoa)
    id = dic_pessoa['id']
    database['interesses'][id] = []
    return database['pessoa']

def localiza_pessoa(id_pessoa):
    for item in database['pessoa']:
        if item['id'] == id_pessoa:
            return item
    raise NotFoundError

def reseta():
    database['interesses'] = {}
    database['pessoa'] = []

def adiciona_interesse(id_interessado, id_alvo_de_interesse):
    interessado = localiza_pessoa(id_interessado)
    alvo_de_interesse = localiza_pessoa(id_alvo_de_interesse)
    (database['interesses'])[id_interessado].append(id_alvo_de_interesse)
    return database['interesses']
    

def consulta_interesses(id_interessado):
    interessado = localiza_pessoa(id_interessado)
    if id_interessado in database['interesses'].keys():
        return database['interesses'][id_interessado]
    else:
        return []

def remove_interesse(id_interessado,id_alvo_de_interesse):
    interessado = localiza_pessoa(id_interessado)
    alvo_de_interesse = localiza_pessoa(id_alvo_de_interesse)
    if id_interessado in database['interesses'].keys():
        (database['interesses'])[id_interessado].remove(id_alvo_de_interesse)
    return database['interesses']



#essa funcao diz se o 1 e o 2 tem match. (retorna True se eles tem, False se não)
#ela não está testada, só existe para fazer aquecimento para a próxima
def verifica_match(id1,id2):
    l1 = consulta_interesses(id1)
    l2 = consulta_interesses(id2)
    if id2 in l1 and id1 in l2:
        return True
    else:
        return False
        
def lista_matches(id_pessoa):
    pessoa = localiza_pessoa(id_pessoa)
    matchesPessoa = []
    for i in database['interesses'][id_pessoa]:
        if (verifica_match(id_pessoa, i)):
            matchesPessoa.append(i)
    return matchesPessoa        




