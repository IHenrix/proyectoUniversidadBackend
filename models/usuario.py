class Usuario:
    def __init__(self, id, username, passw, nombre, paterno, materno,sexo,correo, rol_id, activo):
        self.id = id
        self.username = username
        self.passw = passw
        self.nombre = nombre
        self.paterno = paterno
        self.materno = materno
        self.sexo = sexo
        self.correo = correo
        self.rol_id = rol_id
        self.activo = activo