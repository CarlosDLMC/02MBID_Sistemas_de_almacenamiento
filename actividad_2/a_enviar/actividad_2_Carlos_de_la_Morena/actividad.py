from cassandra.cluster import Cluster

#Clases de modelos conceptuales

class Productor():
    def __init__(self, CodPro, Media_Produccion, Maximo_Produccion, Nombre, Pais, Origen_Energia):
        self.CodPro = CodPro
        self.Media_Produccion = Media_Produccion
        self.Maximo_Produccion = Maximo_Produccion
        self.Nombre = Nombre
        self.Pais = Pais
        self.Origen_Energia = Origen_Energia

class Provee():
    def __init__(self, CodPro, CodEst, Fecha, Cantidad):
        self.CodPro = CodPro
        self.CodEst = CodEst
        self.Fecha = Fecha
        self.Cantidad = Cantidad

class Estacion():
    def __init__(self, CodEst, Nombre):
        self.CodEst = CodEst
        self.Nombre = Nombre

class Distribucion_de_red():
    def __init__(self, CodDis, Longitud_maxima, CodEst):
        self.CodDis = CodDis
        self.Longitud_maxima = Longitud_maxima
        self.CodEst = CodEst

class Linea():
    def __init__(self, CodLin, Longitud, CodDis):
        self.CodLin = CodLin
        self.Longitud = Longitud
        self.CodDis = CodDis

class Subestacion():
    def __init__(self, CodSub, Capacidad, CodLin):
        self.CodSub = CodSub
        self.Capacidad = Capacidad
        self.CodLin = CodLin

class Distribuye():
    def __init__(self, CodSub, ZonCod, Cantidad, Fecha):
        self.CodSub = CodSub
        self.ZonCod = ZonCod
        self.Cantidad = Cantidad
        self.Fecha = Fecha

class Zona():
    def __init__(self, ZonCod, Nombre, Municipios, ProCod):
        self.ZonCod = ZonCod
        self.Nombre = Nombre
        self.Municipios = Municipios
        self.ProCod = ProCod

class Provincia():
    def __init__(self, ProCod, Jefes_provinciales, Nombre):
        self.ProCod = ProCod
        self.Jefes_provinciales = Jefes_provinciales
        self.Nombre = Nombre


def insert_provincia_en_tabla_para_consulta():
    ProCod = int(input("Dame el Código de la provincia: "))
    Jefes_provinciales = set()
    print("Hay varios jefes provinciales, escríbelos de uno en uno.")
    while True:
        jefe = input("Introduce un jefe provincial, pulsa q para terminar: ")
        if jefe == 'q':
            break
        Jefes_provinciales.add(jefe)
    Nombre = input("Dime el nombre de la provincia: ")
    for jefe in Jefes_provinciales:
        insert_statement = session.prepare("INSERT INTO jefes_provinciales_por_provincia (Provincia_Nombre, Provincia_Jefe_provincial) VALUES (?, ?)")
        session.execute(insert_statement, [Nombre, jefe])

def insert_provincia_en_tabla_simple():
    ProCod = int(input("Dame el Código de la provincia: "))
    Jefes_provinciales = set()
    while True:
        jefe = input("Introduce un jefe provincial, pulsa q para terminar: ")
        if jefe == 'q':
            break
        Jefes_provinciales.add(jefe)
    Nombre = input("Dime el nombre de la provincia: ")
    provincia = Provincia(ProCod, Jefes_provinciales, Nombre)
    insert_statement = session.prepare("INSERT INTO Provincias (ProCod, Jefes_provinciales, Nombre) VALUES (?, ?)")
    session.execute(insert_statement, [provincia.ProCod, provincia.Jefes_provinciales, provincia.Nombre])

def insert_productor_en_tabla_para_consulta():
    CodPro = int(input("Dame el Código del productor: "))
    Pais = input("Dime el nombre del país: ")
    Origen = input("Dime el origen de la energía: ")
    Nombre = input("Dime el nombre del productor: ")
    insert_statement = session.prepare("INSERT INTO productor_por_origen (Productor_Origen_energia, Productor_Pais, Productor_CodPro, Productor_Nombre) VALUES (?, ?, ?, ?)")
    session.execute(insert_statement, [Origen, Pais, CodPro, Nombre])

