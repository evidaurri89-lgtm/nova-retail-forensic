import pandas as pd
import numpy as np
import random
from faker import Faker
import os

fake = Faker('es_MX')
random.seed(42)
np.random.seed(42)

NUM_STORES = 187
NUM_SAP_STORES = 125

states = [
    'Aguascalientes', 'Guanajuato', 'Jalisco', 'Nuevo León',
    'Querétaro', 'San Luis Potosí', 'Coahuila', 'Chihuahua',
    'Durango', 'Tamaulipas', 'Zacatecas', 'Sonora',
    'Baja California', 'Sinaloa'
]

cities = {
    'Aguascalientes': ['Aguascalientes'],
    'Guanajuato': ['León', 'Celaya', 'Irapuato', 'Salamanca'],
    'Jalisco': ['Guadalajara', 'Zapopan', 'Tlaquepaque'],
    'Nuevo León': ['Monterrey', 'San Nicolás', 'Apodaca'],
    'Querétaro': ['Querétaro', 'San Juan del Río'],
    'San Luis Potosí': ['San Luis Potosí', 'Soledad'],
    'Coahuila': ['Saltillo', 'Torreón', 'Monclova'],
    'Chihuahua': ['Chihuahua', 'Juárez', 'Delicias'],
    'Durango': ['Durango', 'Gómez Palacio'],
    'Tamaulipas': ['Tampico', 'Reynosa', 'Matamoros'],
    'Zacatecas': ['Zacatecas', 'Fresnillo'],
    'Sonora': ['Hermosillo', 'Obregón'],
    'Baja California': ['Tijuana', 'Mexicali', 'Ensenada'],
    'Sinaloa': ['Culiacán', 'Mazatlán', 'Los Mochis']
}

cedis_route_north = [15, 29, 47, 51, 67, 78, 83, 91, 103, 112, 134, 145, 156, 171, 180]

stores = []

for i in range(1, NUM_STORES + 1):
    state = random.choice(states)
    city = random.choice(cities[state])
    system = 'SAP' if i <= NUM_SAP_STORES else 'AS400'
    route = 'NORTE' if i in cedis_route_north else random.choice(
        ['SUR', 'CENTRO', 'PACIFICO', 'GOLFO']
    )

    regional_manager = f"GR-{(i % 5) + 1:03d}"

    if i in [47, 83, 112]:
        regional_manager = "GR-002"

    ghost_store = (system == 'AS400' and i in cedis_route_north and random.random() < 0.6)

    access_control = 'ELECTRONIC' if random.random() < 0.25 else 'PHYSICAL_KEY'
    has_cctv = random.random() < 0.60

    stores.append({
        'store_id': i,
        'store_name': f"NOVA-{city[:3].upper()}-{i:03d}",
        'city': city,
        'state': state,
        'system': system,
        'cedis_route': route,
        'regional_manager_id': regional_manager,
        'opening_hour': '08:00',
        'has_cctv': has_cctv,
        'cctv_operational': has_cctv and random.random() < 0.7,
        'access_control_type': access_control,
        'ghost_store': ghost_store,
        'monthly_revenue_avg': round(np.random.lognormal(mean=12.5, sigma=0.5)),
        'employee_count': random.randint(8, 35),
        'store_age_years': random.randint(1, 18)
    })

df_stores = pd.DataFrame(stores)

os.makedirs("data/raw", exist_ok=True)
df_stores.to_csv("data/raw/stores.csv", index=False)

print("Archivo generado: data/raw/stores.csv")
print(df_stores.head())
print("\nResumen:")
print(df_stores['system'].value_counts())
print(f"\nGhost stores: {df_stores['ghost_store'].sum()}")
