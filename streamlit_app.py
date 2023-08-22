import streamlit as st
import os
import mysql.connector
import pandas as pd
import plotly.express as px
from datetime import datetime, date, timedelta

def estabelecer_conexao_bd():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="junodwpopulado"
    )
    return connection

def main():
    
    st.sidebar.title(" Grupo 2 - Juno")

    pages = {
        "Introdução 🎈": intro_page,
        "P1. Localização dos Pontos de Origem e Destino 📍 ": bairros_page,
        "P2. Vagas Disponibilizadas X Vagas Ocupadas 👨‍👩‍👦": vagas_disponibilizadas_vagas_ocupadas,
        "P3. Viagens por Dia da Semana 📅": viagens_dia_semana_page,
        "P4. Viagens por Turnos 🌞": viagens_turno_page,
        "P5. Viagens por Horários ⏰": viagens_horario,
        "P6. Caronas Oferecidas por Curso 🎓": caronas_curso_page,
        "P7. Distância Percorrida nas Viagens 🚗": viagens_distancia,

    }

    st.sidebar.markdown("## Análises com Streamlit 📊")

    page = st.sidebar.radio("### Selecione uma página", list(pages.keys()))
    pages[page]()

def intro_page():

    st.markdown("# Introdução 🎈")
    st.divider()
    st.write("  A seguinte análise foi desenvolvida pela equipe Juno (Grupo 2) para a cadeira de Modelagem de Dados e teve como guia uma série de perguntas, que encontram-se listadas a seguir:") 
    st.write("")
    st.write("       1. Quais foram as coordenadas (localizações) que funcionaram como ponto de origem (partida) ou ponto de destino (chegada) de uma viagem, considerando certos dias na semana e um determinado intervalo de tempo?")
    st.write("       2. Qual a relação entre a quantidade de vagas disponibilizadas e a quantidade de vagas ocupadas, considerando um determinado intervalo de distância entre o ponto de origem e o de chegada, bem como um certo período de tempo?")   
    st.write("       3. Quantas caronas foram realizadas em cada dia da semana no intervalo de 1, 2, 3 ou 4 semanas a partir de uma data inicial, considerando um determinado intervalo de distância entre o ponto de origem e o de chegada?")
    st.write("       4. Quantas caronas foram realizadas em cada turno (manhã, tarde, noite e madrugada), considerando um determinado intervalo de distância entre o ponto de origem e o de chegada, bem como um certo período de tempo?")
    st.write("       5. Quantas caronas foram realizadas em cada hora, considerando um determinado intervalo de distância entre o ponto de origem e o de chegada, bem como um certo período de tempo?")
    st.write("       6. Qual a quantidade de caronas oferecidas pelos estudantes matriculados em cada curso ofertado pela UFRPE, considerando os alunos de determinado período e/ou turno, bem como um certo período de tempo?")
    st.write("       7. Quantas caronas foram realizadas, considerando um determinado intervalo de distância entre o ponto de origem e o ponto de chegada (km), dentro de um determinado intervalo de tempo?")
    st.write("")
    st.write("  Essas perguntas foram definidas no início do estudo e da análise do Data Warehouse com objetivo de norter esse processo da melhor forma possível e trazer mais qualidade as análises.")
    st.write("")
    st.write("  Então, vamos seguir para aos resultados! 😊")
    st.write("")
    st.write("  Os resultados da análise podem ser acessado por meio do menu lateral no canto esquerdo, em que cada página está relacionada a uma das 7 perguntas que foram apresentadas")

