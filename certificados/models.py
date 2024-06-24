from pymongo import MongoClient
from marshmallow import Schema, fields, post_load
from flask import current_app

def get_db():
    client = MongoClient(current_app.config['MONGO_URI'])
    db = client['ccbrcertificados']
    return db

class Certificado:
    def __init__(self, uuid, aluno, lider, modulo, arquivo):
        self.uuid = uuid
        self.aluno = aluno
        self.lider = lider
        self.modulo = modulo
        self.arquivo = arquivo

    def save(self):
        db = get_db()
        db.certificados.insert_one(self.__dict__)

class CertificadoSchema(Schema):
    uuid = fields.Str()
    aluno = fields.Str(required=True)
    lider = fields.Str(required=True)
    modulo = fields.Str(required=True)
    arquivo = fields.Str(required=True)

    @post_load
    def make_certificado(self, data, **kwargs):
        return Certificado(**data)
