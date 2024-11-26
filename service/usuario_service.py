from db_connection import get_db_connection, db_config
from models.usuario import Usuario

class UsuarioService:
    def login(self, username, password):

        connection = get_db_connection(db_config)
        cursor = connection.cursor(dictionary=True)
        usuario = None

        try:
            query = "SELECT * FROM usuario u WHERE u.username = %s AND u.pass = %s"
            cursor.execute(query, (username, password))
            user = cursor.fetchone()

            if user:
                usuario = Usuario(
                    id=user['id'],
                    username=user['username'],
                    passw=user['pass'],
                    nombre=user['nombre'],
                    paterno=user['paterno'],
                    materno=user['materno'],
                    sexo=user['sexo'],
                    correo=user['correo'],
                    rol_id=user['rol_id'],
                    activo=user['activo']
                )
        finally:
            cursor.close()
            connection.close()

        return usuario
