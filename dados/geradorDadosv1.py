import datetime
import random
import string
import csv
import pandas as pd
from geopy.distance import geodesic as GD
from geopy.geocoders import Nominatim
import requests
import urllib.parse
from faker import Faker
from enums.Cursos import cursos



def generateCursoData():
    cursoId = list(range(1, len(cursos) + 1))
    turno = [random.randint(1,2) for _ in range(len(cursos))]
    dataCursos = {
        'Id': cursoId,
        'Nome': cursos,
        'Turno': turno
    }
    dfCursos = pd.DataFrame(dataCursos)
    dfCursos.to_csv('dados\data\TabelaCursos.csv', index=False)

def generateSigaaData(QTD_DADOS):
    sigaaID = list(range(1, QTD_DADOS + 1))
    matricula = [str(random.randint(QTD_DADOS, 999999999)) for _ in range(QTD_DADOS)]
    cursoId = [
        random.randint(1, len(cursos)) for _ in range(QTD_DADOS)]
    periodo = [random.randint(1, 12) for _ in range(QTD_DADOS)]
    dataSigaa = {
        'SigaaID': sigaaID,
        'Matricula': matricula,
        'CursoId': cursoId,
        'Periodo': periodo
        }
    dfSigaa = pd.DataFrame(dataSigaa)
    dfSigaa.to_csv('dados\data\TabelaSigaa.csv', index=False)

def generateEnderecoData(QTD_DADOS):
    id = list(range(1, QTD_DADOS + 1))

    enderecoscsv = open("generateData\enums\lista_enderecos2.csv", encoding="utf8")
    enderecos = list(csv.reader(enderecoscsv, delimiter=","))

    cep = []
    rua = []
    bairro = []
    tipoSubdivisao = []
    subdivisao = []
    municipio = []
    estado = []
    
    for endereco in range(1, QTD_DADOS + 1):
        enderecoID = random.randint(1, len(enderecos) - 1)
        cep.append(enderecos[enderecoID][1])
        rua.append(enderecos[enderecoID][2])
        bairro.append(enderecos[enderecoID][3])
        tipoSubdivisao.append(enderecos[enderecoID][4])
        subdivisao.append(enderecos[enderecoID][5])
        municipio.append(enderecos[enderecoID][6])
        estado.append(enderecos[enderecoID][7])
    
    complemento = [random.choice(["Casa", "Apartamento"])for _ in range(QTD_DADOS)]

    dataEndereco = {
        "Id": id,
        'CEP': cep,
        'Rua': rua,
        'Bairro': bairro,
        'Tipo de Subdivisao': tipoSubdivisao,
        'Subdivisao': subdivisao,
        "Municipio": municipio,
        "Estado": estado,
        "Complemento": complemento
        }
    dfEndereco = pd.DataFrame(dataEndereco)
    dfEndereco.to_csv("dados\data\TabelaEndereco.csv", index=False)

def generateUsuarioData(QTD_DADOS_USUARIO, QTD_DADOS_ENDERECO):
    fake = Faker('pt_BR')
    usuarioID = list(range(1, QTD_DADOS_USUARIO + 1))
    sigaaID = list(range(1, QTD_DADOS_USUARIO + 1))
    enderecoID = list(range(1, QTD_DADOS_ENDERECO + 1))
    nome = [fake.first_name_female() for _ in range(QTD_DADOS_USUARIO)]
    sobrenome = []

    for quant_usuario in range(1, QTD_DADOS_USUARIO + 1):
        sobrenome1 = fake.last_name()
        sobrenome2 = fake.last_name()

        while sobrenome1 == sobrenome2:
            sobrenome2 = fake.last_name()

        sobrenome.append(str(sobrenome1) + " " + str(sobrenome2))

    cpf = [fake.cpf() for _ in range(QTD_DADOS_USUARIO)]
    senha = [fake.password() for _ in range(QTD_DADOS_USUARIO)]
    telefone = ['81' + fake.numerify('#######') for _ in range(QTD_DADOS_USUARIO)]  # Gera telefones fictícios com DDD 81
    email = [f"{n.lower().replace(' ', '')}.{s.lower().replace(' ', '')}@ufrpe.br" for n, s in zip(nome, sobrenome)]  # Gera emails fictícios
    nascimento = [fake.date_of_birth(minimum_age=17, maximum_age=70).strftime('%Y-%m-%d') for _ in range(QTD_DADOS_USUARIO)]  # Gera datas de nascimento fictícias com pelo menos 17 anos

    data = {
        'ID': usuarioID,
        'SigaaID': sigaaID,
        'EnderecoID': enderecoID,
        'Nome': nome,
        'Sobrenome': sobrenome,
        'Cpf': cpf,
        'Senha': senha,
        'Telefone': telefone,
        'Email': email,
        'Data de Nascimento': nascimento
    }
    # Criar um DataFrame
    dfUsuarios = pd.DataFrame(data)

    # Exportar o dataframe para um arquivo excel
    dfUsuarios.to_csv('dados\data\TabelaUsuarios.csv', index=False)

