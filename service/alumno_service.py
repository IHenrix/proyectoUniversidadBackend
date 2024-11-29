from db_connection import get_db_connection, db_config
from models.curso_alumno import CursoAlumno
from models.notas_alumnos import NotasAlumnos

class AlumnoService:
    
    def listar_cursos_por_usuario(self, usuario_id):
        """Obtiene la lista de cursos por usuario con información de docente."""
        connection = get_db_connection(db_config)
        cursor = connection.cursor(dictionary=True)
        cursos = []

        try:
            query = """
                SELECT c.id AS curso_id,uc.id alumno_curso_id ,c.nombre AS curso, c.horas_semanales, c.creditos, c.modalidad,
                       CONCAT(u.nombre, ' ', u.paterno, ' ', u.materno) AS alumno,
                       (SELECT CONCAT(d.nombre, ' ', d.paterno, ' ', d.materno) AS docente
                        FROM docente_curso dc
                        INNER JOIN curso cu ON dc.curso_id = cu.id
                        INNER JOIN usuario d ON dc.usuario_id = d.id
                        WHERE cu.id = c.id AND d.rol_id = 2
                        ORDER BY docente ASC
                        LIMIT 1) AS docente,
                        u.id usuario_id,
                        uc.nota_final,
                        LPAD(CAST(uc.nota_alumno_final AS UNSIGNED), 2, '0') AS nota_alumno_final,
                        uc.estado
                FROM alumno_curso uc
                INNER JOIN curso c ON uc.curso_id = c.id
                INNER JOIN usuario u ON uc.usuario_id = u.id
                WHERE uc.usuario_id = %s AND u.rol_id = 1
                ORDER BY curso ASC;
            """
            cursor.execute(query, (usuario_id,))
            results = cursor.fetchall()

            for result in results:
                curso = CursoAlumno(
                    curso_id=result['curso_id'],
                    curso=result['curso'],
                    horas_semanales=result['horas_semanales'],
                    creditos=result['creditos'],
                    modalidad=result['modalidad'],
                    alumno=result['alumno'],
                    docente=result['docente'],
                    alumno_curso_id=result['alumno_curso_id'],
                    usuario_id=result['usuario_id'],
                    notaFinal=result['nota_final'],
                    notaAlumnoFinal=result['nota_alumno_final'],
                    estado=result['estado']
                )
                cursos.append(curso)
        finally:
            cursor.close()
            connection.close()

        return cursos
    
    def listar_notas_alumnos(self, curso_id, alumno_curso_id):
        """Obtiene la lista de criterios de evaluación con notas de un alumno."""
        connection = get_db_connection(db_config)
        cursor = connection.cursor(dictionary=True)
        notas = []

        try:
            query = """
                SELECT a.id, a.nombre_criterio AS criterio, a.orden, a.porcentaje,
                       n.nota,
                       LPAD(CAST(n.nota_alumno AS UNSIGNED), 2, '0') AS nota_alumno
                FROM criterio_evaluacion a
                LEFT JOIN nota n ON a.id = n.criterio_id AND n.alumno_curso_id = %s
                WHERE a.curso_id = %s
                ORDER BY a.orden ASC;
            """
            cursor.execute(query, (alumno_curso_id, curso_id))
            results = cursor.fetchall()
            for result in results:
                nota = NotasAlumnos(
                    id=result['id'],
                    criterio=result['criterio'],
                    orden=result['orden'],
                    porcentaje=result['porcentaje'],
                    nota=result['nota'],
                    notaAlumno=result['nota_alumno']
                )
                notas.append(nota)
        finally:
            cursor.close()
            connection.close()

        return notas