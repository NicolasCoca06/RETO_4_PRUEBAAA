from gettext import Catalog
import config as cf
import model
import csv
import sys
from DISClib.ADT import list as lt
default_limit = 1000
sys.setrecursionlimit(default_limit*10)
csv.field_size_limit(2147483647)

# -----------------------------------------------------
# NEW CONTROLLER
# -----------------------------------------------------

def newController():
    catalog = model.newCatalog()
    return catalog



def loadTrips(catalog):
    trips_file = cf.data_dir + "Bikeshare-ridership-2021-utf8-small.csv"
    input_file = csv.DictReader(open(trips_file, encoding="utf-8"))
    trips = lt.newList("ARRAY_LIST")
    filtro_1 = 0
    filtro_2 = 0
    filtro_3 = 0
    filtro_4 = 0
    filtro_5 = 0
    for trip in input_file:
        # Data Filter
        if trip["Trip  Duration"] == "0":
            filtro_1 += 1
        if (trip["Trip  Duration"] == "") or (trip["Start Station Id"] == "") or (trip["End Station Id"] == "") or (trip["Bike Id"] == ""):
            filtro_3 += 1
        if trip["Start Station Name"] == trip["End Station Name"]:
            filtro_4 += 1
        if (trip["Trip  Duration"] == "") or (trip["Start Station Id"] == "") or (trip["End Station Id"] == "") or (trip["Trip  Duration"] == "0") or (trip["Bike Id"] == "") or (trip["Start Station Name"] == trip["End Station Name"]):
            filtro_5 += 1
            pass
        else:
            # Add Station Info
            model.addStop(catalog, trip)
            filtro_2 += 1
            lt.addLast(trips, trip)
    # Add edges weights
    model.addConnectionsDigraph(catalog)
    # Unify out trips
    model.unifyOutTrips(catalog)
    # Unify bikes info
    model.unifyBikesInfo(catalog)
    
    return(filtro_1, filtro_2, filtro_3, filtro_4, filtro_5, trips)

# -----------------------------------------------------
# REQUIREMENTS FUNCTIONS
# -----------------------------------------------------

def charge(catalog):
    return model.charge(catalog)

def req1(catalog):
    return model.req1(catalog)

def req2(catalog, origin_station, max_time, min_stations, max_routes):
    return model.req2(catalog, origin_station, max_time, min_stations, max_routes)

def req3(catalog):
    return model.req3(catalog)

def req4(catalog, estacion_origen, estacion_destino):
    return model.req4(catalog, estacion_origen, estacion_destino)

def req5(catalog, lim_date_inf, lim_date_sup):
    return model.req5(catalog, lim_date_inf, lim_date_sup)

def req6(catalog, bike_id):
    return model.req6(catalog, bike_id)

