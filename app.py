import datetime
import random
import string
from flask import Flask, jsonify, request, render_template, url_for
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, JWTManager
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from models import db_session, Insumos, Galpoes , Blocos , Sensores, Setores , Leituras , AlertaOcorrencias # Certifique-se que o database.py está na mesma pasta

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'batata'
jwt = JWTManager(app)


@app.route('/')
def home():
    return jsonify({"status": "API de Monitoramento de Nutrição Animal Ativa"}), 200


@app.route('/login')
def tela_login():
    return render_template('login.html')


@app.route('/cadastro')
def tela_cadastro():
    return render_template('cadastro.html')



@app.route('/api/cadastrar_galpoes', methods=['POST'])
def criar_galpao():
    db = db_session()
    dados = request.get_json()
    try:
        if request.method == 'POST':
            json_galpao = request.get_json()
            nome = json_galpao.get('nome')
            descricao = json_galpao.get('descricao')
            id_insumo = json_galpao.get('ID Insumo')

            if not nome or not descricao or not id_insumo:
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
                    'id_insumo': novo_galpao.id_insumos
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
    try:
        if request.method == 'POST':
            json_bloco = request.get_json()
            nome = json_bloco.get('nome')
            id_galpao = json_bloco.get('ID Galpao')
            id_insumo = json_bloco.get('ID Insumo')

            if not nome or not id_galpao or not id_insumo:
                return jsonify({"msg": "Preencher todos os campos"})

            novo_bloco = Blocos(
                nome=nome)
            db.add(novo_bloco)
            db.commit()
            return jsonify({
                "msg": "Bloco criado com sucesso",
                'bloco': {
                    "id": novo_bloco.id,
                    'nome': novo_bloco.nome,
                    'id_galpao': novo_bloco.id_galpoes,
                    'id_insumo': novo_bloco.id_insumos
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
    try:
        if request.method == 'POST':
            json_setor = request.get_json()
            nome = json_setor.get('nome')
            id_galpao = json_setor.get('ID Galpao')
            id_insumo = json_setor.get('ID Insumo')
            id_bloco = json_setor.get('ID Bloco')

            if not nome or not id_galpao or not id_insumo or not id_bloco:
                return jsonify({"msg": "Preencher todos os campos"})

            novo_setor = Blocos(
                nome=nome)
            db.add(novo_setor)
            db.commit()
            return jsonify({
                "msg": "Bloco criado com sucesso",
                'setor': {
                    "id": novo_setor.id,
                    'nome': novo_setor.nome,
                    'id_galpao': novo_setor.id_galpoes,
                    'id_insumo': novo_setor.id_insumos,

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
    try:
        if request.method == 'POST':
            json_insumo = request.get_json()
            nome = json_insumo.get('Nome')
            id_setor = json_insumo.get('ID Bloco')
            tipo = json_insumo.get('Tipo Insumo')
            umid_max = json_insumo.get('Umidade Maxima')
            umid_min = json_insumo.get('Umidade Minima')
            temp_max = json_insumo.get('Temperatura Maxima')
            tem_min = json_insumo.get('Temperatura Minima')

            if not nome or not id_setor or not tipo or not umid_max or not umid_min or not temp_max or not tem_min:
                return jsonify({"msg": "Preencher todos os campos"})

            novo_insumo = Insumos(
                nome=nome)
            db.add(novo_insumo)
            db.commit()
            return jsonify({
                "msg": "Insumo cadastrado com sucesso",
                'insumo': {
                    "id": novo_insumo.id_insumo,
                    'nome': novo_insumo.nome,
                    'id_setor' : novo_insumo.id_setor,
                    'tipo' : novo_insumo.tipo,
                    'umid_max' : novo_insumo.umidade_max,
                    'umid_min' : novo_insumo.umidade_min,
                    'temp_max' : novo_insumo.temperatura_max,
                    'temp_min' : novo_insumo.temperatura_min
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
            id_sensor = json_leitura.get('ID Sensor')
            valor_leitura = json_leitura.get('Valor Leitura')
            data_hora = json_leitura.get('Data Hora')

            if not id_sensor or not valor_leitura or not data_hora:
                return jsonify({"msg": "Preencher todos os campos"})

            nova_leitura = Leituras(
                valor_leitura=valor_leitura,)
            db.add(nova_leitura)
            db.commit()
            return jsonify({
                "msg": "Bloco criado com sucesso",
                'leitura': {
                    'id' : nova_leitura.id,
                    'id_sensor' : nova_leitura.id_sensor,
                    'valor_leitura' : nova_leitura.valor_leitura,
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
    try:
        if request.method == 'POST':
            json_sensor = request.get_json()
            id_setor = json_sensor.get('ID Setor')
            id_insumo = json_sensor.get('ID Insumo')

            if not id_setor or not id_insumo :
                return jsonify({"msg": "Preencher todos os campos"})

            novo_sensor = Sensores(
                id_setor=id_setor)
            db.add(novo_sensor)
            db.commit()
            return jsonify({
                "msg": "Sensor cadastrado com sucesso",
                'sensor': {
                    "id": novo_sensor.id,
                    'id_setor' : novo_sensor.id_setor,
                    'id_insumo' : novo_sensor.id_insumos

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
@app.route('/todos_clientes')
def clientes():
    # Rota que estava faltando e causava o BuildError
    db = db_session()
    try:
        api_cliente = select(Cliente)
        result = db_session.execute(api_cliente).scalars().all()
        clientes = []
        for cliente in result:
            clientes.append(cliente.serialize())
        print(result)
        return jsonify({"clientes": clientes}), 200
    finally:
        db.close()


@app.route('/todos_remetentes')
def lista_remetente():
    db = db_session()
    try:
        api_remetente = select(Remetente)
        result = db_session.execute(api_remetente).scalars().all()
        remetente = []
        for remetentes in result:
            remetente.append(remetentes.serialize())
        print(result)
        return jsonify({"remetentes": remetente}), 200
    finally:
        db.close()


@app.route('/todas_unidades')
def unidades_centro():
    # Rota que estava faltando e causava o BuildError
    db = db_session()
    try:
        api_centro = select(Centro_distribuicao)
        result = db_session.execute(api_centro).scalars().all()
        centros = []
        for centro_distribuicao in result:
            centros.append(centro_distribuicao.serialize())
        print(result)
        return jsonify({"centro_distribuicao": centros}), 200
    finally:
        db.close()



# --- ROTAS DE API (BACKEND) ---

@app.route('/api/login', methods=['POST'])
def login():
    try:
        dados = request.get_json()
        email = dados.get('email')
        senha = dados.get('senha')

        db = db_session()
        sql = select(Funcionario).where(Funcionario.email == email)
        usuario = db.execute(sql).scalar()

        # Importante: No database.py, a classe Usuario precisa do método check_password_hash
        # if usuario and usuario.check_password_hash(senha):
        #     access_token = create_access_token(identity=str(usuario.email))
        #     texto = "Login realizado com sucesso"
        #     return jsonify({
        #         "Sistema": texto,
        #
        #         "Bem Vindo": usuario.nome,
        #
        #     }), 200

        return jsonify({"msg": "E-mail ou senha incorretos"}), 401
    except Exception as e:
        return jsonify({"msg": str(e)}), 500
    finally:
        db.close()


@app.route('/usuario', methods=['POST'])
def cadastro():
    dados = request.get_json()
    nome = dados.get('nome')
    email = dados.get('email')
    cep = dados.get('cep')
    rua = dados.get('rua')
    bairro = dados.get('bairro')
    cidade = dados.get('cidade')
    estado = dados.get('estado')
    numero_casa = dados.get('numero_casa')
    complemento = dados.get('complemento')

    if not nome or not email:
        return jsonify({"msg": "Preencha todos os campos"}), 400

    db = db_session()
    try:
        # Verifica se email já existe
        check = select(Cliente).where(Cliente.email == email)
        if db.execute(check).scalar():
            return jsonify({"msg": "Email já cadastrado"}), 409

        novo_cliente = Cliente(nome=nome, email=email, cep=cep, rua=rua, bairro=bairro, cidade=cidade, estado=estado,
                               numero_casa=numero_casa, complemento=complemento)
        # Método que deve estar no database.py

        db.add(novo_cliente)
        db.commit()
        return jsonify({"msg": "Cadastrado com sucesso"}), 201
    except Exception as e:
        db.rollback()
        return jsonify({"msg": str(e)}), 500
    finally:
        db.close()

@app.route('/verificar_email',methods=['POST'])
def verificar_email():
    db = db_session()
    try:
        json_funcionario_email = request.get_json()
        email = json_funcionario_email.get('email')
        verifica_email = select(Funcionario).where(Funcionario.email == email)
        existe_email = db.execute(verifica_email).scalar_one_or_none()
        print(email)
        if existe_email:
            return jsonify({"funcionario":existe_email.serialize()}), 200

        else:

            return jsonify({"msg": "Email não existe"}), 400

    except SQLAlchemyError as e:
        return jsonify({"msg": f"Erro na base de dados ao logar funcionario: {str(e)}"})
    except Exception as e:
        return jsonify({"msg": f"Erro ao logar funcionario: {str(e)}"}), 500
@app.route('/funcionario', methods=['POST'])
def cadastro_funcionario():
    db = db_session()
    dados = request.get_json()
    try:
        if request.method == 'POST':
            json_funcionario = request.get_json()
            nome = json_funcionario.get('nome')
            cpf = json_funcionario.get('cpf')
            email = json_funcionario.get('email')
            senha = json_funcionario.get('senha')

            # data_convertida = datetime.strptime(data_nascimento, '%Y-%m-%d')
            # data_brasil = datetime.strftime(data_convertida, '%d-%m-%Y')

            if not nome or not email or not senha or not cpf:
                return jsonify({"msg": "Preencher todos os campos"})
            verifica_email = select(Funcionario).where(Funcionario.email == email)
            verifica_cpf = select(Funcionario).where(Funcionario.cpf == cpf)
            existe_email = db.execute(verifica_email, ).scalar_one_or_none()
            existe_cpf = db.execute(verifica_cpf, ).scalar_one_or_none()
            if existe_email:
                return jsonify({"msg": "Email ja existente"})

            if len(cpf) > 11 or len(cpf) < 11:
                return jsonify({"msg": "cpf invalido"})

            if existe_cpf:
                return jsonify({"msg": "cpf ja existente"})

            novo_funcionario = Funcionario(nome=nome, email=email, cpf=cpf, senha=senha)
            # novo_funcionario.set_password(senha)
            db.add(novo_funcionario)
            db.commit()
            funcionario_id = novo_funcionario.id

            return jsonify({"msg": "Funcionario cadastrado com sucesso", "funcionario_id": funcionario_id}), 201
    except SQLAlchemyError as e:
        return jsonify({"msg": f"Erro na base de dados ao cadastrar funcionario: {str(e)}"})
    except Exception as e:
        return jsonify({"msg": f"Erro ao cadastrar funcionario: {str(e)}"}), 500
    return jsonify(dados)


@app.route('/encomendas', methods=['POST'])
def cadastro_encomenda():
    db = db_session()
    try:
        json_encomenda = request.get_json()
        fragilidade = json_encomenda.get('fragilidade')
        tipo = json_encomenda.get('tipo')
        remetente_id = json_encomenda.get('remetente_id')
        cliente_id = json_encomenda.get('cliente_id')

        if not fragilidade or not tipo or not cliente_id or not remetente_id:
            return jsonify({"msg": "Os campos nome, fragilidade e tipo são obrigatórios"}), 400
        codigo_gerado = gerar_codigo_unico(db)

        nova_encomenda = Emcomenda(
            codigo_rastreio=codigo_gerado,
            fragilidade=fragilidade,
            tipo=tipo,
            remetente_id=remetente_id,
            cliente_id=cliente_id
        )

        db.add(nova_encomenda)
        db.commit()

        return jsonify({"msg": "Encomenda cadastrada com sucesso",
                        "encomenda_id": nova_encomenda.id,
                        "codigo_rastreio": nova_encomenda.codigo_rastreio,
                        "fragilidade": nova_encomenda.fragilidade,
                        "tipo": nova_encomenda.tipo,
                        "cliente_id": nova_encomenda.cliente_id,
                        "rementente_id": nova_encomenda.remetente_id
                        }), 201

    except Exception as e:
        db.rollback()
        print(e)
        return jsonify({"msg": f"Erro ao cadastrar encomenda: {str(e)}"}), 500
    finally:
        db.close()


@app.route('/unidades', methods=['POST'])
def centro_distribuicao():
    db = db_session()
    dados = request.get_json()
    try:
        if request.method == 'POST':
            json_distribuicao = request.get_json()
            nome = json_distribuicao.get('nome')
            cidade = json_distribuicao.get('cidade')
            estado = json_distribuicao.get('estado')

            if not cidade or not estado:
                return jsonify({"msg": "Preencher todos os campos"})

            novo_centro_distribuicao = Centro_distribuicao(
                nome=nome, cidade=cidade, estado=estado)
            db.add(novo_centro_distribuicao)
            db.commit()
            return jsonify({
                "msg": "Movimentacao feita com sucesso",
                'unidades': {
                    "id": novo_centro_distribuicao.id,
                    'nome': novo_centro_distribuicao.nome,
                    'cidade': novo_centro_distribuicao.cidade,
                    'estado': novo_centro_distribuicao.estado
                }

            }), 201

    except Exception as e:
        db.rollback()
        return jsonify({"Erro": str(e)}), 500

    return jsonify(dados)


@app.route('/movimentacoes', methods=['POST'])
def cadastro_movimentacao():
    db = db_session()
    try:
        if request.method == 'POST':
            json_movimentacao = request.get_json()
            encomenda_id = json_movimentacao.get('encomenda_id')
            centro_id = json_movimentacao.get('centro_id')
            print("luciano lindo", encomenda_id, centro_id)
            if not encomenda_id or not centro_id:
                return jsonify({"msg": "Preencher todos os campos"}), 400
            # Verificar a ultima movimentação da encomenda
            # Fazer um select para trazer essa movimentação
            sql_movimentacao = (select(Movimentacao, Centro_distribuicao).where(Movimentacao.encomenda_id == encomenda_id)
                                .join(Centro_distribuicao, Centro_distribuicao.id == Movimentacao.centro_id)
                                .order_by(Movimentacao.criado_em.desc()).limit(1))
            ultima_movimentacao = db_session.execute(sql_movimentacao).tuples().one_or_none()

            print("hoje",ultima_movimentacao)



            comparar_cidade = (
                select(Cliente, Emcomenda).where(Emcomenda.id == encomenda_id)
                .join(Emcomenda, Cliente.id == Emcomenda.cliente_id)
            )
            encomenda_cliente = db_session.execute(comparar_cidade).scalars().one_or_none()

            if ultima_movimentacao is None:
                tipo = 'saida'
            else:
                movs = []
                for item in ultima_movimentacao:
                    movs.append(item.serialize())
                if movs[0]["tipo"] == 'saida':

                    tipo = 'chegada'
                    if movs[0]["localizacao"] == centro_id:
                        return jsonify({
                            "msg": "Não pode chegar no mesmo lugar que saiu",
                        }), 400
                else:
                    tipo = 'saida'
                    # Achar como trazer o centro no join da ultima_movimentacao
                    if movs[1]["cidade"] == encomenda_cliente.cidade:
                        tipo = 'entregue'

            nova_movimentacao = Movimentacao(
                tipo=tipo, encomenda_id=encomenda_id, centro_id=centro_id
            )
            db.add(nova_movimentacao)
            db.commit()

            return jsonify({
                "msg": "Movimentacao feita com sucesso",
                'movimentacao': {
                    "id": nova_movimentacao.id,
                    'criado_em': nova_movimentacao.criado_em.strftime('%d/%m/%Y'),
                    'tipo': nova_movimentacao.tipo
                }

            }), 201

    except Exception as e:
        db.rollback()
        print("erro", e)
        return jsonify({"Erro": str(e)}), 500


@app.route('/remetente', methods=['POST'])
def cadastro_remetente():
    db = db_session()
    try:
        if request.method == 'POST':
            json_remetente = request.get_json()
            nome = json_remetente.get('nome')
            cidade = json_remetente.get('cidade')
            estado = json_remetente.get('estado')

            if not cidade or not estado:
                return jsonify({"msg": "Preencher todos os campos"})

            novo_remetente = Remetente(
                nome=nome, cidade=cidade, estado=estado)
            db.add(novo_remetente)
            db.commit()
            return jsonify({
                "msg": "Remetente cadastrado com sucesso",
                'remetente': {
                    "id": novo_remetente.id,
                    'nome': novo_remetente.nome,
                    'cidade': novo_remetente.cidade,
                    'estado': novo_remetente.estado
                }

            }), 201

    except Exception as e:
        db.rollback()
        return jsonify({"Erro": str(e)}), 500


@app.route('/rastreio', methods=['POST'])
def rastreio_encomenda():
    db = db_session()
    try:
        json_rastreio = request.get_json()
        codigo = json_rastreio.get('codigo')

        # traz a encomenda de acordo com o codigo
        rastrear_encomenda = select(Emcomenda).where(Emcomenda.codigo_rastreio == codigo)
        encomenda = db_session.execute(rastrear_encomenda).scalars().one_or_none()

        # traz as movimentacoes da encomenda de acordo com seu id
        rastrear_id_encomenda = select(Movimentacao).where(Movimentacao.encomenda_id == encomenda.id)
        movimentacao_encomenda = db_session.execute(rastrear_id_encomenda).scalars().all()

        movimentacoes = []
        for movimentacao in movimentacao_encomenda:
            sql_centro = select(Centro_distribuicao).where(Centro_distribuicao.id == movimentacao.centro_id)
            centro = db_session.execute(sql_centro).scalars().one_or_none()

            movimentacoes.append(movimentacao.serialize(centro))

        sql_cliente = select(Cliente).where(Cliente.id == encomenda.cliente_id)
        sql_remetente = select(Remetente).where(Remetente.id == encomenda.remetente_id)
        cliente = db_session.execute(sql_cliente).scalars().one_or_none()
        remetente = db_session.execute(sql_remetente).scalars().one_or_none()

        print(encomenda)
        return jsonify({"encomenda": encomenda.serialize(cliente, remetente),
                        "movimentacoes": movimentacoes
                        })
    except Exception as e:
        db.rollback()
        return jsonify({"Erro": str(e)}), 500


def gerar_codigo_unico(db):
    data = datetime.datetime.now()
    alfabeto = ["a", "b", "c", "d", "e", "f", "g", "h",
                "i", "j", "k", "l", "m", "n", "o", "p",
                "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

    codigo_1 = random.choice(alfabeto).upper()
    codigo_2 = random.choice(alfabeto).upper()
    codigo_3 = random.choice(alfabeto).upper()
    codigo_unico = str(data.timestamp()).replace(".", "")
    codigo_final = str(codigo_1 + codigo_2 + codigo_3) + codigo_unico

    consulta = select(Emcomenda).where(Emcomenda.codigo_rastreio == codigo_final)
    resultado = db.execute(consulta).scalars().first()

    if resultado:
        return gerar_codigo_unico(db)

    return codigo_final


@app.route('/api/dados_protegidos', methods=['GET'])
@jwt_required()
def protegido():
    usuario_atual = get_jwt_identity()
    return jsonify({"msg": f"Olá {usuario_atual}, você acessou dados protegidos"}), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')