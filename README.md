# Fluxo criação de formulários

* formulário envia post com parametros de nome dos alunos, lider, data e módulo
* backend recebe e processa os dados (api ENDPOINT Geração)
* responde com um arquivo ZIP com todos os certificados gerados

# Fluxo de checagem de autenticidade

* formuário é preenchido com o UUID
* backend recebe e processa o UUID (api ENDPOINT Checagem)
* responde se válido ou não com um JSON com informações do certificado
* json é exibido no frontend

# Fluxo autenticação de voluntário (OPENID Google)

* voluntário clica em "Login com Google"
* backend recebe e processa credenciais (api ENDPOINT Autenticação)
    * SE TEM LOGIN, acessa página com opção de formulário de geracao de certificados ou checar autenticidade
    * SE NÃO TEM LOGIN, registro de voluntário (API do Victor?)

---

## To Do

[] Fazer formulário html
[] Criar ENDPOINT Geração para geracao de certificados POST
[] Criar ENDPOINT Checagem para responder se o formulário é valido a partir do UUID, também responde sobre a dt_criacao, líder, clube e aluno (Registrados no JSON)
[] Converter JSON em um banco de dados MongoDB