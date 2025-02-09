# import pandas as pd
# import psycopg2
# from psycopg2 import sql
# import os
# import re
# from tqdm import tqdm

# # host:
# # aws-0-eu-central-1.pooler.supabase.com

# # port:
# # 6543

# # database:
# # postgres

# # user:
# # postgres.ezlovmsmtdengapiohfz

# # pool_mode:
# # transaction



# # --- CONFIGURATION ---
# CSV_FILE = "NASA_EXPOPLANET_ARCHIVE.csv"  # Adjust path
# DB_NAME = "postgres"
# DB_USER = "postgres.ezlovmsmtdengapiohfz"   # Uses your macOS username
# DB_PASSWORD = "Kepler-LOL42_GasGiant!"  # If PostgreSQL has no password, leave blank
# DB_HOST = "aws-0-eu-central-1.pooler.supabase.com"
# DB_PORT = "6543"

# # --- FIX DATE FUNCTION ---
# def fix_date(value):
#     """ Fixes date format (YYYY-MM → YYYY-MM-01) and removes invalid 'YYYY-00-01' cases """
#     if pd.isna(value) or value == "" or value == "NaN":
#         return None  # Convert empty values to NULL
    
#     # Fix "YYYY-00-01" format by replacing '00' with '01'
#     fixed_value = re.sub(r"-00-", "-01-", value)

#     if re.match(r"^\d{4}-\d{2}-\d{2}$", fixed_value):  # Ensure proper format
#         return fixed_value
    
#     return None  # Return NULL if the format is still incorrect

# # --- READ CSV ---
# print("Loading CSV...")
# df = pd.read_csv(CSV_FILE, delimiter=",", na_values=["", "NULL", "NaN"])

# # Fix date columns
# date_columns = ["rowupdate", "pl_pubdate", "releasedate"]
# for col in date_columns:
#     if col in df.columns:
#         df[col] = df[col].astype(str).apply(fix_date)

# # Convert boolean flags (PostgreSQL uses TRUE/FALSE)
# bool_columns = ["default_flag", "pl_controv_flag", "ttv_flag"]
# for col in bool_columns:
#     if col in df.columns:
#         df[col] = df[col].astype("boolean")

# # --- DATABASE CONNECTION ---
# print("Connecting to PostgreSQL...")
# conn = psycopg2.connect(
#     dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
# )
# cursor = conn.cursor()

# # --- INSERT DATA WITH ERROR HANDLING ---
# print("Inserting data into PostgreSQL...")

# insert_query = sql.SQL("""
#     INSERT INTO exoplanets (
#         pl_name, hostname, default_flag, sy_snum, sy_pnum, discoverymethod, disc_year, disc_facility,
#         soltype, pl_controv_flag, pl_refname, pl_orbper, pl_orbpererr1, pl_orbpererr2, pl_orbperlim,
#         pl_orbsmax, pl_orbsmaxerr1, pl_orbsmaxerr2, pl_orbsmaxlim, pl_rade, pl_radeerr1, pl_radeerr2,
#         pl_radelim, pl_radj, pl_radjerr1, pl_radjerr2, pl_radjlim, pl_bmasse, pl_bmasseerr1, pl_bmasseerr2,
#         pl_bmasselim, pl_bmassj, pl_bmassjerr1, pl_bmassjerr2, pl_bmassjlim, pl_bmassprov, pl_orbeccen,
#         pl_orbeccenerr1, pl_orbeccenerr2, pl_orbeccenlim, pl_insol, pl_insolerr1, pl_insolerr2, pl_insollim,
#         pl_eqt, pl_eqterr1, pl_eqterr2, pl_eqtlim, ttv_flag, st_refname, st_spectype, st_teff, st_tefferr1,
#         st_tefferr2, st_tefflim, st_rad, st_raderr1, st_raderr2, st_radlim, st_mass, st_masserr1, st_masserr2,
#         st_masslim, st_met, st_meterr1, st_meterr2, st_metlim, st_metratio, st_logg, st_loggerr1, st_loggerr2,
#         st_logglim, sy_refname, rastr, ra, decstr, dec, sy_dist, sy_disterr1, sy_disterr2, sy_vmag,
#         sy_vmagerr1, sy_vmagerr2, sy_kmag, sy_kmagerr1, sy_kmagerr2, sy_gaiamag, sy_gaiamagerr1, sy_gaiamagerr2,
#         rowupdate, pl_pubdate, releasedate
#     ) VALUES ({})
# """).format(sql.SQL(", ").join(sql.Placeholder() * len(df.columns)))

# for _, row in tqdm(df.iterrows()):
#     try:
#         cursor.execute(insert_query, tuple(row))
#         conn.commit()
#     except Exception as e:
#         conn.rollback()
#         print(f"❌ Error inserting row: {row['pl_name']} - {e}")

# # --- CLOSE CONNECTION ---
# cursor.close()
# conn.close()

# print("✅ Data import complete! 🚀")