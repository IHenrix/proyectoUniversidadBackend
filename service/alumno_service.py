from db_connection import get_db_connection, db_config
from models.curso_alumno import CursoAlumno

class AlumnoService:
    
    def listar_cursos_por_usuario(self, usuario_id):
        """Obtiene la lista de cursos por usuario con información de docente."""
        connection = get_db_connection(db_config)
        cursor = connection.cursor(dictionary=True)
        cursos = []

        try:
            # Consulta SQL con subconsulta para obtener el docente
            query = """
                SELECT c.id, c.nombre AS curso, c.horas_semanales, c.creditos, c.modalidad,
                       CONCAT(u.nombre, ' ', u.paterno, ' ', u.materno) AS alumno,
                       (SELECT CONCAT(d.nombre, ' ', d.paterno, ' ', d.materno) AS docente
                        FROM docente_curso dc
                        INNER JOIN curso cu ON dc.curso_id = cu.id
                        INNER JOIN usuario d ON dc.usuario_id = d.id
                        WHERE cu.id = c.id AND d.rol_id = 2
                        ORDER BY docente ASC
                        LIMIT 1) AS docente
                FROM alumno_curso uc
                INNER JOIN curso c ON uc.curso_id = c.id
                INNER JOIN usuario u ON uc.usuario_id = u.id
                WHERE uc.usuario_id = %s AND u.rol_id = 1
                ORDER BY curso ASC;
            """
            cursor.execute(query, (usuario_id,))
            results = cursor.fetchall()

            # Convertimos los resultados en instancias de la clase CursoAlumno
            for result in results:
                curso = CursoAlumno(
                    id=result['id'],
                    curso=result['curso'],
                    horas_semanales=result['horas_semanales'],
                    creditos=result['creditos'],
                    modalidad=result['modalidad'],
                    alumno=result['alumno'],
                    docente=result['docente']
                )
                cursos.append(curso)
        finally:
            cursor.close()
            connection.close()

        return cursos
