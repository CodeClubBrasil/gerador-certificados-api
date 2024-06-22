# Code Clube: Gerador de Certificado

Este projeto é uma aplicação web para gerar certificados personalizados para alunos de clubes de programação. Os usuários podem preencher um formulário com os nomes dos alunos, o nome do líder do clube e o curso, e a aplicação gera certificados em PDF.

## Funcionalidades

- Geração de certificados em PDF com nomes personalizados.
- Adição de um UUID único a cada certificado.
- Compactação dos certificados em um arquivo ZIP se houver mais de um certificado.
- Formulário web para entrada de dados.
- API para geração de certificados via requisição POST.

## Instalação

### Pré-requisitos

- Python 3.6 ou superior
- pip (gerenciador de pacotes do Python)

### Passos para Instalação

1. Clone este repositório:
   ```bash
   git clone https://github.com/seuusuario/code-clube-certificados.git
   cd code-clube-certificados

2. Crie um ambiente virtual: 
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows use `venv\Scripts\activate`

3. Instale dependências
    ```bash
    pip install -r requirements.txt

4. Configure a estrutura de diretórios:
    ```bash
    mkdir -p templates/pdf
    mkdir -p static/assets

5. Adicione os arquivos PDF de templates em `templates/pdf` e a fonte `arial.ttf` em `static/assets`.

## Uso 

### Executando a Aplicação

Para iniciar o servidor Flask, execute: 
    ```bash
    python app.py

A aplicação estará disponível em `http://127.0.0.1:5000`.

### Formulário Web

* Acesse http://127.0.0.1:5000/.

* Preencha os campos do formulário:
    * Alunos: Insira um nome por linha.
    * Líder: Insira o nome do líder do clube.
    * Curso: Selecione o curso.
    * Clique em "Gerar certificados".

### Endpoints da API

`POST /api/v1/generate`
Gera certificados com base nos dados fornecidos.

#### Parâmetros do Formulário

* `students` (texto): Nomes dos alunos, um por linha.
* `leaderName` (texto): Nome do líder do clube.
* `course` (texto): Nome do curso (ex.: python1, scratch2).

#### Exemplo de requisição
```bash
curl -X POST http://127.0.0.1:5000/api/v1/generate \
    -F "students=Aluno1\nAluno2\nAluno3" \
    -F "leaderName=Líder do Clube" \
    -F "course=python1" \
    --output result.zip
```

## Estrutura do Projeto

```code-clube-certificados/
    ├── app.py
    ├── limpar_temp.py
    ├── templates/
    │   └── index.html
    ├── static/
    │   ├── img/
    │   │   └── logo.png
    │   ├── css/
    │   │   └── style.css
    │   └── assets/
    │       └── arial.ttf
    ├── requirements.txt
    └── README.md
```

## Tecnologias

* Flask: Framework web para Python.
* fillpdf: Biblioteca para preenchimento de formulários PDF.
* PyPDF2: Biblioteca para manipulação de arquivos PDF.
* reportlab: Biblioteca para geração de PDFs.
* Bootstrap: Framework CSS para design responsivo.

## Contribuição
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

### Passos para Contribuir
1. Fork este repositório.
2. Crie uma branch para sua feature/bugfix (git checkout -b feature/nova-feature).
3. Commit suas alterações (git commit -am 'Adiciona nova feature').
4. Push para a branch (git push origin feature/nova-feature).
5. Abra um Pull Request.

## Licença
Este projeto está licenciado sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.
