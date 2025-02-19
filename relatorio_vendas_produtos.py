import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from openpyxl import Workbook
import os

# Obter o diretório atual do projeto
diretorio_atual = os.path.dirname(os.path.abspath(__file__))

# Caminhos relativos para salvar os arquivos
output_path_grafico_linhas = os.path.join(diretorio_atual, "grafico_linhas.png")
output_path_json = os.path.join(diretorio_atual, "relatorio_produtos.json")
output_path_excel = os.path.join(diretorio_atual, "relatorio_produtos.xlsx")

# Ajuste da URL de consulta para um exemplo genérico
url = "https://api.mercadolibre.com/sites/MLB/search?q=eletrodomésticos"

response = requests.get(url)

if response.status_code == 200:
    dados = response.json()
    print("Resposta completa da API:", dados)  # Verificando a resposta completa da API
    if "results" in dados and dados["results"]:
        produtos = dados["results"]
    else:
        print("Nenhum produto encontrado para a consulta.")
        exit()
else:
    print("Erro ao acessar a API:", response.status_code, response.text)
    exit()

# Convertendo para DataFrame e verificando colunas
df = pd.DataFrame(produtos)
print("Primeiras linhas do DataFrame:")
print(df.head())  # Exibindo as primeiras linhas para inspecionar os dados
print("Colunas disponíveis:", df.columns)

# Definindo as colunas que vamos usar, com base nas colunas disponíveis
colunas_necessarias = ['id', 'title', 'price', 'sold_quantity', 'seller']

# Verificando se as colunas existem no DataFrame
colunas_existentes = [col for col in colunas_necessarias if col in df.columns]

if colunas_existentes:
    df = df[colunas_existentes]  # Selecionando as colunas desejadas
else:
    print("Erro: Algumas colunas esperadas não foram encontradas na API.")
    exit()

# Convertendo preços para tipo numérico
df['price'] = pd.to_numeric(df['price'], errors='coerce')  # Convertendo 'price' para valores numéricos

# Verificando a coluna 'sold_quantity' na estrutura dos dados
# Caso ela não esteja presente, vamos tentar capturar uma quantidade através de 'seller'
if 'sold_quantity' not in df.columns:
    print("A coluna 'sold_quantity' não está presente nos dados. Tentando usar outra coluna para determinar a popularidade.")
    # Criando uma coluna fictícia de 'sold_quantity' baseado na quantidade de vendedores como alternativa
    df['sold_quantity'] = df['seller'].apply(lambda x: x.get('carried_out_stock', 0))  # Exemplo usando 'carried_out_stock'

# Adicionando a data das vendas (supondo que a API tenha dados de vendas históricas)
# Caso contrário, vamos simular os dados para efeito de gráfico
meses = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
vendas_simuladas = np.random.randint(50, 200, size=(len(df), 6))  # Simulando vendas de 6 meses

# Adicionando as colunas para os 6 meses no DataFrame
for i, mes in enumerate(meses):
    df[mes] = vendas_simuladas[:, i]

# Calculando a soma das vendas nos últimos 6 meses
df['total_vendas'] = df[meses].sum(axis=1)

# Selecionando os 5 produtos mais vendidos
df_top_5 = df.nlargest(5, 'total_vendas')

# Criando gráfico de linha para as vendas dos últimos 6 meses
try:
    plt.figure(figsize=(10, 6))

    # Gerando o gráfico de linhas para as vendas dos últimos 6 meses
    for i, produto in df_top_5.iterrows():
        plt.plot(meses, produto[meses], label=produto['title'])

    plt.xlabel("Meses")
    plt.ylabel("Vendas")
    plt.title("Vendas dos 5 Produtos Mais Vendidos nos Últimos 6 Meses")
    plt.legend(loc='upper left', bbox_to_anchor=(1.05, 1))  # Ajuste para evitar corte dos nomes
    plt.tight_layout()

    # Salvando o gráfico de linhas
    plt.savefig(output_path_grafico_linhas)
    plt.show()
    print(f"Gráfico de Linhas salvo com sucesso em: {output_path_grafico_linhas}")
except Exception as e:
    print(f"Erro ao criar o gráfico de linhas: {e}")

# Salvando os dados em formato JSON
with open(output_path_json, 'w') as json_file:
    json.dump(df_top_5.to_dict(orient='records'), json_file, indent=4)
    print(f"Relatório JSON salvo em: {output_path_json}")

# Criando a planilha Excel com os dados
df_top_5.to_excel(output_path_excel, index=False)
print(f"Planilha Excel salva em: {output_path_excel}")

# Enviando o relatório por email
def enviar_email():
    email_de = "seuemail@dominio.com"
    email_para = "emaildestino@dominio.com"
    senha = "sua_senha_do_email"
    assunto = "Relatório de Produtos Mais Vendidos"
    corpo_email = "Segue em anexo o relatório de produtos mais vendidos."

    # Criando a mensagem do email
    msg = MIMEMultipart()
    msg['From'] = email_de
    msg['To'] = email_para
    msg['Subject'] = assunto
    msg.attach(corpo_email)

    # Anexando o gráfico de linhas
    attach_file = open(output_path_grafico_linhas, "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attach_file.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f"attachment; filename={output_path_grafico_linhas}")
    msg.attach(part)

    # Anexando o JSON
    attach_file = open(output_path_json, "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attach_file.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f"attachment; filename={output_path_json}")
    msg.attach(part)

    # Anexando a planilha Excel
    attach_file = open(output_path_excel, "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attach_file.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f"attachment; filename={output_path_excel}")
    msg.attach(part)

    # Conectando ao servidor SMTP
    try:
        servidor = smtplib.SMTP('smtp.gmail.com', 587)
        servidor.starttls()
        servidor.login(email_de, senha)
        servidor.sendmail(email_de, email_para, msg.as_string())
        servidor.quit()
        print("Email enviado com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar email: {e}")

# Enviar email
enviar_email()
