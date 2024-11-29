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
                SELECT c.id, c.nombre AS curso, c.horas_semanales, c.creditos, c.modalidad,
                (SELECT count(*) FROM alumno_curso cc where cc.curso_id=c.id and activo=true) alumnos
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
                    modalidad=result['modalidad'],
                    alumnos=result['alumnos'],

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
                uc.id,
                uc.nota_final,
                LPAD(CAST(uc.nota_alumno_final AS UNSIGNED), 2, '0') AS nota_alumno_final,
                uc.estado,
                u.nombre,u.paterno,u.materno,u.codigo,
                uc.nota_alumno_real
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
                    codigo=result['codigo'],
                    notaFinal=result['nota_final'],
                    notaAlumnoFinal=result['nota_alumno_final'],
                    estado=result['estado'],
                    notaAlumnoReal=result['nota_alumno_real']
                )
                alumnoListaCursos.append(alumnoListaCurso)
        finally:
            cursor.close()
            connection.close()

        return alumnoListaCursos

    def registrar_o_editar_notas(self, alumno_curso_id, curso_id, notas):
        """Registra, edita o elimina las notas del alumno."""
        connection = get_db_connection(db_config)
        cursor = connection.cursor()
        try:
            for nota in notas:
                criterio_id = nota.get('id')
                nota_valor = self._convert_to_valid_number(nota.get('nota'))
                nota_alumno = self._convert_to_valid_number(nota.get('notaAlumno'))
                cursor.execute(
                    "SELECT COUNT(*) FROM nota WHERE criterio_id = %s AND alumno_curso_id = %s",
                    (criterio_id, alumno_curso_id)
                )
                count = cursor.fetchone()[0]

                if count > 0:
                    if nota_valor is None or nota_alumno is None:
                        cursor.execute(
                            "DELETE FROM nota WHERE criterio_id = %s AND alumno_curso_id = %s",
                            (criterio_id, alumno_curso_id)
                        )
                    else:
                        cursor.execute(
                            """
                            UPDATE nota
                            SET nota = %s, nota_alumno = %s
                            WHERE criterio_id = %s AND alumno_curso_id = %s
                            """,
                            (nota_valor, nota_alumno, criterio_id, alumno_curso_id)
                        )
                elif nota_valor is not None and nota_alumno is not None:
                    cursor.execute(
                        """
                        INSERT INTO nota (alumno_curso_id, criterio_id, nota, nota_alumno)
                        VALUES (%s, %s, %s, %s)
                        """,
                        (alumno_curso_id, criterio_id, nota_valor, nota_alumno)
                    )

            if all(
                self._is_valid_nota(n.get('nota')) and self._is_valid_nota(n.get('notaAlumno'))
                for n in notas
            ):
                promedio_nota = sum(
                    float(n['nota']) * (float(n['porcentaje']) / 100)
                    for n in notas
                )
                promedio_nota_alumno = sum(
                    float(n['notaAlumno']) * (float(n['porcentaje']) / 100)
                    for n in notas
                )
                

                promedio_nota_alumno_transformed = self.nota_favor_alumno(promedio_nota_alumno)


                estado = 'A' if promedio_nota_alumno >= 11.6 else 'D'

                cursor.execute(
                    """
                    UPDATE alumno_curso
                    SET nota_final = %s, nota_alumno_final = %s, estado = %s, nota_alumno_real = %s
                    WHERE id = %s
                    """,
                    (promedio_nota, promedio_nota_alumno_transformed, estado,promedio_nota_alumno,alumno_curso_id)
                )
            else:
                cursor.execute(
                    """
                    UPDATE alumno_curso
                    SET nota_final = NULL, nota_alumno_final = NULL, nota_alumno_real = NULL, estado = 'E'
                    WHERE id = %s
                    """,
                    (alumno_curso_id,)
                )

            connection.commit() 
        except Exception as e:
            connection.rollback()
            raise e
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def _convert_to_valid_number(value):
        """Convierte un valor vacío ('') o inválido en None; valida números"""
        try:
            return float(value) if value not in (None, '') else None
        except ValueError:
            return None

    @staticmethod
    def _is_valid_nota(value):
        """Valida si una nota es un número válido"""
        try:
            return value is not None and float(value) >= 0
        except ValueError:
            return False
        
    @staticmethod
    def nota_favor_alumno(value: float) -> str:
        """Redondea el valor según las reglas dadas (>= 0.6) y devuelve el resultado como un string."""
        decimal_part = round(value % 1, 2) 
        rounded = int(value) + 1 if decimal_part >= 0.6 else int(value)
        return f"0{rounded}" if rounded < 10 else str(rounded)

    def eliminar_nota(self, nota_id, alumno_curso_id):
        """
        Elimina una nota específica basad en su ID y valida si quedan notas asociadas al alumno
        Si no quedan notas, actualiza alumno_curso para resetear los campos
        """
        connection = get_db_connection(db_config)
        cursor = connection.cursor()
        try:
            cursor.execute("DELETE FROM nota WHERE id = %s", (nota_id,))
            filas_afectadas = cursor.rowcount
            if filas_afectadas > 0:
                
                cursor.execute("SELECT count(*) FROM alumno_curso WHERE id=%s and estado='E'", (alumno_curso_id,))
                count = cursor.fetchone()[0]

                if count == 0:
                    cursor.execute(
                        """
                        UPDATE alumno_curso
                        SET nota_final = NULL, nota_alumno_final = NULL, nota_alumno_real = NULL, estado = 'E'
                        WHERE id = %s
                        """,
                        (alumno_curso_id,)
                    )

            connection.commit() 
            return filas_afectadas
        except Exception as e:
            connection.rollback()
            raise e
        finally:
            cursor.close()
            connection.close()