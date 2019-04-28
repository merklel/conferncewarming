import math
def latlon2km(lat1, lon1, lat2, lon2):
    r = 6372.8
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)

    a = (math.sin(dlat / 2))**2 + math.cos(lat1)* math.cos(lat2)* (math.sin(dlon / 2))**2
    c = 2 * math.asin(math.sqrt(a))
    d = r * c
    return d

print(latlon2km(20.79836, -156.331924, 40.287384, -84.161453))