def generate_license_plate():
    letters = random.choices(string.ascii_uppercase, k=3)
    numbers = random.choices(string.digits, k=4)
    return ''.join(letters) + '-' + ''.join(numbers)

def generateVeiculoData(QTD_DADOS, QTD_DADOS_USUARIO):
    veiculoID = list(range(1, QTD_DADOS_USUARIO + 1))
    usuariosIds = list(range(1, QTD_DADOS_USUARIO + 1))
    usuarioID = [random.choice(usuariosIds) for _ in range(QTD_DADOS)] 
    tipo = [random.randint(1,2) for _ in range(QTD_DADOS)]
    placa = [generate_license_plate() for _ in range(QTD_DADOS)]

    carroscsv = open("generateData\enums\lista_carros.csv", encoding="utf8")
    carros = list(csv.reader(carroscsv, delimiter=","))

    ano = []
    marca = []
    modelo = []

    for carro in range(1, QTD_DADOS + 1):
        carroID = random.randint(1, len(carros) - 1)
        ano.append(carros[carroID][0])
        marca.append(carros[carroID][1])
        modelo.append(carros[carroID][2])

    cores = ["Preto", "Branco", "Prata", "Cinza", "Azul", "Vermelho", "Verde", "Amarelo"]
    cor = [random.choice(cores) for _ in range(QTD_DADOS)]
    passageiros = [random.randint(1, 4) for _ in range(QTD_DADOS)]
    dataVeiculos = {
        'VeiculoID': veiculoID,
        'UsuarioID': usuarioID,
        'Tipo': tipo,
        'Placa': placa,
        'Ano': ano,
        'Marca': marca,
        'Modelo': modelo,
        'Cor': cor,
        'Passageiros': passageiros
    }
    dfVeiculos = pd.DataFrame(dataVeiculos)
    dfVeiculos.to_csv('dados\data\TabelaVeiculos.csv', index=False)

def generateHora():
    horaIds = list(range(1, 1441))
    horario = []
    turno = []
    
    turno_madrugada = [23, 24, 0, 1, 2, 3, 4]
    turno_manha = [5, 6, 7, 8, 9, 10, 11]
    turno_tarde = [12, 13, 14, 15, 16, 17]
    turno_noite = [18, 19, 20, 21, 22]

    for hora in range(00, 24):
        for minuto in range(00, 60):
            horario.append([f'{str(hora).zfill(2)}:{str(minuto).zfill(2)}:00'])
            if hora in turno_madrugada:
                turno.append('Madrugada')
            elif hora in turno_manha:
                turno.append('Manhã')
            elif hora in turno_tarde:
                turno.append('Tarde')
            elif hora in turno_noite:
                turno.append('Noite')

    dataHora = {
        'HoraID': horaIds,
        'Hora': horario,
        'Turno': turno
    }   
    dfHora = pd.DataFrame(dataHora)
    dfHora.to_csv('dados\data\TabelaHora.csv', index=False)


