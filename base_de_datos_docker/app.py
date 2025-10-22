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
            rol TEXT NOT NULL,
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            direccion TEXT NOT NULL,
            telefono TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            fecha_registro DATE DEFAULT CURRENT_DATE,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Crear tabla de productos de ejemplo
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Cuenta (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL,
            tipo TEXT NOT NULL,
            saldo decimal NOT NULL,
            fecha_apertura DATE DEFAULT CURRENT_DATE,
            estado TEXT NOT NULL
        )
    ''')
    

    
    # Crear tabla de ventas de ejemplo
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            producto_id INTEGER,
            cantidad INTEGER,
            fecha_venta DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id),
            FOREIGN KEY (producto_id) REFERENCES productos (id)
        )
    ''')
    
    # Insertar datos de ejemplo si no existen
    cursor.execute('SELECT COUNT(*) FROM usuario')
    if cursor.fetchone()[0] == 0:
        usuarios_ejemplo = [
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
        cursor.executemany('INSERT INTO usuario (rol, nombre, direccion, telefono, email, fecha_registro) VALUES (?, ?, ?, ?, ?, ?)', usuarios_ejemplo)
        
        Cuenta_ejemplo = [(1, 'Ahorros', 1500.00, '2022-01-15', 'Activo'),
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

        transacciones_ejemplo = [
        # productos_ejemplo = [
        #     ('Laptop', 999.99, 'Electrónicos', 15),
        #     ('Mouse', 25.50, 'Accesorios', 50),
        #     ('Teclado', 45.00, 'Accesorios', 30),
        #     ('Monitor', 299.99, 'Electrónicos', 20),
        #     ('Silla Gaming', 199.99, 'Muebles', 8)
        # ]
        # cursor.executemany('INSERT INTO productos (nombre, precio, categoria, stock) VALUES (?, ?, ?, ?)', productos_ejemplo)
        
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