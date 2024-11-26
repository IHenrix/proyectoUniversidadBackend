from flask import Flask, request, jsonify
from flask_cors import CORS
from service.usuario_service import UsuarioService

app = Flask(__name__)
CORS(app) 

usuario_service = UsuarioService()

@app.route('/login', methods=['POST'])
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






if __name__ == '__main__':
    app.run(debug=True)
