import requests
from bs4 import BeautifulSoup as bs
from io import StringIO
import pandas as pd

#Funciones para realizar scraping a las paginas

#Diccionario con los nobres de los equipos 
clubes_dict = {
   #Liga española
    'Almeria': 'Almería',
    'Sevilla': 'Sevilla',
    'Sociedad': 'Real Sociedad',
    'Las Palmas': 'Las Palmas',
    'Bilbao': 'Athletic Club',
    'Celta': 'Celta Vigo',
    'Villarreal': 'Villarreal',
    'Getafe': 'Getafe',
    'Cadiz': 'Cádiz',
    'Atletico': 'Atlético Madrid',
    'Mallorca': 'Mallorca',
    'Valencia': 'Valencia',
    'Osasuna': 'Osasuna',
    'Girona': 'Girona',
    'Barcelona': 'Barcelona',
    'Betis': 'Betis',
    'Alaves': 'Alavés',
    'Granada': 'Granada',
    'Rayo Vallecano': 'Rayo Vallecano',
    'Real Madrid': 'Real Madrid',
    'Leganes': 'Leganés',
    'Valladolid': 'Valladolid',
    'Espanyol' : 'Espanyol',
    #Liga Inglesa
    'Burnley': 'Burnley',
    'Arsenal': 'Arsenal',
    'Everton': 'Everton',
    'Sheffield United': 'Sheffield Utd',
    'Brighton': 'Brighton',
    'Bournemouth': 'Bournemouth',
    'Newcastle': 'Newcastle Utd',
    'Brentford': 'Brentford',
    'Chelsea': 'Chelsea',
    'Man United': 'Manchester Utd',
    'Forest': "Nott'ham Forest",
    'Fulham': 'Fulham',
    'Liverpool': 'Liverpool',
    'Wolves': 'Wolves',
    'Tottenham': 'Tottenham',
    'Man City': 'Manchester City',
    'Aston Villa': 'Aston Villa',
    'West Ham': 'West Ham',
    'Crystal Palace': 'Crystal Palace',
    'Luton': 'Luton Town',
    #Serie A
    'Frosinone': 'Frosinone',
    'Empoli': 'Empoli',
    'Inter': 'Inter',
    'Genoa': 'Genoa',
    'Sassuolo': 'Sassuolo',
    'Roma': 'Roma',
    'Lecce': 'Lecce',
    'Udinese': 'Udinese',
    'Torino': 'Torino',
    'Bologna': 'Bologna',
    'Monza': 'Monza',
    'Verona': 'Hellas Verona',
    'Milan': 'Milan',
    'Juventus': 'Juventus',
    'Fiorentina': 'Fiorentina',
    'Napoli': 'Napoli',
    'Lazio': 'Lazio',
    'Salernitana': 'Salernitana',
    'Cagliari': 'Cagliari',
    'Atalanta': 'Atalanta',
    #Ligue One
    'Nice': 'Nice',
    'Marseille': 'Marseille',
    'Paris SG': 'Paris S-G',
    'Brest': 'Brest',
    'Nantes': 'Nantes',
    'Clermont': 'Clermont Foot',
    'Montpellier': 'Montpellier',
    'Rennes': 'Rennes',
    'Strasbourg': 'Strasbourg',
    'Metz': 'Metz',
    'Lyon': 'Lyon',
    'Toulouse': 'Toulouse',
    'Lille': 'Lille',
    'Reims': 'Reims',
    'Le Havre': 'Le Havre',
    'Lorient': 'Lorient',
    'Monaco': 'Monaco',
    'Lens': 'Lens',
    #Bundesliga
    'Werder': 'Werder Bremen',
    'Leverkusen': 'Leverkusen',
    'Wolfsburg': 'Wolfsburg',
    'Stuttgart': 'Stuttgart',
    'Augsburg': 'Augsburg',
    'Hoffenheim': 'Hoffenheim',
    'Dortmund': 'Dortmund',
    'Union Berlin': 'Union Berlin',
    'Frankfurt': 'Eint Frankfurt',
    'RB Leipzig': 'RB Leipzig',
    'Bochum': 'Bochum',
    'Darmstadt': 'Darmstadt 98',
    'Freiburg': 'Freiburg',
    'Koeln': 'Köln',
    'Heidenheim': 'Heidenheim',
    'Gladbach': 'Gladbach',
    'Mainz': 'Mainz 05',
    'Bayern': 'Bayern Munich'
}

