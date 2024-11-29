from flask import Blueprint, request, jsonify
from service.alumno_service import AlumnoService

alumno_blueprint = Blueprint('alumno', __name__)
alumno_service = AlumnoService()

@alumno_blueprint.route('/cursos', methods=['GET'])
def listar_cursos():
    """Endpoint para listar cursos por usuario."""
    usuario_id = request.args.get('usuarioId') 

    cursos = alumno_service.listar_cursos_por_usuario(usuario_id)

    if not cursos:
        return jsonify([]), 200

    return jsonify([curso.__dict__ for curso in cursos]), 200

@alumno_blueprint.route('/notas', methods=['GET'])
def listar_notas_alumno():
    """Endpoint para listar notas de un alumno."""
    curso_id = request.args.get('cursoId')
    alumno_curso_id = request.args.get('alumnoCursoId')
    notas = alumno_service.listar_notas_alumnos(curso_id, alumno_curso_id)

    if not notas:
        return jsonify([]), 200

    return jsonify([nota.__dict__ for nota in notas]), 200
