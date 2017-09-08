from geopy.geocoders import Nominatim

def getLatLong(locNameS):
    geolocator = Nominatim()
    ret = []
    for loc in locNameS:
        location = geolocator.geocode(loc+", Chile")
        ret.append([location.latitude, location.longitude])
    return ret
