from db_connection import get_db_connection, db_config
from models.alumno_lista_curso import AlumnoListaCurso
from models.curso_docente import CursoDocente

class DocenteService:
    def listar_cursos_de_docente(self, docente_id):
        """Obtiene la lista de cursos asignados a un docente."""
        connection = get_db_connection(db_config)
        cursor = connection.cursor(dictionary=True)
        cursos = []

        try:
            query = """
                SELECT c.id, c.nombre AS curso, c.horas_semanales, c.creditos, c.modalidad
                FROM docente_curso dc
                INNER JOIN curso c ON dc.curso_id = c.id
                INNER JOIN usuario u ON dc.usuario_id = u.id
                WHERE dc.usuario_id = %s AND u.rol_id = 2
                ORDER BY curso ASC;
            """
            cursor.execute(query, (docente_id,))
            results = cursor.fetchall()
            for result in results:
                curso = CursoDocente(
                    id=result['id'],
                    curso=result['curso'],
                    horas_semanales=result['horas_semanales'],
                    creditos=result['creditos'],
                    modalidad=result['modalidad']
                )
                cursos.append(curso)
        finally:
            cursor.close()
            connection.close()

        return cursos

    def listar_alumnos_por_cursos(self, curso_id):
        """Obtiene la lista de alumnos por cursos."""
        connection = get_db_connection(db_config)
        cursor = connection.cursor(dictionary=True)
        alumnoListaCursos = []

        try:
            query = """
                SELECT 
                uc.usuario_id id,
                u.nombre,u.paterno,u.materno,u.codigo
                FROM alumno_curso uc
                INNER JOIN usuario u ON uc.usuario_id=u.id
                WHERE uc.curso_id=%s
                ORDER BY paterno asc;
            """
            cursor.execute(query, (curso_id,))
            results = cursor.fetchall()
            for result in results:
                alumnoListaCurso = AlumnoListaCurso(
                    id=result['id'],
                    nombre=result['nombre'],
                    paterno=result['paterno'],
                    materno=result['materno'],
                    codigo=result['codigo']
                )
                alumnoListaCursos.append(alumnoListaCurso)
        finally:
            cursor.close()
            connection.close()

        return alumnoListaCursos
