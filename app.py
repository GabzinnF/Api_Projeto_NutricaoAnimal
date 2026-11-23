from flask import Flask, jsonify, request
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity, JWTManager
)
from sqlalchemy import select
from models import (
    db_session, Usuarios, Insumos, Galpoes, Blocos, Setores,
    Sensores, Leituras, AlertaOcorrencias
)

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "batata"
jwt = JWTManager(app)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route("/")
def home():
    return jsonify({"status": "API ativa"})


@app.route("/cadastro_usuario", methods=["POST"])
def cadastro_usuario():
    dados = request.get_json() or {}
    nome = dados.get("nome")
    email = dados.get("email")
    cpf = str(dados.get("cpf", "")).strip()
    senha = dados.get("senha")

    if not nome or not email or not cpf or not senha:
        return jsonify({"msg": "Preencha todos os campos"}), 400

    if len(cpf) != 11 or not cpf.isdigit():
        return jsonify({"msg": "CPF inválido"}), 400

    try:
        usuario_email = db_session.execute(
            select(Usuarios).where(Usuarios.email == email)
        ).scalar_one_or_none()
        if usuario_email:
            return jsonify({"msg": "E-mail já cadastrado"}), 409

        usuario_cpf = db_session.execute(
            select(Usuarios).where(Usuarios.cpf == cpf)
        ).scalar_one_or_none()
        if usuario_cpf:
            return jsonify({"msg": "CPF já cadastrado"}), 409

        usuario = Usuarios(nome=nome, email=email, cpf=cpf)
        usuario.set_password(senha)
        db_session.add(usuario)
        db_session.commit()

        return jsonify({
            "msg": "Usuário cadastrado com sucesso",
            "usuario": usuario.serialize()
        }), 201
    except Exception as erro:
        db_session.rollback()
        return jsonify({"msg": str(erro)}), 500


@app.route("/api/login", methods=["POST"])
def login():
    dados = request.get_json() or {}
    email = dados.get("email")
    senha = dados.get("senha")

    if not email or not senha:
        return jsonify({"msg": "Preencha todos os campos"}), 400

    usuario = db_session.execute(
        select(Usuarios).where(Usuarios.email == email)
    ).scalar_one_or_none()

    if usuario and usuario.check_password_hash(senha):
        token = create_access_token(identity=str(usuario.id_usuario))
        return jsonify({
            "msg": "Login realizado com sucesso",
            "access_token": token,
            "usuario": usuario.serialize()
        }), 200

    return jsonify({"msg": "E-mail ou senha incorretos"}), 401


@app.route("/api/cadastrar_galpoes", methods=["POST"])
def criar_galpao():
    dados = request.get_json() or {}
    nome = dados.get("nome")
    descricao = dados.get("descricao")
    status = dados.get("status", "Ativo")

    if not nome or not descricao:
        return jsonify({"msg": "Preencha todos os campos"}), 400
    if status not in ["Ativo", "Desativado"]:
        return jsonify({"msg": "Status inválido"}), 400

    try:
        galpao = Galpoes(nome=nome, descricao=descricao, status=status)
        db_session.add(galpao)
        db_session.commit()
        return jsonify({
            "msg": "Galpão cadastrado com sucesso",
            "galpao": galpao.serialize()
        }), 201
    except Exception as erro:
        db_session.rollback()
        return jsonify({"msg": str(erro)}), 500


@app.route("/api/editar_galpao/<int:id_galpao>", methods=["PUT"])
def editar_galpao(id_galpao):
    dados = request.get_json() or {}
    status = dados.get("status")
    if status not in ["Ativo", "Desativado"]:
        return jsonify({"msg": "Status inválido"}), 400

    galpao = db_session.get(Galpoes, id_galpao)
    if not galpao:
        return jsonify({"msg": "Galpão não encontrado"}), 404

    galpao.status = status
    db_session.commit()
    return jsonify({"msg": "Status atualizado", "galpao": galpao.serialize()}), 200


@app.route("/api/cadastrar_blocos", methods=["POST"])
def criar_bloco():
    dados = request.get_json() or {}
    nome = dados.get("nome")
    id_galpao = dados.get("id_galpao")
    if not nome or not id_galpao:
        return jsonify({"msg": "Preencha todos os campos"}), 400

    try:
        if not db_session.get(Galpoes, int(id_galpao)):
            return jsonify({"msg": "Galpão não encontrado"}), 404
        bloco = Blocos(nome=nome, id_galpao=int(id_galpao))
        db_session.add(bloco)
        db_session.commit()
        return jsonify({"msg": "Bloco cadastrado com sucesso", "bloco": bloco.serialize()}), 201
    except Exception as erro:
        db_session.rollback()
        return jsonify({"msg": str(erro)}), 500


