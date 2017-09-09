import math
from lxml import html
import requests
import csvWrite as ew
import coordsLoc as cl
import re

collection = []
for n1 in ['venta','arriendo']:
    #'casa','departamento','oficina','sitio','comercial','agricola','loteo','bodega','parcela','estacionamiento','terreno-en-construcción'
    for n2 in ['departamento']:
        for n3 in ['arica-y-parinacota','tarapaca','antofagasta','atacama','coquimbo','bernardo-ohiggins','maule','biobio','la-araucania','de-los-rios','los-lagos','aysen','magallanes-y-antartica-chilena','valparaiso','metropolitana']:
            collection.append("http://www.portalinmobiliario.com/"+n1+"/"+n2+"/"+n3+"?tp=6&op=2&ca=3&ts=1&dd=0&dh=6&bd=0&bh=6&or=&mn=1&sf=0&sp=0&pg=1")

for collectElement in collection:

    print("SITE:" + collectElement)
    page2 = requests.get(collectElement)
    tree2 = html.fromstring(page2.content)

    paginas = tree2.xpath('//*[@id="wrapper"]/section[2]/div/div/div[1]/article/div[1]/div[1]/div/div/text()[1]')
    if len(paginas) == 0:
        continue

    pagsplit = (str(paginas[0]).split())[2]
    nrOfPubs = int(pagsplit.replace(".", ""))

    nrOfPbsPerPage = 25

    nrPages = math.ceil(nrOfPubs/nrOfPbsPerPage)

    subsites = []
    subsiteBasicUrl = (collectElement)[:-1]
    for i in range(1,nrPages+1):
        subsites.append(subsiteBasicUrl + str(i))

    last = nrOfPubs % 25
    if last == 0:
        last = 25

    master = []
    titles = ["id","Nombre","Precio","link"]
    master.append(titles)

    fileName = collectElement.split('?')
    fileName = fileName[0].split('/')
    fileName = fileName[3]+'_'+fileName[4]+'_'+fileName[5]

    for j in range(0,nrPages):
        print("page nr:" + str(j+1))
        page2 = requests.get(subsites[j])
        tree2 = html.fromstring(page2.content)
        lastRange = 25
        if j == nrPages-1:
            lastRange = last
        for i in range(1,lastRange+3):
            codeSite = '//*[@id="wrapper"]/section[2]/div/div/div[1]/article/div[3]/div[' + str(i) + ']/div[2]/div/div[1]/p[2]'
            nameSite = '//*[@id="wrapper"]/section[2]/div/div/div[1]/article/div[3]/div[' + str(i) +']/div[2]/div/div[1]/h4/a'
            priceSite = '//*[@id="wrapper"]/section[2]/div/div/div[1]/article/div[3]/div['+ str(i) +']/div[2]/div/div[2]/p/span'
            code = tree2.xpath(codeSite)
            name = tree2.xpath(nameSite)
            price = tree2.xpath(priceSite)
            if len(code) > 0:
                aux = []
                code = (code[0]).text
                if "Código" not in code:
                    codeSite = '//*[@id="wrapper"]/section[2]/div/div/div[1]/article/div[3]/div[' + str(
                        i) + ']/div[2]/div/div[1]/p[3]'
                    code = tree2.xpath(codeSite)
                    code = (code[0]).text
                code = int(code[8:])
                aux.append(code)
                newLink = str((name[0]).attrib)
                newLink = newLink[17:]
                newLink = newLink[:-4]
                newLink = 'http://www.portalinmobiliario.com/venta/'+newLink
                name = (name[0]).text
                aux.append(name)
                price = (price[0]).text
                aux.append(price)
                aux.append(newLink)
                master.append(aux)
    ew.write(master, fileName)


