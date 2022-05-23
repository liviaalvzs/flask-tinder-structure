import requests
import unittest

'''
Agora que você já montou a estrutura lógica do tinder (o "model") definida no primeiro
arquivo de testes

Vamos fazer a parte de rede. Permitir que a estrutura seja acessada a partir
de outros computadores.

O exercicio é bem paralelo ao anterior.
'''

'''
p1: controle de pessoas. 
Define as urls 
/pessoas, com GET, para pegar a lista de todas as pessoas
/pessoas, com POST, receber um dicionário de uma pessoa e colocar na lista
/pessoas/30, com GET, para pegar o dicionario da pessoa 30
/reseta, com POST, para esvaziar a lista de pessoas

Exemplo de lista de pessoas:
    [
        {
            "id": 9, 
            "nome": "maximus"
        }, 
        {
            "id": 3, 
            "nome": "aurelia"
        }
    ]
Exemplo de dicionario de uma pessoa:      { "id": 9, "nome": "maximus"}, 

Detalhes: /pessoas/30 pode dar um cod status 404, se a pessoa nao existir
'''

'''
p2: interesses
    
    executar um PUT em /sinalizar_interesse/9/3/ significa que 9 está interessado(a) em 3
    executar DELETE em /sinalizar_interesse/9/3/ significa que 9 não tem interesse em 3
    executar um GET em /interesses/9 devolve uma lista de ids de pessoas, com as pessoas por quem 9 se interessa
    
    Detalhes: Lance um cod de status 404 quando uma das pessoas não existir
              Lembre-se do reseta tb para os interesses (mesma URL, mesmo verbo) -- Ou seja, acessar /reseta com verbo post também limpa a lista de interesses
'''

'''
p3: matches

    executar um GET em /matches/9 devolve uma lista de ids de pessoas, com as pessoas por quem 9 se interessa
'''

'''
p4: preferencias

    as caracteristicas sexo e buscando afetam quem pode sinalizar interesse. Sinalizações inválidas resultam cod status 400
'''


