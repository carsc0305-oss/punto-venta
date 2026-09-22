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

# ============================================================
# CONFIGURACIÓN TRIBUTARIA
# ============================================================

# Tasa diaria utilizada por el módulo de gestión tributaria.
#
# 0.0003 = 0.03 % diario
#
# Se mantiene configurable para poder modificarla posteriormente
# sin tener que cambiar la lógica del controlador.

TIM_DIARIA = 0.0003


# ============================================================
# TIPOS DE TRIBUTO
# ============================================================

TIPOS_TRIBUTO = [
    "IGV",
    "RENTA_3RA",
    "RENTA_4TA",
    "RENTA_5TA",
    "ESSALUD",
    "ONP",
    "AFP"
]


# ============================================================
# ESTADOS DE LAS OBLIGACIONES
# ============================================================

ESTADO_PENDIENTE = "PENDIENTE"

ESTADO_PAGADO = "PAGADO"


# ============================================================
# REPORTES
# ============================================================

REPORTES_DIR = BASE_DIR / "reportes"

REPORTES_EXCEL_DIR = REPORTES_DIR / "excel"

REPORTES_PDF_DIR = REPORTES_DIR / "pdf"


# Crear carpetas automáticamente
REPORTES_EXCEL_DIR.mkdir(parents=True, exist_ok=True)

REPORTES_PDF_DIR.mkdir(parents=True, exist_ok=True)