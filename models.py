import datetime

from flask_login import UserMixin
from sqlalchemy import create_engine, String, Integer, func, Column, DateTime, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
from werkzeug.security import generate_password_hash, check_password_hash

engine = create_engine('mysql+pymysql://root:senaisp@localhost:3306/monitoramento_nutricao_animal')


session_factory = sessionmaker(bind=engine)
db_session = scoped_session(session_factory)

Base = declarative_base()

class Insumos(Base):
    __tablename__ = 'insumos'
    id_insumo = Column(Integer, primary_key=True)
    tipo = Column(String(255))
    nome = Column(String(100))
    umidade_max = Column(String(255))
    umidade_min = Column(String(255))
    temperatura_max = Column(String(255))
    temperatura_min = Column(String(255))
    quantidade = Column (Integer)
    unidade_medida = Column (String(255))

    def serialize(self):
        dados = {
            'id': self.id_insumo,
            'tipo': self.tipo,
            'nome': self.nome,
            'umidade_max': self.umidade_max,
            'umidade_min': self.umidade_min,
            'temperatura_max': self.temperatura_max,
            'temperatura_min': self.temperatura_min,
            'quantidade': self.quantidade,
            'unidade_medida': self.unidade_medida
        }
        return dados

class Galpoes(Base):
    __tablename__ = 'galpoes'
    id = Column(Integer, primary_key=True)
    descricao = Column(String(255))
    nome = Column(String(100))
    def serialize(self):
        dados = {
            'id': self.id,
            'descricao': self.descricao,
            'nome': self.nome,
        }
        return dados

class Blocos(Base):
    __tablename__ = 'blocos'
    id_bloco = Column(Integer, primary_key=True)
    id_galpao = Column(Integer, ForeignKey('galpoes.id'), nullable=False)
    nome = Column(String(100))
    def serialize(self):
        dados = {
            'id': self.id_bloco,
            'id_galpoes': self.id_galpao,
            'nome': self.nome,
        }
        return dados

class Setores (Base):
    __tablename__ = 'setores'
    id_setor = Column(Integer, primary_key=True)
    nome = Column(String(255))
    capacidade = Column (String(255))
    id_insumo = Column(Integer, ForeignKey('insumos.id_insumo'), nullable=False)
    id_bloco = Column(Integer, ForeignKey('blocos.id_bloco'), nullable=False)

    def serialize(self):
        dados = {
            'id_setor': self.id_setor,
            'nome' : self.nome,
            'capacidade': self.capacidade,
            'id_insumo': self.id_insumo,
            'id_bloco': self.id_bloco,
        }
        return dados

class Sensores (Base):
    __tablename__ = 'sensores'
    id_sensor = Column(Integer, primary_key=True)
    id_setor = Column(Integer,ForeignKey('setores.id_setor'), nullable=False)

    def serialize(self):
        dados = {
            'id_sensor': self.id_sensor,
            'id_setor': self.id_setor,
        }
        return dados

class Leituras (Base):
    __tablename__ = 'leituras'
    id_leitura = Column(Integer, primary_key=True)
    id_sensor = Column(Integer,ForeignKey('sensores.id_sensor'), nullable=False)
    valor_leitura_temperatura = Column(String(255))
    valor_leitura_umidade = Column(String(255))
    data_hora= Column(DateTime,default=func.now)

    def serialize(self):
        dados = {
            'id': self.id_leitura,
            'id_sensor': self.id_sensor,
            'valor_leitura_temperatura': self.valor_leitura_temperatura,
            'valor_leitura_umidade': self.valor_leitura_umidade,
            'data_hora': self.data_hora,
        }
        return dados

class AlertaOcorrencias(Base):
    __tablename__ = 'alerta_ocorrencias'
    id = Column(Integer, primary_key=True)
    id_leitura = Column(Integer,ForeignKey('leitura.id'), nullable=False)
    valor_registrado = Column(Float)
    data_hora_inicio= Column(DateTime)
    data_hora_fim= Column(DateTime)
    tipo_alerta = Column(Integer)
    status_ = Column (String(20))

    def serialize(self):
        dados = {
            'id': self.id,
            'id_leitura': self.id_leitura,
            'valor_registrado': self.valor_registrado,
            'data_hora_inicio': self.data_hora_inicio,
            'data_hora_fim': self.data_hora_fim,
            'tipo_alerta': self.tipo_alerta,
            'status_': self.status_,
        }

class Usuarios(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    nome = Column(String(255))
    cpf = Column(String(11))
    email = Column(String(255))
    senha_hash = Column(String(255))

    def serialize(self):
        dados = {
            'id': self.id,
            'nome': self.nome,
            'cpf': self.cpf,
            'email': self.email,
            'senha_hash': self.senha_hash,
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