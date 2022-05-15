import requests
import unittest
import estrutura_interesses as i

'''
p1: Controle de pessoas.

Para termos o tinder, precisamos primeiro de um controle de usuários

A idéia é mantermos uma lista como a seguinte

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

Assim, poderemos adicionar pessoas: i.adiciona_pessoa({'nome':'fernando','id':1})
Pegar a lista de todas as pessoas : i.todas_as_pessoas()
Consultar uma pessoa por id       : i.localiza_pessoa(1) (retorna o dicionario do fernando)

Tb queremos uma função reseta.    : i.reseta() faz a lista de pessoas ficar vazia

note que i equivale ao módulo estrutura_interesses.py

Um detalhe: uma consulta por id pode falhar. Talvez a id não exista.
Nesse caso, espero que você de um raise em um erro NotFoundError, definido
no arquivo estrutura_interesses.

Voce deve criar essa definição lá. Para isso, basta criar uma classe,
que herda de exception, e que nao faz nada (seu conteúdo é "pass")
'''

'''
    p2: interesses

    Vamos agora começar o tinder em si, permitindo a um(a) usuário(a) demonstrar interesse ("dar like")
    em outro usuário

    O plano é definir
    adiciona_interesse(id_interessado, id_alvo_de_interesse)
    
    Executar executar adiciona_interesse(9,3) significa que 9 está interessado(a) em 3

    a idéia é que temos o usuário de id 9 dizendo que tem interesse em conversar com o(a) usuário(a) de id 3.

    Como guardar os interesses?
    
    Eu fiz assim:
    
    database['interesses'] = {}
    colocar uma chave 3 pros interesses do 3, que vao ser uma lista de ids
    por exemplo
    database['interesses'][3]=[9,4,2]
    database['interesses'][2]=[9,3]

    O que isso quer dizer?
    3 se interessa por 9,4,2
    2, por 9 e 3.

    Quais as funções que tem que ser feitas pra essa parte?
    adiciona_interesse(id1,id2) : marca que 1 quer falar com 2
    consulta_interesses(id1)    : devolve a lista de todos os interesses de 1
    remove_interesse(id1,id2)   : marca que 1 não quer mais falar com 2

    Detalhes: 
    * Essas funções devem verificar se o usuário não é válido. Se for o caso,
    devem lançar a excessão NotFoundError
    * O reseta também deve funcionar para apagar os interesses
    '''

'''
    p3: Agora vamos fazer os matches

    usuarios tem uma lista de matches, 
    3 só é um match do 9 se 9 está interessado(a) em 3
    e 3 está interessado(a) em 9
    (3 aparece nos matches de 9 se 3 gosta de 9 e 9 gosta de 3)

    Relembrando a estrutura

    database['interesses'] = {}
    colocar uma chave 3 pros interesses do 3, que vao ser uma lista de ids
    por exemplo
    database['interesses'][3]=[9,4,2]
    database['interesses'][2]=[9,3]

    O que isso quer dizer?
    3 se interessa por 9,4,2
    2, por 9 e 3.

    Como o 3 gosta do 2 e o 2 gosta do 3, existe match entre 3 e 2

    Se eu consultar a lista de matches do 3, eu vou ver o 2 
    Se eu consultar a lista de matches do 2, eu vou ver o 3

    Que funções devo fazer?
    lista_matches(id_pessoa): lista os matches da pessoa
    
    Detalhes:
    * Remover um interesse pode "desligar" um match. A gostava de B, B gostava de A
    existia o match. B remove o interesse, nem A nem B tem match
    * Resetar ainda tem que funcionar
    * Buscar match de pessoa invalida ainda tem que dar raise na excessão NotFoundError
    '''

'''
    p4: compatibilidade
    o perfil do usuário (ou usuária) ganha duas caracteristicas novas
    o sexo e quais pessoas ele(a) está buscando
    por exemplo 
    maximus = {'nome':'maximus','id':9,'sexo':'homem','buscando':['mulher']}
    scipio  = {'nome':'scipio','id':10,'sexo':'homem','buscando':['mulher']}
    adiciona_interesse(9,10) => O adiciona interesse faz um raise exception

    Suponha que vou sinalizar interesse entre A e B.

    Se os dois perfis tem essas características (sexo e buscando) podemos verificar a compatibilidade

    Se você rodar adiciona_interesse(id1,id2) mas o buscando de 1 não for compativel com o sexo de 2
    a sua função deve dar raise em uma excessão do tipo IncompatibleError
    '''
    
