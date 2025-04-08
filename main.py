import csv
import json
import os
import shutil
from collections import defaultdict
import pandas as pd

# Definir variáveis
diretorio_publicacao = 'docs/'
site_url = 'https://tasparasurdos.github.io/api/'

# Definir o ID da planilha de tecnologias
google_sheets_tecnologias_id = '1g-zamZFp5FHTGxZOA0vT3ULXjwROhWS0mz0_K1xTvXc'

# Construir a URL de exportação para CSV
url_tecnologias = f'https://docs.google.com/spreadsheets/d/{google_sheets_tecnologias_id}/export?format=csv'

# Criar diretório se não existir
print(f"Verificando/criando diretório '{diretorio_publicacao}'...")
os.makedirs(diretorio_publicacao, exist_ok=True)

# Copiar o arquivo index.html para dentro do diretório de publicação
print(f"Copiando 'index.html' para o diretório '{diretorio_publicacao}'...")
shutil.copy('index.html', diretorio_publicacao)

# Copiar o diretório imagens/ para dentro do diretório de publicação
print(f"Copiando o diretório 'imagens/' para '{diretorio_publicacao}'...")
shutil.copytree('imagens', os.path.join(diretorio_publicacao, 'imagens'), dirs_exist_ok=True)

# Colunas que estarão no JSON de cada tecnologia
colunas_json = [
    'titulo', 'descricao', 'orientacao', 'dicas', 'etapas_justificativa',
    'imagem', 'categoria', 'custo', 'requer_internet', 'plataformas',
    'autor', 'link', 'etapas'
]

# Dicionários para os índices
indice = []  # Para indice.json
categorias = defaultdict(list)  # Para categorias.json
custos = defaultdict(list)  # Para custo.json
etapas_ensino = defaultdict(list)  # Para etapas_ensino.json
requer_internet_dict = defaultdict(list)  # Para requer_internet.json
plataformas_dict = defaultdict(list)  # Para plataformas.json
descricoes_categorias = {}  # Para armazenar descricao_categoria

print("Iniciando leitura dos dados do Google Sheets...")
# Ler os dados do Google Sheets usando pandas
try:
    df = pd.read_csv(url_tecnologias)
    print("Dados de 'tecnologias' carregados com sucesso do Google Sheets.")
except Exception as e:
    print(f"Erro ao carregar 'tecnologias' do Google Sheets: {e}")
    exit(1)

# Converter o DataFrame para uma lista de dicionários
reader = df.to_dict(orient='records')
total_linhas = len(reader)

# Processar cada linha
for i, row in enumerate(reader, 1):
    print(f"Processando linha {i} de {total_linhas}: {row['titulo']}...")
    
    # Criar objeto com apenas as colunas desejadas
    tech_data = {coluna: row[coluna] for coluna in colunas_json if coluna in row}
    
    # Ajustar caminho da imagem
    if tech_data.get('imagem'):
        tech_data['imagem'] = f"{site_url}imagens/{tech_data['imagem']}"
        
    # Nome do arquivo usando o slug
    filename = os.path.join(diretorio_publicacao, f"{row['slug']}.json")
    
    # Escrever o arquivo JSON individual
    with open(filename, 'w', encoding='utf-8') as jsonfile:
        json.dump(tech_data, jsonfile, ensure_ascii=False, indent=2)
    
    # Adicionar ao índice
    indice.append({
        'titulo': row['titulo'],
        'imagem': f"{site_url}imagens/{row['slug']}-icon.jpg",
        'slug': row['slug'],
        'custo': row['custo'],
        'requer_internet': row['requer_internet'],
        'plataformas': row['plataformas'],
        'etapas': row['etapas'],
        'apresentacao': row['apresentacao'],
    })
    
    # Adicionar às categorias e guardar descrição
    categorias[row['categoria']].append({
        'titulo': row['titulo'],
        'imagem': f"{site_url}imagens/{row['imagem']}",
        'slug': row['slug'],
        'custo': row['custo'],
        'requer_internet': row['requer_internet'],
        'plataformas': row['plataformas'],
        'etapas': row['etapas'],
        'apresentacao': row['apresentacao'],
    })
    descricoes_categorias[row['categoria']] = row['categoria_descricao']
    
    # Adicionar aos custos
    custos[row['custo']].append({
        'titulo': row['titulo'],
        'arquivo': f"{row['slug']}.json"
    })
    
    # Adicionar às etapas de ensino, separando por ponto e vírgula
    etapas = row['etapas'].split(';') if row['etapas'] else ['Não especificado']
    for etapa in etapas:
        etapa_limpa = etapa.strip()
        if etapa_limpa:
            etapas_ensino[etapa_limpa].append({
                'titulo': row['titulo'],
                'arquivo': f"{row['slug']}.json"
            })
        
    # Adicionar ao requer_internet
    requer_internet_dict[row['requer_internet']].append({
        'titulo': row['titulo'],
        'arquivo': f"{row['slug']}.json"
    })
    
    # Adicionar às plataformas, separando por vírgula
    plataformas = row['plataformas'].split(',') if row['plataformas'] else ['Não especificado']
    for plataforma in plataformas:
        plat_limpa = plataforma.strip()
        if plat_limpa:
            plataformas_dict[plat_limpa].append({
                'titulo': row['titulo'],
                'arquivo': f"{row['slug']}.json"
            })

