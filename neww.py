from supabase import create_client, Client
import pandas as pd
import pandas as pd
import requests
import json
# @st.cache_resource
# def init_connection():
#     url = st.secrets["supabase_url"]
#     key = st.secrets["supabase_key"]
#     return create_client(url, key)
def connection():
    url = 'https://mcdrfixrsbjrhjahpdms.supabase.co'
    key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1jZHJmaXhyc2JqcmhqYWhwZG1zIiwicm9sZSI6ImFub24iLCJpYXQiOjE2NzQzMDYzMDMsImV4cCI6MTk4OTg4MjMwM30.WEx55pxaI0It9oXxTigtQa9FYYhZZHGsfWnph4f2fxM'
    # url = st.secrets["https://emvcjkjmiepovnwkwrxr.supabase.co"]
    # key = st.secrets["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVtdmNqa2ptaWVwb3Zud2t3cnhyIiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODY1MDQ5MTAsImV4cCI6MjAwMjA4MDkxMH0.fS_kE-v9H4oYiK641gFNrRUHPzHK5zz-vvqVDHsCjFE"]
    return create_client(url, key)

# supabase = init_connection()
supabase = connection()

# @st.cache_data(max_entries=30)
def run_query():
    sup_list = supabase.table("maintable").select("*").execute().data
    return sup_list


df = pd.DataFrame()
rows = run_query()

for row in rows:
    row["created_at"] = row["created_at"].split(".")[0]
    row["time"] = row["created_at"].split("T")[1]
    row["date"] = row["created_at"].split("T")[0]
    row["DateTime"] = row["created_at"]
    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
df

