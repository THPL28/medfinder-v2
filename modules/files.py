import os

def ler_arquivo(caminho):
    with open(caminho, 'r', encoding='utf-8') as f:
        return f.read()

def salvar_arquivo(caminho, conteudo):
    with open(caminho, 'w', encoding='utf-8') as f:
        f.write(conteudo)

def listar_arquivos_pasta(pasta, extensao=None):
    arquivos = []
    for arquivo in os.listdir(pasta):
        if extensao is None or arquivo.endswith(extensao):
            arquivos.append(arquivo)
    return arquivos
