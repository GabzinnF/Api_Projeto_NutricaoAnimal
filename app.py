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

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'batata'
jwt = JWTManager(app)


# @app.teardown_appcontext
# def shutdown_session(exception=None):
#     db_session.remove()
#
# @login_manager.user_loader
# def load_user(user_id):
#     user = select(Usuarios).where(Usuarios.id_usuario == int(user_id))
#     resultado = db_session.execute(user).scalar_one_or_none()
#     return resultado
@app.route('/')
def home():
    return jsonify({"status": "API de Monitoramento de Nutrição Animal Ativa"}), 200


@app.route('/login')
def tela_login():
    return render_template('login.html')


@app.route('/cadastro')
def tela_cadastro():
    return render_template('cadastro.html')

@app.route('/cadastro_usuario', methods=['POST', 'GET'])
def cadastro_usuario():
    dados = request.get_json()
    nome = dados.get('nome')
    email = dados.get('email')
    cpf = dados.get('cpf')
    senha =  dados.get('senha')
    print(dados)

    if not nome or not email or not cpf or not senha:
        return jsonify({"msg": "Preencha todos os campos"}), 400

    try:
        # Verifica se email já existe
        if not nome or not email or not senha or not cpf:
            return jsonify({"msg": "Preencher todos os campos"})

        user_check = select(Usuarios).where(Usuarios.nome == nome, Usuarios.email == email)
        usuario_existente = db_session.execute(user_check).scalar()

        if usuario_existente:
            dados = {"msg" : "Usuario ja existente"}
            return jsonify(dados), 409

        novo_usuario = Usuarios(nome=nome, email=email, cpf=cpf)
        # Método que deve estar no database.py
        novo_usuario.set_password(senha) #essa linha peguei da IA

        # print(f"SENHA ORIGINAL (LIMPA): {senha}")
        # print(f"SENHA TRANSFORMA EM HASH: {novo_usuario.senha}")
        # #esses print peguei da IA

        db_session.add(novo_usuario)
        db_session.commit()
        return jsonify({
            "msg": "Usuario criado com sucesso",
            'usuario': {
                "id": novo_usuario.id_usuario,
                'nome': novo_usuario.nome,
                'email': novo_usuario.email,
                'cpf': novo_usuario.cpf,
            }

        }), 201
    except Exception as e:
        db_session.rollback()
        return jsonify({"msg": str(e)}), 500
    finally:
        db_session.close()

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

@app.route('/api/cadastrar_galpoes', methods=['POST'])
def criar_galpao():
    db = db_session()
    dados = request.get_json()
    try:
        if request.method == 'POST':
            json_galpao = request.get_json()
            nome = json_galpao.get('nome')
            descricao = json_galpao.get('descricao')

            if not nome or not descricao    :
                return jsonify({"msg": "Preencher todos os campos"})

            novo_galpao = Galpoes(
                nome=nome, descricao=descricao)
            db.add(novo_galpao)
            db.commit()
            return jsonify({
                "msg": "Galpão criado com sucesso",
                'galpao': {
                    "id": novo_galpao.id,
                    'nome': novo_galpao.nome,
                    'descricao': novo_galpao.descricao,
                }

            }), 201

    except Exception as e:
        db.rollback()
        return jsonify({"Erro": str(e)}), 500

    return jsonify(dados)


@app.route('/api/cadastrar_blocos', methods=['POST'])
def criar_bloco():
    db = db_session()
    dados = request.get_json()
    print(dados)
    try:
        if request.method == 'POST':
            json_bloco = request.get_json()
            nome = json_bloco.get('nome')
            id_galpao = json_bloco.get('id_galpao')
            print(nome)
            print(id_galpao)
            if not nome or not id_galpao:
                return jsonify({"msg": "Preencher todos os campos"})

            novo_bloco = Blocos(
                nome=nome, id_galpao=id_galpao)
            db.add(novo_bloco)
            db.commit()
            return jsonify({
                "msg": "Bloco criado com sucesso",
                'bloco': {
                    "id": novo_bloco.id_bloco,
                    'nome': novo_bloco.nome,
                    'id_galpao': novo_bloco.id_galpao,
                }

            }), 201

    except Exception as e:
        db.rollback()
        return jsonify({"Erro": str(e)}), 500

    return jsonify(dados)