def ScrapingTabla(url):
    """
    Obtiene la informacion de las tablas de las paginas

    Args:
        url (str): url para obtener la tabla
    
    Returns:
        data (list): Lista con contenido de la tabla
        titulos (list): Lista con titulos de la tabla
    """
    data = []
    titulos = []
    respuesta = requests.get(url)
    if respuesta.status_code == 200:
        s = bs(respuesta.content, 'html.parser')
        tabla = s.find('table')
        tit = tabla.find('thead').find_all('th')
        titulos = [titulo.text.strip() for titulo in tit]
        filas = tabla.find('tbody').find_all('tr')
        for fila in filas:
            celdas = fila.find_all(['td', 'th'])
            datos_fila = [celda.text.strip() for celda in celdas]
            data.append(datos_fila)
    return data, titulos

def WebScrapingPartidos(url, Liga):
  """
  WebScrapping de los partidos

  Args:
    url (str): url para obtener los partidos
    Liga (str): Nombre de liga deseada

  Returns:
    df (DataFrame): df de partidos
  """
  #Obtener titulos e informacion de los partidos
  data, titulos = ScrapingTabla(url)
  #Nombres de columnas numericas
  numericos = ['Sem.','Asistencia']
  #Convertiir los datos a un Dataframe
  df = pd.DataFrame(data, columns = titulos)
  #Asignar el nombre de la liga
  df['Liga'] = Liga.replace('-', ' ')
  #Eliminar columnas vacias
  df = df[df['Sem.'] != '']
  #Limpieza de datos
  df['Asistencia'] = df['Asistencia'].str.replace(',', '')
  df[numericos] = df[numericos].apply(pd.to_numeric)
  df['xG'] = df['xG'].apply(pd.to_numeric)
  df['Fecha'] = pd.to_datetime(df['Fecha'])
  df['Hora'] = pd.to_datetime(df['Hora'], format='%H:%M').dt.time
  df[['Gol_local', 'Gol_visitante']] = df.Marcador.str.split('–', expand=True)
  #Eliminar columnas inecesarias
  df.drop(['Informe del partido', 'Notas'], axis=1, inplace=True)
  return df

def WebScrapingElo(url, ligas, año):
  """
  WebScrapping de la tabla de Elo

  Args:
    url (str): url para obtener la tabla de Elo

  Returns
    df (DataFrame): df con tabla con Elo
  """
  #Obtener datos del ELO
  respuesta = requests.get(url)
  if respuesta.status_code == 200:
    #Procesar datos para poder pasarlos al pandas
    data = StringIO(respuesta.text)
    #Crear df
    df = pd.read_csv(data, index_col = 'Rank')
    #Filtra por el pais de la liga y la division 
    df = df[df['Country'].isin(ligas) & df['Level'] == 1]
    #Crea nueva columna con la fecha de la puntuacion
    df['Fecha'] = año
    #Remplaza el nombre de los clubes para que coincida con el de partidos
    df.replace(clubes_dict, inplace=True)
    #Eliminar columnas innecesarias
    df.drop(['From', 'To', 'Level', 'Country'], axis=1, inplace=True)
    return df
    
def WebScrappingTabla(url):
  """
  WebScrapping de la tabla de posiciones

  Args:
    url (str): url para obtener la tabla de posiciones

  Returns
    DataFrame: df con la tabla de posiciones
  """
  #Obtiene titulos e informacion de laa tabla de posiciones
  data, titulos = ScrapingTabla(url)
  #Convierte en df
  df = pd.DataFrame(data, columns = titulos)
  #Eliminar columnas inecesarias
  df.drop(['RL','PG','PE','PP','GF','GC','DG','Pts/PJ','xG','xGA','xGD','xGD/90',
          'Últimos 5','Asistencia','Máximo Goleador del Equipo','Portero','Notas'], 
          axis = 1, 
          inplace = True)
  #Convertir Datos
  numericos = ['PJ', 'Pts']
  df[numericos] = df[numericos].apply(pd.to_numeric)
  #Dejar columna Equipos como indice
  df.set_index('Equipo', inplace = True)
  return df