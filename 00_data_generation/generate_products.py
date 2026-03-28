import pandas as pd
import numpy as np
import random
import os

random.seed(42)
np.random.seed(42)

NUM_SKUS = 14000
GHOST_APPLE_SKUS = 22

categories = {
    'ELECTRONICA': {
        'weight': 0.15, 'price_range': (2000, 35000),
        'items': ['TELEVISOR', 'PANTALLA', 'MONITOR', 'BOCINA',
                  'AUDIFONOS', 'CAMARA', 'CONSOLA', 'TABLET'],
        'brands': ['SAMSUNG', 'LG', 'SONY', 'HISENSE', 'TCL', 'JBL']
    },
    'TELEFONIA': {
        'weight': 0.10, 'price_range': (3000, 30000),
        'items': ['IPHONE', 'SAMSUNG GALAXY', 'XIAOMI', 'MOTOROLA',
                  'AIRPODS', 'GALAXY BUDS', 'FUNDA', 'CARGADOR'],
        'brands': ['APPLE', 'SAMSUNG', 'XIAOMI', 'MOTOROLA', 'HUAWEI']
    },
    'ELECTRODOMESTICOS': {
        'weight': 0.12, 'price_range': (1500, 25000),
        'items': ['LICUADORA', 'MICROONDAS', 'REFRIGERADOR',
                  'LAVADORA', 'ESTUFA', 'HORNO', 'CAFETERA',
                  'PLANCHA', 'ASPIRADORA', 'VENTILADOR'],
        'brands': ['MABE', 'WHIRLPOOL', 'LG', 'HAMILTON', 'OSTER']
    },
    'COMPUTO': {
        'weight': 0.08, 'price_range': (5000, 35000),
        'items': ['LAPTOP', 'DESKTOP', 'IMPRESORA', 'TECLADO',
                  'MOUSE', 'WEBCAM', 'DISCO DURO', 'USB'],
        'brands': ['HP', 'LENOVO', 'DELL', 'ACER', 'ASUS', 'LOGITECH']
    },
    'ALIMENTOS': {
        'weight': 0.20, 'price_range': (10, 500),
        'items': ['ACEITE', 'ARROZ', 'FRIJOL', 'AZUCAR',
                  'LECHE', 'HUEVO', 'PAN', 'CEREAL',
                  'GALLETAS', 'REFRESCO', 'AGUA', 'JUGO'],
        'brands': ['MASECA', 'LA COSTENA', 'LALA', 'BIMBO', 'COCA-COLA']
    },
    'LIMPIEZA': {
        'weight': 0.15, 'price_range': (15, 300),
        'items': ['JABON', 'DETERGENTE', 'CLORO', 'SUAVIZANTE',
                  'PAPEL HIGIENICO', 'SERVILLETAS', 'ESCOBA',
                  'TRAPEADOR', 'DESINFECTANTE'],
        'brands': ['FABULOSO', 'PINOL', 'ROMA', 'DOWNY', 'PETALO']
    },
    'CUIDADO_PERSONAL': {
        'weight': 0.10, 'price_range': (20, 800),
        'items': ['SHAMPOO', 'CREMA', 'DESODORANTE', 'PASTA DENTAL',
                  'CEPILLO', 'RASTRILLO', 'TOALLAS'],
        'brands': ['HEAD_SHOULDERS', 'COLGATE', 'GILLETTE', 'DOVE']
    },
    'LICORES': {
        'weight': 0.05, 'price_range': (80, 5000),
        'items': ['TEQUILA', 'WHISKY', 'RON', 'VODKA', 'CERVEZA',
                  'VINO', 'MEZCAL', 'BRANDY'],
        'brands': ['JOSE CUERVO', 'JOHNNIE WALKER', 'BACARDI', 'ABSOLUT']
    },
    'MISCELANEOS': {
        'weight': 0.05, 'price_range': (5, 200),
        'items': ['ENCENDEDOR', 'PILAS', 'FOCO', 'EXTENSION',
                  'CINTA', 'PEGAMENTO', 'TIJERAS'],
        'brands': ['BIC', 'DURACELL', 'PHILIPS', 'TRUPER']
    }
}

sizes_tech = ['32"', '43"', '55"', '65"', '75"', '128GB', '256GB', '512GB']
sizes_general = ['500ML', '1L', '2L', '100G', '250G', '500G', '1KG', '5KG', '6 PACK', '12 PACK']

products_sap = []
products_as400 = []
ghost_count = 0
sku_counter = 0

