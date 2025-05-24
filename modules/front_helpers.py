'''
Arquivo auxiliar para o front end
'''

from django.utils.safestring import mark_safe
import uuid

def tooltip(texto, dica, position="top"):
    return mark_safe(f'<span title="{dica}" data-position="{position}">{texto}</span>')

def badge(texto, cor="primary"):
    cores = {
        "primary": "#007bff",
        "success": "#28a745",
        "danger": "#dc3545",
        "warning": "#ffc107",
        "info": "#17a2b8",
        "dark": "#343a40",
        "light": "#f8f9fa"
    }
    cor_real = cores.get(cor, cor)
    return mark_safe(f'''
    <span style="
        background-color:{cor_real};
        padding:2px 8px;
        border-radius:12px;
        color:#fff;
        font-size:0.8rem;
    ">{texto}</span>
    ''')

def alert(mensagem, tipo="info", dismissible=True):
    alert_id = f"alert-{uuid.uuid4().hex[:6]}"
    close_btn = f'''
        <button type="button" onclick="document.getElementById('{alert_id}').remove();" style="float:right;">×</button>
    ''' if dismissible else ""
    return mark_safe(f'''
    <div id="{alert_id}" style="
        padding: 10px;
        border-radius: 4px;
        margin: 10px 0;
        background-color: {get_alert_color(tipo)};
        color: white;
    ">
        {close_btn}
        {mensagem}
    </div>
    ''')

def get_alert_color(tipo):
    return {
        "success": "#28a745",
        "info": "#17a2b8",
        "warning": "#ffc107",
        "danger": "#dc3545"
    }.get(tipo, "#17a2b8")

def icon(icone_nome, cor="black", tamanho="16px"):
    return mark_safe(f'''
        <i class="{icone_nome}" style="color:{cor};font-size:{tamanho};"></i>
    ''')

def spinner(tamanho="40px", cor="#333"):
    return mark_safe(f'''
    <div class="spinner" style="
        width: {tamanho};
        height: {tamanho};
        border: 5px solid {cor};
        border-top-color: transparent;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin:auto;
    "></div>
    <style>
        @keyframes spin {{
            to {{ transform: rotate(360deg); }}
        }}
    </style>
    ''')

def botao(texto, tipo="button", cor="blue", onclick=None, id=None):
    _id = id or f"btn-{uuid.uuid4().hex[:6]}"
    return mark_safe(f'''
    <button id="{_id}" type="{tipo}" style="
        background-color:{cor};
        color:white;
        padding:8px 16px;
        border:none;
        border-radius:6px;
        cursor:pointer;
    " {'onclick="'+onclick+'"' if onclick else ""}>
        {texto}
    </button>
    ''')

def incluir_script(caminho, externo=True):
    if externo:
        return mark_safe(f'<script src="{caminho}"></script>')
    return mark_safe(f'<script>{caminho}</script>')

def incluir_css(caminho, externo=True):
    if externo:
        return mark_safe(f'<link rel="stylesheet" href="{caminho}">')
    return mark_safe(f'<style>{caminho}</style>')

def modal(id_modal, titulo, conteudo, largura="50%"):
    return mark_safe(f'''
    <div id="{id_modal}" style="display:none; position:fixed; z-index:1000; left:0; top:0; width:100%; height:100%; background:rgba(0,0,0,0.5);">
        <div style="background:white; margin:10% auto; padding:20px; border-radius:8px; width:{largura};">
            <h3>{titulo}</h3>
            <div>{conteudo}</div>
            <button onclick="document.getElementById('{id_modal}').style.display='none'">Fechar</button>
        </div>
    </div>
    <script>
        function abrirModal_{id_modal}() {{
            document.getElementById('{id_modal}').style.display = 'block';
        }}
    </script>
    ''')

def tabela(headers, dados):
    cabecalho = ''.join([f'<th>{h}</th>' for h in headers])
    linhas = ''
    for linha in dados:
        linhas += '<tr>' + ''.join([f'<td>{str(c)}</td>' for c in linha]) + '</tr>'
    return mark_safe(f'''
    <table style="width:100%; border-collapse: collapse;">
        <thead style="background:#eee;">
            <tr>{cabecalho}</tr>
        </thead>
        <tbody>{linhas}</tbody>
    </table>
    ''')

def input_text(name, valor="", placeholder="", width="100%"):
    return mark_safe(f'''
        <input type="text" name="{name}" value="{valor}" placeholder="{placeholder}" style="width:{width};padding:8px;border-radius:6px;border:1px solid #ccc;">
    ''')

def input_hidden(name, valor):
    return mark_safe(f'<input type="hidden" name="{name}" value="{valor}">')
