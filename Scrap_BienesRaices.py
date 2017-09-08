from bs4 import BeautifulSoup
import requests
import re
import math
import sys
import time
import pypyodbc
import googlemaps as gm



# extrae los datos
def extraer(proy):

    try:

        # Obtiene y luego ingresa al link del departamento específico para obtener más información
        link_p = "https://www.portalinmobiliario.com" + proy.find('a').get('href')
        # Ingresa al link del departamento
        r3 = requests.get(link_p)
        datap = r3.text
        soup_p = BeautifulSoup(datap, "html.parser")

        br = bienraiz()

        seg = True

        if n2 == 'casa':

            #gmaps = gm.Client(key='AIzaSyA6AaSaLyq84mS12xm8YnQuMsXuig4toF8')

            # from googlemaps import GoogleMaps
            # gmaps = GoogleMaps(api_key)
            # address = 'Constitution Ave NW & 10th St NW, Washington, DC'
            # lat, lng = gmaps.address_to_latlng(address)

            # Obtiene y luego ingresa al link del departamento específico para obtener más información
            br.datos['Link'] = link_p

            if soup_p.find('section', attrs={"class": "project-features-section"}) != None:

                br.datos['Nuevo'] = True
                br.datos['Operacion'] = 'Venta'

                a = soup_p.find('div',
                                attrs={"class": "row prj-description-panel"}).text.splitlines()  # descripcion 1
                a = [x for x in a if x != '']
                br.datos['Descripcion'] = ''
                for linea in range(len(a) - 1):
                    br.datos['Descripcion'] += a[linea + 1] + ' '

                b = soup_p.find('div',
                                attrs={"class": "row prj-highlights-panel"}).text.splitlines()  # descripcion 2
                b = [x for x in b if x != '']

                if len(b) > 1:
                    for linea in range(len(b) - 1):
                        br.datos['Descripcion'] += b[linea] + ' '
                else:
                    br.datos['Descripcion'] += b[0]

                c = str(
                    soup_p.find('div', attrs={"class": "row text-center prj-other-info"}).text.splitlines()[
                        4]).split(" ")  # entrega / propietario / contruye / arquitectos / gestion (4 o 5)

                br.datos['Fecha_entrega'] = ''
                for linea in range(c.index('Propietario') - 3):
                    br.datos['Fecha_entrega'] += c[linea] + ' '

                d = soup_p.find('div', attrs={"class": "prj-addr"}).text.splitlines()  # direccion
                d = d[2].split(',')
                br.datos['Comuna'] = ''
                br.datos['Calle'] = ''
                br.datos['Region'] = ''
                br.datos['Ciudad'] = ''
                if len(d) == 3:
                    br.datos['Comuna'] = d[1]
                    br.datos['Calle'] = d[0]
                    br.datos['Region'] = d[2]
                elif len(d) == 5:
                    br.datos['Comuna'] = d[3]
                    br.datos['Calle'] = d[0]
                    br.datos['Region'] = d[4]

                try:
                    e = soup_p.find('div', attrs={
                        "class": "row prj-infographics normal-density"}).text.splitlines()  # tipo / dorm / bano / m2
                except:
                    e = soup_p.find('div', attrs={"class": "row prj-infographics hi-density"}).text.splitlines()

                e = [x for x in e if x != '']

                br.datos['Dorm'] = int(e[1][0])

                br.datos['Banos'] = int(e[2][0])

                if 'a' in e[3]:
                    m2 = e[3].split('a')[0].lstrip().rstrip()
                    if ',' in m2:
                        br.datos['m2_construidos'] = float(m2.replace(',','.'))
                    else:
                        br.datos['m2_construidos'] = float(m2)
                else:
                    m2 = e[3][:-3]
                    if ',' in m2:
                        br.datos['m2_construidos'] = float(m2.replace(',', '.'))
                    else:
                        br.datos['m2_construidos'] = float(m2)

                br.datos['m2_terreno'] = 0

                f = soup_p.find('div', attrs={"class": "prj-price"}).text.splitlines()  # valor
                f = [x for x in f if x != '']

                br.datos_precio['Uf'] = float(f[0].split('UF')[1].lstrip().rstrip().replace('.', '').replace(',', '.'))

                if br.datos['m2_construidos'] > 0:
                    br.datos_precio['Razon_construidos'] = br.datos_precio['Uf'] / br.datos['m2_construidos']

                br.datos_precio['Razon_terreno'] = 0
                br.datos['Lat'] = 0
                br.datos['Long'] = 0
                br.datos['Fecha_pub'] = str(time.strftime("%d/%m/%Y"))

                g = soup_p.find('div', attrs={"class": "prj-name"}).text.splitlines()  # nombre

                br.datos['Nombre'] = g[1]

            elif soup_p.find('div', attrs={"class": "map-box map-box-preview"}) != None:

                br.datos['Comuna'] = ''
                br.datos['Calle'] = ''
                br.datos['Region'] = ''
                br.datos['Ciudad'] = ''
                br.datos['Nuevo'] = False

                br.datos['Fecha_entrega'] = ''

                br.datos['Descripcion'] = soup_p.find('div', attrs={"class": "propiedad-descr"}).text.splitlines()[
                    1].rstrip().lstrip()  # descripcion

                if soup_p.find('div', attrs={"class": "propiedad-ficha-equipamiento"}) != None:
                    b = soup_p.find('div',
                                    attrs={"class": "propiedad-ficha-equipamiento"}).text.splitlines()  # equipamiento

                for dato in soup_p.find('div', attrs={"class": "property-data-sheet clearfix"}).find_all(
                        'div'):  # direccion / programa / superfice
                    data = dato.text.splitlines()
                    data = [x for x in data if x != '']  # remueve todos los vacios
                    if data[0] == 'Programa':
                        d = data[1].split(';')
                        br.datos['Dorm'] = int(d[0][0])
                        br.datos['Banos'] = int(d[1][0])

                    elif data[0] == 'Superficie':
                        d = data[1].split('m²')

                        m2c = 0
                        m2t = 0

                        if len(d) > 2:
                            m2c = d[0].lstrip().rstrip().replace('.', '')
                            m2t = d[1][11:].lstrip().rstrip().replace('.', '')

                            if ',' in m2c:
                                m2c = m2c.replace(',','.')

                            if ',' in m2t:
                                m2t = m2t.replace(',','.')

                            m2c = float(m2c)
                            m2t = float(m2t)

                            if m2c > 35000:
                                m2c = int(m2c / 1000)

                            if m2c == m2t and m2c > 500:
                                m2c = 0

                            if m2c > m2t * 3:
                                aux = m2c
                                m2c = m2t
                                m2t = aux

                            br.datos['m2_construidos'] = m2c
                            br.datos['m2_terreno'] = m2t

                        else:
                            if d[1].lspretip().lstrip() == 'terreno':
                                br.datos['m2_terreno'] = d[0]
                            else:
                                br.datos['m2_construidos'] = d[0]

                d = soup_p.find('div', attrs={"class": "media-block-meta"}).text.splitlines()  # valor
                d = [x for x in d if x != '']
                br.datos['Nombre'] = d[0]
                if "m²" not in d[2]:
                    br.datos_precio['Uf'] = float(
                        d[2].split(' ')[1].replace('.', '').lstrip().rstrip().replace(',', '.'))
                else:
                    if br.datos['m2_terreno'] > 0:
                        br.datos_precio['Uf'] = float(
                            d[2].split(' ')[1].replace('.', '').lstrip().rstrip().replace(',', '.').split('/')[0]) * \
                                                br.datos['m2_terreno']

                for div in soup_p.find_all('div', attrs={"class": "content-panel"}):
                    tabla = div.text.splitlines()
                    if len(div['class']) == 2:
                        if div['class'][1] == 'small-content-panel':
                            tabla.remove('')
                            br.datos['Fecha_pub'] = tabla[1].split(':')[1].lstrip().rstrip()
                    else:
                        tabla = [x for x in tabla if x != '']
                        if tabla[0] == 'Vende':
                            br.datos['Operacion'] = 'Venta'
                        elif tabla[0] == 'Arrienda':
                            br.datos['Operacion'] = 'Arriendo'

                        br.datos['Vendedor'] = tabla[1]

                # vendedor

                br.datos['Lat'] = float(
                    soup_p.find('div', attrs={"class": "map-box map-box-preview"}).contents[1]['content'])  # latitud
                br.datos['Long'] = float(
                    soup_p.find('div', attrs={"class": "map-box map-box-preview"}).contents[3]['content'])  # longitud

                br.datos_precio['Razon_terreno'] = ''
                br.datos_precio['Razon_construidos'] = ''
                if br.datos['m2_terreno'] > 0:
                    br.datos_precio['Razon_terreno'] = br.datos_precio['Uf'] / br.datos['m2_terreno']
                if br.datos['m2_construidos'] > 0:
                    br.datos_precio['Razon_construidos'] = br.datos_precio['Uf'] / br.datos['m2_construidos']

            else:
                seg = False



    except:
        tex = sys.exc_info()
        print(tex[2].tb_lineno)
        print(tex[1])
        seg = False

    return br