def update_province_name():
    old_province = input("Dime el nombre de la provincia que quieres renombrar: ")
    new_province = input("Dime el nuevo nombre: ")
    select = session.prepare("SELECT provincia_jefe_provincial FROM jefes_provinciales_por_provincia WHERE provincia_nombre = ?")
    jefes = session.execute(select, [old_province, ])
    if not jefes:
        print("¡Error! Esa provincia no se encuentra en esta tabla.")
        return
    remove = session.prepare("DELETE FROM jefes_provinciales_por_provincia WHERE provincia_nombre = ?")
    session.execute(remove, [old_province, ])
    jefes_string = [jefe[0] for jefe in jefes]
    insert = session.prepare("INSERT INTO jefes_provinciales_por_provincia (provincia_nombre, provincia_jefe_provincial) VALUES (?, ?)")
    for jefe in jefes_string:
        session.execute(insert, [new_province, jefe])

def update_power_source():
    old_source = input("Dime la antigua fuente de energía: ")
    new_source = input("Dime la nueva fuente de energía: ")
    country = input("Dime el país: ")
    select = session.prepare("SELECT productor_codpro, productor_nombre FROM productor_por_origen WHERE productor_origen_energia = ? AND productor_pais = ?")
    datos = session.execute(select, [old_source, country])
    if not datos:
        print("¡Error! No se encontró ninguna columna con ese país y esa fuente de energía.")
        return
    remove = session.prepare("DELETE FROM productor_por_origen WHERE productor_origen_energia = ? AND productor_pais = ?")
    session.execute(remove, [old_source, country])
    insert = session.prepare("INSERT INTO productor_por_origen (productor_origen_energia, productor_pais, productor_codpro, productor_nombre) VALUES (?, ?, ?, ?)")
    for entrada in datos:
        session.execute(insert, [new_source, country, entrada[0], entrada[1]])

def consultar_jefes_provinciales_segun_provincia():
    provincia = input("Por favor, introduzca la provincia que desea buscar: ")
    select = session.prepare("SELECT provincia_jefe_provincial FROM jefes_provinciales_por_provincia WHERE provincia_nombre = ?")
    jefes = session.execute(select, [provincia, ])
    if not jefes:
        print("No se encontró ninguna provincia con ese nombre")
    else:
        for jefe in jefes:
            print(f"Provincia: {provincia}, Jefe: {jefe.provincia_jefe_provincial}")

def consultar_productores_segun_energia():
    energia = input("Por favor, introduce el origen de la energía: ")
    pais = input("Por favor, introduce el país: ")
    select = session.prepare("SELECT * FROM productor_por_origen WHERE productor_origen_energia = ? AND productor_pais = ?")
    productores = session.execute(select, [energia, pais])
    if not productores:
        print("No se encontró ningún productor con esas características")
    else:
        for productor in productores:
            print(f"País: {pais}, Energía: {energia}, Código de productor: {productor.productor_codpro}, Nombre: {productor.productor_nombre}")


cluster = Cluster()
session = cluster.connect('carlosdelamorena')
numero = 1

while numero:
    print("\n\nIntroduce un número para seleccionar una operación. Pulse 0 para salir: ")
    print("1. Insertar una provincia")
    print("2. Insertar un productor")
    print("3. Actualizar nombre de provincia")
    print("4. Actualizar fuente de energía")
    print("5. Consultar jefes provinciales según provincia")
    print("6. Consultar productores según el origen de la energía")
    print("0. Cerrar aplicación")

    numero = int(input("Tu opción: "))
    if numero == 1:
        insert_provincia_en_tabla_para_consulta()
    elif numero == 2:
        insert_productor_en_tabla_para_consulta()
    elif numero == 3:
        update_province_name()
    elif numero == 4:
        update_power_source()
    elif numero == 5:
        consultar_jefes_provinciales_segun_provincia()
    elif numero == 6:
        consultar_productores_segun_energia()
    elif not numero:
        print("¡Adiós! Que tengas un buen día")
    else:
        print("El número seleccionado no se corresponde con ninguna opción. Prueba de nuevo")

session.shutdown()