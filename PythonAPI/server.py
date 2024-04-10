from flask import Flask, request,  jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine, text
from json import dumps

db_connect = create_engine('mysql+mysqlconnector://root@localhost/alunodb')

app = Flask(__name__)
api = Api(app)


class Test(Resource):
    def get(self):
        return('{"message": "Servidor funcionando corretamente"}')


class Users(Resource):
    def get (self):
        # faz a conexão junto ao banco
        conn = db_connect.connect()
        # monta a consulta ao banco e executa a consulta junto ao
        query = conn.execute(
            text('select * from alunos order by id'))
        #
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        # retorna resultado da consulta
        return jsonify(result)
    
    def post(self):
        conn = db_connect.connect()
        name = request.json['name']
        email = request.json['email']
        conn.execute(text("insert into alunos (nome, email) values ( '{0}', '{1}')".format(name, email)))
        conn.commit()
        query = conn.execute(text('select * from alunos order by id'))
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        return jsonify(result)
    
    def put(self):
        conn = db_connect.connect()
        id = request.json['id']
        name = request.json['name']
        email = request.json['email']
        conn.execute(text("update user set nome ='" + str(name) + "', email = '" + str(email) + "' where id =%d" %int(id)))
        conn.commit()
        query = conn.execute(text('select * from alunos where id=%d ' % int(id)))
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        return jsonify(result)

api.add_resource(Test, '/test')
api.add_resource(Users, '/users')


if __name__ == '__main__':
    app.run()