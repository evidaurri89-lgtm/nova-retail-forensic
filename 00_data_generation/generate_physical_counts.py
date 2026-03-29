import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

random.seed(42)
np.random.seed(42)

FRAUD_STORES = [47, 83, 112, 15, 29, 67, 91, 134, 156, 171]

stores_df = pd.read_csv("data/raw/stores.csv")
products_df = pd.read_csv("data/raw/products_sap.csv")
employees_df = pd.read_csv("data/raw/employees.csv")

physical_counts = []

print("Generando conteos fisicos de inventario...")

for store_id in stores_df["store_id"]:
    count_date = datetime(2024, 3, 31) + timedelta(days=random.randint(-5, 5))

    n_counted = random.randint(200, 500)
    counted_skus = products_df.sample(n=min(n_counted, len(products_df)))

    store_emps = employees_df[employees_df["store_id"] == store_id]
    counter_id = ''
    if len(store_emps) > 0 and random.random() > 0.3:
        counter_id = store_emps.sample(1).iloc[0]["user_id"]

    for _, product in counted_skus.iterrows():
        theoretical_qty = random.randint(0, 50)

        if store_id in FRAUD_STORES:
            counted_qty = theoretical_qty
        else:
            variance = random.uniform(-0.03, 0.01)
            counted_qty = max(0, int(theoretical_qty * (1 + variance)))

        physical_counts.append({
            "count_id": f"CNT-{len(physical_counts)+1:08d}",
            "store_id": store_id,
            "sku": product["sku_sap"],
            "counted_quantity": counted_qty,
            "count_date": count_date.strftime("%Y-%m-%d"),
            "counted_by": counter_id,
            "count_method": random.choice(["MANUAL", "MANUAL", "SCANNER", "MANUAL"])
        })

df_counts = pd.DataFrame(physical_counts)

os.makedirs("data/raw", exist_ok=True)
df_counts.to_csv("data/raw/physical_counts.csv", index=False)

print("Archivo generado: data/raw/physical_counts.csv")
print(df_counts.head())

print(f"\nTotal conteos: {len(df_counts):,}")

print("\nMetodos de conteo:")
print(df_counts["count_method"].value_counts())

print(f"\nCampo 'counted_by' vacio: {(df_counts['counted_by'] == '').sum():,}")

print("\nFechas de conteo (muestra):")
print(df_counts["count_date"].head(10))
