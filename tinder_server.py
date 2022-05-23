from flask import Flask, jsonify, request
import estrutura_interesses as i

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route("/")
def ola():
    return "servidor do tinder"

'''p1: controle de pessoas. 
Define as urls 
/pessoas, com GET, para pegar a lista de todas as pessoas
/pessoas, com POST, receber um dicionário de uma pessoa e colocar na lista
/pessoas/30, com GET, para pegar o dicionario da pessoa 30
/reseta, com POST, para esvaziar a lista de pessoas'''

#/pessoas, com GET, para pegar a lista de todas as pessoas
@app.route("/pessoas")
def pessoas():
    return jsonify(i.todas_as_pessoas())


#/pessoas, com POST, receber um dicionário de uma pessoa e colocar na lista
@app.route("/pessoas", methods=["POST"])
def coloca_na_lista():
    dic_recebido = request.json #representa um dicionario enviado pela rede
    i.adiciona_pessoa(dic_recebido)
    return "adicionado"

#/pessoas/30, com GET, para pegar o dicionario da pessoa 30
@app.route("/pessoas/<int:nPessoa>", methods=["GET"])
def encontra_pessoa_pelo_id(nPessoa):
    pessoa = i.localiza_pessoa(nPessoa)
    return pessoa

#/reseta, com POST, para esvaziar a lista de pessoas
@app.route("/reseta", methods=["POST"])
def reseta_pessoas():
    i.reseta()
    return "todas as pessoas removidas"
    
'''p2: interesses
    
    executar um PUT em /sinalizar_interesse/9/3/ significa que 9 está interessado(a) em 3
    executar DELETE em /sinalizar_interesse/9/3/ significa que 9 não tem interesse em 3
    executar um GET em /interesses/9 devolve uma lista de ids de pessoas, com as pessoas por quem 9 se interessa
    
    Detalhes: Lance um cod de status 404 quando uma das pessoas não existir
              Lembre-se do reseta tb para os interesses (mesma URL, mesmo verbo) -- Ou seja, acessar /reseta com verbo post também limpa a lista de interesses
'''

#executar um PUT em /sinalizar_interesse/9/3/ significa que 9 está interessado(a) em 3
@app.route("/sinalizar_interesse/<int:nInteressado>/<int:nAlvo>/", methods=["PUT"])
def sinaliza_interesse(nInteressado, nAlvo):
    try:
        i.adiciona_interesse(nInteressado, nAlvo)
        return "interesse adicionado"
    except:
        return {'erro':'não encontrado!'}, 404

#executar DELETE em /sinalizar_interesse/9/3/ significa que 9 não tem interesse em 3
@app.route("/sinalizar_interesse/<int:nInteressado>/<int:nAlvo>/", methods=["DELETE"])
def deleta_interesse(nInteressado, nAlvo):
    try:
        i.remove_interesse(nInteressado, nAlvo)
        return "interesse removido"
    except:
        return {'erro':'não encontrado!'}, 404


#executar um GET em /interesses/9 devolve uma lista de ids de pessoas, com as pessoas por quem 9 se interessa
@app.route("/interesses/<int:nPessoa>", methods=["GET"])
def ver_interesses(nPessoa):
    try:
        lista = i.consulta_interesses(nPessoa)
        return jsonify(lista)
    except:
        return {'erro':'não encontrado!'}, 404


if __name__ == '__main__':
    app.run(host='localhost', port=5003, debug=True)