class TestStringMethods(unittest.TestCase):


    def test_p1_00_pessoas_retorna_lista(self):
        res = i.todas_as_pessoas()
        self.assertEqual(type(res),type([]))


    def test_p1_01_adiciona_pessoas(self):
        i.reseta()
        #se ainda nao estiver funcionando, 
        #esse reseta acima, nao se preocupe
        #Esse teste nao precisa dele

        #crio fernando e roberto. Se houver algum Exception, abortará a execução
        # e você verá no teste
        
        i.adiciona_pessoa({'nome':'fernando','id':1})
        i.adiciona_pessoa({'nome':'roberto','id':2})
       
        lista_devolvida = i.todas_as_pessoas()

        #verifico se as duas pessoas criadas aparecem na lista
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

    def test_p1_02_pessoa_por_id(self):
        i.adiciona_pessoa({'nome':'mario','id':20})
        dicionario_pessoa = i.localiza_pessoa(20)
        self.assertEqual(type(dicionario_pessoa),type({}))
        self.assertEqual(dicionario_pessoa['nome'],'mario')


    #reseta faz o banco de pessoas e de interesses zerar, 
    #ficar vazio
    def test_p1_03_reseta(self):
        #crio um usuário
        i.adiciona_pessoa({'nome':'cicero','id':29})
        #pego a lista de todos os usuários
        lista = i.todas_as_pessoas()
        #essa lista tem que ter pelo menos 1 elemento, que eu 
        #acabei de criar
        self.assertTrue(len(lista) > 0)

        i.reseta()
        #agora a lista de usuários deve estar vazia
        lista_depois = i.todas_as_pessoas()
        self.assertEqual(len(lista_depois),0)


    def test_p1_04_pessoa_invalida(self):
        #começo com 0 usuários cadastrados
        i.reseta()

        #crio um usuário
        i.adiciona_pessoa({'nome':'cicero','id':29})

        #isso daqui nao pode dar erro
        dicionario_pessoa = i.localiza_pessoa(29)

        try:
            #isso daqui tem que dar erro
            dicionario_pessoa = i.localiza_pessoa(20) #ZZZ
            #e, portanto, a linha seguinte nao deve rodar. Se rodar, seu código não
            #deu o erro necessário, meu teste vai falar isso
            self.fail("uma Exception do tipo NotFoundError deveria ter ocorrido")
        except i.NotFoundError:
            #se a linha ZZZ deu o erro esperado, nao preciso fazer mais nada, você passou
            #no teste
            pass
        except:
            # a Excessão não foi a que eu queria
            self.fail("uma Exception do tipo NotFoundError deveria ter ocorrido, mas ocorreu alguma outra")
        
    '''
    Esse teste verifica se a chamada adiciona_interesse(id_interessado, id_alvo_de_interesse)
    dá erro quando pessoa_a ou pessoa_b nao existe
    voce nao precisa nem pensar ainda como salvar um interesse,
    só dê um erro se alguma das pessoas envolvidas nao existe
    '''
    def test_p2_00_interesse_com_pessoas_validas(self):
        #reseto
        i.reseta()
        
        #crio a pessoa 9
        i.adiciona_pessoa({'nome':'maximus','id':9})
        
        try:
            i.adiciona_interesse(9,3)
            #se chegar na linha de baixo, nao deu erro. Mas devia ter dado
            self.fail("adiciona interesse devia ter dado erro, mas nao deu. Pessoas ainda nao existem")
        except i.NotFoundError:
            #se der o erro NotFoundError, está tudo ok, nao preciso fazer nada
            pass
        except:
            # a Excessão não foi a que eu queria
            self.fail("uma Exception do tipo NotFoundError deveria ter ocorrido, mas ocorreu alguma outra")

        try:
            i.adiciona_interesse(3,9)
            self.fail("adiciona interesse devia ter dado erro, mas nao deu. Pessoas ainda nao existem")
        except i.NotFoundError:
            #se der o erro NotFoundError, está tudo ok, nao preciso fazer nada
            pass
        except:
            # a Excessão não foi a que eu queria
            self.fail("uma Exception do tipo NotFoundError deveria ter ocorrido, mas ocorreu alguma outra")


        
        #agora crio a pessoa 3
        i.adiciona_pessoa({'nome':'aurelia','id':3})
       
        #e consigo adicionar os interesses sem problemas
        i.adiciona_interesse(3,9)
        i.adiciona_interesse(9,3)
        #se desse pau nas funcoes acima, o teste te avisaria. Se nao avisou, deu tudo certo
       
        
    '''
    (a lista de interesse de A estará disponivel em
    i.consulta_interesses(id_interessado))
    '''
    def test_p2_01_consulta_interesse(self):
        #reseto
        i.reseta()

        
        #maximus acabou de ser criado, nao tem interesses
        i.adiciona_pessoa({'nome':'maximus','id':9})
        lista_interesses = i.consulta_interesses(9)
        self.assertEqual(lista_interesses,[])
        
        #crio aurelia
        i.adiciona_pessoa({'nome':'aurelia','id':3})
        
        #maximus está interessado em aurélia
        i.adiciona_interesse(9,3)
        lista_interesses_v2 = i.consulta_interesses(9)
        self.assertEqual(lista_interesses_v2,[3])

        #crio diana
        i.adiciona_pessoa({'nome':'diana','id':30})
        
        
        #maximus está interessado em diana
        #(veja na URL, estamos marcando interesse de 9 para 30)
        i.adiciona_interesse(9,30)
        lista_interesses_v3 = i.consulta_interesses(9)
        #maximus está interessado tanto em diana quanto em aurelia
        #3 aparece na lista
        self.assertIn(3,lista_interesses_v3)
        #30 tb aparece na lista
        self.assertIn(30,lista_interesses_v3)
        #tamanho da lista é 2
        self.assertEqual(len(lista_interesses_v3),2)
    
    def test_p2_02_resetar_afeta_interesses(self):
        #reseto
        i.reseta()

        
        #maximus acabou de ser criado, nao tem interesses
        i.adiciona_pessoa({'nome':'maximus','id':9})
        lista_interesses = i.consulta_interesses(9)
        self.assertEqual(lista_interesses,[])
        
        #crio aurelia
        i.adiciona_pessoa({'nome':'aurelia','id':3})
        
        #maximus está interessado em aurélia
        i.adiciona_interesse(9,3)
        lista_interesses_v2 = i.consulta_interesses(9)
        self.assertEqual(lista_interesses_v2,[3])
        
        #reseto
        i.reseta()
        
        #maximus acabou de ser criado, nao tem interesses
        i.adiciona_pessoa({'nome':'maximus','id':9})
        lista_interesses = i.consulta_interesses(9)
        self.assertEqual(lista_interesses,[])
        

    def test_p2_03_deletar_interesses(self):
        i.reseta()
        
        i.adiciona_pessoa({"nome":"vinicius", "id":30}) #30, vinicius
        l1 = i.consulta_interesses(30)
        #l1 tem que ser lista com 0 indices, lista vazia
        self.assertEqual(l1, [])
        
        i.adiciona_pessoa({"nome":"Toni Ramos", "id": 77})
        l2 = i.consulta_interesses(30)
        self.assertEqual(l2, [])
        #como vinicius deu like no toni ramos
        i.adiciona_interesse(30,77)
        l3 = i.consulta_interesses(30)
        #o toni ramos aparece na lista do vinicius
        self.assertEqual(l3, [77])
        #mas o vinicius nao aparece na lista do toni ramos
        l4 = i.consulta_interesses(77)
        self.assertEqual(l4, [])
    
        i.remove_interesse(30,77)
        l5 = i.consulta_interesses(30)
        #o toni ramos nao aparece na lista do vinicius
        self.assertEqual(l5, [])
        #o vinicius nao aparece na lista do toni ramos
        l6 = i.consulta_interesses(77)
        self.assertEqual(l6, [])

    def test_p3_00_verifica_match(self):
        #reseto
        i.reseta()

        #maximus acabou de ser criado, nao tem interesses
        i.adiciona_pessoa({'nome':'maximus','id':9})
        
        #crio aurelia
        i.adiciona_pessoa({'nome':'aurelia','id':3})
        
        #maximus está interessado em aurélia, mas ainda não é correspondido
        i.adiciona_interesse(9,3)
        self.assertFalse(i.verifica_match(9,3))
        
        #agora ele é correspondido por aurelia
        i.adiciona_interesse(3,9)
        self.assertTrue(i.verifica_match(9,3))
        

        #crio diana
        i.adiciona_pessoa({'nome':'diana','id':30})
        
        #maximus está interessado em diana, mas ainda não é correspondido
        i.adiciona_interesse(9,30)
        self.assertTrue(i.verifica_match(9,3))
        self.assertFalse(i.verifica_match(9,30))
        
        

        #agora é correspondido
        i.adiciona_interesse(30,9)
        self.assertTrue(i.verifica_match(9,3))
        self.assertTrue(i.verifica_match(9,30))
        self.assertTrue(i.verifica_match(30,9))
        self.assertTrue(i.verifica_match(3,9))


    #matches serao acessados em i.lista_matches(id_pessoa)
    def test_p3_01_match(self):
        #reseto
        i.reseta()

        #maximus acabou de ser criado, nao tem interesses
        i.adiciona_pessoa({'nome':'maximus','id':9})
        lista_interesses = i.consulta_interesses(9)
        self.assertEqual(lista_interesses,[])
        
        #crio aurelia
        i.adiciona_pessoa({'nome':'aurelia','id':3})
        
        #maximus está interessado em aurélia, mas ainda não é correspondido
        i.adiciona_interesse(9,3)
        lista_interesses2 = i.consulta_interesses(9)
        self.assertEqual(lista_interesses2,[3])
        lista_matches_v1 = i.lista_matches(9)
        self.assertEqual(lista_matches_v1,[])
        
        
        
        #agora ele é correspondido por aurelia
        i.adiciona_interesse(3,9)
        lista_matches_v2 = i.lista_matches(9) 
        self.assertEqual(lista_matches_v2,[3]) #agora sim aparece o match

        #crio diana
        i.adiciona_pessoa({'nome':'diana','id':30})
        
        #maximus está interessado em diana, mas ainda não é correspondido
        i.adiciona_interesse(9,30)
        lista_matches_v3 = i.lista_matches(9)
        self.assertEqual(lista_matches_v3,[3])

        #agora é correspondido
        i.adiciona_interesse(30,9)
        lista_matches_v4 = i.lista_matches(9)
        #agora maximus tem 2 matches. A ordem nao importa
        self.assertIn(3,lista_matches_v4) #id da aurelia
        self.assertIn(30,lista_matches_v4) #id da diana

        #aurélia também tem o match
        matchs_aurelia = i.lista_matches(3)
        self.assertEqual(matchs_aurelia,[9])

        #diana também tem o match
        matchs_diana = i.lista_matches(30)
        self.assertEqual(matchs_diana,[9])

    #consultar matches de uma pessoa que nao existe
    def test_p3_02_match_com_pessoas_invalidas(self):
        #reseto
        i.reseta()
        
        #nenhum usuario tem matches ainda, porque nao existe usuário
        try:
            m = i.lista_matches(9)
            #se chegar na linha de baixo, nao deu erro. Mas devia ter dado
            self.fail("matches(9) devia ter dado erro, mas nao deu.")
        except i.NotFoundError:
            #se der o erro NotFoundError, está tudo ok, nao preciso fazer nada
            pass

        #crio a pessoa de id 9
        i.adiciona_pessoa({'nome':'maximus','id':9})
        
        #agora nao da erro
        m = i.lista_matches(9)
        

        try:
            m = i.lista_matches(4)
            #se chegar na linha de baixo, nao deu erro. Mas devia ter dado
            self.fail("matches(4) devia ter dado erro, mas nao deu.")
        except i.NotFoundError:
            #se der o erro NotFoundError, está tudo ok, nao preciso fazer nada
            pass
        

    #remover um interesse (e o match, se existia um)

    # A gosta B
    # B gosta A -> match
    # B remove gostar A -> match desaparece
    #(mesmo que A ainda goste de B)

    #perceba, removi o interesse, nao o match
    #mas o match muda como consequencia
    
    def test_p3_03_match_perdido(self):
        #reseto
        i.reseta()
        
        #nenhum usuario tem matches ainda, porque nao existe usuário
        try:
            m = i.lista_matches(9)
            #se chegar na linha de baixo, nao deu erro. Mas devia ter dado
            self.fail("matches(9) devia ter dado erro, mas nao deu.")
        except i.NotFoundError:
            #se der o erro NotFoundError, está tudo ok, nao preciso fazer nada
            pass

        #crio a pessoa de id 9
        i.adiciona_pessoa({'nome':'maximus','id':9})
        
        #maximus acabou de ser criado, nao tem matches
        m = i.lista_matches(9)
        self.assertEqual(m,[])
        
        #crio aurelia
        i.adiciona_pessoa({'nome':'aurelia','id':3})
        
        #maximus está interessado em aurélia, mas ainda não é reciproco
        i.adiciona_interesse(9,3)
        m2 = i.lista_matches(9)
        self.assertEqual(m2,[])

        #aurélia tb tem interesse, a lista de matches de maximus contém ela
        i.adiciona_interesse(3,9)
        m3 = i.lista_matches(9)
        self.assertEqual(m3,[3])

        #aurélia perde o interesse, a lista de matches de maximus esvazia
        i.remove_interesse(3,9)
        m4 = i.lista_matches(9)
        self.assertEqual(m4,[])
        

    #o perfil do usuário (ou usuária) ganha duas caracteristicas novas
    #o sexo e quais pessoas ele(a) está buscando
    #maximus = {'nome':'maximus','id':9,'sexo':'homem','buscando':['mulher']}
    def test_p4_01_match_incompativel(self):
        i.reseta()
        maximus = {'nome':'maximus','id':9,'sexo':'homem','buscando':['mulher']}
        i.adiciona_pessoa(maximus)
        

        #maximus acabou de ser criado, nao tem matches
        m = i.lista_matches(9)
        self.assertEqual(m,[])
        
        #crio aurelia
        aurelia = {'nome':'aurelia','id':3,'sexo':'mulher','buscando':['mulher']}
        i.adiciona_pessoa(aurelia)
        
        #maximus está interessado em aurélia
        i.adiciona_interesse(9,3)
        m2 = i.lista_matches(9)
        self.assertEqual(m2,[])

        #aurelia manifesta interesse em maximus, mas isso é incompativel
        #com suas preferências anteriores
        try:
            i.adiciona_interesse(3,9)
            #se passar dessa linha sem dar erro, sua adiciona interesse nao verificou a compatibilidade
            self.fail("erro na verificacao de compatibilidade")
        except i.IncompatibleError:
            #esse erro é desejado, nao faço nada
            pass
        #esse erro ocorre quando A manifesta interesse em M, 
        #mas A declarou anteriormente que nao tem interesse 
        #em ninguém do sexo de M
        m3 = i.lista_matches(9)
        self.assertEqual(m3,[])

    def test_p4_02_match_compativel(self):
        i.reseta()
        maximus = {'nome':'maximus','id':9,'sexo':'homem','buscando':['mulher']}
        i.adiciona_pessoa(maximus)
        

        #maximus acabou de ser criado, nao tem matches
        m = i.lista_matches(9)
        self.assertEqual(m,[])
        
        #crio aurelia
        aurelia = {'nome':'aurelia','id':3,'sexo':'mulher','buscando':['mulher',"homem"]}
        i.adiciona_pessoa(aurelia)
        
        #maximus está interessado em aurélia
        i.adiciona_interesse(9,3)
        m2 = i.lista_matches(9)
        self.assertEqual(m2,[])

        #aurelia manifesta interesse em maximus
        i.adiciona_interesse(3,9)

        #eles sao compativeis, ocorre match
        m3 = i.lista_matches(9)
        self.assertEqual(m3,[3])
        print("ok")
        print("-------------------------------------------------------------------")
        print("-------------------------------------------------------------------")
        print("Você terminou de montar a estrutura! Agora, vamos montar o servidor")
        print("-------------------------------------------------------------------")
        print("-------------------------------------------------------------------")

        






#esse codigo nao te ajuda em nada, nem atrapalha
#está aqui para fins burocraticos, nao se preocupe
try:
    import estrutura_interesses_gabarito as i
except:
    pass    
try:
    import estrutura_interesses_gabarito_sql as i
except:
    pass

def runTests():
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestStringMethods)
        unittest.TextTestRunner(verbosity=2,failfast=True).run(suite)


if __name__ == '__main__':
    runTests()
