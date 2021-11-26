CREATE KEYSPACE carlosdelamorena WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 3};
CREATE TABLE jefes_provinciales_por_provincia (Provincia_Nombre text, Provincia_Jefe_provincial text, PRIMARY KEY(Provincia_Nombre, Provincia_Jefe_provincial));
CREATE TABLE longitud_por_capacidad (Subestacion_capacidad float, Linea_CodLin text, Linea_Longitud text, PRIMARY KEY(Subestacion_capacidad, Linea_CodLin));
CREATE TABLE info_provincia_por_jefe (Provincia_ProCod text, Provincia_Jefe_provincial text, Provincia_Nombre text, PRIMARY KEY(Provincia_ProCod, Provincia_Jefe_provincial));
CREATE TABLE estaciones_y_productores_por_fecha_y_cantidad (Provee_Fecha date, Provee_Cantidad float, Estacion_CodEst text, Productor_CodPro text, Estacion_Nombre text, Productor_Nombre text, PRIMARY KEY((Provee_Fecha, Provee_Cantidad),Estacion_CodEst, Productor_CodPro));
CREATE TABLE Subestaciones_por_distribucion (Distribucion_de_red_CodDis text, Linea_CodLin text, Subestacion_CodSub text, Linea_Longitud float, PRIMARY KEY(Distribucion_de_red_CodDis, Linea_CodLin, Subestacion_CodSub));
CREATE TABLE suma_capacidad_por_zona (Zona_ZonCod text, Subestacion_CodSub text, SumCapacidad counter, PRIMARY KEY(Zona_ZonCod, Subestacion_CodSub));
CREATE TABLE productores_por_longitud_maxima (Distribucion_de_red_Longitud_maxima float, Distribucion_de_red_CodDis text, Estacion_CodEst text, Productor_CodPro text, Productor_Nombre text, PRIMARY KEY(Distribucion_de_red_Longitud_maxima, Distribucion_de_red_CodDis, Estacion_CodEst, Productor_CodPro));
CREATE TABLE productor_por_origen (Productor_Origen_energia text, Productor_Pais text, Productor_CodPro float, Productor_Nombre text, PRIMARY KEY((Productor_Origen_energia, Productor_Pais), Productor_CodPro));

CREATE TABLE Provincias (ProCod float, Jefes_provinciales SET<text>, Nombre text, PRIMARY KEY(ProCod));
CREATE TABLE Productores (CodPro float, Media_produccion float, Maximo_produccion float, Nombre text, Pais text, Origen_energia text, PRIMARY KEY(CodPro));


