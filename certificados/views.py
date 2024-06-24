from flask import request, send_file, jsonify, render_template
from datetime import datetime
import os
import zipfile
from . import certificados_bp
from .utils import processar_certificados
import logging

@certificados_bp.route("/")
def index():
    return render_template('index.html')

@certificados_bp.route('/api/v1/generate', methods=['POST'])
def generate_certificates():
    nomes_alunos = request.form.get('students').splitlines()
    nome_lider = request.form.get('leaderName')
    modulo = request.form.get('course')

    logging.info(f"Recebido pedido de geração de certificados para o módulo {modulo} com líder {nome_lider}")
    logging.info(f"Alunos: {nomes_alunos}")

    templates_dir = './templates/pdf'
    output_dir = './temp'
    font_path = './static/assets/arial.ttf'
    os.makedirs(output_dir, exist_ok=True)

    certificados = processar_certificados(modulo, nomes_alunos, nome_lider, templates_dir, output_dir, font_path)

    # Verificar se algum certificado foi gerado
    if not certificados:
        logging.error("Nenhum certificado foi gerado. Verifique se os arquivos de template existem e se os dados fornecidos estão corretos.")
        return jsonify({"error": "Nenhum certificado foi gerado. Verifique se os arquivos de template existem e se os dados fornecidos estão corretos."}), 400

    if len(certificados) > 1:
        data_atual = datetime.now().strftime("%Y%m%d")
        output_filename = f"{data_atual}_{modulo}_certificados.zip"
        zip_path = os.path.join(output_dir, output_filename)
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for certificado in certificados:
                zipf.write(certificado['path'], os.path.basename(certificado['path']))
        return send_file(zip_path, as_attachment=True)
    else:
        return send_file(certificados[0]['path'], as_attachment=True)
