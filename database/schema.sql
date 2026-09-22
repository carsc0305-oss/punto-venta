-- Tabla para definir los niveles de acceso
CREATE TABLE IF NOT EXISTS roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL UNIQUE,
    descripcion TEXT
);

-- Tabla de Usuarios con relación a roles y soporte para "Soft Delete"
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_completo TEXT NOT NULL,
    nombre_usuario TEXT NOT NULL UNIQUE,
    contrasena TEXT NOT NULL,
    rol_id INTEGER NOT NULL,
    activo INTEGER DEFAULT 1, -- 1 = Activo, 0 = Inactivo (Cumple con RF-3.3)
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (rol_id) REFERENCES roles (id)
);

-- Tabla principal de Productos e Inventario
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo_barras TEXT NOT NULL UNIQUE,
    nombre TEXT NOT NULL,
    precio REAL NOT NULL,
    stock_actual INTEGER NOT NULL DEFAULT 0
);

-- Índice de rendimiento
CREATE INDEX IF NOT EXISTS idx_producto_codigo_barras ON productos(codigo_barras);

-- Tabla de Ventas (Cabecera)
CREATE TABLE IF NOT EXISTS ventas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    fecha_venta DATETIME DEFAULT CURRENT_TIMESTAMP,
    subtotal REAL NOT NULL,
    impuestos REAL NOT NULL DEFAULT 0,
    total REAL NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
);

-- Tabla de Detalle de Ventas (Cuerpo). Relación N:M usando snake_case
CREATE TABLE IF NOT EXISTS detalle_ventas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    venta_id INTEGER NOT NULL,
    producto_id INTEGER NOT NULL,
    cantidad INTEGER NOT NULL,
    precio_unitario REAL NOT NULL,
    subtotal REAL NOT NULL,
    FOREIGN KEY (venta_id) REFERENCES ventas (id) ON DELETE CASCADE,
    FOREIGN KEY (producto_id) REFERENCES productos (id)
);

-- Insertar roles básicos por defecto si no existen
INSERT OR IGNORE INTO roles (nombre, descripcion) VALUES ('Administrador', 'Acceso total al sistema');
INSERT OR IGNORE INTO roles (nombre, descripcion) VALUES ('Cajero', 'Acceso a terminal de ventas');
INSERT OR IGNORE INTO roles (nombre, descripcion) VALUES ('Almacenista', 'Acceso a gestión de inventario');

-- Insertar un usuario administrador por defecto (contraseña: admin, hasheada con SHA-256)
INSERT OR IGNORE INTO usuarios (nombre_completo, nombre_usuario, contrasena, rol_id, activo) VALUES ('Administrador del Sistema', 'admin', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 1, 1);

-- Migrar contraseña plaintext si existe de versiones anteriores
UPDATE usuarios SET contrasena = '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918' WHERE nombre_usuario = 'admin' AND contrasena = 'admin';