# escribe los datos en la base de datos
def escribir(pro):

    try:

        if n2 == 'casa' and seg:
            # Intenta conectarse con la base de datos
            conn = pypyodbc.connect(r"Driver={Microsoft Access Driver (*.mdb, *.accdb)}; Dbq=C:\Users\Javier\Documents\Departamentos_DB3.accdb;")
            cur = conn.cursor()
            cur.execute("SELECT count(Id) FROM Casas WHERE Nombre='{}';".format(pro.datos['Nombre']));
            repeticiones = cur.fetchone()[0]
            nuevo = False

            if repeticiones == 0:
                nuevo = True

                # Crea un nuevo edificio en la base de datos
            if nuevo:
                cur.execute(("INSERT INTO Casas (Nombre, m2_terreno, m2_construidos, Dormitorios, Baños, Link," +
                             " Operacion, Latitud, Longitud,Fecha_publicacion, Descripcion) VALUES " +
                             "('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}');").format(
                    pro.datos['Nombre'], pro.datos['m2_terreno'],
                    pro.datos['m2_construidos'], pro.datos['Dorm'],
                    pro.datos['Banos'], pro.datos['Link'],
                    pro.datos['Operacion'], pro.datos['Lat'],
                    pro.datos['Long'], pro.datos['Fecha_pub'],
                    pro.datos['Descripcion']))

                cur.commit()

                cur.execute(("UPDATE Casas SET Nuevo = {}, Fecha_entrega = '{}', Calle = '{}', Comuna = '{}', Ciudad = '{}'," +
                         " Region = '{}' WHERE Nombre = '{}';").format(
                pro.datos['Nuevo'],
                pro.datos['Fecha_entrega'], pro.datos['Calle'],
                pro.datos['Comuna'], pro.datos['Ciudad'],
                pro.datos['Region'], pro.datos['Nombre']));

                cur.commit()



                cur.execute("SELECT Id FROM Casas WHERE Nombre='{}';".format(pro.datos['Nombre']));
                id = cur.fetchone().get("Id")


                cur.execute(("INSERT INTO Relacion_casaprecio (Casa, Precio, Actualizado, Razon_cons, Razon_terr, Fecha) VALUES ({},{},{},{},{},{}" +
                            ")").format(id,
                            pro.datos_precio['Uf'],
                            True,
                            pro.datos_precio['Razon_construidos'],
                            pro.datos_precio['Razon_terreno'],
                            str(time.strftime("%d/%m/%Y"))));

                cur.commit()

            # Actualiza el precio y razon
            else:
                cur.execute("SELECT Id FROM Casas WHERE Nombre='{}';".format(pro.datos['Nombre']));
                id = cur.fetchone().get("Id")

                cur.execute(("UPDATE Relacion_casaprecio SET Actualizado = {} WHERE Casa = {}").format(False,id));

                cur.commit()

                cur.execute(("INSERT INTO Relacion_casaprecio (Casa, Precio, Actualizado, Razon_cons, Razon_terr, Fecha) VALUES ({},{},{},{},{},{}" +
                            ")").format(id,
                                        pro.datos_precio['Uf'],
                                        True,
                                        pro.datos_precio['Razon_construidos'],
                                        pro.datos_precio['Razon_terreno'],
                                        str(time.strftime("%d/%m/%Y"))));

                cur.commit()



            cur.close()
            conn.close()



    except:
        tex = sys.exc_info()
        print(tex[2].tb_lineno)
        print(tex[1])

