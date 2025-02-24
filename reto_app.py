
import streamlit as st
import pandas as pd
from google.cloud import firestore
from google.oauth2 import service_account

import json
key_dict = json.loads(st.secrets["textkey"])
creds= service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds, project="movies-reto")

dbmov = db.collection("movies")

st.header("Movies app")

#==============================
# lectura de BD para despliege
@st.cache_data
def load_BD():
    mov_ref = list(dbmov.stream())
    mov_dict = [doc.to_dict() for doc in mov_ref]
    mov_df = pd.DataFrame(mov_dict)
    
    return mov_df

#=============================================
#      Funcion para filtrar por título
#============================================

def filtrar_titulo(name, df):
    filtered_name = df[df['name'].str.contains(name, case=False, na=False)]
    return filtered_name


#==============================

#==============================================
#           Filtrar por Director
#==============================================

def filter_director(df,director):
  movies_by_director = df[(df['director']==director)]

  return movies_by_director

#=========================================
#                  agregar película
#========================================
def new_movie(titulo,company,director,genero):
    doc_ref = dbmov.document(titulo)
    doc_ref.set({
        "company":company,
        "director":director,
        "genre":genero,
        "name":titulo
    })
#================================================
#                   listas unicas 
#===============================================
def obtener_directores_unicos(df):
    return df['director'].unique().tolist()

def obtener_companias_unicas(df):
    return df['company'].unique().tolist()

def obtener_generos_unicos(df):
    return df['genre'].unique().tolist()    
# componentes:
#1) Check box
movies_df = load_BD()
check_mov = st.sidebar.checkbox("Mostrar películas disponibles")

if check_mov:
    
    st.dataframe(movies_df)

#2) text_input and button
st.sidebar.markdown("___")
st.sidebar.subheader("Buscar por título")

titulo = st.sidebar.text_input("Ingresa un título")
boton = st.sidebar.button("Buscar título")

if boton and titulo:
    title = filtrar_titulo(titulo, movies_df)
    count_row = title.shape[0]
    st.write(f"Total movies: {count_row}")
    st.dataframe(title)

#3) lista de directores
st.sidebar.markdown("___")
st.sidebar.subheader("Seleccionar Director")
lista_directores = obtener_directores_unicos(movies_df)
selection = st.sidebar.selectbox("selecciona un director",lista_directores)
dir_boton = st.sidebar.button("Filtrar director")

if selection and dir_boton:
  lista_dir = filter_director(movies_df,selection)
  count_row = lista_dir.shape[0]
  st.write(f"Total de titulos encontrados: {count_row}" )
  st.dataframe(lista_dir)

# 4) añadir nueva película
st.sidebar.markdown("___")
st.sidebar.subheader("Añadir Película")

new_name = st.sidebar.text_input("Nombre")


lista_comp = obtener_companias_unicas(movies_df)
selection_comp = st.sidebar.selectbox("Company",lista_comp)

lista_directores = obtener_directores_unicos(movies_df)
selection_dire = st.sidebar.selectbox("Director",lista_directores)

lista_generos = obtener_generos_unicos(movies_df)
selection_gen = st.sidebar.selectbox("Genero",lista_generos)

buton_add = st.sidebar.button("Agregar nuevo registro")

if buton_add and selection_gen and selection_dire and selection_comp and new_name:
  new_movie(new_name,selection_comp,selection_dire,selection_gen)
  st.sidebar.write("registro agregado con exito")
  st.cache_data.clear()
  movies_df = load_BD()




