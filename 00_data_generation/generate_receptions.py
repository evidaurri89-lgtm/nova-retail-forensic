import pandas as pd
import numpy as np
import random
from datetime import timedelta
import os

random.seed(42)
np.random.seed(42)

FRAUD_STORES = [47, 83, 112, 15, 29, 67, 91, 134, 156, 171]

dispatches_df = pd.read_csv("data/raw/dispatches.csv")
stores_df = pd.read_csv("data/raw/stores.csv")
products_df = pd.read_csv("data/raw/products_sap.csv")
employees_df = pd.read_csv("data/raw/employees.csv")

receptions = []

print("Generando recepciones en tienda...")

for _, dispatch in dispatches_df.iterrows():
    store_id = dispatch['store_id']
    qty_dispatched = dispatch['quantity_dispatched']
    product_sku = dispatch['sku']

    product_info = products_df[products_df['sku_sap'] == product_sku]
    is_high_value = False
    if len(product_info) > 0:
        is_high_value = product_info.iloc[0]['price_sap'] > 2000

    is_fraud_store = store_id in FRAUD_STORES

    if is_fraud_store and is_high_value and random.random() < 0.70:
        theft_pct = random.uniform(0.12, 0.18)
        qty_received = max(1, int(qty_dispatched * (1 - theft_pct)))
        reception_hour = f"05:{random.randint(30,59):02d}"
    elif random.random() < 0.02:
        error_pct = random.uniform(0.01, 0.03)
        qty_received = max(1, int(qty_dispatched * (1 - error_pct)))
        reception_hour = f"{random.randint(7,9):02d}:{random.randint(0,59):02d}"
    else:
        qty_received = qty_dispatched
        reception_hour = f"{random.randint(7,9):02d}:{random.randint(0,59):02d}"

    dispatch_date = pd.to_datetime(dispatch['dispatch_date'])
    reception_date = dispatch_date + timedelta(days=random.randint(0, 1))

    date_format_choice = random.randint(1, 3)
    if date_format_choice == 1:
        date_str = reception_date.strftime('%d/%m/%Y')
    elif date_format_choice == 2:
        date_str = reception_date.strftime('%m/%d/%Y')
    else:
        date_str = reception_date.strftime('%Y-%m-%d')

    unit_type = 'UNIDAD'
    qty_reported = qty_received
    if random.random() < 0.25:
        unit_type = 'CAJA'
        items_per_box = random.choice([6, 12, 24])
        qty_reported = max(1, qty_received // items_per_box)

    received_by = ''
    if random.random() > 0.41:
        store_employees = employees_df[employees_df['store_id'] == store_id]
        if len(store_employees) > 0:
            received_by = store_employees.sample(1).iloc[0]['user_id']

    receptions.append({
        'reception_id': f"REC-{len(receptions)+1:08d}",
        'store_id': store_id,
        'sku': product_sku,
        'quantity_received': qty_reported,
        'unit_type': unit_type,
        'reception_date_str': date_str,
        'reception_time': reception_hour,
        'received_by': received_by,
        'dispatch_reference': dispatch['dispatch_id'],
        'system_source': stores_df[stores_df['store_id'] == store_id].iloc[0]['system'] if len(stores_df[stores_df['store_id'] == store_id]) > 0 else 'UNKNOWN',
        'notes': random.choice([
            '', '', '', '', '',
            'caja dañada', 'faltante parcial',
            'revisar con proveedor', 'OK',
            'producto sin codigo en sistema'
        ])
    })

df_receptions = pd.DataFrame(receptions)

os.makedirs("data/raw", exist_ok=True)
df_receptions.to_csv("data/raw/receptions.csv", index=False)

print("Archivo generado: data/raw/receptions.csv")
print(df_receptions.head())

print(f"\nTotal recepciones: {len(df_receptions):,}")

print(f"\nRecepciones a las 05:XX AM: {df_receptions['reception_time'].str.startswith('05:').sum():,}")

print(f"\nCampo 'received_by' vacio: {(df_receptions['received_by'] == '').sum():,}")

print("\nTipo de unidad:")
print(df_receptions['unit_type'].value_counts())

print("\nFormatos de fecha detectados (muestra):")
print(df_receptions['reception_date_str'].head(10))
