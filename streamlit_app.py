import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px

# Estabelece a conexão com o banco de dados
def estabelecer_conexao_bd():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='1234',
        database='junobaseorigem'
    )
    return connection

def main():
    st.title("Juno")
    st.header("Bairros")
    page = st.radio("Selecione uma opção:", ("Bairros de Origem", "Bairros de Destino"))

    if page == "Bairros de Origem":
        st.subheader("Bairros de Origem")
        coluna = "origem.Bairro"
        cabecalho = "Bairro de Origem"
        latitude_col = "origem.Latitude"
        longitude_col = "origem.Longitude"
    elif page == "Bairros de Destino":
        st.subheader("Bairros de Destino")
        coluna = "destino.Bairro"
        cabecalho = "Bairro de Destino"
        latitude_col = "destino.Latitude"
        longitude_col = "destino.Longitude"

    data_inicial = st.date_input("Data Inicial")
    data_final = st.date_input("Data Final")

    if page == "Bairros de Origem" or page == "Bairros de Destino":
        if st.button("Gerar Mapa"):
            # Estabelece uma conexão
            conexao = estabelecer_conexao_bd()

            # Converte as datas para o formato do banco de dados
            data_inicial_formatada = data_inicial.strftime('%Y-%m-%d')
            data_final_formatada = data_final.strftime('%Y-%m-%d')

            # Executa a consulta SQL
            query = f"""
                SELECT {coluna}, COUNT(*) AS TotalViagens, {latitude_col}, {longitude_col}
                FROM Deslocamento d
                JOIN Endereco origem ON d.OrigemID = origem.ID
                JOIN Endereco destino ON d.DestinoID = destino.ID
                JOIN Data dt ON d.DataID = dt.ID
                WHERE dt.Data BETWEEN '{data_inicial_formatada}' AND '{data_final_formatada}'
                GROUP BY {coluna}, {latitude_col}, {longitude_col}
                """

            df = pd.read_sql(query, conexao)
            conexao.close()

            df['TotalViagens'] = pd.to_numeric(df['TotalViagens'])  # Converte a coluna TotalViagens para numérica

            total_viagens = df['TotalViagens'].sum()
            st.write(f"Total de Viagens: {total_viagens}")

            df['Latitude'] = df['Latitude'].astype(float)
            df['Longitude'] = df['Longitude'].astype(float)

            df.rename(columns={'Latitude': 'LAT', 'Longitude': 'LON'}, inplace=True)
            st.map(df[['LAT', 'LON', 'Bairro', 'TotalViagens']])

    
    page = "Viagens por Dia da Semana"
    st.header("Viagens por Dia da Semana")
    st.subheader("Selecione uma data:")

    data_inicial = st.date_input(f"Data Inicial ({page})", key=f"data_inicial_{page}")
    data_final = st.date_input(f"Data Final ({page})", key=f"data_final_{page}")

    if page == "Viagens por Dia da Semana": 
        if st.button(f"Gerar gráfico", key=f"gerar_grafico_{page}"):
            conexao = estabelecer_conexao_bd()
            # Converte as datas para o formato do banco de dados
            data_inicial_formatada = data_inicial.strftime('%Y-%m-%d')
            data_final_formatada = data_final.strftime('%Y-%m-%d')

            # Executa a consulta SQL para viagens por dia da semana
            query = f"""
                SELECT dt.DiaNumeroNaSemana AS DiaSemana,
                    COUNT(*) AS TotalViagens
                FROM Deslocamento d
                JOIN Data dt ON d.DataID = dt.ID
                WHERE dt.Data BETWEEN '{data_inicial_formatada}' AND '{data_final_formatada}'
                GROUP BY DiaSemana
            """
            x_labels = {
                1:'Segunda-feira',
                2: 'Terça-feira',
                3: 'Quarta-feira',
                4: 'Quinta-feira',
                5: 'Sexta-feira',
                6: 'Sábado', 
                7: 'Domingo',
            }
            # Usa o pandas para executar a consulta e obter o resultado
            df = pd.read_sql(query, conexao)
            df['DiaSemana'] = df['DiaSemana'].map(x_labels)

            df['DiaSemana'] = pd.Categorical(df['DiaSemana'], categories=list(x_labels.values()), ordered=True)
            df = df.sort_values('DiaSemana')

            # Gera o gráfico de barras usando Plotly
            fig = px.bar(df, x='DiaSemana', y='TotalViagens', labels={'TotalViagens': 'Total de Viagens'})
            st.plotly_chart(fig)

    page = "Viagens por turnos"
    st.header("Viagens por turnos")
    st.subheader("Selecione uma data:")

    data_inicial = st.date_input(f"Data Inicial ({page})", key=f"data_inicial_{page}")
    data_final = st.date_input(f"Data Final ({page})", key=f"data_final_{page}")

    if page == "Viagens por turnos": 
        if st.button(f"Gerar gráfico", key=f"gerar_grafico_{page}"):
            conexao = estabelecer_conexao_bd()
            # Converte as datas para o formato do banco de dados
            data_inicial_formatada = data_inicial.strftime('%Y-%m-%d')
            data_final_formatada = data_final.strftime('%Y-%m-%d')

            # Executa a consulta SQL para viagens por dia da semana
            query = f"""SELECT h.Turno, COUNT(*) AS TotalCaronas
                FROM Deslocamento d
                JOIN Horario h ON d.HorarioID = h.ID
                JOIN Data dt ON d.DataID = dt.ID
                WHERE dt.Data BETWEEN '{data_inicial_formatada}' AND '{data_final_formatada}'
                GROUP BY h.Turno;
            """
            # Usa o pandas para executar a consulta e obter o resultado
            df = pd.read_sql(query, conexao)

            # Gera o gráfico de barras usando Plotly
            fig = px.bar(df, x='Turno', y='TotalCaronas', labels={'TotalCaronas': 'Total de Caronas'})
            st.plotly_chart(fig)

    page = "Caronas oferecidas por curso"
    st.header("Caronas oferecidas por curso")
    st.subheader("Selecione uma data:")

    data_inicial = st.date_input(f"Data Inicial ({page})", key=f"data_inicial_{page}")
    data_final = st.date_input(f"Data Final ({page})", key=f"data_final_{page}")

    if page == "Caronas oferecidas por curso": 
        if st.button(f"Gerar gráfico", key=f"gerar_grafico_{page}"):
            conexao = estabelecer_conexao_bd()
            # Converte as datas para o formato do banco de dados
            data_inicial_formatada = data_inicial.strftime('%Y-%m-%d')
            data_final_formatada = data_final.strftime('%Y-%m-%d')

            # Executa a consulta SQL para quantidade de caronas oferecidas por curso
            query = f"""SELECT cs.Nome AS CursoNome,
                    COUNT(*) AS TotalCaronas
                FROM Deslocamento d
                JOIN Data dt ON d.DataID = dt.ID
                JOIN ParticipanteDeslocamento pd ON d.ID = pd.ID
                JOIN Sigaa sg ON pd.ID = sg.ID
                JOIN Cursos cs ON sg.cursoID = cs.ID
                WHERE dt.Data BETWEEN '{data_inicial_formatada}' AND '{data_final_formatada}'
                GROUP BY CursoNome
            """
            # Usa o pandas para executar a consulta e obter o resultado
            df = pd.read_sql(query, conexao)

            # Gera o gráfico de barras usando Plotly
            fig = px.bar(df, x='CursoNome', y='TotalCaronas', labels={'TotalCaronas': 'Total de Caronas', 'CursoNome': 'Nome do Curso'})
            st.plotly_chart(fig)

# Executa o aplicativo Streamlit
if __name__ == "__main__":
    main()
