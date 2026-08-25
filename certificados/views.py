import logging
import os
import zipfile
from datetime import datetime, timezone

from flask import jsonify, render_template, request, send_file

from . import certificados_bp
from .db import ping_db
from .utils import processar_certificados

logger = logging.getLogger(__name__)


@certificados_bp.route("/health", methods=['GET'])
def health_check():
    db_ok, db_msg = ping_db()
    status_code = 200 if db_ok else 503
    return jsonify({
        "status": "healthy" if db_ok else "unhealthy",
        "database": {
            "connected": db_ok,
            "message": db_msg
        }
    }), status_code

@certificados_bp.route("/")
def index():
    return render_template('index.html')

@certificados_bp.route('/api/v1/generate', methods=['POST'])
def generate_certificates():
    nomes_alunos = request.form.get('students').splitlines()
    nome_lider = request.form.get('leaderName')
    modulo = request.form.get('course')

    logger.info(f"Recebido pedido de geração de certificados para o módulo {modulo} com líder {nome_lider}")
    logger.info(f"Alunos: {nomes_alunos}")

    templates_dir = './templates/pdf'
    output_dir = './temp'
    font_path = './static/assets/arial.ttf'
    os.makedirs(output_dir, exist_ok=True)

    certificados = processar_certificados(modulo, nomes_alunos, nome_lider, templates_dir, output_dir, font_path)

    # Verificar se algum certificado foi gerado
    if not certificados:
        logger.error("Nenhum certificado foi gerado. Verifique se os arquivos de template existem e se os dados fornecidos estão corretos.")
        return jsonify({"error": "Nenhum certificado foi gerado. Verifique se os arquivos de template existem e se os dados fornecidos estão corretos."}), 400

    if len(certificados) > 1:
        data_atual = datetime.now(timezone.utc).strftime("%Y%m%d")
        output_filename = f"{data_atual}_{modulo}_certificados.zip"
        zip_path = os.path.join(output_dir, output_filename)
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for certificado in certificados:
                zipf.write(certificado['path'], os.path.basename(certificado['path']))
        return send_file(zip_path, as_attachment=True)
    else:
        return send_file(certificados[0]['path'], as_attachment=True)

