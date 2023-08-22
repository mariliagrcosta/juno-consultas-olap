import streamlit as st
import os
import mysql.connector
import pandas as pd
import plotly.express as px
from datetime import datetime, date, timedelta

def estabelecer_conexao_bd():
    connection = mysql.connector.connect(
        host="YOUR_MYSQL_HOST",
        user="YOUR_MYSQL_USER",
        password="YOUR_MYSQL_PASSWORD",
        database="DATABASE_NAME"
    )
    return connection

def main():
    
    st.title("Juno")

    st.sidebar.title("Juno")

    pages = {
        "Viagens por Bairros": bairros_page,
        "Viagens por Dia da Semana": viagens_dia_semana_page,
        "Viagens por Turnos": viagens_turno_page,
        "Caronas por Curso": caronas_curso_page,
    }

    page = st.sidebar.radio("Selecione uma página", list(pages.keys()))
    pages[page]()

def bairros_page():
    st.header("Viagens por Bairros")
    page = st.radio("Selecione uma opção:", ("Bairros de Origem", "Bairros de Destino"))

    if page == "Bairros de Origem":
        coluna = "origem.bairro"
        cabecalho = "Bairro de Origem"
        latitude_col = "origem.Latitude"
        longitude_col = "origem.Longitude"
    elif page == "Bairros de Destino":
        coluna = "destino.bairro"
        cabecalho = "Bairro de Destino"
        latitude_col = "destino.Latitude"
        longitude_col = "destino.Longitude"

    data_inicial = st.date_input("Data Inicial")
    data_final = st.date_input("Data Final")
    
    dias_semana = st.multiselect("Selecione os dias da semana", ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"])

    if page == "Bairros de Origem" or page == "Bairros de Destino":
        if st.button("Gerar Mapa"):
            conexao = estabelecer_conexao_bd()

            data_inicial_formatada = data_inicial.strftime('%Y-%m-%d')
            data_final_formatada = data_final.strftime('%Y-%m-%d')
            
            dias_semana_numeros = [1 if "Segunda-feira" in dias_semana else 0,
                                   2 if "Terça-feira" in dias_semana else 0,
                                   3 if "Quarta-feira" in dias_semana else 0,
                                   4 if "Quinta-feira" in dias_semana else 0,
                                   5 if "Sexta-feira" in dias_semana else 0,
                                   6 if "Sábado" in dias_semana else 0,
                                   7 if "Domingo" in dias_semana else 0]

            query = f"""
                SELECT {coluna}, COUNT(*) AS TotalViagens, {latitude_col}, {longitude_col}
                FROM FatoDeslocamento AS fd
                JOIN DimEndereco AS origem ON fd.dimenderecoorigem_codigo = origem.dimendereco_codigo
                JOIN DimEndereco AS destino ON fd.dimenderecodestino_codigo = destino.dimendereco_codigo
                JOIN DimData AS dd ON fd.dimdata_codigo = dd.dimdata_codigo
                WHERE dd.data BETWEEN '{data_inicial_formatada}' AND '{data_final_formatada}'
                    AND dd.dia_numeronasemana IN ({','.join(map(str, dias_semana_numeros))})
                GROUP BY {coluna}, {latitude_col}, {longitude_col}
            """

            df = pd.read_sql(query, conexao)
            conexao.close()

            df['TotalViagens'] = pd.to_numeric(df['TotalViagens'])  

            total_viagens = df['TotalViagens'].sum()
            st.write(f"Total de Viagens: {total_viagens}")

            df['Latitude'] = df['Latitude'].astype(float)
            df['Longitude'] = df['Longitude'].astype(float)

            df.rename(columns={'Latitude': 'LAT', 'Longitude': 'LON'}, inplace=True)
            st.map(df[['LAT', 'LON', 'bairro', 'TotalViagens']])

def viagens_dia_semana_page():
    st.header("Viagens por Dia da Semana")
    st.subheader("Selecione uma data:")
    
    data_inicial = st.date_input("Data Inicial")
    dataFinalInput = st.selectbox(
        "Número de Semanas", (1, 2, 3, 4))
    
    dataMult = dataFinalInput * 7

    dataFinal = data_inicial + timedelta(days=dataMult)

    
    # dias_semana = st.multiselect("Selecione os dias da semana", ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"])

    if st.button("Gerar gráfico"):
        conexao = estabelecer_conexao_bd()
        
        data_inicial_formatada = data_inicial.strftime('%Y-%m-%d')
        data_final_formatada = dataFinal.strftime('%Y-%m-%d')
        
        # dias_semana_numeros = [1 if "Segunda-feira" in dias_semana else 0,
        #                        2 if "Terça-feira" in dias_semana else 0,
        #                        3 if "Quarta-feira" in dias_semana else 0,
        #                        4 if "Quinta-feira" in dias_semana else 0,
        #                        5 if "Sexta-feira" in dias_semana else 0,
        #                        6 if "Sábado" in dias_semana else 0,
        #                        7 if "Domingo" in dias_semana else 0]

        query = f"""
            SELECT dt.dia_numeronasemana AS DiaSemana,
                COUNT(*) AS TotalViagens
            FROM FatoDeslocamento fd
            JOIN DimData dt ON fd.dimdata_codigo = dt.dimdata_codigo
            WHERE dt.data BETWEEN '{data_inicial_formatada}' AND '{data_final_formatada}'
            GROUP BY DiaSemana
        """
        x_labels = {
            1: 'Segunda-feira',
            2: 'Terça-feira',
            3: 'Quarta-feira',
            4: 'Quinta-feira',
            5: 'Sexta-feira',
            6: 'Sábado',
            7: 'Domingo',
        }

        df = pd.read_sql(query, conexao)
        df['DiaSemana'] = df['DiaSemana'].map(x_labels)

        df['DiaSemana'] = pd.Categorical(df['DiaSemana'], categories=list(x_labels.values()), ordered=True)
        df = df.sort_values('DiaSemana')

        fig = px.bar(df, x='DiaSemana', y='TotalViagens', labels={'TotalViagens': 'Total de Viagens', "DiaSemana": "Dias da semana"})
        st.plotly_chart(fig)

def viagens_turno_page():
    st.header("Viagens por Turnos")
    st.subheader("Selecione uma data:")

    data_inicial = st.date_input("Data Inicial")
    data_final = st.date_input("Data Final")
    
    if st.button(f"Gerar gráfico", key="gerar_grafico_viagens_turno"):
        conexao = estabelecer_conexao_bd()
        
        data_inicial_formatada = data_inicial.strftime('%Y-%m-%d')
        data_final_formatada = data_final.strftime('%Y-%m-%d')

        query = f"""
            SELECT h.Turno, COUNT(*) AS TotalCaronas
            FROM FatoDeslocamento f
            JOIN DimHorario h ON f.dimhorario_codigo = h.dimhorario_codigo
            JOIN DimData dt ON f.dimdata_codigo = dt.dimdata_codigo
            WHERE dt.data BETWEEN '{data_inicial_formatada}' AND '{data_final_formatada}'
            GROUP BY h.turno;
        """
        
        df = pd.read_sql(query, conexao)

        fig = px.bar(df, x='Turno', y='TotalCaronas', labels={'TotalCaronas': 'Total de Caronas'})
        fig.update_layout(barmode='stack', xaxis={'categoryorder':'array', 'categoryarray':['Manhã','Tarde','Noite','Madrugada']})
        st.plotly_chart(fig)

def caronas_curso_page():
    st.header("Caronas oferecidas por curso")
    st.subheader("Selecione uma data:")

    data_inicial = st.date_input("Data Inicial")
    data_final = st.date_input("Data Final")
    
    if st.button(f"Gerar gráfico", key="gerar_grafico_caronas_curso"):
        conexao = estabelecer_conexao_bd()

        data_inicial_formatada = data_inicial.strftime('%Y-%m-%d')
        data_final_formatada = data_final.strftime('%Y-%m-%d')

        query = f"""SELECT da.nomecurso, COUNT(*) AS TotalCaronas
            FROM FatoDeslocamento fd
            JOIN DimData dt ON fd.dimdata_codigo = dt.dimdata_codigo
            JOIN DimAluno da ON fd.dimaluno_codigo = da.dimaluno_codigo
            JOIN DimData dd ON fd.dimdata_codigo = dd.dimdata_codigo
            WHERE dt.Data BETWEEN '{data_inicial_formatada}' AND '{data_final_formatada}'
            GROUP BY da.nomecurso;
        """

        df = pd.read_sql(query, conexao)

        fig = px.bar(df, x='TotalCaronas', y='nomecurso', labels={'TotalCaronas': 'Total de Caronas', 'nomecurso': 'Nome do Curso'} , height=850)

        fig.update_layout(barmode='stack', yaxis={'categoryorder': 'total descending'})
        st.plotly_chart(fig)

if __name__ == "__main__":
    main()

