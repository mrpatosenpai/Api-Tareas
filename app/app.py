from flask import Flask, jsonify , request
from flask_mysqldb import MySQL
from config import config

app = Flask(__name__)
conexion = MySQL(app)

# Página principal
@app.route('/')
def index():
    return '¡Hola! Esta es la página principal.'

@app.route('/listatareas', methods=['GET'])
def listatareas():
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT * FROM tareas"
        cursor.execute(sql)
        datos = cursor.fetchall()
        tareas =[]
        for fila in datos:
            tarea = {
                'id_tarea': fila[0],
                'nombre': fila[1],
                'fechainicio': str(fila[2]),
                'fechafinal': str(fila[3]),
                'estado': fila[4]
            }
            tareas.append(tarea)
        return jsonify(tareas)

    except Exception as ex:
        return jsonify({'error': 'Error al obtener las tareas', 'mensaje': str(ex), 'exito': False})
    

@app.route('/buscartareas', methods=['GET'])
def buscartareas():
    consulta = 'SELECT * FROM tareas'
    filtro = []
    parametros = []

    nombre = request.args.get('nombre')
    if nombre:
        filtro.append("nombre LIKE %s")
        parametros.append(f"%{nombre}%")
    if not filtro:
        return jsonify({'message' :'no tiene parametros la busqueda'}),400

    consulta += "WHERE" + "AND".join(filtro)
    cursor = conexion.connection.cursor()
    cursor.execute(consulta, parametros)
    datos = cursor.fetchall()
    tareas =[]
    for fila in datos:
            tarea = {
                'id_tarea': fila[0],
                'nombre': fila[1],
                'fechainicio': str(fila[2]),
                'fechafinal': str(fila[3]),
                'estado': fila[4]
            }
            tareas.append(tarea)
    return jsonify(tareas)


if __name__ == '__main__':
    app.config.from_object(config['config'])
    app.run(debug=True)
