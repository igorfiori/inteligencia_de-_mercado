# 📊 Relatório de Produtos Mais Vendidos

Este projeto tem como objetivo coletar dados sobre produtos de eletrodomésticos na API do Mercado Livre, processá-los, gerar gráficos de vendas e criar relatórios em formatos JSON e Excel. Além disso, ele envia esses relatórios automaticamente por email.

## 🔍 Funcionalidade

- **Coleta de dados**: Utiliza a API do Mercado Livre para buscar informações sobre produtos.
- **Processamento de dados**: Converte os dados em um DataFrame e calcula informações importantes como as vendas dos últimos 6 meses.
- **Visualização de dados**: Gera gráficos de linha representando as vendas mais recentes de produtos.
- **Relatórios**: Cria um relatório com os 5 produtos mais vendidos, tanto em formato JSON quanto em Excel.
- **Envio por email**: Envia os relatórios gerados automaticamente para um destinatário via email.

## 🚀 Tecnologias Usadas

- **Python**: Linguagem principal do projeto.
- **Requests**: Para fazer requisições à API do Mercado Livre.
- **Pandas**: Para manipulação de dados e criação de DataFrame.
- **Matplotlib**: Para gerar gráficos de linha.
- **OpenPyXL**: Para criação de arquivos Excel.
- **SMTP**: Para envio de emails com anexos (relatórios gerados).

## 💻 Como Usar

### 1. Clone o repositório

```bash
git clone https://github.com/seuusuario/nome-do-repositorio.git
```

### 2. Instale as dependências

Instale as bibliotecas necessárias com o pip:

```bash
pip install requests pandas matplotlib openpyxl
```

### 3. Configure seu email

No código, configure seu email, senha e destinatário para o envio dos relatórios:

```python
email_de = "seuemail@dominio.com"
email_para = "emaildestino@dominio.com"
senha = "sua_senha_do_email"
```

### 4. Execute o script

Após realizar as configurações, execute o script `main.py`:

```bash
python main.py
```

### 5. Relatórios gerados

Após a execução do script, você encontrará três arquivos na pasta do projeto:

- **Gráfico de Vendas 📈**: `grafico_linhas.png`
- **Relatório JSON 📝**: `relatorio_produtos.json`
- **Relatório Excel 📊**: `relatorio_produtos.xlsx`

Os relatórios serão enviados por email para o destinatário especificado.

## 📧 Email Enviado

O script enviará automaticamente os arquivos gerados para o email que você configurou, com o assunto **"Relatório de Produtos Mais Vendidos"**.

## 🤖 Como Funciona?

1. O script faz uma requisição para a API do Mercado Livre e coleta os dados dos produtos.
2. Com os dados recebidos, ele gera gráficos de vendas e cria relatórios em formatos JSON e Excel.
3. O script envia esses relatórios por email automaticamente para o destinatário.

## 🛠️ Possíveis Melhorias

- Implementar autenticação para usar outras APIs que exigem credenciais.
- Permitir a personalização da consulta de produtos (exemplo: mais categorias).
- Melhorar a geração de gráficos com mais detalhes e opções de customização.

## 📬 Contatos

- **Autor**: Igor Fiori  
- **Email**: [fioriqf@gmail.com](mailto:fioriqf@gmail.com)

## 💡 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