# analiza la pagina en busca de proyectos inmobiliarios
def analizar_link(soup, atributo,progreso):

    if soup.find_all('div', attrs={"class": atributo}) != []:

        for proy in soup.find_all('div', attrs={"class": atributo}):
            escribir(extraer(proy))
            progreso += 1
            print(str(progreso) + "/" + str(num_tot) + " // " + str(contador) + "/" + str(2 * 11 * 15))

    return int(progreso)

# Links de Ñuñoa, Providencia y Las Condes

pypyodbc.lowercase = False
collection = []

class bienraiz():

    def __init__(self):
        self.datos = {}

        self.datos_precio = {}

for n1 in ['venta','arriendo']:
    #'casa','departamento','oficina','sitio','comercial','agricola','loteo','bodega','parcela','estacionamiento','terreno-en-construcción'
    for n2 in ['casa']:
        for n3 in ['arica-y-parinacota','metropolitana','tarapaca','antofagasta','atacama','coquimbo','valparaiso','bernardo-ohiggins','maule','biobio','la-araucania','de-los-rios','los-lagos','aysen','magallanes-y-antartica-chilena']:
            collection.append("http://www.portalinmobiliario.com/"+n1+"/"+n2+"/"+n3+"?tp=6&op=2&ca=3&ts=1&dd=0&dh=6&bd=0&bh=6&or=&mn=1&sf=0&sp=0&pg=1")

contador = 1

#Loop que recorre todos los links del buscador
for link in collection:

    # Ingresa al link
    r  = requests.get(link)

    data1 = r.text

    # Busca el número de coincidencias encontradas
    m = re.search('Actualmente tenemos (\d+\.?\d*) publicaciones de', data1)
    if m:
        num_tot = float(m.group(1))
    else:
        num_tot = 0

    # de proyectos por hoja (hay que tener ojo con que no cambie)
    num_pro = 25

    # Calcula el número de pagínas que debe haber
    num_pag = math.ceil(num_tot/num_pro)
    progres = int(0)

    # Loop que recorre cada una de todas las páginas que hay por comuna
    for pag in range(num_pag):

        try:
            #Ingresa al link
            resta = str(pag).__len__()
            r2 = requests.get(link[:-resta] + str(pag+1))
            data = r2.text

            #Analiza la info
            soup = BeautifulSoup(data,"html.parser")

        except:
            tex = sys.exc_info()
            print(tex[2].tb_lineno)
            print(tex[1])


        #Loop que recorre todos los departamentos que hay en cada una de las páginas
        seg = True
        progres = analizar_link(soup, "col-sm-9 product-item-data", progres)

    contador += 1