@app.route('/api/cadastrar_setores', methods=['POST'])
def criar_setores():
    db = db_session()
    dados = request.get_json()
    print(dados)
    try:
        if request.method == 'POST':
            json_setor = request.get_json()
            nome = json_setor.get('nome')
            id_insumo = json_setor.get('id_insumo')
            id_bloco = json_setor.get('id_bloco')
            capacidade = json_setor.get('capacidade')

            if not nome or not id_insumo or not id_bloco or not capacidade:
                return jsonify({"msg": "Preencher todos os campos"})

            novo_setor = Setores(
                nome=nome,id_bloco=id_bloco, id_insumo=id_insumo, capacidade=capacidade)
            db.add(novo_setor)
            db.commit()
            return jsonify({
                "msg": "Setor criado com sucesso",
                'setor': {
                    "id_setor": novo_setor.id_setor,
                    'nome': novo_setor.nome,
                    'id_insumo': novo_setor.id_insumo,
                    'capacidade' : novo_setor.capacidade

                }

            }), 201

    except Exception as e:
        db.rollback()
        return jsonify({"Erro": str(e)}), 500

    return jsonify(dados)


@app.route('/api/cadastrar_insumos', methods=['POST'])
def criar_insumos():
    db = db_session()
    dados = request.get_json()
    print(dados)
    try:
        if request.method == 'POST':
            json_insumo = request.get_json()
            nome = json_insumo.get('nome')
            tipo = json_insumo.get('tipo')
            umidade_max = json_insumo.get('umidade_max')
            umidade_min = json_insumo.get('umidade_min')
            temperatura_max = json_insumo.get('temperatura_max')
            temperatura_min = json_insumo.get('temperatura_min')
            quantidade = json_insumo.get('quantidade')
            unidade_medida= json_insumo.get('unidade_medida')
            # print(nome)
            # print(tipo)
            # print(umidade_max,"ddd")
            # print(umidade_min)
            # print(umidade_atual)
            # print(temperatura_max)
            # print(temperatura_min)
            # print(temperatura_atual)
            if (not nome or not tipo or not umidade_max or not umidade_min or not temperatura_max or not temperatura_min
                    or not quantidade or not unidade_medida):
                return jsonify({"msg": "Preencher todos os campos"})

            novo_insumo = Insumos(
                nome=nome , tipo=tipo, umidade_max=umidade_max, umidade_min=umidade_min, temperatura_max=temperatura_max,
                temperatura_min=temperatura_min, quantidade=quantidade, unidade_medida=unidade_medida)
            db.add(novo_insumo)
            db.commit()
            return jsonify({
                "msg": "Insumo cadastrado com sucesso",
                'insumo': {
                    "id": novo_insumo.id_insumo,
                    'nome': novo_insumo.nome,
                    'tipo' : novo_insumo.tipo,
                    'umidade_max' : novo_insumo.umidade_max,
                    'umidade_min' : novo_insumo.umidade_min,
                    'temperatura_max' : novo_insumo.temperatura_max,
                    'temperatura_min' : novo_insumo.temperatura_min,
                    'quantidade' : novo_insumo.quantidade,
                    'unidade_medida' : novo_insumo.unidade_medida
                }

            }), 201

    except Exception as e:
        db.rollback()
        return jsonify({"Erro": str(e)}), 500

    return jsonify(dados)

@app.route('/api/cadastrar_leitura', methods=['POST'])
def criar_leitura():
    db = db_session()
    dados = request.get_json()
    try:
        if request.method == 'POST':

            json_leitura= request.get_json()
            id_sensor = json_leitura.get('id_sensor')
            valor_leitura_umidade = json_leitura.get('valor_leitura_umidade')
            valor_leitura_temperatura = json_leitura.get('valor_leitura_temperatura')
            data_hora = datetime.now()

            if not id_sensor or not valor_leitura_temperatura or not valor_leitura_umidade :
                return jsonify({"msg": "Preencher todos os campos"})

            nova_leitura = (Leituras
                (
                valor_leitura_temperatura=valor_leitura_temperatura,valor_leitura_umidade=valor_leitura_umidade, id_sensor=id_sensor, data_hora=data_hora))
            db.add(nova_leitura)
            db.commit()
            return jsonify({

                "msg": "Leitura criado com sucesso",
                'leitura': {
                    'id' : nova_leitura.id_leitura,
                    'id_sensor' : nova_leitura.id_sensor,
                    'valor_leitura_temperatura' : nova_leitura.valor_leitura_temperatura,
                    'valor_leitura_umidade' : nova_leitura.valor_leitura_umidade,
                    'data_hora' : nova_leitura.data_hora
                }

            }), 201

    except Exception as e:
        db.rollback()
        return jsonify({"Erro": str(e)}), 500

    return jsonify(dados)

