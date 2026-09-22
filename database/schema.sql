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
INSERT OR IGNORE INTO roles (nombre, descripcion) VALUES ('Auxiliar Contable', 'Acceso a gestión tributaria y reportes contables');

-- Insertar un usuario administrador por defecto (contraseña: admin, hasheada con SHA-256)
INSERT OR IGNORE INTO usuarios (nombre_completo, nombre_usuario, contrasena, rol_id, activo) VALUES ('Administrador del Sistema', 'admin', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 1, 1);

-- Migrar contraseña plaintext si existe de versiones anteriores
UPDATE usuarios SET contrasena = '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918' WHERE nombre_usuario = 'admin' AND contrasena = 'admin';

-- ============================================================
-- GESTIÓN TRIBUTARIA
-- ============================================================

-- Tabla de clientes/contribuyentes
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ruc TEXT NOT NULL UNIQUE,
    razon_social TEXT NOT NULL,
    estado TEXT NOT NULL DEFAULT 'ACTIVO'
);

-- Obligaciones tributarias por periodo
CREATE TABLE IF NOT EXISTS obligaciones_tributarias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    periodo TEXT NOT NULL,
    tipo_tributo TEXT NOT NULL,
    monto_original REAL NOT NULL,
    fecha_vencimiento DATE NOT NULL,
    estado TEXT NOT NULL DEFAULT 'PENDIENTE',

    FOREIGN KEY (cliente_id)
        REFERENCES clientes(id)
        ON DELETE CASCADE,

    CHECK (
        tipo_tributo IN (
            'IGV',
            'RENTA_3RA',
            'RENTA_4TA',
            'RENTA_5TA',
            'ESSALUD',
            'ONP',
            'AFP'
        )
    ),

    CHECK (
        estado IN ('PENDIENTE', 'PAGADO')
    ),

    CHECK (monto_original >= 0)
);

-- Pagos adelantados realizados por el contribuyente
CREATE TABLE IF NOT EXISTS pagos_adelantados (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    fecha_pago DATE NOT NULL,
    monto REAL NOT NULL,
    tipo_tributo_destino TEXT NOT NULL,

    FOREIGN KEY (cliente_id)
        REFERENCES clientes(id)
        ON DELETE CASCADE,

    CHECK (
        tipo_tributo_destino IN (
            'IGV',
            'RENTA_3RA',
            'RENTA_4TA',
            'RENTA_5TA',
            'ESSALUD',
            'ONP',
            'AFP'
        )
    ),

    CHECK (monto > 0)
);

-- Imputación de pagos a obligaciones tributarias
CREATE TABLE IF NOT EXISTS imputaciones_pago (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pago_id INTEGER NOT NULL,
    obligacion_id INTEGER NOT NULL,
    monto_aplicado REAL NOT NULL,

    FOREIGN KEY (pago_id)
        REFERENCES pagos_adelantados(id)
        ON DELETE CASCADE,

    FOREIGN KEY (obligacion_id)
        REFERENCES obligaciones_tributarias(id)
        ON DELETE CASCADE,

    CHECK (monto_aplicado > 0)
);

-- Índices para gestión tributaria
CREATE INDEX IF NOT EXISTS idx_clientes_ruc
ON clientes(ruc);

CREATE INDEX IF NOT EXISTS idx_obligaciones_cliente
ON obligaciones_tributarias(cliente_id);

CREATE INDEX IF NOT EXISTS idx_obligaciones_periodo
ON obligaciones_tributarias(periodo);

CREATE INDEX IF NOT EXISTS idx_obligaciones_tipo
ON obligaciones_tributarias(tipo_tributo);

CREATE INDEX IF NOT EXISTS idx_pagos_cliente
ON pagos_adelantados(cliente_id);

CREATE INDEX IF NOT EXISTS idx_imputaciones_pago
ON imputaciones_pago(pago_id);

CREATE INDEX IF NOT EXISTS idx_imputaciones_obligacion
ON imputaciones_pago(obligacion_id);