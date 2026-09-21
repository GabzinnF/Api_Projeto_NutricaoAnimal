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
    umidade_atual = Column(String(255))
    temperatura_max = Column(String(255))
    temperatura_min = Column(String(255))
    temperatura_atual = Column(String(255))

    def serialize(self):
        dados = {
            'id': self.id_insumo,
            'tipo': self.tipo,
            'nome': self.nome,
            'umidade_max': self.umidade_max,
            'umidade_min': self.umidade_min,
            'umidade_atual' : self.umidade_atual,
            'temperatura_max': self.temperatura_max,
            'temperatura_min': self.temperatura_min,
            'temepratura_atual': self.temperatura_atual
        }
        return dados

class Galpoes(Base):
    __tablename__ = 'galpoes'
    id_galpao = Column(Integer, primary_key=True)
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
    id = Column(Integer, primary_key=True)
    id_insumos = Column(Integer)
    id_galpoes = Column(Integer)
    nome = Column(String(100))
    fk_blocos_insumos = Column(Integer, ForeignKey('insumos.id_insumo'), nullable=False)
    fk_blocos_galpoes = Column(Integer, ForeignKey('galpoes.id_galpao   '), nullable=False)
    def serialize(self):
        dados = {
            'id': self.id,
            'id_insumos': self.id_insumos,
            'id_galpoes': self.id_galpoes,
            'nome': self.nome,
        }
        return dados

class Setores (Base):
    __tablename__ = 'setores'
    id = Column(Integer, primary_key=True)
    id_insumos = Column(Integer)
    id_galpoes = Column(Integer)
    id_blocos = Column(Integer)
    fk_setores_insumos = Column(Integer, ForeignKey('insumos.id'), nullable=False)
    fk_setores_galpoes = Column(Integer, ForeignKey('galpoes.id'), nullable=False)
    fk_setores_blocos = Column(Integer, ForeignKey('blocos.id'), nullable=False)
    def serialize(self):
        dados = {
            'id': self.id,
            'id_insumos': self.id_insumos,
            'id_galpoes': self.id_galpoes,
            'id_blocos': self.id_blocos,
        }
        return dados

class Sensores (Base):
    __tablename__ = 'sensores'
    id = Column(Integer, primary_key=True)
    id_setor = Column(Integer,ForeignKey('setores.id'), nullable=False)
    id_insumos = Column(Integer,ForeignKey('insumos.id'), nullable=False)
    id_setores = Column(Integer)

    def serialize(self):
        dados = {
            'id': self.id,
            'id_setor': self.id_setor,
            'id_insumos': self.id_insumos,
            'id_setores': self.id_setores,
        }
        return dados

class Leituras (Base):
    __tablename__ = 'leitura'
    id = Column(Integer, primary_key=True)
    id_sensor = Column(Integer,ForeignKey('sensors.id'), nullable=False)
    valor_leitura = Column(Float)
    data_hora= Column(DateTime,default=func.now)

    def serialize(self):
        dados = {
            'id': self.id,
            'id_sensor': self.id_sensor,
            'valor_leitura': self.valor_leitura,
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

    def serialize(self):
        dados = {
            'id': self.id,
            'id_leitura': self.id_leitura,
            'valor_registrado': self.valor_registrado,
            'data_hora_inicio': self.data_hora_inicio,
            'data_hora_fim': self.data_hora_fim,
            'tipo_alerta': self.tipo_alerta,
        }

class Usuarios(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    nome = Column(String(255))
    cpf = Column(String(11))
    email = Column(String(255))

    def serialize(self):
        dados = {
            'id': self.id,
            'nome': self.nome,
            'cpf': self.cpf,
            'email': self.email,
        }
