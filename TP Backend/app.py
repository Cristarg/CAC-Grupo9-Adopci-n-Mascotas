import mysql.connector

class Catalogo:
    mascotas = []

    def __init__(self,host,user,password,database):

        self.conn = mysql.connector.connect(
            host = host,
            user = user,
            password = password,
            database = database
        )
        self.cursor = self.conn.cursor(dictionary=True)

    def agregar_mascota(self,nombre,edad,descripcion,imagen):
        sql = "INSERT INTO mascotas (nombre,edad,descripcion,imagen_url) VALUES (%s, %s, %s, %s)"
        valores = (nombre, edad, descripcion, imagen)
        self.cursor.execute(sql, valores)
        self.conn.commit()
        return self.cursor.lastrowid

    def consultar_mascota(self,codigo):
        self.cursor.execute(f"SELECT * FROM mascotas WHERE codigo = {codigo}")
        return self.cursor.fetchone()

    def modificar_mascota(self,codigo,nuevo_nombre,nueva_edad,nueva_descripcion,nueva_imagen):
        sql = "UPDATE mascotas SET nombre = %s, edad = %s, descripcion = %s, imagen_url = %s WHERE codigo = %s"
        valores = (nuevo_nombre, nueva_edad, nueva_descripcion, nueva_imagen, codigo)
        self.cursor.execute(sql, valores)
        self.conn.commit()
        return self.cursor.rowcount > 0

    def mostrar_mascota(self,codigo):
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

    def listar_mascota(self):
        self.cursor.execute("SELECT * FROM mascotas")
        mascota = self.cursor.fetchall()
        return mascota

    def eliminar_mascota(self, codigo):
        self.cursor.execute(f"DELETE FROM mascotas WHERE codigo = {codigo}")
        self.conn.commit()
        return self.cursor.rowcount > 0

catalogo = Catalogo(host='localhost', user='root', password='',database='miapp')

'''
catalogo.agregar_mascota("Elisio","8 meses", "Negro con marron",'perrito.jfif')
catalogo.agregar_mascota("Chicho", "3 años", "blanco",'perrito2.jfif')
catalogo.agregar_mascota("Fifi", "2 meses", "marron",'perrito3.jfif')
catalogo.agregar_mascota('licho', '2 años', 'hembra marron', 'perrito1.jfif')
'''
catalogo.agregar_mascota('licho', '2 años', 'hembra marron', 'perrito1.jfif')

cod_mascota = int(input("Ingrese el codigo del producto: "))
mascota = catalogo.consultar_mascota(cod_mascota)
if mascota:
    print(f"Mascota encontrada: {mascota['codigo']} - {mascota['nombre']}")
else:
    print(f'Mascota {cod_mascota} no encontrada.')

catalogo.mostrar_mascota(4)
catalogo.modificar_mascota(4,'Lali', '1 año', 'hembrita negra','perrito4.jfif')
catalogo.mostrar_mascota(4)

mascotas = catalogo.listar_mascota()
for mascota in mascotas:
    print(mascota)


catalogo.eliminar_mascota(8)
mascotas = catalogo.listar_mascota()
for mascota in mascotas:
    print(mascota)

