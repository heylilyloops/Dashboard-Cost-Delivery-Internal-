import gspread
import pandas as pd
import json
import os
from google.oauth2.service_account import Credentials

creds_json = os.environ['GOOGLE_CREDENTIALS']
creds_dict = json.loads(creds_json)

scopes = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
client = gspread.authorize(creds)

SPREADSHEET_ID = '1wumoDA8SrXmaEXRkI_2lNlvof9JVtsXceeE2qhLtb7A'

SITES = [
    {'gid': 1129886851, 'output': 'HCI_JABABEKA.csv'},
    {'gid': 111957912,  'output': 'AHI_JABABEKA.csv'},
    {'gid': 197682446,  'output': 'KLS_JABABEKA.csv'},
    {'gid': 1019046386, 'output': 'HCI_CIKUPA.csv'},
    {'gid': 1111207228, 'output': 'CORP_SIDOARJO.csv'},
    {'gid': 1950770306, 'output': 'CORP_TALLO.csv'},
    {'gid': 1447314605, 'output': 'CORP_TAMORA.csv'},
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
    
    output_path = f"data/{site['output']}"
    df.to_csv(output_path, index=False)
    print(f"✅ {site['output']} — {len(df)} rows")

print("Done.")
