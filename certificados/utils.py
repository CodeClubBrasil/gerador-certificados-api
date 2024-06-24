import os
import logging
import uuid
from pymongo import MongoClient
from io import BytesIO
from fillpdf import fillpdfs
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from flask import current_app
from .models import Certificado, CertificadoSchema

def get_db():
    client = MongoClient(current_app.config['MONGO_URI'])
    db = client['ccbrcertificados']
    return db

def preencher_campos_pdf(template_path, nome_aluno, nome_lider, output_path):
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

    # Certifique-se de que page_width e page_height são números
    page_width, page_height = letter
    if isinstance(page_width, tuple):
        page_width, page_height = page_width

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
    os.makedirs(output_dir, exist_ok=True)
    certificados = []

    logging.info(f"Processando certificados para o módulo {modulo} com líder {nome_lider}")

    db = get_db()

    for i, nome_aluno in enumerate(nomes_alunos):
        template_path = os.path.join(templates_dir, f'{modulo}.pdf')
        output_path = os.path.join(output_dir, f"certificado_{modulo}_{nome_aluno}.pdf")

        logging.info(f"Processando certificado para {nome_aluno}")
        logging.info(f"Usando template: {template_path}")

        if not os.path.exists(template_path):
            logging.error(f"Template não encontrado: {template_path}")
            continue

        try:
            filled_pdf_path = preencher_campos_pdf(template_path, nome_aluno, nome_lider, output_path)
            logging.info(f"PDF preenchido salvo em: {filled_pdf_path}")

            certificado_uuid = adicionar_uuid_pdf(filled_pdf_path, output_path, font_path)
            logging.info(f"UUID adicionado: {certificado_uuid}")

            certificados.append({'path': output_path, 'uuid': certificado_uuid})

            certificado_data = {
                "uuid": certificado_uuid,
                "aluno": nome_aluno,
                "lider": nome_lider,
                "modulo": modulo,
                "arquivo": output_path
            }
            db.certificados.insert_one(certificado_data)
        except Exception as e:
            logging.error(f"Erro ao processar certificado para {nome_aluno}: {e}")

    logging.info(f"{len(certificados)} certificados foram gerados.")
    return certificados
