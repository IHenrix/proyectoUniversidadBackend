from flask import Blueprint, request, jsonify
from service.docente_service import DocenteService

docente_blueprint = Blueprint('docente', __name__)
docente_service = DocenteService()

@docente_blueprint.route('/cursos', methods=['GET'])
def listar_cursos_docente():
    """Endpoint para listar cursos asignados a un docente."""
    docente_id = request.args.get('docenteId') 

    cursos = docente_service.listar_cursos_de_docente(docente_id)

    if not cursos:
        return jsonify([]), 200

    return jsonify([curso.__dict__ for curso in cursos]), 200

@docente_blueprint.route('/cursos/alumnos', methods=['GET'])
def listar_alumnos_por_cursos():
    """Endpoint para listar alumnos por curso."""
    curso_id = request.args.get('cursoId') 

    usuarios = docente_service.listar_alumnos_por_cursos(curso_id)

    if not usuarios:
        return jsonify([]), 200

    return jsonify([usuario.__dict__ for usuario in usuarios]), 200

@docente_blueprint.route('/registrar-editar-notas', methods=['POST'])
def registrar_o_editar_notas():
    """Endpoint para registrar o editar notas."""
    data = request.json
    alumno_curso_id = data.get('alumnoCursoId')
    curso_id = data.get('cursoId')
    notas = data.get('notas')

    try:
        docente_service.registrar_o_editar_notas(alumno_curso_id, curso_id, notas)
        return jsonify({"message": "Notas registradas o editadas con éxito"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@docente_blueprint.route('/nota/<int:nota_id>/alumno/<int:alumno_curso_id>', methods=['DELETE'])
def eliminar_nota(nota_id, alumno_curso_id):
    """
    Endpoint para eliminar una nota y validar si quedan notas asociadas.
    La URL incluye nota_id y alumno_curso_id.
    """
    try:
        filas_afectadas = docente_service.eliminar_nota(nota_id, alumno_curso_id)
        if filas_afectadas > 0:
            return jsonify({"message": "Nota eliminada con éxito"}), 200
        else:
            return jsonify({"message": "Nota no encontrada"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