print("Ordenando índices alfabeticamente...")
# Ordenar o índice alfabeticamente pelo título
indice.sort(key=lambda x: x['titulo'].lower())

# Ordenar as listas dentro de cada dicionário
for cat in categorias:
    categorias[cat].sort(key=lambda x: x['titulo'].lower())
for custo in custos:
    custos[custo].sort(key=lambda x: x['titulo'].lower())
for etapa in etapas_ensino:
    etapas_ensino[etapa].sort(key=lambda x: x['titulo'].lower())
for req in requer_internet_dict:
    requer_internet_dict[req].sort(key=lambda x: x['titulo'].lower())
for plat in plataformas_dict:
    plataformas_dict[plat].sort(key=lambda x: x['titulo'].lower())

# Preparar categorias com descrição
categorias_com_desc = {}
for cat, tecnologias in categorias.items():
    categorias_com_desc[cat] = {
        'descricao': descricoes_categorias[cat],
        'tecnologias': tecnologias
    }

print("Gerando arquivos de índice...")
# Escrever os arquivos de índice
with open(os.path.join(diretorio_publicacao, 'indice.json'), 'w', encoding='utf-8') as f:
    json.dump(indice, f, ensure_ascii=False, indent=2)
    print("Arquivo 'indice.json' gerado.")

with open(os.path.join(diretorio_publicacao, 'categorias.json'), 'w', encoding='utf-8') as f:
    json.dump(categorias_com_desc, f, ensure_ascii=False, indent=2)
    print("Arquivo 'categorias.json' gerado com descrições.")

with open(os.path.join(diretorio_publicacao, 'custo.json'), 'w', encoding='utf-8') as f:
    json.dump(dict(custos), f, ensure_ascii=False, indent=2)
    print("Arquivo 'custo.json' gerado.")

with open(os.path.join(diretorio_publicacao, 'etapas_ensino.json'), 'w', encoding='utf-8') as f:
    json.dump(dict(etapas_ensino), f, ensure_ascii=False, indent=2)
    print("Arquivo 'etapas_ensino.json' gerado.")

with open(os.path.join(diretorio_publicacao, 'requer_internet.json'), 'w', encoding='utf-8') as f:
    json.dump(dict(requer_internet_dict), f, ensure_ascii=False, indent=2)
    print("Arquivo 'requer_internet.json' gerado.")

with open(os.path.join(diretorio_publicacao, 'plataformas.json'), 'w', encoding='utf-8') as f:
    json.dump(dict(plataformas_dict), f, ensure_ascii=False, indent=2)
    print("Arquivo 'plataformas.json' gerado.")

print("Processamento concluído com sucesso!")
