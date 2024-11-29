class CursoAlumno:
    def __init__(self, curso_id, curso, horas_semanales, creditos, modalidad, alumno, docente,alumno_curso_id,usuario_id,notaFinal,notaAlumnoFinal,estado):
        self.curso_id = curso_id
        self.curso = curso
        self.horas_semanales = horas_semanales
        self.creditos = creditos
        self.modalidad = modalidad
        self.alumno = alumno
        self.docente = docente
        self.alumno_curso_id=alumno_curso_id
        self.usuario_id=usuario_id
        self.notaFinal = notaFinal
        self.notaAlumnoFinal = notaAlumnoFinal
        self.estado = estado