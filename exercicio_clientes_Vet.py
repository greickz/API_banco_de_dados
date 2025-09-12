from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
import json
app = Flask('carros')
app.config
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Senai%40134@127.0.0.1/db_clinicavetbd'
mybd = SQLAlchemy(app)
class Clientes(mybd.Model):
    __tablename__ = 'tb_clientes'
    id_cliente = mybd.Column(mybd.Integer, primary_key = True)
    nome = mybd.Column(mybd.String(100))
    endereco = mybd.Column(mybd.String(100))
    telefone = mybd.Column(mybd.String(50))

    def to_json(self):
        return {
            "id_cliente" : self.id_cliente,
            "nome" : self.nome,
            "endereco" : self.endereco,
            "telefone" : self.telefone
        }
    
# Método 1: GET - O surgimento de uma lenda

@app.route('/frequentadores_do_estabelecimento', methods=['GET'])
def selecionar_clientes():
    cliente_slc = Clientes.query.all()
    cliente_json = [cliente.to_json()
                    for cliente in cliente_slc]
    return gera_resposta(200, "Clientes", cliente_json, "Selecionado com sucesso!!" )

# Método 1.5: GET - O retorno pelos caminhos do ID

@app.route('/frequentadores_do_estabelecimento/<id_cliente>', methods = ['GET'])
def selecionar_clientes_ID(id_cliente):
    cliente_selecionado = Clientes.query.filter_by(id_cliente = id_cliente).first()
    cliente_json = cliente_selecionado.to_json()
    return gera_resposta(200, 'Cliente', cliente_json, "Filtrado com Sucesso!!")


# Método 2: POST - O sucessor de uma grande lenda

@app.route('/frequentadores_do_estabelecimento', methods =['POST'])
def inserir_cliente():
    requisicao = request.get_json()
    try:
        cliente = Clientes(
            id_cliente = requisicao['id_cliente'],
            nome = requisicao['nome'],
            endereco = requisicao['endereco'],
            telefone = requisicao['telefone']
        )

        mybd.session.add(cliente)
        mybd.session.commit()
        return gera_resposta(201, 'Cliente', cliente.to_json(), "Cliente adicionado com Sucesso!!")
    
    except Exception as e:
        print('ERRO')
        return gera_resposta(400, 'Cliente', {}, 'Erro ao cadastrar')



# Método 3: DELETE - A volta do inimigo, Mais forte do que nunca

@app.route('/frequentadores_do_estabelecimento/<id_cliente>', methods = ['DELETE'])
def deletar_cliente(id_cliente):
    cliente = Clientes.query.filter_by(id_cliente = id_cliente).first()

    try:
        mybd.session.delete(cliente)
        mybd.session.commit()
        return gera_resposta(200, 'Cliente', cliente.to_json(), "Deletado com sucesso, O mal venceu neste filme então será necessário mais uma continuação")

    except Exception as e:
        print('ERRO', e)
        return gera_resposta(400, "Cliente", {}, "Erro ao deletar")




# Método 4: PUT - A batalha final, os fãs não aguentaram por esperar Dan, Dan Dan    

@app.route('/frequentadores_do_estabelecimento/<id_cliente>', methods = ['PUT'])
def atualizacao_cliente(id_cliente):
    cliente = Clientes.query.filter_by(id_cliente = id_cliente).first()
    requisicao = request.get_json()

    try:
        if ('nome' in requisicao):
            cliente.nome = requisicao['nome']
        if ('endereco' in requisicao):
            cliente.endereco = requisicao['endereco']
        if ('telefone' in requisicao):
            cliente.telefone = requisicao['telefone']

        mybd.session.add(cliente)
        mybd.session.commit()
        return gera_resposta(200, 'Cliente', cliente.to_json(), "Fim de história depois da mais e sangrenta grandiosa batalha chamade de 'A batalha do Nexus' ao estar entre a vida e a morte os seus ancestrais, GET, POST aparecem em suas formas espirituais movidas pelo main.py codificam todas os seus poderes de python e abençoando o PUT assim ele utiliza de seus IF'S para o colocar em uma condição infinita e aprisiona o DELETE de uma vez por todas em sua própria arrogância. ✋ABSOLUTE CINEMA ✋")
    
    except Exception as e:
        print('ERRO', e)
        return gera_resposta(400, "O filme teve que ser adiado", {}, "Erro ao atualizar")





def gera_resposta(status, nome_do_conteudo, conteudo, mensagem=False):
    body = {}
    body[nome_do_conteudo] = conteudo
    if(mensagem):
        body['mensagem'] = mensagem
    return Response(json.dumps(body), status=status, mimetype= 'application/json') 

app.run(port=5000, host='localhost', debug= True)