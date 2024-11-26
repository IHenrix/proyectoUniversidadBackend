from db_connection import get_db_connection, db_config
from models.usuario import Usuario

class UserService:
    
    def get_users(self):
        """Obtiene todos los usuarios de la tabla 'usuario'."""
        connection = get_db_connection(db_config)
        cursor = connection.cursor(dictionary=True)

        try:
            cursor.execute("SELECT * FROM usuario")
            users = cursor.fetchall()

            # Convertimos los resultados en instancias de la clase Usuario
            usuarios = [
                Usuario(
                    id=user['id'],
                    username=user['username'],
                    passw=user['pass'],
                    nombre=user['nombre'],
                    paterno=user['paterno'],
                    materno=user['materno'],
                    rol_id=user['rol_id'],
                    activo=user['activo']
                )
                for user in users
            ]
        finally:
            cursor.close()
            connection.close()

        return usuarios
