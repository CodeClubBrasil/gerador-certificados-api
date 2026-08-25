from unittest.mock import MagicMock, patch

from certificados.models import Certificado, CertificadoSchema


def test_certificado_schema_deserialization():
    data = {
        "uuid": "test-uuid-1234",
        "aluno": "João Silva",
        "lider": "Maria Santos",
        "modulo": "python1",
        "arquivo": "/path/to/cert.pdf",
    }
    schema = CertificadoSchema()
    certificado = schema.load(data)

    assert isinstance(certificado, Certificado)
    assert certificado.uuid == "test-uuid-1234"
    assert certificado.aluno == "João Silva"
    assert certificado.lider == "Maria Santos"
    assert certificado.modulo == "python1"
    assert certificado.arquivo == "/path/to/cert.pdf"


def test_certificado_save():
    cert = Certificado(
        uuid="uuid-123",
        aluno="Ana",
        lider="Carlos",
        modulo="scratch1",
        arquivo="/tmp/cert.pdf",
    )

    with patch("certificados.models.get_db") as mock_get_db:
        mock_db = MagicMock()
        mock_get_db.return_value = mock_db

        cert.save()

        mock_get_db.assert_called_once()
        mock_db.certificados.insert_one.assert_called_once_with({
            "uuid": "uuid-123",
            "aluno": "Ana",
            "lider": "Carlos",
            "modulo": "scratch1",
            "arquivo": "/tmp/cert.pdf",
        })
