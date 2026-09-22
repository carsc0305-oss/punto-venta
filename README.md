# 🛒 Punto de Venta

Sistema de Punto de Venta (POS) de escritorio desarrollado en Python con interfaz gráfica moderna usando **CustomTkinter**. Permite gestionar usuarios, productos e inventario, y realizar ventas con generación automática de comprobantes en PDF.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![CustomTkinter](https://img.shields.io/badge/CustomTkinter-GUI-green)
![SQLite](https://img.shields.io/badge/SQLite-Database-blue?logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## ✨ Características

- **Autenticación segura** con contraseñas hasheadas (SHA-256).
- **Control de acceso por roles**: Administrador, Cajero y Almacenista.
- **Gestión de usuarios**: Crear, activar y desactivar cuentas.
- **Gestión de productos**: CRUD completo con validación de datos.
- **Terminal de ventas**: Búsqueda por código de barras, carrito de compras, cálculo de IGV (18%) y vuelto.
- **Comprobantes PDF**: Generación automática de tickets de venta.
- **Interfaz moderna**: Temas claro/oscuro con CustomTkinter.

---

## 🏗️ Arquitectura

El proyecto sigue el patrón **MVC (Modelo - Vista - Controlador)**:

```
punto-venta/
├── main.py                  # Punto de entrada de la aplicación
├── config.py                # Rutas y configuración global
├── database/
│   ├── db_conection.py      # Conexión a SQLite
│   └── schema.sql           # Esquema de tablas y datos iniciales
├── models/
│   ├── usuario.py           # Modelo de Usuario
│   ├── producto.py          # Modelo de Producto
│   └── venta.py             # Modelos de Venta y DetalleVenta
├── controllers/
│   ├── usuario_controller.py    # Lógica de autenticación y gestión de usuarios
│   ├── producto_controller.py   # Lógica de inventario
│   └── venta_controller.py      # Lógica de ventas y generación de PDF
├── views/
│   ├── estilos.py           # Estilos compartidos para tablas (Treeview)
│   ├── login_view.py        # Pantalla de inicio de sesión
│   ├── main_view.py         # Dashboard principal con sidebar
│   ├── usuarios_view.py     # Vista de administración de usuarios
│   ├── producto_view.py     # Vista de gestión de productos
│   └── venta_view.py        # Terminal de ventas
├── assets/                  # Iconos e imágenes
└── ventas_pdf/              # Comprobantes PDF generados
```

---

## 🚀 Instalación

### Requisitos previos

- Python 3.10 o superior

### Pasos

1. **Clonar el repositorio:**

```bash
git clone https://github.com/alexroel/punto-venta.git
cd punto-venta
```

2. **Crear un entorno virtual:**

```bash
python -m venv .env
# Windows
.env\Scripts\activate
# Linux/Mac
source .env/bin/activate
```

3. **Instalar dependencias:**

```bash
pip install -r requirements.txt
```

4. **Ejecutar la aplicación:**

```bash
python main.py
```

---

## 🔐 Credenciales por defecto

| Usuario | Contraseña | Rol            |
|---------|------------|----------------|
| `admin` | `admin`    | Administrador  |

> ⚠️ Se recomienda cambiar la contraseña del administrador tras el primer inicio de sesión.

---

## 👥 Roles del sistema

| Rol            | Permisos                                          |
|----------------|---------------------------------------------------|
| Administrador  | Acceso total: usuarios, productos y ventas         |
| Cajero         | Acceso a la terminal de ventas                     |
| Almacenista    | Acceso a la gestión de productos e inventario      |

---

## 🛠️ Tecnologías

- **Python 3.10+** — Lenguaje principal
- **CustomTkinter** — Interfaz gráfica moderna
- **SQLite** — Base de datos local
- **Pillow** — Procesamiento de imágenes
- **fpdf2** — Generación de comprobantes PDF

---

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

---

Desarrollado por **ROELCODE** 🚀
