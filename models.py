
from sqlalchemy import create_engine, String, Integer, Column, DateTime, Float, ForeignKey, func
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
from werkzeug.security import generate_password_hash, check_password_hash

engine = create_engine('mysql+pymysql://root:senaisp@localhost:3306/monitoramento_nutricao_animal')

session_factory = sessionmaker(bind=engine)
db_session = scoped_session(session_factory)
Base = declarative_base()


class Usuarios(Base):
    __tablename__ = 'usuarios'

    id_usuario = Column(Integer, primary_key=True)
    nome = Column(String(255))
    cpf = Column(String(255))
    email = Column(String(255))
    senha = Column(String(255))

    def serialize(self):
        return {
            'id': self.id_usuario,
            'nome': self.nome,
            'cpf': self.cpf,
            'email': self.email
        }

    def set_password(self, password):
        self.senha = generate_password_hash(password)

    def check_password_hash(self, password):
        return check_password_hash(self.senha, password)


class Galpoes(Base):
    __tablename__ = 'galpoes'

    id_galpao = Column(Integer, primary_key=True)
    nome = Column(String(100))
    descricao = Column(String(255))
    status = Column(String(20), default='Ativo')

    def serialize(self):
        return {
            'id': self.id_galpao,
            'nome': self.nome,
            'descricao': self.descricao,
            'status': self.status
        }


class Blocos(Base):
    __tablename__ = 'blocos'

    id_bloco = Column(Integer, primary_key=True)
    id_galpao = Column(Integer, ForeignKey('galpoes.id_galpao'))
    nome = Column(String(255))

    def serialize(self):
        return {
            'id': self.id_bloco,
            'id_bloco': self.id_bloco,
            'id_galpao': self.id_galpao,
            'nome': self.nome
        }


class Insumos(Base):
    __tablename__ = 'insumos'

    id_insumo = Column(Integer, primary_key=True)
    tipo = Column(String(255))
    nome = Column(String(100))
    umidade_max = Column(String(255))
    umidade_min = Column(String(255))
    umidade_atual = Column(String(255))
    temperatura_max = Column(String(255))
    temperatura_min = Column(String(255))
    temperatura_atual = Column(String(255))
    quantidade = Column(Integer)
    unidade_medida = Column(String(255))

    def serialize(self):
        return {
            'id': self.id_insumo,
            'id_insumo': self.id_insumo,
            'tipo': self.tipo,
            'nome': self.nome,
            'umidade_max': self.umidade_max,
            'umidade_min': self.umidade_min,
            'umidade_atual': self.umidade_atual,
            'temperatura_max': self.temperatura_max,
            'temperatura_min': self.temperatura_min,
            'temperatura_atual': self.temperatura_atual,
            'quantidade': self.quantidade,
            'unidade_medida': self.unidade_medida
        }



class Setores(Base):
    __tablename__ = 'setores'

    id_setor = Column(Integer, primary_key=True)
    nome = Column(String(255))
    id_insumo = Column(Integer, ForeignKey('insumos.id_insumo'))
    id_bloco = Column(Integer, ForeignKey('blocos.id_bloco'))
    capacidade = Column('capacitade', String(255))
    quantidade_atual = Column(Float, default=0)

    def serialize(self):
        return {
            'id_setor': self.id_setor,
            'nome': self.nome,
            'id_insumo': self.id_insumo,
            'id_bloco': self.id_bloco,
            'capacidade': self.capacidade,
            'quantidade_atual': self.quantidade_atual
        }


class Sensores(Base):
    __tablename__ = 'sensores'

    id_sensor = Column(Integer, primary_key=True)
    id_setor = Column(Integer, ForeignKey('setores.id_setor'))

    def serialize(self):
        return {
            'id_sensor': self.id_sensor,
            'id_setor': self.id_setor
        }


class Leituras(Base):
    __tablename__ = 'leitura'

    id_leitura = Column(Integer, primary_key=True)
    id_sensor = Column(Integer, ForeignKey('sensores.id_sensor'))
    valor_leitura = Column(Integer)
    tipo_leitura = Column(String(20))
    data_hora = Column(DateTime, default=func.now())

    def serialize(self):
        return {
            'id_leitura': self.id_leitura,
            'id_sensor': self.id_sensor,
            'valor_leitura': self.valor_leitura,
            'tipo_leitura': self.tipo_leitura,
            'data_hora': self.data_hora.isoformat() if self.data_hora else None
        }


class AlertaOcorrencias(Base):
    __tablename__ = 'alertas_ocorrencias'

    id_alerta = Column(Integer, primary_key=True)
    id_leitura = Column(Integer, ForeignKey('leitura.id_leitura'))
    valor_registrado = Column(Integer)
    data_hora_inicio = Column(DateTime, default=func.now())
    data_hora_fim = Column(DateTime)
    tipo_alerta = Column(Integer)
    status_ = Column(String(20))

    def serialize(self):
        return {
            'id_alerta': self.id_alerta,
            'id_leitura': self.id_leitura,
            'valor_registrado': self.valor_registrado,
            'data_hora_inicio': self.data_hora_inicio.isoformat() if self.data_hora_inicio else None,
            'data_hora_fim': self.data_hora_fim.isoformat() if self.data_hora_fim else None,
            'tipo_alerta': self.tipo_alerta,
            'status_': self.status_
        }

'''
No "prever a temp e umidade" seria o seguinte. vamos supor que o mulho aguente 80% de umidade e 20 de temp.
se a temperatura aumentar ou diminuir, por ex se tiver chegando no 78 ja da um alerta avisando. "a temperatura do bloco tal ou setor tal esta em risco"
seria um alerta de prevenção. isso previne a perda de insumo, e se chegar na temperatura que pode ter a perda avisa SEU INSUMO CORRE RISCO DE PERDA
'''

'''
o de quantidade de insumos ele pode receber Toneladas, Litros, sacos e afins então sera mandado um campo no cadastrod de qual é a unidade de medida que ele esta recebendo
e no setor está a capacidade pois ele não quer o total do bloco, mas se em 1 setor cabe tudo ou precisara de varios
e insumos agora tem quantidade para saber quanto tem de insumos totais de cada
'''

'''
fazer uma verificação se o setor tem algo nele ou nada, se for nada não mandar as leituras do sensor deixando ele inativo
caso tenha insumos ele manter ele ativo e o sensor mandando a leitura 
'''