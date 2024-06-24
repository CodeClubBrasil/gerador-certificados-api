from flask import Flask
from config import Config
from certificados import certificados_bp

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config.from_object(Config)

# Registrar o blueprint
app.register_blueprint(certificados_bp)

if __name__ == '__main__':
    app.run(debug=True)
