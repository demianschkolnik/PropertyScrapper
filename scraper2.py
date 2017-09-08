from lxml import html
import requests
import csvWrite as ew
import coordsLoc as cl

collection = []
for n1 in ['venta','arriendo']:
    #'casa','departamento','oficina','sitio','comercial','agricola','loteo','bodega','parcela','estacionamiento','terreno-en-construcción'
    for n2 in ['casa']:
        for n3 in ['arica-y-parinacota','metropolitana','tarapaca','antofagasta','atacama','coquimbo','valparaiso','bernardo-ohiggins','maule','biobio','la-araucania','de-los-rios','los-lagos','aysen','magallanes-y-antartica-chilena']:
            collection.append("http://www.portalinmobiliario.com/"+n1+"/"+n2+"/"+n3+"?tp=6&op=2&ca=3&ts=1&dd=0&dh=6&bd=0&bh=6&or=&mn=1&sf=0&sp=0&pg=1")


page2 = requests.get('https://www.gochile.cl/es/destinos.htm')
tree2 = html.fromstring(page2.content)
destinos1 = tree2.xpath('//*[@id="content"]/article/section[1]/ul/li[1]/a')
listaNombres = []
descList = []
quantlist = [0, 44, 9, 63, 56, 10, 44, 32, 15]
for sec in range(1,9):
    listaLinks = []
    for n in range(1,  quantlist[sec]):
        xpath = '//*[@id="content"]/article/section[' + str(sec) + ']/ul/li['+ str(n)+ ']/a'
        destinos = tree2.xpath(xpath)
        listaNombres.append(destinos[0].text)
        aux = str(destinos[0].attrib)
        aux = aux[10:]
        aux = aux[:-2]
        aux = 'https://www.gochile.cl/es/' + aux
        listaLinks.append(aux)

    for site in listaLinks:
        print('getting:',site)
        page3 = requests.get(site)
        tree3 = html.fromstring(page3.content)
        short = tree3.xpath('//*[@id="content"]/p/text()')
        if len(short) == 0:
            short = '-'
        else:
            short = str(short[0])
        descList.append(short)
    latLong = cl.getLatLong(listaNombres)
ew.writeTwoListsToColumns('try1','nombre','desc',listaNombres,descList)

print(listaNombres)
print(latLong)