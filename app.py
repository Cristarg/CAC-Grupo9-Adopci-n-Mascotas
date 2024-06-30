from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import mysql.connector.errorcode
from werkzeug.utils import secure_filename
import os
import time
app = Flask (__name__)
CORS(app)

class Catalogo:

    def __init__(self,host,user,password,database):
        self.conn = mysql.connector.connect(
            host = host,
            user = user,
            password = password,
            database=database
        )
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute(f"USE {database}")
        except mysql.connector.Error as err:
            if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                self.cursor.execute(f"CREATE DATABASE {database}")
                self.conn.database = database
            else:
                raise err
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS mascotas (codigo INT AUTO_INCREMENT PRIMARY KEY, nombre VARCHAR(255) NOT NULL, edad VARCHAR(255) NOT NULL, descripcion VARCHAR(255) NOT NULL, imagen_url VARCHAR(255))''')
        self.conn.commit()
        self.cursor.close()
        self.cursor = self.conn.cursor(dictionary=True)

    def listar_mascotas(self):
        self.cursor.execute("SELECT * FROM mascotas")
        mascotas = self.cursor.fetchall()
        return mascotas

    def consultar_mascota(self, codigo):
        self.cursor.execute(f"SELECT * FROM mascotas WHERE codigo = {codigo}")
        return self.cursor.fetchone()

    def mostrar_mascota(self, codigo):
        mascota = self.consultar_mascota(codigo)
        if mascota:
            print('=' * 40)
            print (f"Codigo..........: {mascota['codigo']}")
            print (f"Nombre..........: {mascota['nombre']}")
            print (f"Edad............: {mascota['edad']}")
            print (f"Descripción.....: {mascota['descripcion']}")
            print (f"Imagen..........: {mascota['imagen_url']}")
            print('=' * 50 )
        else:
            print("Producto no encontrado.")

    def agregar_mascota(self,nombre,edad,descripcion,imagen):
        sql = "INSERT INTO mascotas (nombre,edad,descripcion,imagen_url) VALUES (%s, %s, %s, %s)"
        valores = (nombre, edad, descripcion, imagen)
        self.cursor.execute(sql, valores)
        self.conn.commit()
        return self.cursor.lastrowid

    def modificar_mascota(self,codigo,nuevo_nombre,nueva_edad,nueva_descripcion,nueva_imagen):
        sql = "UPDATE mascotas SET nombre = %s, edad = %s, descripcion = %s, imagen_url = %s WHERE codigo = %s"
        valores = (nuevo_nombre, nueva_edad, nueva_descripcion, nueva_imagen, codigo)
        self.cursor.execute(sql, valores)
        self.conn.commit()
        return self.cursor.rowcount > 0

    def eliminar_mascota(self, codigo):
        self.cursor.execute(f"DELETE FROM mascotas WHERE codigo = {codigo}")
        self.conn.commit()
        return self.cursor.rowcount > 0

catalogo = Catalogo(host='Sasonador85.mysql.pythonanywhere-services.com', user='Sasonador85', password='root1234', database='Sasonador85$miapp')
ruta_destino = '/home/Sasonador85/mysite/static/imagenes'

@app.route("/mascotas", methods=["GET"])
def listar_mascotas():
    mascotas = catalogo.listar_mascotas()
    return jsonify(mascotas)

@app.route("/mascotas/<int:codigo>", methods=["GET"])
def mostrar_mascota(codigo):
    mascota = catalogo.consultar_mascota(codigo)
    if mascota:
        return jsonify(mascota), 201
    else:
        return "Producto no encontrado", 404

@app.route("/mascotas", methods=["POST"])
def agregar_producto():

    nombre = request.form['nombre']
    edad = request.form['edad']
    descripcion = request.form['descripcion']
    imagen = request.files['imagen']
    nombre_imagen = ""

    nombre_imagen = secure_filename(imagen.filename)
    nombre_base, extension = os.path.splitext(nombre_imagen)
    nombre_imagen = f"{nombre_base}_{int(time.time())}{extension}"

    nuevo_codigo = catalogo.agregar_mascota(nombre, edad, descripcion, nombre_imagen)
    if nuevo_codigo:
        imagen.save(os.path.join(ruta_destino, nombre_imagen))
        return jsonify({"mensaje": "Mascota agregada correctamente.","codigo": nuevo_codigo, "imagen": nombre_imagen}), 201
    else:
        return jsonify({"mensaje": "Error al agregar mascota."}), 500

@app.route("/mascotas/<int:codigo>", methods=["PUT"])
def modificar_mascota(codigo):

    nuevo_nombre = request.form.get("nombre")
    nueva_edad = request.form.get("edad")
    nueva_descripcion = request.form.get("descripcion")

    if 'imagen' in request.files:
        imagen = request.files['imagen']
        nombre_imagen = secure_filename(imagen.filename)
        nombre_base, extension = os.path.splitext(nombre_imagen)
        nombre_imagen = f"{nombre_base}_{int(time.time())}{extension}"
        imagen.save(os.path.join(ruta_destino, nombre_imagen))

    mascota = catalogo.consultar_mascota(codigo)
    if mascota:
        imagen_vieja = mascota["imagen_url"]
        ruta_imagen = os.path.join(ruta_destino, imagen_vieja)
        if os.path.exists(ruta_imagen):
            os.remove(ruta_imagen)
    else:
        mascota = catalogo.consultar_mascota(codigo)
        if mascota:
            nombre_imagen = mascota["imagen_url"]

    if catalogo.modificar_mascota(codigo, nuevo_nombre, nueva_edad, nueva_descripcion, nombre_imagen):
        return jsonify({"mensaje": "Mascota modificada"}), 200
    else:
        return jsonify({"mensaje": "Mascota no encontrada"}), 403

@app.route("/mascotas/<int:codigo>", methods=["DELETE"])
def eliminar_mascota(codigo):
    mascota = catalogo.consultar_mascota(codigo)
    if mascota:
        ruta_imagen = os.path.join(ruta_destino, mascota["imagen_url"])
        if os.path.exists(ruta_imagen):
            os.remove(ruta_imagen)

        if catalogo.eliminar_mascota(codigo):
            return jsonify({"mensaje": "Mascota eliminada"}), 200
        else:
            return jsonify({"mensaje": "Error al eliminar mascota."}), 500

    else:
        return jsonify({"mensaje": "Mascota no encontrada"}), 404

if __name__ == "__main__":
    app.run(debug=True)
