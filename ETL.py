#   Extract, Transform, Load

import pandas as pd
import re
from pymongo import MongoClient

URI = "mongodb+srv://User:Password@cluster.krvhb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster"

#1. Extract
df = pd.read_csv('C:/Users/nalva/OneDrive/Escritorio/Python/Datos/CSV/Video_Games_Sales_as_at_22_Dec_2016.csv')

#2. Transform
df.info()

#mostrar valores nulos de df
print(df.isnull().sum())

#Limpiar valores nulos
columns_to_clean = ['Name', 'Year_of_Release', 'Genre','Publisher', 'NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales', 'Developer', 'Rating']
for col in columns_to_clean:
    df = df.dropna(subset=[col])

#Eliminar columnas poco relevantes
columns_to_drop = ['Critic_Score', 'Critic_Count', 'User_Score', 'User_Count']
for col in columns_to_drop:
    df = df.drop(col, axis=1)

#verificar valores nulos
print("\nValores nulos después de eliminar filas:")
print(df.isnull().sum())

#eliminar filas duplicadas
df = df.drop_duplicates()

#Aplicar expresion regular para limpiar caracteres especiales
def clean_text(value):
        if pd.isnull(value):
            return None
        return re.sub(r'[^A-Za-z0-9\s:]', '', str(value)).strip()

for column in df.columns:
    df[column] = df[column].apply(clean_text)

#Load
try:
    connection = MongoClient(URI)
    
except:
    print("Error")

db = connection['Sales']
collection = db['VideoGames']

if collection.count_documents({}) > 0:
    print("La colección ya contiene datos.")
else:
    data = df.to_dict(orient='records')
    collection.insert_many(data)
    print("Datos insertados correctamente.")

resultado = collection.find({})
for i in resultado:
    print(i)