@app.route("/api/cadastrar_insumos", methods=["POST"])
def criar_insumo():
    dados = request.get_json() or {}
    campos = [
        "nome", "tipo", "umidade_max", "umidade_min",
        "temperatura_max", "temperatura_min", "quantidade",
        "unidade_medida"
    ]
    if any(dados.get(campo) in [None, ""] for campo in campos):
        return jsonify({"msg": "Preencha todos os campos"}), 400

    try:
        insumo = Insumos(
            nome=dados["nome"], tipo=dados["tipo"],
            umidade_max=dados["umidade_max"],
            umidade_min=dados["umidade_min"], umidade_atual="0",
            temperatura_max=dados["temperatura_max"],
            temperatura_min=dados["temperatura_min"],
            temperatura_atual="0", quantidade=int(dados["quantidade"]),
            unidade_medida=dados["unidade_medida"]
        )
        if insumo.quantidade < 0:
            return jsonify({"msg": "A quantidade não pode ser negativa"}), 400
        db_session.add(insumo)
        db_session.commit()
        return jsonify({"msg": "Insumo cadastrado com sucesso", "insumo": insumo.serialize()}), 201
    except Exception as erro:
        db_session.rollback()
        return jsonify({"msg": str(erro)}), 500


@app.route("/api/cadastrar_setores", methods=["POST"])
def criar_setor():
    dados = request.get_json() or {}
    nome = dados.get("nome")
    id_insumo = dados.get("id_insumo")
    id_bloco = dados.get("id_bloco")
    capacidade = dados.get("capacidade")
    quantidade_atual = dados.get("quantidade_atual", 0)

    if not nome or not id_insumo or not id_bloco or capacidade in [None, ""]:
        return jsonify({"msg": "Preencha todos os campos"}), 400

    try:
        id_insumo = int(id_insumo)
        id_bloco = int(id_bloco)
        capacidade = float(capacidade)
        quantidade_atual = float(quantidade_atual)

        if capacidade <= 0 or quantidade_atual < 0:
            return jsonify({"msg": "Quantidade inválida"}), 400
        if quantidade_atual > capacidade:
            return jsonify({"msg": "A quantidade ultrapassa a capacidade do setor"}), 400

        insumo = db_session.get(Insumos, id_insumo)
        bloco = db_session.get(Blocos, id_bloco)
        if not insumo:
            return jsonify({"msg": "Insumo não encontrado"}), 404
        if not bloco:
            return jsonify({"msg": "Bloco não encontrado"}), 404

        setores_existentes = db_session.execute(
            select(Setores).where(Setores.id_insumo == id_insumo)
        ).scalars().all()
        quantidade_distribuida = sum(float(s.quantidade_atual or 0) for s in setores_existentes)

        if quantidade_distribuida + quantidade_atual > float(insumo.quantidade or 0):
            return jsonify({"msg": "Estoque insuficiente para essa distribuição"}), 400

        setor = Setores(
            nome=nome, id_insumo=id_insumo, id_bloco=id_bloco,
            capacidade=capacidade, quantidade_atual=quantidade_atual
        )
        db_session.add(setor)
        db_session.commit()
        return jsonify({"msg": "Setor cadastrado com sucesso", "setor": setor.serialize()}), 201
    except Exception as erro:
        db_session.rollback()
        return jsonify({"msg": str(erro)}), 500


@app.route("/api/cadastrar_sensores", methods=["POST"])
def criar_sensor():
    dados = request.get_json() or {}
    id_setor = dados.get("id_setor")
    if not id_setor:
        return jsonify({"msg": "Informe o setor"}), 400

    try:
        setor = db_session.get(Setores, int(id_setor))
        if not setor:
            return jsonify({"msg": "Setor não encontrado"}), 404
        sensor_existente = db_session.execute(
            select(Sensores).where(Sensores.id_setor == int(id_setor))
        ).scalar_one_or_none()
        if sensor_existente:
            return jsonify({"msg": "Esse setor já possui um sensor"}), 409

        sensor = Sensores(id_setor=int(id_setor))
        db_session.add(sensor)
        db_session.commit()
        return jsonify({"msg": "Sensor cadastrado com sucesso", "sensor": sensor.serialize()}), 201
    except Exception as erro:
        db_session.rollback()
        return jsonify({"msg": str(erro)}), 500


def verificar_alerta(leitura, sensor, insumo, setor):
    valor = float(leitura.valor_leitura)

    if leitura.tipo_leitura == "temperatura":
        minimo = float(insumo.temperatura_min)
        maximo = float(insumo.temperatura_max)
        tipo = 1
        nome_tipo = "temperatura"
    else:
        minimo = float(insumo.umidade_min)
        maximo = float(insumo.umidade_max)
        tipo = 2
        nome_tipo = "umidade"

    if valor < minimo or valor > maximo:
        status = "CRÍTICO"
    elif valor <= minimo + 2 or valor >= maximo - 2:
        status = "ATENÇÃO"
    else:
        return

    alerta_aberto = db_session.execute(
        select(AlertaOcorrencias).where(
            AlertaOcorrencias.id_leitura == leitura.id_leitura
        )
    ).scalar_one_or_none()

    if not alerta_aberto:
        alerta = AlertaOcorrencias(
            id_leitura=leitura.id_leitura,
            valor_registrado=leitura.valor_leitura,
            tipo_alerta=tipo,
            status_=status
        )
        db_session.add(alerta)


