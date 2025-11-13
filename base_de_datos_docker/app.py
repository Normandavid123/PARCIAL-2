from flask import Flask, request, render_template, jsonify
import sqlite3
import os
import json
from datetime import datetime

app = Flask(__name__)

# Configuración de la base de datos
DATABASE_PATH = 'database/consultas.db'

def init_db():
    """Inicializa la base de datos con algunas tablas de ejemplo"""
    if not os.path.exists('database'):
        os.makedirs('database')
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Crear tabla de usuarios de ejemplo
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuario (
            id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
            rol TEXT NOT NULL,
            nombre TEXT NOT NULL,
            direccion TEXT NOT NULL,
            telefono TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            fecha_registro DATE DEFAULT CURRENT_DATE
        )
    ''')
    
    # Crear tabla de cuentas de ejemplo
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Cuenta (
            id_Cuenta INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL,
            tipo TEXT NOT NULL,
            saldo decimal NOT NULL,
            fecha_apertura DATE DEFAULT CURRENT_DATE,
            estado TEXT NOT NULL
        )
    ''')
    
    # Crear tabla de transacciones de ejemplo
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transaccion (
            id_transaccion INTEGER PRIMARY KEY AUTOINCREMENT,
            cuenta INTEGER,
            tipo INTEGER,
            monto DECIMAL NOT NULL,
            fecha_hora DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Crear tabla de tarjeta de ejemplo
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tarjeta (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cuenta INTEGER,
            tipo TEXT NOT NULL,
            numero_tarjeta TEXT UNIQUE NOT NULL,
            fecha_emision DATE DEFAULT CURRENT_DATE,
            fecha_vencimiento DATE NOT NULL,
            estado TEXT NOT NULL,
            FOREIGN KEY (cuenta) REFERENCES Cuenta(id_Cuenta)
         )                  
    ''')

    # Insertar datos de ejemplo si no existen
    cursor.execute('SELECT COUNT(*) FROM usuario')
    if cursor.fetchone()[0] == 0:
        usuario_ejemplo = [
            ("admin", "Juan Perez", "Calle Falsa 123", "3217659678", "juanperez@example.com", "2023-01-15"),
            ("cliente", "Maria Gomez", "Avenida Siempre Viva 742", "3218945793", "mariagomez@example.com", "2023-02-20"),
            ("cliente", "Carlos Ruiz", "Boulevard Central 456", "3217334698", "Carlosruiz@example.com", "2023-03-10"),
            ("admin", "Ana Torres", "Calle Luna 789", "3105903519", "anatorres@example.com", "2023-04-05"),
            ("cliente", "Luis Fernandez", "Avenida Sol 321", "3128549613", "luisfernandez@example.com", "2023-05-12"),
            ("cliente", "Sofia Martinez", "Calle Estrella 654", "3102569813", "sofiamartinez@example.com", "2023-06-18"),
            ("admin", "Pedro Sanchez", "Avenida Nube 987", "3217845613", "pedrosanchez@example.com", "2023-07-22"),
            ("cliente", "Laura Diaz", "Calle Mar 159", "3104789652", "lauradiaz@example.com", "2023-08-30"),
            ("cliente", "Jorge Ramirez", "Boulevard Rio 753", "3123698745", "jorgeramirez@example.com", "2023-09-14"),
            ("admin", "Elena Morales", "Avenida Cielo 852", "3216549870", "elenamorales@example.com", "2023-10-01"),
            ("cliente", "Andres Gutierrez", "Calle Tierra 951", "3107894561", "andresgutierrez@example.com", "2023-11-11"),
            ("cliente", "Marta Lopez", "Avenida Viento 357", "3124789653", "martalopez@example.com", "2023-12-25"),
            ("admin", "Ricardo Jimenez", "Calle Agua 258", "3219876540", "ricardojimenez@example.com", "2024-01-05"),
            ("cliente", "Gabriela Castillo", "Boulevard Fuego 147", "3106543219", "gabrielacastillo@example.com", "2024-02-14"),
            ("cliente", "Fernando Vega", "Avenida Montaña 369", "3123456789", "fernandovega@example.com", "2024-03-22"),
            ("admin", "Isabel Rojas", "Calle Valle 741", "3211234567", "isabelrojas@example.com", "2024-04-18"),
            ("cliente", "Diego Moreno", "Avenida Playa 852", "3109876543", "diegomoreno@example.com", "2024-05-30"),
            ("cliente", "Natalia Herrera", "Calle Bosque 963", "3128765432", "nataliaherrera@example.com", "2024-06-15"),
            ("admin", "Santiago Alvarez", "Boulevard Campo 159", "3214567890", "santiagoalvarez@example.com", "2024-07-04"),
            ("cliente", "Valentina Cruz", "Avenida Ciudad 753", "3103216548", "valentinacruz@example.com", "2024-08-19"),
            ("cliente", "Sebastian Flores", "Calle Pueblo 258", "3121598746", "sebastianflorez@example.com", "2024-09-27"),
            ("admin", "Camila Medina", "Avenida Centro 147", "3217894562", "camilamedina@example.com", "2024-10-13"),
            ("cliente", "Alejandro Soto", "Boulevard Distrito 369", "3106549871", "alejandrosoto@example.com", "2024-11-29"),
            ("cliente", "Daniela Vargas", "Calle Municipio 741", "3129871234", "danielavargas@example.com", "2024-12-31"),
            ("admin", "Miguel Ortega", "Avenida Provincia 852", "3213216549", "miguelortega@example.com", "2025-01-20")
        ]
        cursor.executemany('INSERT INTO usuario (rol, nombre, direccion, telefono, email, fecha_registro) VALUES (?, ?, ?, ?, ?, ?)', usuario_ejemplo)
        
        Cuenta_ejemplo = [
            (1, 'Ahorros', 1500.00, '2022-01-15', 'Activo'),
            (2, 'Corriente', 2500.50, '2021-06-20', 'Activo'),
            (3, 'Ahorros', 3000.75, '2023-03-10', 'Inactivo'),
            (4, 'Corriente', 1200.00, '2020-11-05', 'Activo'),
            (5, 'Ahorros', 500.25, '2022-08-30', 'Inactivo'),
            (6, 'Corriente', 750.00, '2021-12-12', 'Activo'),
            (7, 'Ahorros', 2000.00, '2023-05-22', 'Activo'),
            (8, 'Corriente', 1800.40, '2022-03-14', 'Inactivo'),
            (9, 'Ahorros', 2200.60, '2021-09-18', 'Activo'),
            (10, 'Corriente', 1600.80, '2020-07-25', 'Activo'),
            (11, 'Ahorros', 1400.90, '2023-01-30', 'Inactivo'),
            (12, 'Corriente', 2700.10, '2022-04-16', 'Activo'),
            (13, 'Ahorros', 3200.55, '2021-11-11', 'Activo'),
            (14, 'Corriente', 1300.35, '2020-10-09', 'Inactivo'),
            (15, 'Ahorros', 600.45, '2023-06-05', 'Activo'),
            (16, 'Corriente', 800.75, '2022-02-28', 'Activo'),
            (17, 'Ahorros', 2100.85, '2021-08-23', 'Inactivo'),
            (18, 'Corriente', 1700.95, '2020-12-19', 'Activo'),
            (19, 'Ahorros', 1500.15, '2023-04-07', 'Activo'),
            (20, 'Corriente', 2600.25, '2022-05-13', 'Inactivo'),
            (21, 'Ahorros', 3100.35, '2021-10-29', 'Activo'),
            (22, 'Corriente', 1400.45, '2020-09-17', 'Activo'),
            (23, 'Ahorros', 700.55, '2023-02-03', 'Inactivo'),
            (24, 'Corriente', 900.65, '2022-06-21', 'Activo'),
            (25, 'Ahorros', 2300.75, '2021-07-14', 'Activo')
        ]
        cursor.executemany('INSERT INTO Cuenta (usuario, tipo, saldo, fecha_apertura, estado) VALUES (?, ?, ?, ?, ?)', Cuenta_ejemplo)
        
        transaccion_ejemplo = [
            (1, 'Deposito', 500.00, '2023-07-01 10:30:00'),
            (2, 'Retiro', 200.00, '2023-07-02 14:15:00'),
            (3, 'Transferencia', 150.00, '2023-07-03 09:45:00'),
            (4, 'Retiro', 100.00, '2023-07-04 11:20:00'),
            (5, 'Deposito', 300.00, '2023-07-05 16:50:00'),
            (6, 'Transferencia', 250.00, '2023-07-06 13:10:00'),
            (7, 'Deposito', 400.00, '2023-07-07 12:00:00'),
            (8, 'Retiro', 150.00, '2023-07-08 15:30:00'),
            (9, 'Transferencia', 350.00, '2023-07-09 10:05:00'),
            (10, 'Deposito', 600.00, '2023-07-10 14:40:00'),
            (11, 'Retiro', 200.00, '2023-07-11 09:25:00'),
            (12, 'Transferencia', 450.00, '2023-07-12 11:55:00'),
            (13, 'Deposito', 700.00, '2023-07-13 16:15:00'),
            (14, 'Retiro', 300.00, '2023-07-14 13:35:00'),
            (15, 'Transferencia', 500.00, '2023-07-15 10:50:00'),
            (16, 'Deposito', 800.00, '2023-07-16 15:20:00'),
            (17, 'Retiro', 250.00, '2023-07-17 12:45:00'),
            (18, 'Transferencia', 600.00, '2023-07-18 09:30:00'),
            (19, 'Deposito', 900.00, '2023-07-19 14:10:00'),
            (20, 'Retiro', 350.00, '2023-07-20 11:55:00'),
            (21, 'Transferencia', 700.00, '2023-07-21 10:20:00'),
            (22, 'Deposito', 1000.00, '2023-07-22 15:45:00'),
            (23, 'Retiro', 400.00, '2023-07-23 13:15:00'),
            (24, 'Transferencia', 800.00, '2023-07-24 09:40:00'),
            (25, 'Deposito', 1100.00, '2023-07-25 14:05:00')
        ]
        cursor.executemany('INSERT INTO transaccion (cuenta, tipo, monto, fecha_hora) VALUES (?, ?, ?, ?)', transaccion_ejemplo)

        tarjeta_ejemplo = [
            (1, 'Debito', '1234-5678-9012-3456', '2023-01-15', '2026-01-15', 'Activo'),
            (2, 'Credito', '2345-6789-0123-4567', '2022-06-20', '2025-06-20', 'Activo'),
            (3, 'Debito', '3456-7890-1234-5678', '2023-03-10', '2026-03-10', 'Inactivo'),
            (4, 'Credito', '4567-8901-2345-6789', '2021-11-05', '2024-11-05', 'Activo'),
            (5, 'Debito', '5678-9012-3456-7890', '2022-08-30', '2025-08-30', 'Inactivo'),
            (6, 'Credito', '6789-0123-4567-8901', '2021-12-12', '2024-12-12', 'Activo'),
            (7, 'Debito', '7890-1234-5678-9012', '2023-05-22', '2026-05-22', 'Activo'),
            (8, 'Credito', '8901-2345-6789-0123', '2022-03-14', '2025-03-14', 'Inactivo'),
            (9, 'Debito', '9012-3456-7890-1234', '2021-09-18', '2024-09-18', 'Activo'),
            (10, 'Credito', '0123-4567-8901-2345', '2020-07-25', '2023-07-25', 'Activo'),
            (11, 'Debito', '1123-4567-8901-2345', '2023-01-30', '2026-01-30', 'Inactivo'),
            (12, 'Credito', '2123-4567-8901-2345', '2022-04-16', '2025-04-16', 'Activo'),
            (13, 'Debito', '3123-4567-8901-2345', '2021-11-11', '2024-11-11', 'Activo'),
            (14, 'Credito', '4123-4567-8901-2345', '2020-10-09', '2023-10-09', 'Inactivo'),
            (15, 'Debito', '5123-4567-8901-2345', '2023-06-05', '2026-06-05', 'Activo'),
            (16, 'Credito', '6123-4567-8901-2345', '2022-02-28', '2025-02-28', 'Activo'),
            (17, 'Debito', '7123-4567-8901-2345', '2021-08-23', '2024-08-23', 'Inactivo'),
            (18, 'Credito', '8123-4567-8901-2345', '2020-12-19', '2023-12-19', 'Activo'),
            (19, 'Debito', '9123-4567-8901-2345', '2023-04-07', '2026-04-07', 'Activo'),
            (20, 'Credito', '0223-4567-8901-2345', '2022-05-13', '2025-05-13', 'Inactivo'),
            (21, 'Debito', '1323-4567-8901-2345', '2021-10-29', '2024-10-29', 'Activo'),
            (22, 'Credito', '2423-4567-8901-2345', '2020-09-17', '2023-09-17', 'Activo'),
            (23, 'Debito', '3523-4567-8901-2345', '2023-02-03', '2026-02-03', 'Inactivo'),
            (24, 'Credito', '4623-4567-8901-2345', '2022-06-21', '2025-06-21', 'Activo'),
            (25, 'Debito', '5723-4567-8901-2345', '2021-07-14', '2024-07-14', 'Activo')
        ]    
        cursor.executemany('INSERT INTO tarjeta (cuenta, tipo, numero_tarjeta, fecha_emision, fecha_vencimiento, estado) VALUES (?, ?, ?, ?, ?, ?)', tarjeta_ejemplo)

        # ventas_ejemplo = [
        #     (1, 1, 1),
        #     (2, 2, 2),
        #     (1, 3, 1),
        #     (3, 1, 1),
        #     (4, 4, 1)
        # ]
        # cursor.executemany('INSERT INTO ventas (usuario_id, producto_id, cantidad) VALUES (?, ?, ?)', ventas_ejemplo)
    
    conn.commit()
    conn.close()

def execute_query(query, params=None):
    """Ejecuta una consulta SQL y retorna los resultados"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = sqlite3.Row  # Para obtener resultados como diccionarios
        cursor = conn.cursor()
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        # Determinar si es una consulta SELECT o una operación de modificación
        if query.strip().upper().startswith('SELECT'):
            results = [dict(row) for row in cursor.fetchall()]
            columns = [description[0] for description in cursor.description]
        else:
            conn.commit()
            results = {"affected_rows": cursor.rowcount, "message": "Query executed successfully"}
            columns = []
        
        conn.close()
        return {"success": True, "data": results, "columns": columns}
    
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.route('/')
def index():
    """Página principal con el formulario para consultas SQL"""
    return render_template('index.html')

@app.route('/execute', methods=['POST'])
def execute_sql():
    """Endpoint para ejecutar consultas SQL"""
    data = request.get_json()
    query = data.get('query', '').strip()
    
    if not query:
        return jsonify({"success": False, "error": "Query cannot be empty"})
    
    result = execute_query(query)
    return jsonify(result)

@app.route('/schema')
def get_schema():
    """Endpoint para obtener el esquema de la base de datos"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        # Obtener información de las tablas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
        tables = cursor.fetchall()
        
        schema = {}
        for table in tables:
            table_name = table[0]
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            schema[table_name] = [{"name": col[1], "type": col[2], "nullable": not col[3], "primary_key": bool(col[5])} for col in columns]
        
        conn.close()
        return jsonify({"success": True, "schema": schema})
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/examples')
def get_examples():
    """Endpoint que retorna consultas SQL de ejemplo"""
    examples = [
        {
            "title": "Listar todos los usuarios",
            "query": "SELECT * FROM usuarios;"
        },
        {
            "title": "Productos con precio mayor a 100",
            "query": "SELECT * FROM productos WHERE precio > 100;"
        },
        {
            "title": "Contar usuarios por edad",
            "query": "SELECT edad, COUNT(*) as cantidad FROM usuarios GROUP BY edad ORDER BY edad;"
        },
        {
            "title": "Ventas con información de usuarios y productos",
            "query": """SELECT 
                v.id as venta_id,
                u.nombre as usuario,
                p.nombre as producto,
                v.cantidad,
                v.fecha_venta
            FROM ventas v
            JOIN usuarios u ON v.usuario_id = u.id
            JOIN productos p ON v.producto_id = p.id
            ORDER BY v.fecha_venta DESC;"""
        },
        {
            "title": "Insertar nuevo usuario",
            "query": "INSERT INTO usuarios (nombre, email, edad) VALUES ('Nuevo Usuario', 'nuevo@email.com', 25);"
        },
        {
            "title": "Actualizar precio de producto",
            "query": "UPDATE productos SET precio = 899.99 WHERE nombre = 'Laptop';"
        }
    ]
    return jsonify({"examples": examples})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)