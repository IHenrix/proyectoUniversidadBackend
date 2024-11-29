from flask import Flask
from flask_cors import CORS
from controllers.alumno_controller import alumno_blueprint
from controllers.docente_controller import docente_blueprint
from controllers.usuario_controller import usuario_blueprint

app = Flask(__name__)
CORS(app)

# Registrar los Blueprints
app.register_blueprint(alumno_blueprint, url_prefix='/alumno')
app.register_blueprint(docente_blueprint, url_prefix='/docente')
app.register_blueprint(usuario_blueprint, url_prefix='/usuario')

if __name__ == '__main__':
    app.run(debug=True)
