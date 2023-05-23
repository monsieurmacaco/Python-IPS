"""
Marche à suivre : 
    1°) Appuyer sur Play (triangle vert)
    2°) Trouver le numéro de la colonne dans names_columns
    3°) Lancer make_csv(df,numero de la colonne qui t'intéresse, nom du csv en sortie)
    4°) Patienter jusqu'à ce qu'il trouve tout.
"""





import requests
import pandas as pd
import numpy as np

df = pd.read_csv("data_questionnaires.csv",sep = ";")
df = df.drop(columns = ["ID de la réponse","Date de soumission","Dernière page", "Langue de départ","Tête de série", "Date de lancement", "Date de la dernière action"])
names_columns = df.columns



#22 : nom lycée dans colonne 22



def adresse_to_coordonnees(string):
    def string_to_request(string):
        replace = string.replace(" ","+")
        return replace
    url = 'https://nominatim.openstreetmap.org/search.php?q=' + string_to_request(string) + '&format=jsonv2'
    response = requests.get(url)
    if response.json() != []:
        json = response.json()[0]
        latitude  = float(json["lat"])
        longitude = float(json["lon"])
        boolean = True
    else:
        boolean = False
        latitude = 0
        longitude = 0
    return boolean,longitude,latitude

def make_coord(df):
    colonne_lycee = df[df.columns[22]]
    liste_longitude = []
    liste_latitude = []
    liste_index = []
    for index,lycee in enumerate(colonne_lycee):
        try:
            boolean,longitude,latitude = adresse_to_coordonnees(lycee)
            if boolean:
                print(longitude,latitude)
                liste_index.append(index)
                liste_longitude.append(longitude)
                liste_latitude.append(latitude)
            else:
                liste_index.append(index)
                liste_longitude.append("a chercher")
                liste_latitude.append("a chercher")
                print("à chercher")
        except:
            print("non renseigné")
    return liste_index,liste_latitude,liste_longitude

def make_df_from_cood(df,numero_colonne_info_en_plus):
    liste_index,liste_latitude,liste_longitude = make_coord(df)
    liste_info = list(df[df.columns[numero_colonne_info_en_plus]][liste_index])
    array = np.array(liste_info,liste_longitude,liste_latitude)
    df_coord = pd.DataFrame(np.transpose(array),columns = [names_columns[numero_colonne_info_en_plus],"longitude","latitude"])
    return df_coord
            


def make_csv(df,numero_colonne_info_en_plus,nom_csv):
    df_coord = make_df_from_cood(df, numero_colonne_info_en_plus)
    df_coord.to_csv(nom_csv)
    