print("Generando catalogo de productos...")

for category, config in categories.items():
    n_products = int(NUM_SKUS * config['weight'])

    for j in range(n_products):
        sku_counter += 1
        item = random.choice(config['items'])
        brand = random.choice(config['brands'])

        if category in ['ELECTRONICA', 'TELEFONIA', 'COMPUTO']:
            size = random.choice(sizes_tech)
        else:
            size = random.choice(sizes_general)

        price_mxn = round(random.uniform(*config['price_range']), 2)

        sap_code = f"SAP-{sku_counter:07d}"
        sap_desc = f"{item} {brand} {size}"

        products_sap.append({
            'sku_sap': sap_code,
            'description_sap': sap_desc,
            'category_sap': category,
            'brand': brand,
            'price_sap': price_mxn,
            'supplier_id': f"PROV-{random.randint(1,50):03d}",
        })

        is_apple = brand == 'APPLE'
        is_high_value = price_mxn > 5000
        is_ghost = is_apple and is_high_value and ghost_count < GHOST_APPLE_SKUS

        if is_ghost:
            ghost_count += 1
            products_as400.append({
                'sku_as400': None,
                'description_as400': None,
                'category_as400': None,
                'price_as400': None,
                'sku_sap_reference': sap_code,
                'is_ghost': True
            })
            continue

        format_choice = random.randint(1, 4)
        if format_choice == 1:
            as400_code = f"{category[:4]}-{random.randint(1000,9999)}"
        elif format_choice == 2:
            as400_code = f"{random.randint(1,999):03d}-{item[:4]}-{random.randint(1,99):02d}"
        elif format_choice == 3:
            as400_code = f"{item} {brand} {size}"
        else:
            as400_code = f"{sku_counter:08d}"

        as400_desc = sap_desc
        if random.random() < 0.30:
            corruptions = [
                lambda s: s.replace('SAMSUNG', 'SAMSNG'),
                lambda s: s.replace('APPLE', 'APLE'),
                lambda s: s.replace('TELEVISOR', 'TV'),
                lambda s: s.replace('PANTALLA', 'PANT'),
                lambda s: s.replace('REFRIGERADOR', 'REFRI'),
                lambda s: s.replace('LICUADORA', 'LICUAD'),
                lambda s: s[:len(s)//2],
                lambda s: s.upper().replace(' ', ''),
                lambda s: s.replace('O', '0').replace('E', '3'),
            ]
            corruption = random.choice(corruptions)
            as400_desc = corruption(as400_desc)

        as400_price = price_mxn
        currency_chaos = random.random()
        if currency_chaos < 0.08:
            as400_price = round(price_mxn / 17.3, 2)
        elif currency_chaos < 0.12:
            as400_price = None

        as400_cat = category
        if random.random() < 0.20:
            as400_cat = ''
        elif random.random() < 0.15:
            cat_variants = {
                'ELECTRONICA': ['ELECTRON', 'ELECTR', 'PANTALLAS', 'AUDIO Y VIDEO'],
                'TELEFONIA': ['TEL', 'CELULARES', 'MOVILES'],
                'ALIMENTOS': ['ALIM', 'ABARROTES', 'COMIDA'],
                'LIMPIEZA': ['LIMP', 'HOGAR', 'ASEO']
            }
            if category in cat_variants:
                as400_cat = random.choice(cat_variants[category])

        products_as400.append({
            'sku_as400': as400_code,
            'description_as400': as400_desc,
            'category_as400': as400_cat,
            'price_as400': as400_price,
            'sku_sap_reference': sap_code,
            'is_ghost': False
        })

df_sap = pd.DataFrame(products_sap)
df_as400 = pd.DataFrame(products_as400)

os.makedirs("data/raw", exist_ok=True)
df_sap.to_csv("data/raw/products_sap.csv", index=False)
df_as400.to_csv("data/raw/products_as400.csv", index=False)

print(f"\nProductos SAP: {len(df_sap)}")
print(f"Productos AS400: {len(df_as400)}")
print(f"Apple Ghosts: {ghost_count}")
print(f"\nSAP - primeras filas:")
print(df_sap.head())
print(f"\nAS400 - primeras filas:")
print(df_as400.head())
print(f"\nAS400 - ejemplos de ghosts:")
print(df_as400[df_as400['is_ghost'] == True].head())
print(f"\nAS400 - precios nulos: {df_as400['price_as400'].isna().sum()}")
print(f"AS400 - categorias vacias: {(df_as400['category_as400'] == '').sum()}")
