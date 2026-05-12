import gspread
import pandas as pd
import json
import os
from google.oauth2.service_account import Credentials

# Load credentials dari GitHub Secret
creds_json = os.environ['GOOGLE_CREDENTIALS']
creds_dict = json.loads(creds_json)

# Auth
scopes = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
client = gspread.authorize(creds)

# MASTER Spreadsheet ID
SPREADSHEET_ID = '1wumoDA8SrXmaEXRkI_2lNlvof9JVtsXceeE2qhLtb7A'

# Config per site
SITES = [
    {'gid': 1129886851, 'owner': 'HCI', 'output': 'HCI_JABABEKA.csv'},
    {'gid': 1129886851, 'owner': 'AHI', 'output': 'AHI_JABABEKA.csv'},
    {'gid': 1129886851, 'owner': 'KLS', 'output': 'KLS_JABABEKA.csv'},
]

spreadsheet = client.open_by_key(SPREADSHEET_ID)
sheet_cache = {}

for site in SITES:
    gid = site['gid']
    if gid not in sheet_cache:
        worksheet = spreadsheet.get_worksheet_by_id(gid)
        data = worksheet.get_all_records()
        sheet_cache[gid] = pd.DataFrame(data)
    
    df = sheet_cache[gid].copy()
    df = df[df['OWNER'] == site['owner']]
    df = df[df['Shipment Area'] == 'DALAM KOTA']
    
    output_path = f"data/{site['output']}"
    df.to_csv(output_path, index=False)
    print(f"✅ {site['output']} — {len(df)} rows")

print("Done.")
