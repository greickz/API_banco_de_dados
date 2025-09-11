# pip install flask_sqlalchemy
# permite a conexão da API com o banco de dados
# o Flask permite a criação de API com Python
# Response e Request = Requisição
# pip install mysqlclient
from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy # permite a conxao do sql com a biblioteca
import json
app = Flask('carros')
app.config
#Rastrear as modificações realizadas
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Configuração de conexão com o banco
# %40 -> faz o papel do @
# 1 - Usuário (root) - 2 Senha (Senai%40134) 3 -Localhost (127.0.0.1) 4- Nome do banco (db_carro)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Senai%40134@127.0.0.1/db_carro' # string de conexão do MYSQL = a conexão de um banco com a aplicação

mybd = SQLAlchemy(app) # armazena a conexão com o banco de dados

# Classe para definir o modelo dos dados que correspondem a tabela do banco de dados
class Carros(mybd.Model): # na classe a primeira letra tem que estar em maiusculo
    __tablename__ = 'tb_carro'
    id_carro = mybd.Column(mybd.Integer, primary_key=True)
    marca = mybd.Column(mybd.String(255))
    modelo = mybd.Column(mybd.String(255))
    ano = mybd.Column(mybd.String(255))
    valor = mybd.Column(mybd.String(255))
    cor = mybd.Column(mybd.String(255))
    numero_Vendas = mybd.Column(mybd.String(255))

# Esse método to_jon vai ser usado para converter o objeto em json
    def to_json(self):
        return {
            "id_carro": self.id_carro, # self permite aceesar as variaveis em qualquer parte do código
            "marca": self.marca,
            "modelo": self.modelo,
            "ano": self.ano,
            "valor": float(self.valor),
            "cor": self.cor,
            "numero_Vendas": self.numero_Vendas
        }

# ------------------------------------------------------------------
# MÉTODO 1 - GET
@app.route('/carros', methods = ['GET'])
def seleciona_carro():
    carro_selecionado = Carros.query.all() # Seleciona tudo e inseri em um template que ainda esta em linhas e colunas
    # Executa uma consulta no banco de dados (SELECT * FROM tb_carro)
    carro_json = [carro.to_json() # transforma o que esta em linhas e colunas e transforma em chave valor(JSON)
                  for carro in carro_selecionado]
    return  gera_resposta(200, "Lista de Carros", carro_json, 'Carros Retonardos') # status = 200 código https que deu tudo certo


# ---------------------------
# RESPOSTA PADRÃO
    # status (200.201)
    # nome do conteúdo
    # conteúdo
    # Mensagem (opcional)



# Metodo 2 - GET (Por ID)
@app.route('/carros/<id_carro_pam>', methods = ['GET'])
def seleciona_carro_id(id_carro_pam):
    carro_selecionado = Carros.query.filter_by(id_carro=id_carro_pam).first()
    carro_json = carro_selecionado.to_json() # se trata de um unico registro e não uma lista 
    return gera_resposta(200, "Carros",carro_json,'Carro encontrado!!')



# Metodo 3 - POST
@app.route('/carros', methods = ['POST'])
def criar_carro():
    requisicao = request.get_json()
    try:
        carro = Carros(
            id_carro = requisicao['id_carro'],
            marca = requisicao['marca'],
            modelo = requisicao['modelo'],
            ano = requisicao['ano'],
            valor = requisicao['valor'],
            cor = requisicao['cor'],
            numero_Vendas = requisicao['numero_Vendas']
        )

        mybd.session.add(carro) # adiciona o novo registro ao banco de dados
        mybd.session.commit() # salva

        return gera_resposta(201, "Carro",carro.to_json(), 'Criado com sucesso')
    
    except Exception as e:
        print('ERRO', e)
        return gera_resposta(400, "Carro",{}, 'Erro ao cadastrar!!')


# Metodo 4 - DELETE

@app.route('/carros/<id_carro_pam>', methods= ['DELETE'])
def deleta_carro(id_carro_pam):
    carro = Carros.query.filter_by(id_carro = id_carro_pam).first()

    try:
        mybd.session.delete(carro)
        mybd.session.commit()
        return gera_resposta(200, "Carro",carro.to_json(), "Deletado com sucesso!!")
    
    except Exception as e:
        print('ERRO', e)
        return gera_resposta(400, "Carro",{}, "Erro ao deletar!")



# Metodo 5 - PUT
@app.route("/carros/<id_carro_pam>", methods = ['PUT'])
def atualiza_carro(id_carro_pam):
    carro = Carros.query.filter_by(id_carro = id_carro_pam).first()
    requisicao = request.get_json()

    try:
        if ('marca' in requisicao):
            carro.marca = requisicao['marca']
        if ('modelo' in requisicao):
            carro.modelo = requisicao['modelo']
        if ('ano' in requisicao):
            carro.ano = requisicao['ano']        
        if ('valor' in requisicao):
            carro.valor = requisicao['valor']
        if ('cor' in requisicao):
            carro.cor = requisicao['cor']
        if ('numero_Vendas' in requisicao):
            carro.numero_Vendas = requisicao['numero_Vendas']

        mybd.session.add(carro)
        mybd.session.commit()
        return gera_resposta(200, "Carro",carro.to_json(), "Carro atualizado com sucesso")
    
    except Exception as e:
        print('ERRO', e)
        return gera_resposta(400, "Carro",{}, "Erro ao atualizar!!")


def gera_resposta(status, nome_do_conteudo, conteudo, mensagem=False): # mensagem=False = deixa a mensagem opcional
    body = {}
    body[nome_do_conteudo] = conteudo

    if(mensagem):
        body['mensagem'] = mensagem

    return Response(json.dumps(body), status=status, mimetype= 'application/json') # mimetype = tipo de resposta, Dumps - Converte o dicionário criado (body) em Json (json.dumps)

app.run(port=5000, host='localhost', debug=True)