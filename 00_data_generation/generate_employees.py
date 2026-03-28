import pandas as pd
import numpy as np
import random
from faker import Faker
from datetime import datetime, date
import os

fake = Faker('es_MX')
random.seed(42)
np.random.seed(42)

REFERENCE_DATE = date(2024, 6, 30)
FIVE_YEARS_AGO = date(2019, 6, 30)
SIX_MONTHS_AGO = date(2024, 1, 1)

NUM_EMPLOYEES = 2800

roles = [
    'CAJERO', 'ALMACENISTA', 'PISO_VENTAS',
    'RECEPCION', 'GERENTE_TIENDA', 'SUBGERENTE',
    'SEGURIDAD', 'LIMPIEZA'
]

stores_df = pd.read_csv("data/raw/stores.csv")

employees = []

for i in range(NUM_EMPLOYEES):
    store = random.choice(stores_df['store_id'].tolist())

    hire_date = fake.date_between(start_date=FIVE_YEARS_AGO, end_date=REFERENCE_DATE)

    if random.random() < 0.55:
        hire_date = fake.date_between(start_date=SIX_MONTHS_AGO, end_date=REFERENCE_DATE)

    termination_date = None
    is_active = True

    if random.random() < 0.40:
        termination_date = fake.date_between(start_date=hire_date, end_date=REFERENCE_DATE)
        is_active = False

    last_name = fake.last_name().upper().replace(" ", "")[:5]
    user_id = f"{last_name}{random.randint(10,99):02d}"

    employees.append({
        'employee_id': f"EMP-{i+1:05d}",
        'user_id': user_id,
        'name': fake.name(),
        'role': random.choice(roles),
        'store_id': store,
        'hire_date': hire_date,
        'termination_date': termination_date,
        'is_active': is_active,
        'background_check': random.choice(
            ['COMPLETED', 'PENDING', 'NOT_DONE', 'NOT_DONE', 'NOT_DONE']
        ),
        'salary_monthly': round(random.uniform(6000, 25000), 2)
    })

employees.append({
    'employee_id': "EMP-99999",
    'user_id': "RCISNE04",
    'name': "Raul Cisneros Medina",
    'role': 'JEFE_TRANSPORTES',
    'store_id': 0,
    'hire_date': datetime(2019, 3, 15).date(),
    'termination_date': None,
    'is_active': True,
    'background_check': 'COMPLETED',
    'salary_monthly': 35000.00
})

df_employees = pd.DataFrame(employees)

os.makedirs("data/raw", exist_ok=True)
df_employees.to_csv("data/raw/employees.csv", index=False)

print("Archivo generado: data/raw/employees.csv")
print(df_employees.head())

print("\nResumen:")
print(f"Total empleados: {len(df_employees)}")
print(f"Activos: {df_employees['is_active'].sum()}")
print(f"Inactivos: {(~df_employees['is_active']).sum()}")

print("\nBackground checks:")
print(df_employees['background_check'].value_counts())

print("\nRoles:")
print(df_employees['role'].value_counts())

print("\nUsuario especial:")
print(df_employees[df_employees['user_id'] == 'RCISNE04'])