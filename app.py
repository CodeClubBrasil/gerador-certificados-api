from flask import Flask, request, send_file, jsonify, render_template
import os
import zipfile
import uuid
import json
from io import BytesIO
from fillpdf import fillpdfs
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

app = Flask(__name__, static_folder='static', template_folder='templates')

# Conectar ao MongoDB
mongo_uri = os.getenv('MONGO_URI')
client = MongoClient(mongo_uri)
db = client['ccbrcertificados']  # Nome do banco de dados


def preencher_campos_pdf(template_path, nome_aluno, nome_lider, output_path):
    """Preenche os campos do formulário PDF usando fillpdf."""
    data_dict = {
        'txt_aluno': nome_aluno,
        'txt_lider': nome_lider
    }
    temp_filled_path = output_path.replace(".pdf", "_filled.pdf")
    fillpdfs.write_fillable_pdf(template_path, temp_filled_path, data_dict)
    fillpdfs.flatten_pdf(temp_filled_path, temp_filled_path)
    return temp_filled_path


def adicionar_uuid_pdf(filled_pdf_path, output_path, font_path):
    """Adiciona um UUID ao PDF preenchido usando reportlab e PyPDF2."""
    certificado_uuid = str(uuid.uuid4())

    # Criar o UUID usando reportlab e embutir uma fonte TrueType ou OpenType
    uuid_packet = BytesIO()
    can = canvas.Canvas(uuid_packet, pagesize=letter)
    font_name = os.path.splitext(os.path.basename(font_path))[0]
    pdfmetrics.registerFont(TTFont(font_name, font_path))
    can.setFont(font_name, 8)
    page_width, page_height = letter
    x_position = (page_width / 2) - 50
    y_position = 73
    can.drawString(x_position, y_position, certificado_uuid)
    can.save()
    uuid_packet.seek(0)

    # Mesclar o UUID com o PDF preenchido
    uuid_pdf = PdfReader(uuid_packet)
    uuid_page = uuid_pdf.pages[0]

    pdf_reader = PdfReader(filled_pdf_path)
    pdf_writer = PdfWriter()

    for i, page in enumerate(pdf_reader.pages):
        if i == 0:
            page.merge_page(uuid_page)
        pdf_writer.add_page(page)

    with open(output_path, "wb") as output_stream:
        pdf_writer.write(output_stream)

    os.remove(filled_pdf_path)

    return certificado_uuid


def processar_certificados(modulo, nomes_alunos, nome_lider, templates_dir, output_dir, font_path):
    """Processa os certificados para todos os alunos e salva os dados em um arquivo JSON."""
    os.makedirs(output_dir, exist_ok=True)
    certificados = []

    for i, nome_aluno in enumerate(nomes_alunos):
        template_path = os.path.join(templates_dir, f'{modulo}.pdf')
        output_path = os.path.join(output_dir, f"certificado_{modulo}_{nome_aluno}.pdf")

        try:
            filled_pdf_path = preencher_campos_pdf(template_path, nome_aluno, nome_lider, output_path)
            certificado_uuid = adicionar_uuid_pdf(filled_pdf_path, output_path, font_path)
            certificados.append({'path': output_path, 'uuid': certificado_uuid})

            # Inserir dados no MongoDB
            certificado_data = {
                "uuid": certificado_uuid,
                "aluno": nome_aluno,
                "lider": nome_lider,
                "modulo": modulo,
                "arquivo": output_path
            }
            db.certificados.insert_one(certificado_data)
        except Exception as e:
            print(f"Erro ao processar certificado para {nome_aluno}: {e}")

    return certificados


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/api/v1/generate', methods=['POST'])
def generate_certificates():
    nomes_alunos = request.form.get('students').splitlines()
    nome_lider = request.form.get('leaderName')
    modulo = request.form.get('course')

    templates_dir = './templates/pdf'
    output_dir = './temp'
    font_path = './static/assets/arial.ttf'
    os.makedirs(output_dir, exist_ok=True)

    certificados = processar_certificados(
        modulo, nomes_alunos, nome_lider, templates_dir, output_dir, font_path)

    # Se houver mais de dois certificados, criar um arquivo zip
    if len(certificados) > 1:

        # Obter a data atual no formato AAAAMMDD
        data_atual = datetime.now().strftime('%Y%m%d')

        output_filename = f'{data_atual}_{modulo}_certificados.zip'

        zip_path = os.path.join(output_dir, output_filename)
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for certificado in certificados:
                zipf.write(certificado['path'],
                           os.path.basename(certificado['path']))
        return send_file(zip_path, as_attachment=True)
    else:
        return send_file(certificados[0]['path'], as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