@app.route("/api/cadastrar_leituras", methods=["POST"])
def criar_leitura():
    dados = request.get_json() or {}
    id_sensor = dados.get("id_sensor")
    temperatura = dados.get("valor_leitura_temperatura")
    umidade = dados.get("valor_leitura_umidade")

    if id_sensor is None or temperatura is None or umidade is None:
        return jsonify({"msg": "Preencha todos os campos"}), 400

    try:
        sensor = db_session.get(Sensores, int(id_sensor))
        if not sensor:
            return jsonify({"msg": "Sensor não encontrado"}), 404

        setor = db_session.get(Setores, sensor.id_setor)
        if not setor:
            return jsonify({"msg": "Setor não encontrado"}), 404

        if float(setor.quantidade_atual or 0) <= 0:
            return jsonify({"msg": "Sensor inativo. O setor está vazio."}), 400

        insumo = db_session.get(Insumos, setor.id_insumo)
        if not insumo:
            return jsonify({"msg": "Insumo não encontrado"}), 404

        temperatura = float(temperatura)
        umidade = float(umidade)

        leitura_temperatura = Leituras(
            id_sensor=int(id_sensor), valor_leitura=temperatura,
            tipo_leitura="temperatura"
        )
        db_session.add(leitura_temperatura)
        db_session.flush()
        verificar_alerta(leitura_temperatura, sensor, insumo, setor)

        leitura_umidade = Leituras(
            id_sensor=int(id_sensor), valor_leitura=umidade,
            tipo_leitura="umidade"
        )
        db_session.add(leitura_umidade)
        db_session.flush()
        verificar_alerta(leitura_umidade, sensor, insumo, setor)

        insumo.temperatura_atual = str(temperatura)
        insumo.umidade_atual = str(umidade)
        db_session.commit()

        return jsonify({
            "msg": "Leituras cadastradas com sucesso",
            "temperatura": leitura_temperatura.serialize(),
            "umidade": leitura_umidade.serialize()
        }), 201
    except Exception as erro:
        db_session.rollback()
        return jsonify({"msg": str(erro)}), 500


def listar(modelo, chave):
    try:
        resultado = db_session.execute(select(modelo)).scalars().all()
        return jsonify({chave: [item.serialize() for item in resultado]}), 200
    except Exception as erro:
        return jsonify({"msg": str(erro)}), 500


@app.route("/todos_galpoes")
def listar_galpoes():
    return listar(Galpoes, "Galpoes")


@app.route("/todos_blocos")
def listar_blocos():
    return listar(Blocos, "Blocos")


@app.route("/todos_setores")
def listar_setores():
    return listar(Setores, "Setores")


@app.route("/todos_insumos")
def listar_insumos():
    return listar(Insumos, "Insumos")


@app.route("/todos_sensores")
def listar_sensores():
    return listar(Sensores, "Sensores")


@app.route("/todas_leituras")
def listar_leituras():
    return listar(Leituras, "Leitura")


@app.route("/todos_usuarios")
def listar_usuarios():
    return listar(Usuarios, "Usuario")


@app.route("/todos_alertas")
def listar_alertas():
    try:
        resultado = db_session.execute(select(AlertaOcorrencias)).scalars().all()
        alertas = []

        for alerta in resultado:
            dados = alerta.serialize()
            leitura = db_session.get(Leituras, alerta.id_leitura)
            setor = None
            bloco = None
            galpao = None

            if leitura:
                sensor = db_session.get(Sensores, leitura.id_sensor)
                if sensor:
                    setor = db_session.get(Setores, sensor.id_setor)
                    if setor:
                        bloco = db_session.get(Blocos, setor.id_bloco)
                        if bloco:
                            galpao = db_session.get(Galpoes, bloco.id_galpao)

            dados["nome_setor"] = setor.nome if setor else "Não identificado"
            dados["nome_bloco"] = bloco.nome if bloco else "Não identificado"
            dados["nome_galpao"] = galpao.nome if galpao else "Não identificado"
            dados["tipo_leitura"] = leitura.tipo_leitura if leitura else "Não identificado"
            alertas.append(dados)

        return jsonify({"Alerta": alertas}), 200
    except Exception as erro:
        db_session.rollback()
        return jsonify({"msg": str(erro)}), 500


@app.route("/api/dados_protegidos")
@jwt_required()
def protegido():
    return jsonify({
        "msg": "Acesso autorizado",
        "usuario": get_jwt_identity()
    }), 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)