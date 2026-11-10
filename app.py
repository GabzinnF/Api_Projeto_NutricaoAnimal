
import datetime
import random
import string
from flask import Flask, jsonify, request, render_template, url_for
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, JWTManager
from flask_login import login_manager
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from models import db_session, Insumos, Galpoes , Blocos , Sensores, Setores , Leituras , AlertaOcorrencias, Usuarios # Certifique-se que o database.py está na mesma pasta

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from models import (db_session, Usuarios, Insumos, Galpoes, Blocos, Setores, Sensores, Leituras, AlertaOcorrencias)

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'batata'
jwt = JWTManager(app)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

#
# @login_manager.user_loader
# def load_user(user_id):
#     user = select(Usuarios).where(Usuarios.id_usuario == int(user_id))
#     resultado = db_session.execute(user).scalar_one_or_none()
#     return resultado
@app.route('/')
def home():
    return jsonify({"status": "API de Monitoramento de Nutrição Animal Ativa"}), 200


@app.route('/cadastro_usuario', methods=['POST'])
def cadastro_usuario():
    dados = request.get_json()
    nome = dados.get('nome')
    email = dados.get('email')
    cpf = dados.get('cpf')
    senha = dados.get('senha')

    if not nome or not email or not cpf or not senha:
        return jsonify({"msg": "Preencha todos os campos"}), 400

    try:
        if len(cpf) != 11: #Essa linha peguei da IA
            return jsonify({"msg": "CPF inválido"}), 400

        verifica_email = select(Usuarios).where(Usuarios.email == email)

        verifica_cpf = select(Usuarios).where(Usuarios.cpf == cpf)

        if db_session.execute(verifica_email).scalar_one_or_none():
            return jsonify({"msg": "E-mail já cadastrado"}), 409

        if db_session.execute(verifica_cpf).scalar_one_or_none():
            return jsonify({"msg": "CPF já cadastrado"}), 409

        novo_usuario = Usuarios(nome=nome, email=email, cpf=cpf)

        novo_usuario.set_password(senha)

        db_session.add(novo_usuario)
        db_session.commit()

        return jsonify({
            "msg": "Usuário cadastrado com sucesso",
            "usuario": novo_usuario.serialize()
        }), 201

        # print(f"SENHA ORIGINAL (LIMPA): {senha}")
        # print(f"SENHA TRANSFORMA EM HASH: {novo_usuario.senha}")
        # #esses print peguei da IA

    except Exception as e:
        db_session.rollback()
        return jsonify({"msg": str(e)}), 500



@app.route('/api/login', methods=['POST'])
def login():
    dados = request.get_json()
    email = dados.get('email')
    senha = dados.get('senha')

    print("EMAIL RECEBIDO:", email)
    print("SENHA RECEBIDA:", "SIM" if senha else "NÃO")

    if not email or not senha:
        return jsonify({
            "msg": "Preencha todos os campos"
        }), 400

    try:
        consulta = select(Usuarios).where(Usuarios.email == email)

        usuario = db_session.execute(consulta).scalar_one_or_none()

        if usuario and usuario.check_password_hash(senha):

            token = create_access_token(identity=str(usuario.id_usuario))

            return jsonify({
                "msg": "Login realizado com sucesso",
                "access_token": token,
                "usuario": usuario.serialize()
            }), 200

        return jsonify({
            "msg": "E-mail ou senha incorretos"
        }), 401

    except Exception as e:
        print("ERRO NO LOGIN:", str(e))

        return jsonify({
            "msg": "Erro interno ao realizar login"
        }), 500

@app.route('/api/cadastrar_galpoes', methods=['POST'])
def criar_galpao():

    dados = request.get_json(silent=True) or {}

    nome = dados.get('nome')
    descricao = dados.get('descricao')

    if not nome or not descricao:
        return jsonify({"msg": "Preencha todos os campos"}), 400

    try:
        novo_galpao = Galpoes(nome=nome, descricao=descricao)

        db_session.add(novo_galpao)
        db_session.commit()

        return jsonify({
            "msg": "Galpão cadastrado com sucesso",
            "galpao": novo_galpao.serialize()
        }), 201

    except Exception as e:
        db_session.rollback()
        return jsonify({"msg": str(e)}), 500

