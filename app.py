from flask import Flask, request, jsonify
from flask_cors import CORS
from service import alumno_service
from service.usuario_service import UsuarioService
from service.alumno_service import AlumnoService
from service.docente_service import DocenteService

app = Flask(__name__)
CORS(app) 

usuario_service = UsuarioService()

alumno_service = AlumnoService()

docente_service = DocenteService()


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

@app.route('/alumno/cursos', methods=['GET'])
def listar_cursos():
    """Endpoint para listar cursos por usuario."""
    usuario_id = request.args.get('usuarioId') 

    cursos = alumno_service.listar_cursos_por_usuario(usuario_id)

    if not cursos:
        return jsonify([]), 200

    return jsonify([curso.__dict__ for curso in cursos]), 200


@app.route('/docente/cursos', methods=['GET'])
def listar_cursos_docente():
    """Endpoint para listar cursos asignados a un docente."""
    docente_id = request.args.get('docenteId') 

    cursos = docente_service.listar_cursos_de_docente(docente_id)

    if not cursos:
        return jsonify([]), 200

    return jsonify([curso.__dict__ for curso in cursos]), 200

@app.route('/docente/cursos/alumnos', methods=['GET'])
def listar_alumnos_por_cursos():
    """Endpoint para listar alumnos por curso."""
    curso_id = request.args.get('cursoId') 

    usuarios = docente_service.listar_alumnos_por_cursos(curso_id)

    if not usuarios:
        return jsonify([]), 200

    return jsonify([usuario.__dict__ for usuario in usuarios]), 200

if __name__ == '__main__':
    app.run(debug=True)