def bairros_page():
    
    st.markdown("# PERGUNTA 1: Localização dos Pontos de Origem e Destino 📍 ")
    st.divider()
    st.markdown("### Apresentação")
    st.write("A seguinte consulta tem como objetivo indicar a **localização (coordenadas)** dos **pontos de origem e pontos de destino** das viagens que ocorreram em determinado intervalo de tempo e em certos dias da semana. De modo que seja possível perceber de forma visual quais regiões costumam servir mais como ponto de partida ou de chegada.")
    st.write("")
    st.markdown("### Dados")

    escolha_bairro = st.radio("Selecione uma opção:", ("Bairros de Origem", "Bairros de Destino"))

    if escolha_bairro == "Bairros de Origem":
        coluna = "origem.bairro"
        cabecalho = "Bairro de Origem"
        latitude_col = "origem.Latitude"
        longitude_col = "origem.Longitude"
        color = '#845ec2'
    
    elif escolha_bairro == "Bairros de Destino":
        coluna = "destino.bairro"
        cabecalho = "Bairro de Destino"
        latitude_col = "destino.Latitude"
        longitude_col = "destino.Longitude"
        color = '#5887c2'


    data_inicial = st.date_input("Data Inicial")
    data_final = st.date_input("Data Final")
    
    dias_semana = st.multiselect("Selecione os dias da semana", ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"])

    if escolha_bairro == "Bairros de Origem" or escolha_bairro == "Bairros de Destino":
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
                INNER JOIN DimEndereco AS origem ON fd.dimenderecoorigem_codigo = origem.dimendereco_codigo
                INNER JOIN DimEndereco AS destino ON fd.dimenderecodestino_codigo = destino.dimendereco_codigo
                INNER JOIN DimData AS dd ON fd.dimdata_codigo = dd.dimdata_codigo
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
            st.map(df[['LAT', 'LON', 'bairro', 'TotalViagens']], color = color)

def vagas_disponibilizadas_vagas_ocupadas():
    
    st.markdown("# PERGUNTA 2: Vagas Disponibilizadas VS Vagas Ocupadas 👨‍👩‍👦")
    st.divider()
    st.markdown("### Apresentação")
    st.write("A seguinte consulta apresenta a **relação entre a quantidade de vagas disponibilizadas e a quantidade de vagas ocupadas**, considerando um determinado intervalo de distância entre o ponto de origem e o de chegada, bem como um certo período de tempo. De maneira que seja possível identificar o quanto das vagas disponibilizadas estão sendo efetivamente ocupadas.")
    st.markdown("### Dados")
   
    data_inicial = st.date_input("Data Inicial")
    data_final = st.date_input("Data Final")

    range_quilometragem = st.slider("Selecione o intervalo da distância da viagem", value=[0,30])

    if st.button(f"Gerar gráfico", key="gerar_grafico_viagens_turno"):
        conexao = estabelecer_conexao_bd()
        
        data_inicial_formatada = data_inicial.strftime('%Y-%m-%d')
        data_final_formatada = data_final.strftime('%Y-%m-%d')

        query = f"""
            SELECT fd.vagasdisponibilizadas as VagasDisponibilizadas, fd.vagasocupadas as VagasOcupadas, COUNT(*) as Total
            FROM FatoDeslocamento fd
            INNER JOIN DimData dt ON fd.dimdata_codigo = dt.dimdata_codigo
            WHERE dt.data BETWEEN '{data_inicial_formatada}' AND '{data_final_formatada}'
                AND fd.distanciadeslocamento BETWEEN {range_quilometragem[0]} AND {range_quilometragem[1]}
            GROUP BY VagasDisponibilizadas, VagasOcupadas;
        """
        
        df = pd.read_sql(query, conexao)

        fig = px.scatter(df, x="VagasDisponibilizadas", y="VagasOcupadas", labels={'VagasDisponibilizadas': 'Vagas Disponibilizadas', "VagasOcupadas": "Vagas Ocupadas"}, color = "Total", size='Total',)
        fig.update_layout(barmode='stack')
        st.plotly_chart(fig)

def viagens_dia_semana_page():

    st.markdown("# PERGUNTA 3: Viagens por Dia da Semana 📅")
    st.divider()
    st.markdown("### Apresentação")
    st.write("A seguinte consulta tem como objetivo apresentar a **quantidade de viagens que ocorreram em cada dia da semana** no período de 1, 2, 3 ou 4 semanas, a partir de uma data inicial, considerando um determinado intervalo de distância entre o ponto de origem e o de chegada. De maneira que seja possível identificar se há relação entre o dia da semana e a quantidade de viagens que foram realizadas.")
    st.markdown("### Dados")

    st.subheader("Selecione uma data:")
    
    data_inicial = st.date_input("Data Inicial")
    dataFinalInput = st.selectbox(
        "Número de Semanas", (1, 2, 3, 4))
    
    dataMult = dataFinalInput * 6

    dataFinal = data_inicial + timedelta(days=dataMult)

    range_quilometragem = st.slider("Selecione o intervalo da distância da viagem", value=[0,30])
    st.write("Obs.: O intervalo de distância varia de 0 até 30")

    if st.button("Gerar gráfico"):
        conexao = estabelecer_conexao_bd()
        
        data_inicial_formatada = data_inicial.strftime('%Y-%m-%d')
        data_final_formatada = dataFinal.strftime('%Y-%m-%d')
        
        query = f"""
            SELECT dt.dia_numeronasemana AS DiaSemana,
                COUNT(*) AS TotalViagens
            FROM FatoDeslocamento fd
            INNER JOIN DimData dt ON fd.dimdata_codigo = dt.dimdata_codigo
            WHERE dt.data BETWEEN '{data_inicial_formatada}' AND '{data_final_formatada}'
                AND fd.distanciadeslocamento BETWEEN {range_quilometragem[0]} AND {range_quilometragem[1]}
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

        fig = px.line(df, x="DiaSemana", y="TotalViagens", labels={'TotalViagens': 'Total de Viagens', "DiaSemana": "Dias da semana"}) 

        st.plotly_chart(fig)

def viagens_turno_page():
    
    st.markdown("# PERGUNTA 4: Viagens por Turnos 🌞")
    st.divider()
    st.markdown("### Apresentação")
    st.write("A seguinte consulta tem como objetivo apresentar a **quantidade de viagens que ocorreram em certa turno do dia (manhã, tarde, noite e madruda)**, considerando um determinado intervalo de distância entre o ponto de origem e o de chegada, bem como um certo período de tempo. De maneira que seja possível identificar se há relação entre o turno e a quantidade de viagens realizadas.")
    st.markdown("### Dados")
   
    data_inicial = st.date_input("Data Inicial")
    data_final = st.date_input("Data Final")
    
    range_quilometragem = st.slider("Selecione o intervalo da distância da viagem", value=[0,30])
    st.write("Obs.: O intervalo de distância varia de 0 até 30")

    if st.button(f"Gerar gráfico", key="gerar_grafico_viagens_turno"):
        conexao = estabelecer_conexao_bd()
        
        data_inicial_formatada = data_inicial.strftime('%Y-%m-%d')
        data_final_formatada = data_final.strftime('%Y-%m-%d')

        query = f"""
            SELECT h.Turno, COUNT(*) AS TotalCaronas
            FROM FatoDeslocamento fd
            INNER JOIN DimHorario h ON fd.dimhorario_codigo = h.dimhorario_codigo
            INNER JOIN DimData dt ON fd.dimdata_codigo = dt.dimdata_codigo
            WHERE dt.data BETWEEN '{data_inicial_formatada}' AND '{data_final_formatada}'
                AND fd.distanciadeslocamento BETWEEN {range_quilometragem[0]} AND {range_quilometragem[1]}
            GROUP BY h.turno;
        """
        
        df = pd.read_sql(query, conexao)

        fig = px.bar(df, x='Turno', y='TotalCaronas', labels={'TotalCaronas': 'Total de Caronas'})
        fig.update_layout(barmode='stack', xaxis={'categoryorder':'array', 'categoryarray':['Manhã','Tarde','Noite','Madrugada']})
        st.plotly_chart(fig)

def viagens_horario():
    
    st.markdown("# PERGUNTA 5: Viagens por Horários ⏰")
    st.divider()
    st.markdown("### Apresentação")
    st.write("A seguinte consulta tem como objetivo apresentar a **quantidade de viagens que ocorreram em certa hora do dia**, considerando um determinado intervalo de distância entre o ponto de origem e o de chegada, bem como um certo período de tempo. De maneira que seja possível identificar se há relação entre a hora do dia e a quantidade de viagens realizadas.")
    st.markdown("### Dados")

    data_inicial = st.date_input("Data Inicial")
    data_final = st.date_input("Data Final")

    turno = st.radio("Selecione o Turno:", ("Manhã","Tarde", "Noite", "Madrugada", "Todos os Turnos"))
    
    range_quilometragem = st.slider("Selecione o intervalo da distância da viagem", value=[0,30])
    st.write("Obs.: O intervalo de distância varia de 0 até 30")

    if st.button(f"Gerar gráfico", key="gerar_grafico_viagens_turno"):
        conexao = estabelecer_conexao_bd()
        
        data_inicial_formatada = data_inicial.strftime('%Y-%m-%d')
        data_final_formatada = data_final.strftime('%Y-%m-%d')

        if turno == "Todos os Turnos":

            query= f"""
                SELECT HOUR(h.horario) as Hora, COUNT(*) AS TotalCaronas
                FROM FatoDeslocamento fd
                INNER JOIN DimHorario h ON fd.dimhorario_codigo = h.dimhorario_codigo
                INNER JOIN DimData dt ON fd.dimdata_codigo = dt.dimdata_codigo
                WHERE dt.data BETWEEN '{data_inicial_formatada}' AND '{data_final_formatada}'
                    AND fd.distanciadeslocamento BETWEEN {range_quilometragem[0]} AND {range_quilometragem[1]}
                GROUP BY HOUR(h.horario);
            """
        else:

            query = f"""
                SELECT HOUR(h.horario) as Hora, COUNT(*) AS TotalCaronas
                FROM FatoDeslocamento fd
                INNER JOIN DimHorario h ON fd.dimhorario_codigo = h.dimhorario_codigo
                INNER JOIN DimData dt ON fd.dimdata_codigo = dt.dimdata_codigo
                WHERE dt.data BETWEEN '{data_inicial_formatada}' AND '{data_final_formatada}'
                    AND h.turno = '{turno}'
                    AND fd.distanciadeslocamento BETWEEN {range_quilometragem[0]} AND {range_quilometragem[1]}
                GROUP BY HOUR(h.horario);
            """

        
        df = pd.read_sql(query, conexao)

        fig = px.bar(df, x='Hora', y='TotalCaronas', labels={'TotalCaronas': 'Total de Caronas'})
        fig.update_layout(barmode='stack')
        st.plotly_chart(fig)


def caronas_curso_page():

    st.markdown("# PERGUNTA 6: Caronas Oferecidas por Curso 🎓")
    st.divider()
    st.markdown("### Apresentação")
    st.write("A seguinte consulta tem como objetivo apresentar a **quantidade de caronas oferecidas pelos estudantes matriculados em cada curso ofertado pela UFRPE**, considerando os alunos de determinado período e/ou turno, bem como um certo período de tempo. De maneira que seja possível identificar se há relação entre o curso e a quantidade de viagens ofertadas.")
    st.markdown("### Dados")


    data_inicial = st.date_input("Data Inicial")
    data_final = st.date_input("Data Final")
    
    periodo = st.multiselect("Selecione os Períodos", ["1º Periodo", "2º Periodo", "3º Periodo", "4º Periodo", "5º Periodo", "6º Periodo", "7º Periodo", "8º Periodo", "9º Periodo", "10º Periodo", "11º Periodo", "12º Periodo"])
    turno = st.multiselect("Selecione os Turnos", ["Manhã", "Tarde"])


    if st.button(f"Gerar gráfico", key="gerar_grafico_caronas_curso"):
        conexao = estabelecer_conexao_bd()

        data_inicial_formatada = data_inicial.strftime('%Y-%m-%d')
        data_final_formatada = data_final.strftime('%Y-%m-%d')

        periodo_numero = [1 if "1º Periodo" in periodo else 0,
                          2 if "2º Periodo" in periodo else 0,
                          3 if "3º Periodo" in periodo else 0,
                          4 if "4º Periodo" in periodo else 0,
                          5 if "5º Periodo" in periodo else 0,
                          6 if "6 Periodo" in periodo else 0,
                          7 if "7º Periodo" in periodo else 0,
                          8 if "8º Periodo" in periodo else 0,
                          9 if "9º Periodo" in periodo else 0,
                          10 if "10º Periodo" in periodo else 0,
                          11 if "11º Periodo" in periodo else 0,
                          12 if "12º Periodo" in periodo else 0]
        
        turno_numero = [1 if "Manhã" in turno else 0,
                        2 if "Tarde" in turno else 0]

        query = f"""SELECT da.nomecurso, COUNT(*) AS TotalCaronas
            FROM FatoDeslocamento fd
            INNER JOIN DimData dt ON fd.dimdata_codigo = dt.dimdata_codigo
            INNER JOIN DimAluno da ON fd.dimaluno_codigo = da.dimaluno_codigo
            INNER JOIN DimData dd ON fd.dimdata_codigo = dd.dimdata_codigo
            WHERE dt.Data BETWEEN '{data_inicial_formatada}' AND '{data_final_formatada}'
                AND da.periodo IN ({','.join(map(str, periodo_numero))})
                AND da.turno IN ({','.join(map(str, turno_numero))})
            GROUP BY da.nomecurso;
        """

        df = pd.read_sql(query, conexao)

        fig = px.bar(df, x='TotalCaronas', y='nomecurso', labels={'TotalCaronas': 'Total de Caronas', 'nomecurso': 'Nome do Curso'}, height=850)

        fig.update_layout(barmode='stack', yaxis={'categoryorder': 'total descending'})
        st.plotly_chart(fig)

def viagens_distancia():
    
    st.markdown("# PERGUNTA 7: Distância Percorrida nas Viagens 🚗")
    st.divider()
    st.markdown("### Apresentação")
    st.write("A seguinte consulta tem como objetivo apresentar a **quantidade de viagens realizadas com determinada quilometragem** em determinado intervalo de tempo. De maneira que seja possível identificar se há relação entre a distância percorrida e a quantidade de viagens realizadas.")
    st.markdown("### Dados")
   
    data_inicial = st.date_input("Data Inicial")
    data_final = st.date_input("Data Final")

    range_quilometragem = st.slider("Selecione o intervalo da distância da viagem", value=[0,30])
    st.write("Obs.: O intervalo de distância varia de 0 até 30")

    if st.button(f"Gerar gráfico", key="gerar_grafico_viagens_turno"):
        conexao = estabelecer_conexao_bd()
        
        data_inicial_formatada = data_inicial.strftime('%Y-%m-%d')
        data_final_formatada = data_final.strftime('%Y-%m-%d')

        query = f"""
            SELECT ROUND(fd.distanciadeslocamento) as Distancia, COUNT(*) AS TotalCaronas
            FROM FatoDeslocamento fd
            INNER JOIN DimData dt ON fd.dimdata_codigo = dt.dimdata_codigo
            WHERE dt.data BETWEEN '{data_inicial_formatada}' AND '{data_final_formatada}'
                AND fd.distanciadeslocamento BETWEEN {range_quilometragem[0]} AND {range_quilometragem[1]}
            GROUP BY ROUND(fd.distanciadeslocamento);
        """
        
        df = pd.read_sql(query, conexao)

        fig = px.scatter(df, x="Distancia", y="TotalCaronas", labels={'TotalCaronas': 'Total de Caronas', 'Distancia': 'Distância Percorrida'}, color = "TotalCaronas", size='TotalCaronas',)
        fig.update_layout(barmode='stack')
        st.plotly_chart(fig)

if __name__ == "__main__":
    main()