@app.route('/api/cadastrar_blocos', methods=['POST'])
def criar_bloco():
    dados = request.get_json()
    nome = dados.get('nome')
    id_galpao = dados.get('id_galpao')

    if not nome or id_galpao is None:
        return jsonify({"msg": "Preencha todos os campos"}), 400

    try:
        novo_bloco = Blocos(nome=nome, id_galpao=id_galpao)

        db_session.add(novo_bloco)
        db_session.commit()

        return jsonify({
            "msg": "Bloco cadastrado com sucesso",
            "bloco": novo_bloco.serialize()
        }), 201

    except Exception as e:
        db_session.rollback()
        return jsonify({"msg": str(e)}), 500

@app.route('/api/cadastrar_setores', methods=['POST'])
def criar_setor():
    dados = request.get_json()
    nome = dados.get('nome')
    id_insumo = dados.get('id_insumo')
    id_bloco = dados.get('id_bloco')
    capacidade = dados.get('capacidade')

    if (
        not nome or id_insumo is None or
        id_bloco is None or capacidade is None
    ):
        return jsonify({"msg": "Preencha todos os campos"}), 400

    try:
        novo_setor = Setores(nome=nome, id_insumo=id_insumo, id_bloco=id_bloco, capacidade=capacidade)

        db_session.add(novo_setor)
        db_session.commit()

        return jsonify({
            "msg": "Setor cadastrado com sucesso",
            "setor": novo_setor.serialize()
        }), 201

    except Exception as e:
        db_session.rollback()
        return jsonify({"msg": str(e)}), 500

@app.route('/api/cadastrar_insumos', methods=['POST'])
def criar_insumo():
    dados = request.get_json()
    nome = dados.get('nome')
    tipo = dados.get('tipo')
    umidade_max = dados.get('umidade_max')
    umidade_min = dados.get('umidade_min')
    temperatura_max = dados.get('temperatura_max')
    temperatura_min = dados.get('temperatura_min')
    quantidade = dados.get('quantidade')
    unidade_medida = dados.get('unidade_medida')

    if (
        not nome or not tipo or
        umidade_max is None or umidade_min is None or
        temperatura_max is None or temperatura_min is None or
        quantidade is None or not unidade_medida
    ):
        #Fiz essa linha anterior com ajuda da IA
        return jsonify({"msg": "Preencha todos os campos"}), 400

    try:
        novo_insumo = Insumos(nome=nome, tipo=tipo, umidade_max=umidade_max, umidade_min=umidade_min, temperatura_max=temperatura_max, temperatura_min=temperatura_min, quantidade=quantidade, unidade_medida=unidade_medida)

        db_session.add(novo_insumo)
        db_session.commit()

        return jsonify({
            "msg": "Insumo cadastrado com sucesso",
            "insumo": novo_insumo.serialize()
        }), 201

    except Exception as e:
        db_session.rollback()
        return jsonify({"msg": str(e)}), 500

@app.route('/api/cadastrar_sensores', methods=['POST'])
def criar_sensor():
    dados = request.get_json()
    id_setor = dados.get('id_setor')

    if id_setor is None:
        return jsonify({"msg": "Informe o setor"}), 400

    try:
        novo_sensor = Sensores(id_setor=id_setor)

        db_session.add(novo_sensor)
        db_session.commit()

        return jsonify({
            "msg": "Sensor cadastrado com sucesso",
            "sensor": novo_sensor.serialize()
        }), 201

    except Exception as e:
        db_session.rollback()
        return jsonify({"msg": str(e)}), 500

@app.route('/api/cadastrar_leituras', methods=['POST'])
def criar_leitura():
    dados = request.get_json()
    id_sensor = dados.get('id_sensor')
    temperatura = dados.get('valor_leitura_temperatura')
    umidade = dados.get('valor_leitura_umidade')

    if (
        id_sensor is None or
        temperatura is None or
        umidade is None
    ):
        return jsonify({"msg": "Preencha todos os campos"}), 400

    try:
        nova_leitura = Leituras(id_sensor=id_sensor, valor_leitura_temperatura=temperatura, valor_leitura_umidade=umidade)

        db_session.add(nova_leitura)
        db_session.commit()

        return jsonify({
            "msg": "Leitura cadastrada com sucesso",
            "leitura": nova_leitura.serialize()
        }), 201

    except Exception as e:
        db_session.rollback()
        return jsonify({"msg": str(e)}), 500

