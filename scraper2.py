import math
from lxml import html
import requests
import csvWrite as ew
import coordsLoc as cl
import re

collection = []
for n1 in ['venta','arriendo']:
    #'casa','departamento','oficina','sitio','comercial','agricola','loteo','bodega','parcela','estacionamiento','terreno-en-construcción'
    for n2 in ['departamento','casa']:
        for n3 in ['arica-y-parinacota','tarapaca','antofagasta','atacama','coquimbo','bernardo-ohiggins','maule','biobio','la-araucania','de-los-rios','los-lagos','aysen','magallanes-y-antartica-chilena','valparaiso','metropolitana']:
            collection.append("http://www.portalinmobiliario.com/"+n1+"/"+n2+"/"+n3+"?tp=6&op=2&ca=3&ts=1&dd=0&dh=6&bd=0&bh=6&or=&mn=1&sf=0&sp=0&pg=1")



for collectElement in collection:

    # TESTING
    oneTesting = True
    if oneTesting:
        collectElement = 'http://www.portalinmobiliario.com/venta/departamento/metropolitana?tp=6&op=2&ca=3&ts=1&dd=0&dh=6&bd=0&bh=6&or=&mn=1&sf=0&sp=0&pg=1'
    # ENDTESTING



    print("SITE:" + collectElement)
    page2 = requests.get(collectElement, allow_redirects=False)
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
    titles = ["id","Nombre","Precio","minMet","maxMet","promM","lat","lon","link"]
    master.append(titles)

    fileName = collectElement.split('?')
    fileName = fileName[0].split('/')
    fileName = fileName[3]+'_'+fileName[4]+'_'+fileName[5]

    for j in range(0,nrPages):
        print("page nr:" + str(j+1))
        page2 = requests.get(subsites[j], allow_redirects=False)
        tree2 = html.fromstring(page2.content)
        lastRange = 25
        if j == nrPages-1:
            lastRange = last
        for i in range(1,lastRange+3):
            codeSite = '//*[@id="wrapper"]/section[2]/div/div/div[1]/article/div[3]/div[' + str(i) + ']/div[2]/div/div[1]/p[2]'
            nameSite = '//*[@id="wrapper"]/section[2]/div/div/div[1]/article/div[3]/div[' + str(i) +']/div[2]/div/div[1]/h4/a'
            priceSite = '//*[@id="wrapper"]/section[2]/div/div/div[1]/article/div[3]/div['+ str(i) +']/div[2]/div/div[2]/p/span'
            meterSite = '//*[@id="wrapper"]/section[2]/div/div/div[1]/article/div[3]/div['+ str(i) +']/div[2]/div/div[3]/p/span'
            code = tree2.xpath(codeSite)
            name = tree2.xpath(nameSite)
            price = tree2.xpath(priceSite)
            meters = tree2.xpath(meterSite)
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
                price = (price[0]).text

                if len(meters) > 0:
                    meters = meters[0].text
                else:
                    meters = 'missing'
                if '-' in meters:
                    meters = meters.split('-')
                    minMeters = (meters[0])[:-1]
                    maxMeters = (meters[1])[:-3]
                    maxMeters = maxMeters[1:]
                    minMeters = float(minMeters.replace(',','.'))
                    maxMeters = float(maxMeters.replace(',','.'))
                elif 'missing' in meters:
                    minMeters = -1
                    maxMeters = -1
                else:
                    meters = meters[:-3]
                    meters = float(meters.replace(',','.'))
                    minMeters = meters
                    maxMeters = meters
                meanMeters = (minMeters+maxMeters)/2.0

                page3 = requests.get(newLink, allow_redirects=False)
                tree3 = html.fromstring(page3.content)
                latSite = '/html/head/meta[18]'
                lat = tree3.xpath(latSite)
                if len(lat) > 0:
                    lat = str((lat[0]).attrib).split(':')
                    lat = lat[3]
                    lat = (lat[2:])[:-2]
                else:
                    lat = -1

                lonSite = '/html/head/meta[19]'
                lon = tree3.xpath(lonSite)
                if len(lon) > 0:
                    lon = (((str((lon[0]).attrib).split(':'))[3])[2:])[:-2]
                else:
                    lon = -1

                aux.append(name)
                aux.append(price)
                aux.append(minMeters)
                aux.append(maxMeters)
                aux.append(meanMeters)
                aux.append(lat)
                aux.append(lon)
                aux.append(newLink)

                master.append(aux)
        #write every 100 pages.
        if j % 100 == 0:
            ew.write(master, fileName)

    ew.write(master, fileName)
    if oneTesting:
        break

