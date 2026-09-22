from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent 

DB_PATH = BASE_DIR / 'database' / 'data' / 'punto_venta.db'

SCHEMA_PATH = BASE_DIR / 'database' / 'schema.sql'


# Ruta de ímagenes
ICON_PATH = BASE_DIR / 'assets' / 'icons'/ 'pos-icon.ico'

# Ruta de la imagen de login
IMAGE_POST = BASE_DIR / "assets" / "images" / "pos-image.png"

ADMIN_IMG = BASE_DIR / 'assets' / 'images' / 'admin.png'
VENTAS_IMG = BASE_DIR / 'assets' / 'images' / 'ventas.png'
ALMACEN_IMG = BASE_DIR / 'assets' / 'images' / 'almacen.png'

