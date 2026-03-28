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
employees_df = pd.read_csv("data/raw/employees.csv")

pos_transactions = []

print("Generando transacciones POS...")

for _, store in stores_df.iterrows():
    store_id = store['store_id']
    system = store['system']
    ghost_store = store['ghost_store']

    if ghost_store:
        continue

    daily_transactions = random.randint(20, 60)
    current_date = START_DATE

    while current_date <= END_DATE:
        if system == 'SAP' and random.random() < 0.01:
            gap_days = random.randint(2, 4)
            current_date += timedelta(days=gap_days)
            continue

        n_trans = random.randint(
            int(daily_transactions * 0.7),
            int(daily_transactions * 1.3)
        )

        store_employees = employees_df[employees_df['store_id'] == store_id]
        cashier_pool = store_employees['user_id'].tolist() if len(store_employees) > 0 else ['UNKNOWN']

        for _ in range(n_trans):
            product = products_df.sample(1).iloc[0]

            qty = 1 if product['price_sap'] > 2000 else random.randint(1, 5)

            hour = random.randint(8, 21)
            minute = random.randint(0, 59)
            ts = current_date.replace(hour=hour, minute=minute)

            if random.random() < 0.005:
                ts = datetime(1970, 1, 1, hour, minute)

            unit_price = product['price_sap']
            discount = 0

            if random.random() < 0.15:
                discount = random.choice([5, 10, 15, 20, 25])

            if system == 'AS400' and discount > 0:
                unit_price = round(unit_price * (1 - discount / 100), 2)
                discount = 0

            is_return = False
            if random.random() < 0.002:
                qty = -qty
                if random.random() < 0.5:
                    is_return = True

            total = round(qty * unit_price * (1 - discount / 100), 2)

            pos_transactions.append({
                'transaction_id': f"TX-{len(pos_transactions)+1:09d}",
                'store_id': store_id,
                'sku': product['sku_sap'],
                'quantity': qty,
                'unit_price': unit_price,
                'discount_pct': discount if system == 'SAP' else None,
                'total': total,
                'timestamp': ts,
                'payment_method': random.choice(['CASH', 'CARD', 'CARD', 'CARD', 'TRANSFER']),
                'cashier_id': random.choice(cashier_pool),
                'is_return': is_return,
                'system_source': system,
                'sync_status': random.choice(['SYNCED', 'SYNCED', 'SYNCED', 'OFFLINE_PENDING'])
            })

        current_date += timedelta(days=1)

df_pos = pd.DataFrame(pos_transactions)

os.makedirs("data/raw", exist_ok=True)
df_pos.to_csv("data/raw/pos_transactions.csv", index=False)

print("Archivo generado: data/raw/pos_transactions.csv")
print(df_pos.head())

print("\nResumen:")
print(f"Total transacciones: {len(df_pos)}")
print("\nPor sistema:")
print(df_pos['system_source'].value_counts())

print("\nSync status:")
print(df_pos['sync_status'].value_counts())

print(f"\nTimestamps 1970: {(df_pos['timestamp'].astype(str).str.contains('1970-01-01')).sum()}")
print(f"Cantidad negativa: {(df_pos['quantity'] < 0).sum()}")