@app.route('/api/cadastrar_sensores', methods=['POST'])
def criar_sensores():
    db = db_session()
    dados = request.get_json()
    print(dados)
    try:
        if request.method == 'POST':
            json_sensor = request.get_json()
            id_setor = json_sensor.get('id_setor')

            if not id_setor :
                return jsonify({"msg": "Preencher todos os campos"})

            novo_sensor = Sensores(
                id_setor=id_setor)
            db.add(novo_sensor)
            db.commit()
            return jsonify({
                "msg": "Sensor cadastrado com sucesso",
                'sensor': {
                    "id_sensor": novo_sensor.id_sensor,
                    'id_setor' : novo_sensor.id_setor,

                }

            }), 201

    except Exception as e:
        db.rollback()
        return jsonify({"Erro": str(e)}), 500

    return jsonify(dados)

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
@app.route('/todos_galpoes')
def listar_galpoes():
    # Rota que estava faltando e causava o BuildError
    db = db_session()
    try:
        api_galpoes = select(Galpoes)
        result = db_session.execute(api_galpoes).scalars().all()
        galpoes = []
        for galpao in result:
            galpoes.append(galpao.serialize())
        print(result)
        return jsonify({"Galpoes": galpoes}), 200
    finally:
        db.close()


@app.route('/todos_blocos')
def listar_blocos():
    db = db_session()
    try:
        api_bloco = select(Blocos)
        result = db_session.execute(api_bloco).scalars().all()
        blocos = []
        for bloco in result:
            blocos.append(bloco.serialize())
        print(result)
        return jsonify({"Blocos": blocos}), 200
    finally:
        db.close()


@app.route('/todos_setores')
def listar_setores():
    # Rota que estava faltando e causava o BuildError
    db = db_session()
    try:
        api_setor = select(Setores)
        result = db_session.execute(api_setor).scalars().all()
        setores = []
        for setor in result:
            setores.append(setor.serialize())
        print(result)
        return jsonify({"Setores": setores}), 200
    finally:
        db.close()

@app.route('/todos_insumos')
def listar_insumos():
    # Rota que estava faltando e causava o BuildError
    db = db_session()
    try:
        api_insumo = select(Insumos)
        result = db_session.execute(api_insumo).scalars().all()
        insumos = []
        for insumo in result:
            insumos.append(insumo.serialize())
        print(result)
        return jsonify({"Insumos": insumos}), 200
    finally:
        db.close()


@app.route('/todos_sensores')
def listar_sensores():
    # Rota que estava faltando e causava o BuildError
    db = db_session()
    try:
        api_sensor = select(Sensores)
        result = db_session.execute(api_sensor).scalars().all()
        sensores = []
        for sensor in result:
            sensores.append(sensor.serialize())
        print(result)
        return jsonify({"Sensores": sensores}), 200
    finally:
        db.close()


@app.route('/todas_leituras')
def listar_leituras():
    # Rota que estava faltando e causava o BuildError
    db = db_session()
    try:
        api_leitura = select(Leituras)
        result = db_session.execute(api_leitura).scalars().all()
        leituras = []
        for leitura in result:
            leituras.append(leitura.serialize())
        print(result)
        return jsonify({"Leitura": leituras}), 200
    finally:
        db.close()


@app.route('/todos_usuarios')
def listar_usuarios():
    # Rota que estava faltando e causava o BuildError
    db = db_session()
    try:
        api_usuario = select(Usuarios)
        result = db_session.execute(api_usuario).scalars().all()

        usuarios = []
        for usuario in result:
            usuarios.append(usuario.serialize())
        print(usuarios)
        return jsonify({"Usuario": usuarios}), 200
    finally:
        db.close()

