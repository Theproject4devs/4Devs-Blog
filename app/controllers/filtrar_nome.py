import re


def filtrar_nome_arquivo(nome_arquivo):
    return re.sub(r'\W+', ' ', nome_arquivo)
