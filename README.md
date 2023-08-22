# UFRPE-BSI 2022.2 | Modelagem de Dados

## Grupo 2 - Juno

No seguinte repositório encontra-se as análises em Streamlit desenvolvidas pelo Grupo 2 (Juno) para a disciplina de Modelagem de Dados.

## Dependências do Projeto

Para instalar as depedências necessárias para o funcionamento do projeto, que foi desenvolvido em Python, basta executar o seguinte comando:

    pip install -r requirements.txt

No arquivo "requirements.txt" estão listadas as bibliotecas/módulos utilizados e suas versões.

## Variáveis de Ambiente

Agora, para rodar o projeto localmente é necessário acessar o arquivo "streamlit_app.py", navegar para a linha 8 e substitutir as seguintes variáveis, como indicado a seguir:

    def estabelecer_conexao_bd():
        connection = mysql.connector.connect(
            host="YOUR_MYSQL_HOST",
            user="YOUR_MYSQL_USER",
            password="YOUR_MYSQL_PASSWORD",
            database="DATABASE_NAME"
        )
        return connection

## Execução do Projeto (Local)

Para executar o projeto basta rodar o seguinte comando no terminal, na pasta do projeto:

    python3 -m streamlit run streamlit_app.py

## Execução do Projeto (Remoto)

Para executar o projeto remotamente basta acessar:

    https://narwhal-nearby-adder.ngrok-free.app/
