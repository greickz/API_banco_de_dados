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

class Pets(mybd.Model):
    __tablename__ = 'tb_pets'
    id_pet = mybd.Column(mybd.Integer, primary_key = True, auto_increment=True)
    nome = mybd.Column(mybd.String(100))
    tipo = mybd.Column(mybd.String(50))
    raca = mybd.Column(mybd.String(50))
    data_nascimento = mybd.Column(mybd.Date())
    id_cliente = mybd.Column(mybd.Integer, mybd.ForeignKey('tb_clientes.id_cliente'), nullable = False)
    idade = mybd.Column(mybd.Integer)


    def pets_to_json(self):
        return {
            "id_pet" : self.id_pet,
            "nome" : self.nome,
            "tipo" : self.tipo,
            "raca" : self.raca,
            "data_nascimento" : str(self.data_nascimento),
            "id_cliente" : self.id_cliente,   
            "idade" : self.idade         
        }

# Método 1: GET - O surgimento de uma lenda

@app.route('/frequentadores_do_estabelecimento', methods=['GET'])
def selecionar_clientes():
    cliente_slc = Clientes.query.all()
    cliente_json = [cliente.to_json()
                    for cliente in cliente_slc]
    return gera_resposta(200, "Clientes", cliente_json, "Selecionado com sucesso!!" )


# Método 1.2.5: GET - A jornada no reino dos Pets
@app.route('/seres_de_origem_animal', methods = ['GET'])
def selecionar_pets():
    pets_slc = Pets.query.all()
    pets_json = [pet.pets_to_json()
                 for pet in pets_slc]
    return gera_resposta(200, "Pets", pets_json, "Mais uma aventura concluida com sucesso e mais dinheiro no bolso do pai!!")


# Método 1.5: GET - O retorno pelos caminhos do ID

@app.route('/frequentadores_do_estabelecimento/<id_cliente>', methods = ['GET'])
def selecionar_clientes_ID(id_cliente):
    cliente_selecionado = Clientes.query.filter_by(id_cliente = id_cliente).first()
    cliente_json = cliente_selecionado.to_json()
    return gera_resposta(200, 'Cliente', cliente_json, "Filtrado com Sucesso!!")

# Método 1.5.5: GET - A continuação indireta do retorno pelos caminhos do ID

@app.route('/seres_de_origem_animal/<id_pet>', methods = ['GET'])
def selecionar_pets_ID(id_pet):
    pet_selecionado = Pets.query.filter_by(id_pet = id_pet).first()
    pet_json = pet_selecionado.pets_to_json()
    return gera_resposta(200, 'Pet', pet_json, "Oh não o GET se foi, o grande vilão DELETE deletou ele, agora podemos fazer mais 4 continuações por conta disso")


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



# Método 2.5: POST - O fardo de ser o sucessor de uma grande lenda

@app.route('/seres_de_origem_animal', methods = ['POST'])
def inserir_pet():
    requisicao = request.get_json()
    try:
        pet = Pets(
            id_pet = requisicao['id_pet'],
            nome = requisicao['nome'],
            tipo = requisicao['tipo'],
            raca = requisicao['raca'],
            data_nascimento = requisicao['data_nascimento'],
            id_cliente = requisicao['id_cliente'],
            idade = requisicao['idade']
        )

        mybd.session.add(pet)
        mybd.session.commit()
        return gera_resposta(201, 'Pet', pet.pets_to_json(), "Mais um sucesso de bilheteria rapazeada, os fãs não suspeitam sobre a quantidade de filmes assomrossos e suspeitos, tigrinho sltou a carta ")

    except Exception as e:
        print('ERRO')
        return gera_resposta(400, 'Pet', {}, 'Filme cancelado família, a grana acabou 😔')



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


# Método 3.5: DELETE - Só Deus sabe a mente do palhaço 🤡

@app.route('/seres_de_origem_animal/<id_pet>', methods = ['DELETE'])
def deletar_pet(id_pet):
    pet = Pets.query.filter_by(id_pet = id_pet).first()

    try:
        mybd.session.delete(pet)
        mybd.session.commit()
        return gera_resposta(200, 'Pet', pet.pets_to_json(), "Deu muito ruim família os fãs notaram que esta tendo muito filme com roteiro supostamente duvidosos e foi um fracasso de bilheteria parece que precisamos contratar um roterista denovo 😭")

    except Exception as e:
        print('ERRO')
        return gera_resposta(400, "Cliente", {}, "Erro ao deletar")

# Método 4: PUT -   A tentativa contra a falência

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
        return gera_resposta(200, 'Cliente', cliente.to_json(), "A favela venceu família resgatamo toda a fanbase e triplicamo a bilheteria, ainda deixamo brecha oara fazer um ultimo filmes alá Vingadores Ultimato ")
    
    except Exception as e:
        print('ERRO', e)
        return gera_resposta(400, "O filme teve que ser adiado e declaramos falência 😭", {}, "Erro ao atualizar")

# Método 4.5 - PUT: A batalha final, os fãs não aguentaram por esperar Dan, Dan Dan  

@app.route('/seres_de_origem_animal/<id_pet>', methods = ['PUT'])
def atualizacao_pet(id_pet):
    pet = Pets.query.filter_by(id_pet = id_pet).first()
    requisicao = request.get_json()

    try:
        if ('nome' in requisicao):
            pet.nome = requisicao['nome']
        if ('tipo' in requisicao):
            pet.tipo = requisicao['tipo']
        if ('raca' in requisicao):
            pet.raca = requisicao['raca']
        if ('data_nascimento' in requisicao):
            pet.data_nascimento = requisicao['data_nascimento']
        if ('id_cliente' in requisicao):
            pet.id_cliente = requisicao['id_cliente']
        if ('idade' in requisicao):
            pet.idade = requisicao['idade']

        mybd.session.add(pet)
        mybd.session.commit()
        return gera_resposta(200, 'Cliente', pet.pets_to_json(), "Fim de história depois da mais e sangrenta grandiosa batalha chamade de 'A batalha do Nexus' ao estar entre a vida e a morte os seus ancestrais, GET, POST aparecem em suas formas espirituais movidas pelo main.py codificam todas os seus poderes de python e abençoando o PUT assim ele utiliza de seus IF'S para o colocar em uma condição infinita e aprisiona o DELETE de uma vez por todas em sua própria arrogância. ✋ABSOLUTE CINEMA ✋")
    
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