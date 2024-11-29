from flask import Blueprint, request, jsonify
from service.usuario_service import UsuarioService

usuario_blueprint = Blueprint('usuario', __name__)
usuario_service = UsuarioService()

@usuario_blueprint.route('/login', methods=['POST'])
def login():
    """Endpoint para autenticar usuario."""
    data = request.json
    username = data.get('usuario')
    password = data.get('pass')

    if not username or not password:
        return '', 400 

    usuario = usuario_service.login(username, password)

    if not usuario:
        return '', 204

    return jsonify(usuario.__dict__), 200