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

# Master data tahun berjalan (2026)
MASTER_2026 = '1wumoDA8SrXmaEXRkI_2lNlvof9JVtsXceeE2qhLtb7A'
# Master LC 2025 - data historis untuk YoY
MASTER_2025 = '12wgZfgGHTXfMztFQ59KwXHQz9wQezxoSp82MhyPIS38'

SITES = [
    # --- Data 2026 (berjalan) ---
    {'spreadsheet_id': MASTER_2026, 'gid': 1129886851, 'output': 'HCI_JABABEKA.csv'},
    {'spreadsheet_id': MASTER_2026, 'gid': 111957912,  'output': 'AHI_JABABEKA.csv'},
    {'spreadsheet_id': MASTER_2026, 'gid': 197682446,  'output': 'KLS_JABABEKA.csv'},
    {'spreadsheet_id': MASTER_2026, 'gid': 1019046386, 'output': 'HCI_CIKUPA.csv'},
    {'spreadsheet_id': MASTER_2026, 'gid': 1111207228, 'output': 'CORP_SIDOARJO.csv'},
    {'spreadsheet_id': MASTER_2026, 'gid': 1950770306, 'output': 'CORP_TALLO.csv'},
    {'spreadsheet_id': MASTER_2026, 'gid': 1447314605, 'output': 'CORP_TAMORA.csv'},

    # --- Data 2025 (historis, untuk YoY) ---
    {'spreadsheet_id': MASTER_2025, 'gid': 247161117,   'output': 'HCI_JABABEKA_2025.csv'},
    {'spreadsheet_id': MASTER_2025, 'gid': 1333858878,  'output': 'AHI_JABABEKA_2025.csv'},
    {'spreadsheet_id': MASTER_2025, 'gid': 446090471,   'output': 'KLS_JABABEKA_2025.csv'},
    {'spreadsheet_id': MASTER_2025, 'gid': 0,           'output': 'HCI_CIKUPA_2025.csv'},
    {'spreadsheet_id': MASTER_2025, 'gid': 1944909599,  'output': 'CORP_SIDOARJO_2025.csv'},
    {'spreadsheet_id': MASTER_2025, 'gid': 1357711592,  'output': 'CORP_TALLO_2025.csv'},
    {'spreadsheet_id': MASTER_2025, 'gid': 444859252,   'output': 'CORP_TAMORA_2025.csv'},
]

spreadsheet_cache = {}
sheet_cache = {}

for site in SITES:
    sid = site['spreadsheet_id']
    gid = site['gid']
    cache_key = (sid, gid)

    if sid not in spreadsheet_cache:
        spreadsheet_cache[sid] = client.open_by_key(sid)

    if cache_key not in sheet_cache:
        worksheet = spreadsheet_cache[sid].get_worksheet_by_id(gid)
        data = worksheet.get_all_records()
        sheet_cache[cache_key] = pd.DataFrame(data)

    df = sheet_cache[cache_key].copy()

    output_path = f"data/{site['output']}"
    df.to_csv(output_path, index=False)
    print(f"✅ {site['output']} — {len(df)} rows")

print("Done.")