def generateDeslocamentosData(QTD_DADOS, QTD_DADOS_ENDERECO, QTD_DADOS_USUARIO, QTD_DADOS_VEICULO):
    id = list(range(1, QTD_DADOS + 1))
    usuarioIds = list(range(1, QTD_DADOS_USUARIO + 1))
    usuarioID = [random.choice(usuarioIds) for _ in range(QTD_DADOS)]
    veiculoIds = list(range(1, QTD_DADOS_VEICULO+ 1))
    veiculoID = [random.choice(veiculoIds) for _ in range(QTD_DADOS)]
    dataID = [random.randint(20080101, 20230828) for _ in range(QTD_DADOS)]
    horaIds = list(range(1, 1441))
    horaID = [random.choice(horaIds) for _ in range(QTD_DADOS)]
    enderecoIds = list(range(1, QTD_DADOS_ENDERECO + 1))
    origemID = []
    destinoID = []

    enderecoscsv = open("dados\data\TabelaEndereco.csv", encoding="utf8")
    enderecos = list(csv.reader(enderecoscsv, delimiter=","))

    geoLocalizador = Nominatim(user_agent="my_user_agent")

    while len(origemID) < QTD_DADOS:

        origemEscolhida = random.choice(enderecoIds)
        origemCompleta = str(enderecos[origemEscolhida][2])  + ", " + str(enderecos[origemEscolhida][1])

        dadosLocalOrigem = geoLocalizador.geocode(origemCompleta)

        if dadosLocalOrigem != None:
            origemID.append(origemEscolhida)
            
    while len(destinoID) < QTD_DADOS:

        destinoEscolhido = random.choice(enderecoIds)
        destinoCompleto = str(enderecos[destinoEscolhido][2])  + ", " + str(enderecos[destinoEscolhido][1])

        dadosLocalDestino = geoLocalizador.geocode(destinoCompleto)

        if origemID[len(destinoID)] != destinoEscolhido and dadosLocalDestino != None:
            destinoID.append(destinoEscolhido)

    status = [random.randint(1,2) for _ in range(QTD_DADOS)]
    vagasDisponiveis = [random.randint(0,4) for _ in range(QTD_DADOS)]
    distancia = []

    for localizacoes in range(0, len(id)):
        origem = str(enderecos[origemID[localizacoes]][2])  + ", " + str(enderecos[origemID[localizacoes]][1])
        destino = str(enderecos[destinoID[localizacoes]][2]) + ", " + str(enderecos[destinoID[localizacoes]][1])

        dadosLocalOrigem = geoLocalizador.geocode(origem)
        dadosLocalDestino = geoLocalizador.geocode(destino)

        coordenadasorigem = (dadosLocalOrigem.latitude, dadosLocalOrigem.longitude)
        coordenadasdestino = (dadosLocalDestino.latitude, dadosLocalDestino.longitude)

        distancia.append(round(GD(coordenadasorigem,coordenadasdestino).km, 2))

    dataDeslocamento = {
        "id": id,
        "UsuarioID": usuarioID,
        "VeiculoID": veiculoID,
        'DataID': dataID,
        "HorarioID": horaID,
        "OrigemID": origemID,
        "DestinoID": destinoID,
        "Status": status,
        "VagasDisponiveis": vagasDisponiveis,
        "Distancia": distancia
    }

    dfDeslocamento = pd.DataFrame(dataDeslocamento)
    dfDeslocamento.to_csv('dados\data\TabelaDeslocamentos.csv', index=False)

def generatePassageirosData(QTD_DADOS, QTD_DADOS_USUARIO, QTD_DADOS_DESLOCAMENTOS):
    id = list(range(1, QTD_DADOS + 1))
    usuarioIds = list(range(1, QTD_DADOS_USUARIO + 1))
    usuarioId = [random.choice(usuarioIds) for _ in range(QTD_DADOS)]
    deslocamentoIds = list(range(1, QTD_DADOS_DESLOCAMENTOS + 1))
    deslocamentoId = [random.choice(deslocamentoIds) for _ in range(QTD_DADOS)]
    dataPassageiros = {
        'id': id,
        'usuarioId': usuarioId,
        'deslocamentoId': deslocamentoId
    }
    dfPassageiros = pd.DataFrame(dataPassageiros)
    dfPassageiros.to_csv('dados\data\TabelaPassageiros.csv', index=False)

if __name__ == '__main__':

    qtd_dados_usuario = int(input('Escolha a quantidade de Usuários:'))
    qtd_dados_endereco = int(input('Escolha a quantidade de Endereços:'))
    qtd_dados_veiculos = int(input('Escolha a quantidade de Veiculos:'))
    qtd_dados_deslocamento = int(input('Escolha a quantidade de Deslocamentos:'))

    generateCursoData()
    generateEnderecoData(qtd_dados_endereco)
    generateSigaaData(qtd_dados_usuario)
    generateUsuarioData(qtd_dados_usuario, qtd_dados_endereco)
    generateVeiculoData(QTD_DADOS=qtd_dados_veiculos, QTD_DADOS_USUARIO=qtd_dados_usuario)
    generateHora()
    generateDeslocamentosData(QTD_DADOS=qtd_dados_deslocamento, QTD_DADOS_ENDERECO=qtd_dados_endereco, QTD_DADOS_USUARIO=qtd_dados_usuario, QTD_DADOS_VEICULO=qtd_dados_veiculos)
    generatePassageirosData(QTD_DADOS=qtd_dados_deslocamento, QTD_DADOS_USUARIO= qtd_dados_usuario, QTD_DADOS_DESLOCAMENTOS=qtd_dados_deslocamento)
    
    print("Os dados foram gerados com sucesso!")