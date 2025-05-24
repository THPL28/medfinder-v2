"""
FRONT_HELPERS - Guia de Uso Completo

Este módulo fornece funções auxiliares para geração dinâmica de componentes HTML
úteis para projetos Django, permitindo retorno direto em views ou integração com templates.

IMPORTAÇÃO:
    from utils.front_helpers import *

-----------------------------

🟦 tooltip(texto, dica, position="top")
Cria um span com título (tooltip) ao passar o mouse.

Exemplo:
    tooltip("Ajuda", "Clique aqui para ajuda")

-----------------------------

🟩 badge(texto, cor="primary")
Cria um selo colorido com texto.

Exemplo:
    badge("Novo", "success")

-----------------------------

🟥 alert(mensagem, tipo="info", dismissible=True)
Cria um alerta estilizado com cor e botão de fechar.

Tipos disponíveis: success, info, warning, danger

Exemplo:
    alert("Item salvo com sucesso!", tipo="success")

-----------------------------

⚪ icon(icone_nome, cor="black", tamanho="16px")
Insere um ícone com classe customizada (ex: FontAwesome, Bootstrap Icons).

Exemplo:
    icon("fa fa-check", cor="green", tamanho="24px")

-----------------------------

🔄 spinner(tamanho="40px", cor="#333")
Gera um loader animado.

Exemplo:
    spinner()

-----------------------------

🔘 botao(texto, tipo="button", cor="blue", onclick=None, id=None)
Cria um botão estilizado com evento JS opcional.

Exemplo:
    botao("Salvar", onclick="alert('Salvo!')")

-----------------------------

📜 incluir_script(caminho, externo=True)
Adiciona um script externo ou inline.

Exemplo externo:
    incluir_script("https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js")

Exemplo inline:
    incluir_script("console.log('Hello');", externo=False)

-----------------------------

🎨 incluir_css(caminho, externo=True)
Adiciona CSS externo ou inline.

Exemplo:
    incluir_css("https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css")

-----------------------------

🧱 modal(id_modal, titulo, conteudo, largura="50%")
Cria um modal com ID e botão para fechar.

Exemplo:
    modal("infoModal", "Título do Modal", "Conteúdo aqui")

Para abrir via botão:
    botao("Abrir", onclick="abrirModal_infoModal()")

-----------------------------

📊 tabela(headers, dados)
Cria uma tabela HTML com cabeçalhos e dados.

Exemplo:
    headers = ["Nome", "Idade"]
    dados = [["Tiago", 28], ["Ana", 32]]
    tabela(headers, dados)

-----------------------------

🔠 input_text(name, valor="", placeholder="", width="100%")
Cria um input de texto com placeholder.

Exemplo:
    input_text("nome", placeholder="Digite seu nome")

-----------------------------

📥 input_hidden(name, valor)
Cria um input hidden (invisível) para formulários.

Exemplo:
    input_hidden("token", "123abc")

"""

# Exemplo real: renderizando uma view
from django.http import HttpResponse
from utils.front_helpers import *

def view_demo(request):
    html = f"""
    <html>
    <head><title>Demo Front Helpers</title></head>
    <body style="font-family:sans-serif; padding:20px;">

        <h1>Exemplos</h1>

        {tooltip("Ajuda", "Clique aqui para ajuda")}
        <br><br>

        {badge("Versão Beta", "warning")}
        <br><br>

        {alert("Isso é um alerta!", tipo="info")}
        <br><br>

        {icon("fa fa-check", cor="green", tamanho="20px")}
        <br><br>

        {spinner()}
        <br><br>

        {botao("Clique-me", onclick="alert('Clicado!')")}
        <br><br>

        {modal("idModal", "Título Modal", "Este é o conteúdo do modal")}
        {botao("Abrir Modal", onclick="abrirModal_idModal()")}
        <br><br>

        {tabela(["Nome", "Idade"], [["Tiago", 28], ["Ana", 32]])}
        <br><br>

        <form method="post">
            {input_text("nome", placeholder="Seu nome")}
            {input_hidden("csrf_token", "ABC123")}
            {botao("Enviar", tipo="submit")}
        </form>

    </body>
    </html>
    """
    return HttpResponse(html)
