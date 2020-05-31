from flask import request, jsonify
from flask_restplus import Resource, Namespace, fields
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)

from src.models.login_model import db, Users

api = Namespace('login', description='rotas de login')


@api.route('/')
class Logar_sistema(Resource):
    @api.doc('logar no sistema')
    def post(self):
        """ Rota de login no sistema """

        data = request.get_json()
        print(data)

        current_user = Users.find_by_username(data['email'])
        if not current_user:
            return {'message': 'Usuário não existe'}

        if Users.verify_hash(data['password'], current_user.password):
            access_token = create_access_token(identity=data['email'])
            refresh_token = create_refresh_token(identity=data['email'])
            return {'messagem': 'usuário logado', 'access_token': access_token}
        else:
            return {'message': 'Algo de errado no login'}


       # return Users.return_all()


@api.route('/cadastrar')
class Cadastrar_usuario(Resource):
    @api.doc('cadastar usuario no sistema')
    def post(self):

        data = request.get_json()

        if Users.find_by_username(data['email']):
            return {"message": "Usuário já cadastrado no sistema"}

        novo_usuario = Users(
            name=data['name'], email=data['email'], password=Users.generate_hash(data['password']))

        try:
            novo_usuario.salve_to_db()
            return jsonify(message="Cadastrado com sucesso")
        except:
            return {'message': 'Something went wrong'}, 500


@api.route('/protegida')
class Protegida(Resource):
    @jwt_required
    def get(self):
        return 'rota liberada'
