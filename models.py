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
    id_setor = Column(Integer)
    tipo = Column(String(255))
    nome = Column(String(100))
    umidade_max = Column(Integer)
    umidade_min = Column(Integer)
    temperatura_max = Column(Integer)
    temperatura_min = Column(Integer)
    def serialize(self, centro=None):
        dados = {
            'id': self.id_insumo,
            'idSensores': self.id_setor,
            'tipo': self.tipo,
            'nome': self.nome,
            'umidade_max': self.umidade_max,
            'umidade_min': self.umidade_min,
            'temperatura_max': self.temperatura_max,
            'temperatura_min': self.temperatura_min,
        }
        return dados

class Galpoes(Base):
    __tablename__ = 'galpoes'
    id = Column(Integer, primary_key=True)
    descricao = Column(String(255))
    nome = Column(String(100))
    id_insumos = Column(Integer)
    FK_Galpoes_Insumos = Column(Integer, ForeignKey('insumos.id'), nullable=False)
    def serialize(self):
        dados = {
            'id': self.id,
            'descricao': self.descricao,
            'nome': self.nome,
            'id_insumos': self.id_insumos,
        }
        return dados

class Blocos(Base):
    __tablename__ = 'blocos'
    id = Column(Integer, primary_key=True)
    id_insumos = Column(Integer)
    id_galpoes = Column(Integer)
    nome = Column(String(100))
    FK_Blocos_Insumos = Column(Integer, ForeignKey('insumos.id'), nullable=False)
    FK_Blocos_Galpoes = Column(Integer, ForeignKey('galpoes.id'), nullable=False)
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
    idInsumos = Column(Integer)
    idGalpoes = Column(Integer)
    idBlocos = Column(Integer)
    FK_Setores_Insumos = Column(Integer, ForeignKey('insumos.id'), nullable=False)
    FK_Setores_Galpoes = Column(Integer, ForeignKey('galpoes.id'), nullable=False)
    FK_Setores_Blocos = Column(Integer, ForeignKey('blocos.id'), nullable=False)
    def serialize(self):
        dados = {
            'id': self.id,
            'idInsumos': self.idInsumos,
            'idGalpoes': self.idGalpoes,
            'idBlocos': self.idBlocos,
        }
        return dados

class Sensores (Base):
    __tablename__ = 'sensores'
    id = Column(Integer, primary_key=True)
    id_setor = Column(Integer,ForeignKey('setores.id'), nullable=False)
    id_insumos = Column(Integer,ForeignKey('insumos.id'), nullable=False)
    id_Setores = Column(Integer)

    def serialize(self):
        dados = {
            'id': self.id,
            'id_setor': self.id_setor,
            'id_insumos': self.id_insumos,
            'id_Setores': self.id_Setores,
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
            'idSensor': self.id_sensor,
            'valor_leitura': self.valor_leitura,
            'data_hora': self.data_hora,
        }
        return dados

class AlertaOcorrencias(Base):
    __tablename__ = 'alerta_ocorrencias'
    id = Column(Integer, primary_key=True)
    idLeitura = Column(Integer,ForeignKey('leitura.id'), nullable=False)
    valor_registrado = Column(Float)
    data_hora_inicio= Column(DateTime)
    data_hora_fim= Column(DateTime)
    tipo_alerta = Column(Integer)

    def serialize(self):
        dados = {
            'id': self.id,
            'idLeitura': self.idLeitura,
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
