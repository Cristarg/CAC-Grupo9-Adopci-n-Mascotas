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
        self.cursor.execute('''CREATE DATABASE IF NOT EXISTS miapp;
            USE miapp;
            CREATE TABLE IF NOT EXISTS productos (
            codigo INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR (255) NOT Null,
            edad VARCHAR (255) NOT Null,
            descripcion VARCHAR(255) NOT NULL,
            imagen_url VARCHAR(255),
            ''')
        self.conn.commit()

    def agregar_mascota(self,codigo,nombre,edad,descripcion,imagen):
        if self.consultar_mascota(codigo):
            return False

        nueva_mascota = {
            'codigo': codigo,
            'nombre': nombre,
            'edad': edad,
            'descripcion': descripcion,
            'imagen': imagen
        }
        self.mascotas.append(nueva_mascota)
        return True

    def consultar_mascota(self,codigo):
        for mascota in self.mascotas:
            if mascota['codigo'] == codigo:
                return mascota
        return False

    def modificar_mascota(self,codigo,nuevo_nombre,nueva_edad,nueva_descripcion,nueva_imagen):
        for mascota in self.mascotas:
            if mascota['codigo'] == codigo:
                mascota['nombre'] = nuevo_nombre
                mascota['edad'] = nueva_edad
                mascota['descripcion'] = nueva_descripcion
                mascota['imagen'] = nueva_imagen
                return True
        return False

    def listar_mascota(self):
        print('/' * 50)
        for mascota in self.mascotas:
            print (f"Codigo..........: {mascota['codigo']}")
            print (f"Nombre..........: {mascota['nombre']}")
            print (f"Edad............: {mascota['edad']}")
            print (f"Descripción.....: {mascota['descripcion']}")
            print (f"Imagen..........: {mascota['imagen']}")
            print('/' * 50 )

    def eliminar_mascota(self,codigo):
        for mascota in self.mascotas:
            if mascota['codigo'] == codigo:
                self.mascotas.remove(mascota)
                return True
        return False

    def mostrar_mascota(self, codigo):
        mascota = self.consultar_mascota(codigo)
        if mascota:
            print("/" * 50)
            print(f"Código.......: {mascota['codigo']}")
            print(f"Nombre.......: {mascota['nombre']}")
            print(f"Edad.........: {mascota['edad']}")
            print(f"Descripcion..: {mascota['descripcion']}")
            print(f"Imagen.......: {mascota['imagen']}")
            print("/" * 50)
        else:
            print(f'La mascota {codigo} no existe')

catalogo = Catalogo()

catalogo.agregar_mascota (1,"Elisio","8 meses", "Negro con marron",'perrito.jfif')
catalogo.agregar_mascota (2,"Chicho", "3 años", "blanco",'perrito2.jfif')
catalogo.agregar_mascota (3, "Fifi", "2 meses", "marron",'perrito3.jfif')

print("Imprimo la mascota 3 antes de modificarla:")
print(catalogo.consultar_mascota(3))
catalogo.modificar_mascota(3, 'licha', "2 años", 'moteada','perrito3.jfif')
print("Imprimo la mascota 3 después de modificarla:")
print(catalogo.consultar_mascota(3))

catalogo.listar_mascota()

catalogo.mostrar_mascota(2)