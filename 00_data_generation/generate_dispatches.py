import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

random.seed(42)
np.random.seed(42)

START_DATE = datetime(2024, 1, 1)
END_DATE = datetime(2024, 3, 31)

stores_df = pd.read_csv("data/raw/stores.csv")
products_df = pd.read_csv("data/raw/products_sap.csv")

dispatches = []

print("Generando despachos del CEDIS...")

for _, store in stores_df.iterrows():
    store_id = store['store_id']
    route = store['cedis_route']

    current_date = START_DATE

    while current_date <= END_DATE:
        if current_date.weekday() in [1, 4]:
            n_products = random.randint(30, 80)
            selected_skus = products_df.sample(n=min(n_products, len(products_df)))

            for _, product in selected_skus.iterrows():
                if product['price_sap'] < 1000:
                    qty = random.randint(5, 50)
                else:
                    qty = random.randint(1, 12)

                hour = random.randint(3, 5)
                minute = random.randint(0, 59)

                dispatches.append({
                    'dispatch_id': f"DSP-{len(dispatches)+1:08d}",
                    'store_id': store_id,
                    'sku': product['sku_sap'],
                    'quantity_dispatched': qty,
                    'dispatch_date': current_date.strftime('%Y-%m-%d'),
                    'dispatch_time': f"{hour:02d}:{minute:02d}",
                    'route': route,
                    'truck_id': f"TRUCK-{random.randint(1,25):03d}",
                    'driver_id': f"DRV-{random.randint(1,40):03d}",
                    'authorized_by': random.choice(
                        ['RCISNE04', 'RCISNE04', 'RCISNE04',
                         'JLOPEZ11', 'MGARCI07']
                    ),
                    'cedis_system_record': 'SAP'
                })

        current_date += timedelta(days=1)

df_dispatches = pd.DataFrame(dispatches)

os.makedirs("data/raw", exist_ok=True)
df_dispatches.to_csv("data/raw/dispatches.csv", index=False)

print("Archivo generado: data/raw/dispatches.csv")
print(df_dispatches.head())

print(f"\nTotal despachos: {len(df_dispatches):,}")

print("\nPor ruta:")
print(df_dispatches['route'].value_counts())

print("\nAutorizados por:")
print(df_dispatches['authorized_by'].value_counts())