class TestStringMethods(unittest.TestCase):


    def test_p1_00_pessoas_retorna_lista(self):
        #se eu acessar a url /pessoas
        r = requests.get('http://localhost:5003/pessoas')
        #vou ter um retorno que deve ser uma lista
        objeto_retornado = r.json()
        self.assertEqual(type(objeto_retornado),type([]))



    def test_p1_01_adiciona_pessoas(self):
        r_reset = requests.post('http://localhost:5003/reseta')
        #se o reseta ainda nao estiver funcionando, nao se preocupe
        #esse teste deve passar, outro teste vai conferir isso

        #crio fernando, verificando se deu erro
        r = requests.post('http://localhost:5003/pessoas',
                           json={'nome':'fernando','id':1})
        if r.status_code != 200:
            try:
                print('erro',r.json())
            except:
                print("criacao do fernando nao retornou json")
            self.fail("criação do fernando nao deu certo. Cod status:"+str(r.status_code))

        #crio roberto
        r = requests.post('http://localhost:5003/pessoas',json={'nome':'roberto','id':2})
        if r.status_code != 200:
            try:
                print('erro',r.json())
            except:
                print("criacao do roberto nao retornou json")
            self.fail("criação do roberto nao deu certo")

        #pego a lista de pessoas do servidor e vejo se apareceram
        #roberto e fernando
        r_lista = requests.get('http://localhost:5003/pessoas')
        lista_devolvida = r_lista.json()

        achei_fernando = False
        achei_roberto = False
        for dic_pessoa in lista_devolvida:
            if dic_pessoa['nome'] == 'fernando':
                achei_fernando = True
            if dic_pessoa['nome'] == 'roberto':
                achei_roberto = True
        if not achei_fernando:
            self.fail('pessoa fernando nao apareceu na lista de pessoas')
        if not achei_roberto:
            self.fail('pessoa roberto nao apareceu na lista de pessoas')

    #acessando /pessoas/5, vejo só o dicionario da pessoa 5
    def test_p1_02_pessoa_por_id(self):
        r = requests.post('http://localhost:5003/pessoas',
                           json={'nome':'mario','id':20})
        r = requests.get('http://localhost:5003/pessoas/20')
        dicionario_retornado = r.json()
        self.assertEqual(type(dicionario_retornado),type({}))
        self.assertEqual(dicionario_retornado['nome'],'mario')


    #reseta faz o banco de pessoas e de interesses zerar, 
    #ficar vazio
    def test_p1_03_reseta_apaga_pessoas(self):
        #crio um usuário
        r = requests.post('http://localhost:5003/pessoas',json={'nome':'cicero','id':29})
        #pego a lista de todos os usuários
        r_lista = requests.get('http://localhost:5003/pessoas')
        #essa lista tem que ter pelo menos 1 elemento, que eu 
        #acabei de criar
        self.assertTrue(len(r_lista.json()) > 0)

        #acesso a url reseta
        r_reset = requests.post('http://localhost:5003/reseta')
        #e a url reseta funciona sem reclamar (retorna cod status 200)
        self.assertEqual(r_reset.status_code,200)

        #agora a lista de usuários deve estar vazia
        r_lista_depois = requests.get('http://localhost:5003/pessoas')
        self.assertEqual(len(r_lista_depois.json()),0)

    '''
    Esse teste verifica se a chamada PUT em /sinalizar_interesse/pessoa_a/pessoa_b
    dá erro quando pessoa_a ou pessoa_b nao existe
    voce nao precisa nem pensar ainda como salvar um interesse,
    só dê um erro se alguma das pessoas envolvidas nao existe
    '''
    def test_p2_00_interesse_com_pessoas_validas(self):
        #reseto
        r_reset = requests.post('http://localhost:5003/reseta')

        #crio a pessoa 9
        r = requests.post('http://localhost:5003/pessoas',json={'nome':'maximus','id':9})
        self.assertEqual(r.status_code,200)

        #interesse de 9 para 3 dá erro, pois 3 nao existe ainda
        r = requests.put('http://localhost:5003/sinalizar_interesse/9/3/')
        self.assertEqual(r.status_code,404)

        #interesse de 3 para 9 dá erro, pois 3 nao existe ainda
        r = requests.put('http://localhost:5003/sinalizar_interesse/3/9/')
        self.assertEqual(r.status_code,404)
        
        #agora crio a pessoa 3
        r = requests.post('http://localhost:5003/pessoas',json={'nome':'aurelia','id':3})
        self.assertEqual(r.status_code,200)

        #agora posso marcar interesse de 3 pra 9 e de 9 pra 3 sem problemas
        r = requests.put('http://localhost:5003/sinalizar_interesse/9/3/')
        self.assertEqual(r.status_code,200)
        r = requests.put('http://localhost:5003/sinalizar_interesse/3/9/')
        self.assertEqual(r.status_code,200)

        #esse finalizinho é só uma piada sobre amor proprio que ficou no teste :P
        r = requests.put('http://localhost:5003/sinalizar_interesse/9/9/')
        self.assertEqual(r.status_code,200)

    '''
    Quando uma pessoa A sinaliza interesse por B,
    B aparece na lista de interesses de A

    (a lista de interesse de A estará disponivel em
    /interesses/A, com o verbo GET)
    '''
    def test_p2_01_consulta_interesse(self):
        #reseto
        r_reset = requests.post('http://localhost:5003/reseta')
        self.assertEqual(r_reset.status_code,200)

        
        #maximus acabou de ser criado, nao tem interesses
        r = requests.post('http://localhost:5003/pessoas',json={'nome':'maximus','id':9})
        self.assertEqual(r.status_code,200)
        r = requests.get('http://localhost:5003/interesses/9')
        self.assertEqual(r.status_code,200)
        lista_interesses = r.json() 
        self.assertEqual(lista_interesses,[])
        
        #crio aurelia
        r = requests.post('http://localhost:5003/pessoas',json={'nome':'aurelia','id':3})
        self.assertEqual(r.status_code,200)
        
        #maximus está interessado em aurélia
        r = requests.put('http://localhost:5003/sinalizar_interesse/9/3/')
        self.assertEqual(r.status_code,200)
        r = requests.get('http://localhost:5003/interesses/9')
        self.assertEqual(r.status_code,200)
        lista_interesses = r.json() 
        self.assertEqual(lista_interesses,[3])

        #crio diana
        r = requests.post('http://localhost:5003/pessoas',json={'nome':'diana','id':30})
        self.assertEqual(r.status_code,200)
        
        #maximus está interessado em diana
        #(veja na URL, estamos marcando interesse de 9 para 30)
        r = requests.put('http://localhost:5003/sinalizar_interesse/9/30/')
        self.assertEqual(r.status_code,200)
        r = requests.get('http://localhost:5003/interesses/9')
        self.assertEqual(r.status_code,200)
        lista_interesses = r.json() 
        #maximus está interessado tanto em diana quanto em aurelia
        #3 aparece na lista
        self.assertIn(3,lista_interesses)
        #30 tb aparece na lista
        self.assertIn(30,lista_interesses)
        #tam da lista é 2
        self.assertEqual(len(lista_interesses),2)
    
    def test_p2_03_resetar_afeta_interesses(self):
        #reseto
        r_reset = requests.post('http://localhost:5003/reseta')
        self.assertEqual(r_reset.status_code,200)

        
        #maximus acabou de ser criado, nao tem interesses
        r = requests.post('http://localhost:5003/pessoas',json={'nome':'maximus','id':9})
        self.assertEqual(r.status_code,200)
        r = requests.get('http://localhost:5003/interesses/9')
        self.assertEqual(r.status_code,200)
        lista_interesses = r.json() 
        self.assertEqual(lista_interesses,[])
        
        #crio aurelia
        r = requests.post('http://localhost:5003/pessoas',json={'nome':'aurelia','id':3})
        self.assertEqual(r.status_code,200)
        
        #maximus está interessado em aurélia
        r = requests.put('http://localhost:5003/sinalizar_interesse/9/3/')
        self.assertEqual(r.status_code,200)
        r = requests.get('http://localhost:5003/interesses/9')
        self.assertEqual(r.status_code,200)
        lista_interesses = r.json() 
        self.assertEqual(lista_interesses,[3])
        
        #reseto
        r_reset = requests.post('http://localhost:5003/reseta')
        self.assertEqual(r_reset.status_code,200)
        
        #maximus acabou de ser criado, nao tem interesses
        r = requests.post('http://localhost:5003/pessoas',json={'nome':'maximus','id':9})
        self.assertEqual(r.status_code,200)
        r = requests.get('http://localhost:5003/interesses/9')
        self.assertEqual(r.status_code,200)
        lista_interesses = r.json() 
        self.assertEqual(lista_interesses,[])

    def test_p2_04_deleta_interesse(self):
        #reseto
        r_reset = requests.post('http://localhost:5003/reseta')
        self.assertEqual(r_reset.status_code,200)

        
        #maximus acabou de ser criado, nao tem interesses
        r = requests.post('http://localhost:5003/pessoas',json={'nome':'maximus','id':9})
        self.assertEqual(r.status_code,200)
        r = requests.get('http://localhost:5003/interesses/9')
        self.assertEqual(r.status_code,200)
        lista_interesses = r.json() 
        self.assertEqual(lista_interesses,[])
        
        #crio aurelia
        r = requests.post('http://localhost:5003/pessoas',json={'nome':'aurelia','id':3})
        self.assertEqual(r.status_code,200)
        
        #maximus está interessado em aurélia
        r = requests.put('http://localhost:5003/sinalizar_interesse/9/3/')
        self.assertEqual(r.status_code,200)
        r = requests.get('http://localhost:5003/interesses/9')
        self.assertEqual(r.status_code,200)
        lista_interesses = r.json() 
        self.assertEqual(lista_interesses,[3])

        #crio diana
        r = requests.post('http://localhost:5003/pessoas',json={'nome':'diana','id':30})
        self.assertEqual(r.status_code,200)
        
        #maximus está interessado em diana
        #(veja na URL, estamos marcando interesse de 9 para 30)
        r = requests.put('http://localhost:5003/sinalizar_interesse/9/30/')
        self.assertEqual(r.status_code,200)
        r = requests.get('http://localhost:5003/interesses/9')
        self.assertEqual(r.status_code,200)
        lista_interesses = r.json() 
        #maximus está interessado tanto em diana quanto em aurelia
        #3 aparece na lista
        self.assertIn(3,lista_interesses)
        #30 tb aparece na lista
        self.assertIn(30,lista_interesses)
        #tam da lista é 2
        self.assertEqual(len(lista_interesses),2)

        #deletei o interesse de 9 em 30
        requests.delete('http://localhost:5003/sinalizar_interesse/9/30/')
        #consultei os interesses de 9
        r = requests.get('http://localhost:5003/interesses/9')
        lista_interesses = r.json() 
        # 9 ainda gosta de 3
        self.assertIn(3,lista_interesses)
        # 9 gosta de apenas 1 pessoa
        self.assertEqual(len(lista_interesses),1)
        #deletei o interesse de 9 em 30
        requests.delete('http://localhost:5003/sinalizar_interesse/9/3/')
        #consultei os interesses de 9
        r = requests.get('http://localhost:5003/interesses/9')
        lista_interesses = r.json() 
        # 9 no gosta de ninguem
        self.assertEqual(len(lista_interesses),0)

    #matches serão acessados em /matches/id_pessoa, com GET

    def test_p3_01_match(self):
        #reseto
        r_reset = requests.post('http://localhost:5003/reseta')
        self.assertEqual(r_reset.status_code,200)

        
        #maximus acabou de ser criado, nao tem matches
        r = requests.post('http://localhost:5003/pessoas',json={'nome':'maximus','id':9})
        self.assertEqual(r.status_code,200)
        r = requests.get('http://localhost:5003/matches/9')
        self.assertEqual(r.status_code,200)
        lista_matches = r.json() 
        self.assertEqual(lista_matches,[])
        
        #crio aurelia
        r = requests.post('http://localhost:5003/pessoas',json={'nome':'aurelia','id':3})
        self.assertEqual(r.status_code,200)
        
        #maximus está interessado em aurélia, mas ainda não é correspondido
        r = requests.put('http://localhost:5003/sinalizar_interesse/9/3/')
        self.assertEqual(r.status_code,200)
        r = requests.get('http://localhost:5003/matches/9')
        self.assertEqual(r.status_code,200)
        lista_matches = r.json() 
        self.assertEqual(lista_matches,[])
        
        
        #agora ele é correspondido por aurelia
        r = requests.put('http://localhost:5003/sinalizar_interesse/3/9/')
        self.assertEqual(r.status_code,200)
        r = requests.get('http://localhost:5003/matches/9')
        self.assertEqual(r.status_code,200)
        self.assertEqual(r.json(),[3]) #agora sim aparece o match

        #crio diana
        r = requests.post('http://localhost:5003/pessoas',json={'nome':'diana','id':30})
        self.assertEqual(r.status_code,200)
        
        #maximus está interessado em diana, mas ainda não é correspondido
        #(veja na URL, estamos marcando interesse de 9 para 30)
        r = requests.put('http://localhost:5003/sinalizar_interesse/9/30/')
        self.assertEqual(r.status_code,200)
        r = requests.get('http://localhost:5003/matches/9')
        self.assertEqual(r.status_code,200)
        self.assertEqual(r.json(),[3])

        #agora é correspondido
        r = requests.put('http://localhost:5003/sinalizar_interesse/30/9/')
        self.assertEqual(r.status_code,200)
        r = requests.get('http://localhost:5003/matches/9')
        self.assertEqual(r.status_code,200)
        lista_de_matches = r.json()
        #agora maximus tem 2 matches. A ordem nao importa
        self.assertIn(3,lista_de_matches) #id da aurelia
        self.assertIn(30,lista_de_matches) #id da diana

        #aurélia também tem o match
        r = requests.get('http://localhost:5003/matches/3')
        self.assertEqual(r.status_code,200)
        self.assertEqual(r.json(),[9])

        #diana também tem o match
        r = requests.get('http://localhost:5003/matches/30')
        self.assertEqual(r.status_code,200)
        self.assertEqual(r.json(),[9])

    #consultar matches de uma pessoa que nao existe resulta
    #cod status 404
    def test_p3_02_match_404(self):
        #reseto
        r_reset = requests.post('http://localhost:5003/reseta')
        self.assertEqual(r_reset.status_code,200)
        
        #nao tem ninguem ainda, devo ter um erro
        r = requests.get('http://localhost:5003/matches/9')
        self.assertEqual(r.status_code,404)

        #crio a pessoa de id 9
        r = requests.post('http://localhost:5003/pessoas',json={'nome':'maximus','id':9})
        self.assertEqual(r.status_code,200)

        #agora funciona
        r = requests.get('http://localhost:5003/matches/9')
        self.assertEqual(r.status_code,200)

        #mas nao para outras pessoas
        r = requests.get('http://localhost:5003/matches/4')
        self.assertEqual(r.status_code,404)


    #uso do verbo delete, na url sinalizar_interesse, para
    #remover um interesse (e o match, se existia um)

    # A gosta B
    # B gosta A -> match
    # B remove gostar A -> match desaparece
    #(mesmo que A ainda goste de B)

    #perceba, DELETE na url sinalizar interesse, 
    #nao no match
    #mas o match muda como consequencia
    
    def test_p3_03_match_perdido(self):
        #resetei
        r_reset = requests.post('http://localhost:5003/reseta')
        self.assertEqual(r_reset.status_code,200)

        #nenhum usuario tem matches ainda, porque nao existe usuário
        r = requests.get('http://localhost:5003/matches/9')
        self.assertEqual(r.status_code,404)

        #criei o primeiro usuário
        r = requests.post('http://localhost:5003/pessoas',json={'nome':'maximus','id':9})
        self.assertEqual(r.status_code,200)

        #maximus acabou de ser criado, nao tem matches
        r = requests.get('http://localhost:5003/matches/9')
        self.assertEqual(r.status_code,200)
        self.assertEqual(r.json(),[])
        
        #crio aurelia
        r = requests.post('http://localhost:5003/pessoas',json={'nome':'aurelia','id':3})
        self.assertEqual(r.status_code,200)
        
        #maximus está interessado em aurélia, mas ainda não é reciproco
        r = requests.put('http://localhost:5003/sinalizar_interesse/9/3/')
        self.assertEqual(r.status_code,200)
        r = requests.get('http://localhost:5003/matches/9')
        self.assertEqual(r.status_code,200)
        self.assertEqual(r.json(),[])

        #aurélia tb tem interesse, a lista de matches de maximus contém ela
        r = requests.put('http://localhost:5003/sinalizar_interesse/3/9/')
        self.assertEqual(r.status_code,200)
        r = requests.get('http://localhost:5003/matches/9')
        self.assertEqual(r.status_code,200)
        self.assertEqual(r.json(),[3])

        #aurélia perde o interesse, a lista de matches de maximus esvazia
        r = requests.delete('http://localhost:5003/sinalizar_interesse/3/9/')
        self.assertEqual(r.status_code,200)
        #consulto a lista de maximus
        r = requests.get('http://localhost:5003/matches/9')
        self.assertEqual(r.status_code,200)
        #e tem que ser vazia
        self.assertEqual(r.json(),[])

    #o perfil do usuário (ou usuária) ganha duas caracteristicas novas
    #o sexo e quais pessoas ele(a) está buscando
    #maximus = {'nome':'maximus','id':9,'sexo':'homem','buscando':['mulher']}
    def test_p4_01_match_incompativel(self):
        r_reset = requests.post('http://localhost:5003/reseta')
        self.assertEqual(r_reset.status_code,200)
        r = requests.get('http://localhost:5003/matches/9')
        self.assertEqual(r.status_code,404)
        maximus = {'nome':'maximus','id':9,'sexo':'homem','buscando':['mulher']}
        r = requests.post('http://localhost:5003/pessoas',json=maximus)
        self.assertEqual(r.status_code,200)

        #maximus acabou de ser criado, nao tem matches
        r = requests.get('http://localhost:5003/matches/9')
        self.assertEqual(r.status_code,200)
        self.assertEqual(r.json(),[])
        
        #crio aurelia
        aurelia = {'nome':'aurelia','id':3,'sexo':'mulher','buscando':['mulher']}
        r = requests.post('http://localhost:5003/pessoas',json=aurelia)
        self.assertEqual(r.status_code,200)

        #maximus está interessado em aurélia
        r = requests.put('http://localhost:5003/sinalizar_interesse/9/3/')
        self.assertEqual(r.status_code,200)
        r = requests.get('http://localhost:5003/matches/9')
        self.assertEqual(r.status_code,200)
        self.assertEqual(r.json(),[])

        #aurelia manifesta interesse em maximus, mas isso é incompativel
        #com suas preferências anteriores
        r = requests.put('http://localhost:5003/sinalizar_interesse/3/9/')
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'interesse incompativel')
        #esse erro ocorre quando A manifesta interesse em M, 
        #mas A declarou anteriormente que nao tem interesse 
        #em ninguém do sexo de M
        r = requests.get('http://localhost:5003/matches/9')
        self.assertEqual(r.status_code,200)
        self.assertEqual(r.json(),[])

    def test_p4_02_match_compativel(self):
        r_reset = requests.post('http://localhost:5003/reseta')
        self.assertEqual(r_reset.status_code,200)
        r = requests.get('http://localhost:5003/matches/9')
        self.assertEqual(r.status_code,404)
        maximus = {'nome':'maximus','id':9,'sexo':'homem','buscando':['homem','mulher']}
        r = requests.post('http://localhost:5003/pessoas',json=maximus)
        self.assertEqual(r.status_code,200)

        #maximus acabou de ser criado, nao tem matches
        r = requests.get('http://localhost:5003/matches/9')
        self.assertEqual(r.status_code,200)
        self.assertEqual(r.json(),[])
        
        #crio aurelia
        aurelia = {'nome':'aurelia','id':3,'sexo':'mulher','buscando':['mulher','homem']}
        r = requests.post('http://localhost:5003/pessoas',json=aurelia)
        self.assertEqual(r.status_code,200)

        #maximus está interessado em aurélia
        r = requests.put('http://localhost:5003/sinalizar_interesse/9/3/')
        self.assertEqual(r.status_code,200)
        r = requests.get('http://localhost:5003/matches/9')
        self.assertEqual(r.status_code,200)
        self.assertEqual(r.json(),[])

        #aurelia manifesta interesse em maximus
        r = requests.put('http://localhost:5003/sinalizar_interesse/3/9/')
        self.assertEqual(r.status_code,200)
        r = requests.get('http://localhost:5003/matches/9')
        self.assertEqual(r.status_code,200)
        self.assertEqual(r.json(),[3])


        





    

    


def runTests():
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestStringMethods)
        unittest.TextTestRunner(verbosity=2,failfast=True).run(suite)


if __name__ == '__main__':
    runTests()
