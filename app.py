import os

from flask import Flask

from certificados import certificados_bp
from config import Config

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config.from_object(Config)

# Registrar o blueprint
app.register_blueprint(certificados_bp)

if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_DEBUG', 'false').lower() in ('true', '1', 't')
    app.run(debug=debug_mode)

