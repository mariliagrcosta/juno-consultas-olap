import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px
import os


def estabelecer_conexao_bd():
    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USERNAME"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
    return connection


def pagina_bairros(page):
    st.title("Juno - Bairros de Origem")
    page = st.radio("Selecione uma opção:", ("Bairros de Origem", "Bairros de Destino"))

    if page == "Bairros de Origem":
        coluna = "origem.Bairro"
        latitude_col = "origem.Latitude"
        longitude_col = "origem.Longitude"
    elif page == "Bairros de Destino":
        coluna = "destino.Bairro"
        latitude_col = "destino.Latitude"
        longitude_col = "destino.Longitude"

    data_inicial = st.date_input("Data Inicial")
    data_final = st.date_input("Data Final")

    if st.button("Gerar Mapa"):
        
        conexao = estabelecer_conexao_bd()

        
        data_inicial_formatada = data_inicial.strftime('%Y-%m-%d')
        data_final_formatada = data_final.strftime('%Y-%m-%d')

        
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

        df['TotalViagens'] = pd.to_numeric(df['TotalViagens'])  

        total_viagens = df['TotalViagens'].sum()
        st.write(f"Total de Viagens: {total_viagens}")

        df['Latitude'] = df['Latitude'].astype(float)
        df['Longitude'] = df['Longitude'].astype(float)

        df.rename(columns={'Latitude': 'LAT', 'Longitude': 'LON'}, inplace=True)
        st.map(df[['LAT', 'LON', 'Bairro', 'TotalViagens']])

def pagina_viagens_dia_semana(page):
    st.header("Viagens por Dia da Semana")
    st.subheader("Selecione uma data:")
    
    data_inicial = st.date_input("Data Inicial")
    data_final = st.date_input("Data Final")
    
    dias_semana = st.multiselect("Selecione os dias da semana", ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"])

    if st.button("Gerar gráfico"):
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
            SELECT dt.DiaNumeroNaSemana AS DiaSemana,
                COUNT(*) AS TotalViagens
            FROM Deslocamento d
            JOIN Data dt ON d.DataID = dt.ID
            WHERE dt.Data BETWEEN '{data_inicial_formatada}' AND '{data_final_formatada}'
                AND dt.DiaNumeroNaSemana IN ({','.join(map(str, dias_semana_numeros))})
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

        fig = px.bar(df, x='DiaSemana', y='TotalViagens', labels={'TotalViagens': 'Total de Viagens'})
        st.plotly_chart(fig)
        

def pagina_viagens_turnos(page):
    st.title("Juno - Viagens por Turnos")
    st.header("Viagens por turnos")
    st.subheader("Selecione uma data:")

    data_inicial = st.date_input(f"Data Inicial ({page})", key=f"data_inicial_{page}")
    data_final = st.date_input(f"Data Final ({page})", key=f"data_final_{page}")
    
    if st.button(f"Gerar gráfico", key=f"gerar_grafico_{page}"):
        conexao = estabelecer_conexao_bd()
        
        data_inicial_formatada = data_inicial.strftime('%Y-%m-%d')
        data_final_formatada = data_final.strftime('%Y-%m-%d')

        
        query = f"""SELECT h.Turno, COUNT(*) AS TotalCaronas
            FROM Deslocamento d
            JOIN Horario h ON d.HorarioID = h.ID
            JOIN Data dt ON d.DataID = dt.ID
            WHERE dt.Data BETWEEN '{data_inicial_formatada}' AND '{data_final_formatada}'
            GROUP BY h.Turno;
        """
        
        df = pd.read_sql(query, conexao)

        
        fig = px.bar(df, x='Turno', y='TotalCaronas', labels={'TotalCaronas': 'Total de Caronas'})
        st.plotly_chart(fig)


def pagina_caronas_por_curso(page):
    st.title("Juno - Caronas por Curso")
    st.header("Caronas oferecidas por curso")
    st.subheader("Selecione uma data:")

    data_inicial = st.date_input(f"Data Inicial ({page})", key=f"data_inicial_{page}")
    data_final = st.date_input(f"Data Final ({page})", key=f"data_final_{page}")
    
    if st.button(f"Gerar gráfico", key=f"gerar_grafico_{page}"):
        conexao = estabelecer_conexao_bd()
        
        data_inicial_formatada = data_inicial.strftime('%Y-%m-%d')
        data_final_formatada = data_final.strftime('%Y-%m-%d')

        
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
       
        df = pd.read_sql(query, conexao)

        
        fig = px.bar(df, x='CursoNome', y='TotalCaronas', labels={'TotalCaronas': 'Total de Caronas', 'CursoNome': 'Nome do Curso'})

        
        fig.update_layout(barmode='stack', xaxis={'categoryorder': 'total descending'})
        st.plotly_chart(fig)


def main():
    st.sidebar.title("Menu")
    opcao = st.sidebar.radio("Selecione uma opção:", 
                            ("Bairros", "Viagens por Dia da Semana", 
                             "Viagens por Turnos", "Caronas por Curso"))

    if opcao == "Bairros":
        pagina_bairros(opcao)
    elif opcao == "Viagens por Dia da Semana":
        pagina_viagens_dia_semana(opcao)
    elif opcao == "Viagens por Turnos":
        pagina_viagens_turnos(opcao)
    elif opcao == "Caronas por Curso":
        pagina_caronas_por_curso(opcao)

if __name__ == "__main__":
    main()