def listar(modelo, nome_chave):
    try:
        consulta = select(modelo)
        resultado = db_session.execute(consulta).scalars().all()

        dados = []

        for item in resultado:
            dados.append(item.serialize())

        return jsonify({nome_chave: dados}), 200

    except Exception as e:
        return jsonify({"msg": str(e)}), 500

@app.route('/todos_galpoes')
def listar_galpoes():
    return listar(Galpoes, "Galpoes")


# @app.route('/verificar_email',methods=['POST'])
# def verificar_email():
#     db = db_session()
#     try:
#         json_funcionario_email = request.get_json()
#         email = json_funcionario_email.get('email')
#         verifica_email = select(Usuarios).where(Usuarios.email == email)
#         existe_email = db.execute(verifica_email).scalar_one_or_none()
#         print(email)
#         if existe_email:
#             return jsonify({"funcionario":existe_email.serialize()}), 200
#
#         else:
#
#             return jsonify({"msg": "Email não existe"}), 400
#
#     except SQLAlchemyError as e:
#         return jsonify({"msg": f"Erro na base de dados ao logar funcionario: {str(e)}"})
#     except Exception as e:
#         return jsonify({"msg": f"Erro ao logar funcionario: {str(e)}"}), 500



@app.route('/todos_blocos')
def listar_blocos():
    return listar(Blocos, "Blocos")

@app.route('/todos_setores')
def listar_setores():
    return listar(Setores, "Setores")

@app.route('/todos_insumos')
def listar_insumos():
    return listar(Insumos, "Insumos")

@app.route('/todos_sensores')
def listar_sensores():
    return listar(Sensores, "Sensores")

@app.route('/todas_leituras')
def listar_leituras():
    return listar(Leituras, "Leitura")

@app.route('/todos_usuarios')
def listar_usuarios():
    return listar(Usuarios, "Usuario")

@app.route('/todos_alertas')
def listar_alertas():
    return listar(AlertaOcorrencias, "Alerta")


# @app.route('/api/alertas_ocorrencias', methods=['GET'])
# def alerta_ocorrencias():
#     db = db_session()
#     dados = request.get_json()
#     try:
#         if request.method == 'GET':
#             json_setor = request.get_json()
#             nome = json_setor.get('nome')
#             id_galpao = json_setor.get('ID Galpao')
#             id_insumo = json_setor.get('ID Insumo')
#             id_bloco = json_setor.get('ID Bloco')
#
#             if not nome or not id_galpao or not id_insumo or not id_bloco:
#                 return jsonify({"msg": "Preencher todos os campos"})
#
#             novo_setor = Blocos(
#                 nome=nome)
#             db.add(novo_setor)
#             db.commit()
#             return jsonify({
#                 "msg": "Bloco criado com sucesso",
#                 'bloco': {
#                     "id": novo_setor.id,
#                     'nome': novo_setor.nome,
#                     'id_galpao': novo_setor.id_galpoes,
#                     'id_insumo': novo_setor.id_insumos,
#                     'id_bloco' : novo_setor.id_blocos
#                 }
#
#             }), 201
#
#     except Exception as e:
#         db.rollback()
#         return jsonify({"Erro": str(e)}), 500
#
#     return jsonify(dados)


@app.route('/verificar_email', methods=['POST'])
def verificar_email():
    dados = request.get_json()
    email = dados.get('email')

    if not email:
        return jsonify({"msg": "Informe o e-mail"}), 400

    consulta = select(Usuarios).where(Usuarios.email == email)

    usuario = db_session.execute(consulta).scalar_one_or_none()

    if usuario:
        return jsonify({
            "Usuario": usuario.serialize()
        }), 200

    return jsonify({
        "msg": "E-mail não encontrado"
    }), 404

@app.route('/api/dados_protegidos')
@jwt_required()
def protegido():
    usuario_atual = get_jwt_identity()

    return jsonify({
        "msg": "Acesso autorizado",
        "usuario": usuario_atual
    }), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