@app.route('/todos_alertas')
def listar_alertas():
    # Rota que estava faltando e causava o BuildError
    db = db_session()
    try:
        api_alerta = select(AlertaOcorrencias)
        result = db_session.execute(api_alerta).scalars().all()
        alertas = []
        for alerta in result:
            alertas.append(alerta.serialize())
        print(result)
        return jsonify({"Alerta": alertas}), 200
    finally:
        db.close()

@app.route('/api/login', methods=['POST'])
def login():
    if request.method == 'POST':
        try:
            dados = request.get_json()
            email = dados.get('email')
            senha = dados.get('senha')

            db = db_session()
            sql = select(Usuarios).where(Usuarios.email == email)
            usuario = db.execute(sql).scalar()

            print(usuario)

            # Importante: No database.py, a classe Usuario precisa do metodo check_password_hash
            if usuario and usuario.check_password_hash(senha):
                access_token = create_access_token(identity=str(usuario.email))
                texto = "Login realizado com sucesso"
                return jsonify({
                    "Sistema": texto,

                    "Bem Vindo": usuario.nome,

                }), 200

            return jsonify({"msg": "E-mail ou senha incorretos"}), 401
        except Exception as e:
            print(f'error {e}')
            return jsonify({"msg": str(e)}), 500
        finally:
            db_session.close()



@app.route('/verificar_email',methods=['POST'])
def verificar_email():
    db = db_session()
    try:
        json_usuario_email = request.get_json()
        email = json_usuario_email.get('email')
        verifica_email = select(Usuarios).where(Usuarios.email == email)
        existe_email = db.execute(verifica_email).scalar_one_or_none()
        print(email)
        if existe_email:
            return jsonify({"Usuarios":existe_email.serialize()}), 200

        else:

            return jsonify({"msg": "Email não existe"}), 400

    except SQLAlchemyError as e:
        return jsonify({"msg": f"Erro na base de dados ao logar Usuario: {str(e)}"})
    except Exception as e:
        return jsonify({"msg": f"Erro ao logar Usuario: {str(e)}"}), 500



# @app.route('/funcionario', methods=['POST'])
# def cadastro_funcionario():
#     db = db_session()
#     dados = request.get_json()
#     try:
#         if request.method == 'POST':
#             json_funcionario = request.get_json()
#             nome = json_funcionario.get('nome')
#             cpf = json_funcionario.get('cpf')
#             email = json_funcionario.get('email')
#             senha = json_funcionario.get('senha')
#
#             # data_convertida = datetime.strptime(data_nascimento, '%Y-%m-%d')
#             # data_brasil = datetime.strftime(data_convertida, '%d-%m-%Y')
#
#             if not nome or not email or not senha or not cpf:
#                 return jsonify({"msg": "Preencher todos os campos"})
#             verifica_email = select(Usuarios).where(Usuarios.email == email)
#             verifica_cpf = select(Usuarios).where(Usuarios.cpf == cpf)
#             existe_email = db.execute(verifica_email, ).scalar_one_or_none()
#             existe_cpf = db.execute(verifica_cpf, ).scalar_one_or_none()
#             if existe_email:
#                 return jsonify({"msg": "Email ja existente"})
#
#             if len(cpf) > 11 or len(cpf) < 11:
#                 return jsonify({"msg": "cpf invalido"})
#
#             if existe_cpf:
#                 return jsonify({"msg": "cpf ja existente"})
#
#             novo_funcionario = Usuarios(nome=nome, email=email, cpf=cpf)
#             # novo_funcionario.set_password(senha)
#             db.add(novo_funcionario)
#             db.commit()
#             funcionario_id = novo_funcionario.id
#
#             return jsonify({"msg": "Funcionario cadastrado com sucesso", "funcionario_id": funcionario_id}), 201
#     except SQLAlchemyError as e:
#         return jsonify({"msg": f"Erro na base de dados ao cadastrar funcionario: {str(e)}"})
#     except Exception as e:
#         return jsonify({"msg": f"Erro ao cadastrar funcionario: {str(e)}"}), 500
#     return jsonify(dados)
#
#


@app.route('/api/dados_protegidos', methods=['GET'])
@jwt_required()
def protegido():
    usuario_atual = get_jwt_identity()
    return jsonify({"msg": f"Olá {usuario_atual}, você acessou dados protegidos"}), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')