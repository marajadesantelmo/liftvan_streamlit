from supabase import create_client, Client
import pandas as pd
#from dotenv import load_dotenv
import os
#import ast
#load_dotenv()

#De aca agarra las keys streamlit. En caso de correr manual no correr estos comandos
url_supabase = os.getenv("url_supabase")
key_supabase= os.getenv("key_supabase")

supabase_client = create_client(url_supabase, key_supabase)

def fetch_table_data(table_name):
    query = (
        supabase_client
        .from_(table_name)
        .select('*')
        .execute()
    )
    return pd.DataFrame(query.data)

def insert_review(data):
    # Wrap data in a list for single row insert
    response = supabase_client.table("reviews").insert([data]).execute()
    return response

def fetch_reviews():
    query = (
        supabase_client
        .from_("reviews")
        .select('*')
        .order('created_at', desc=True)
        .execute()
    )
    return pd.DataFrame(query.data)

def get_fake_review():
    import datetime
    return {
        "username": "test_user",
        "asistencia_estimador": 4,
        "coordinador_trafico": 5,
        "cortesia_coordinador": 4,
        "apoyo_coordinador": 5,
        "precision_informacion": 3,
        "servicio_general_coordinador": 4,
        "embaladores": 5,
        "cortesia": 4,
        "colaboracion_personal": 5,
        "puntualidad": 5,
        "calidad_empaque": 4,
        "recomendaria": True,
        "comentarios": "Probando probando.",
    }
#insert_review(get_fake_review()) 