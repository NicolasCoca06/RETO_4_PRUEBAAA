from mimetypes import init

from pyparsing import java_style_comment
import config as cf
import sys
import controller
import time
assert cf
from DISClib.ADT import list as lt
from DISClib.DataStructures import mapentry as me
from tabulate import tabulate



def newController():
    control = controller.newController()
    return control



def getTime():
  
    return float(time.perf_counter()*1000)


def deltaTime(end, start):
  
    elapsed = float(end - start)
    return elapsed

def printMenu():
    print("Bienvenido")
    print("0- Cargar información en el catálogo")
    print("1- Comprar bicicletas para las estaciones con más viajes de origen")
    print("2- Planear paseos turísticos por la ciudad")
    print("3- Reconocer los componentes fuertemente conectados")
    print("4- Planear una ruta rápida para el usuario")
    print("5- Reportar rutas en un rango de fechas para los usuarios anuales")
    print("6- Planear el mantenimiento preventivo de bicicleta")
    print("7- La estación más frecuentada por los visitantes")


def loadTrips():
    trips = controller.loadTrips(catalog)
    return trips

def req1(catalog):
    carga = controller.charge(catalog)

    print("========== Req No. 1 Inputs ==========")
    print("Top 5 stations inside in the Bikeshre Network.")
    print("Number of stations in the network: " + str(carga[0])+"\n")
    print("========== Req No. 1 Answer ==========")
    print("TOP 5 stations used as trip origins are:")

    resp = controller.req1(catalog)
    tabla_final = []
    for i in lt.iterator(resp):
        station_id = i[0].split('-')[0]
        station_name = i[0].split('-')[1]
        outdegree = i[6]
        suscriber_out_trips = i[4]
        tourist_out_trips = i[3]
        total = i[5]
        rush_hours = i[1]
        rush_dates = i[2]

        linea = [station_id, station_name, total, suscriber_out_trips, tourist_out_trips, outdegree,(rush_hours[1][0], rush_hours[0]),(rush_dates[1][0], rush_dates[0])]
        tabla_final.append(linea)
    
    print(tabulate(tabla_final, headers=["Station ID", "Station Name", "Out Trips", "Suscriber Out Trips","Tourist Out Trips", "Out Degree (Routes)", "Rush hour", "Rush date"], tablefmt="grid"))

def req2(catalog):
    start_station = input('Ingrese estación de inicio: ')
    user_time = int(input('Ingrese disponibilidad de tiempo del usuario: '))
    min_stations = int(input('Ingrese el número mínimo de estaciones: '))
    max_routes = int(input('Ingrese el número máximo de rutas '))
    res = controller.req2(catalog, start_station, user_time, min_stations, max_routes)
    total_routes = res[0]
    user_routes = res[1]

    print(f'\nThere are in total {total_routes} routes\n')

    for path in lt.iterator(user_routes):
        path_duration = path[0]
        print(f'\n The trip duration is: {path_duration}')
        print(f'\n The round trip duration is: {path_duration * 2}')
        path_stations = path[1]
        path_len = lt.size(path[1]) + 1
        print(f'\n The trip len is: {path_len}\n')
        for station in lt.iterator(path_stations):
            init_station = station[1]
            finish_station = station[2]
            weigth = station[0]
            print(f'Init Station: {init_station} | Time for next station: {weigth} | Next Station: {finish_station}')

        print('---------------------------------------------------------------------------------------------------------')

def req3(control):
    print("========== Req No. 3 Inputs ==========" + "\n")
    print("+++ calculating the strongly connected components +++" + "\n")
    print("========== Req No. 3 Answer ==========")
    


    def printreq3(lcc):
        tabla_final = []
        for i in lt.iterator(lcc):
            numero_estaciones = i[0]
            viajes_inician = i[1]
            viajes_inician = viajes_inician.split('-')
            viajes_terminan = i[2]
            viajes_terminan = viajes_terminan.split('-')
            linea = [numero_estaciones, 0, viajes_inician[0], viajes_inician[1], 0, viajes_terminan[0],viajes_terminan[1]]
            tabla_final.append(linea)
    
        print(tabulate(tabla_final, headers=["SCCID", "Max out station ID", "Max out station name", "Max out station trips","Max in station ID", "Max in station name", "Max in station trips"], tablefmt="grid"))

       
            
    lcc = controller.req3(control) 
    size_lcc = lt.size(lcc)
    print("There are " + str(size_lcc) + " Strongly Connected Componentes (SCC) in the graph.")
    print("+++ The SCC details are: +++")

    if size_lcc < 6:
        printreq3(lcc)
    else: 
        first_3 = lt.newList('ARRAY_LIST')
        last_3 = lt.newList('ARRAY_LIST')
        for i in range(1, size_lcc):
            if i > 3:
                pass
            else:
                firstcc = lt.getElement(lcc, i)
                lt.addLast(first_3, firstcc)
            if i < size_lcc - 3:
                pass
            else:
                lastcc = lt.getElement(lcc, i)
                lt.addLast(last_3, lastcc)
        print("The first 3 and last 3 of the SCC are:")
        printreq3(first_3)
        printreq3(last_3)
        

def req4(catalog):
    estacion_origen = input("Ingrese la estación de origen: ") 
    estacion_destino = input("Ingrese la estación de destino: ") 
    res = controller.req4(catalog, estacion_origen, estacion_destino)
    print(f'\nThe average time for the trip is {int(res[1])} minutes')
    for station in lt.iterator(res[0]):
        if station[0] != 0:
            print(f'Station -> {station[1]} / Time for next station -> {int(station[0])} minutes')
        else:
            print(f'Last Station -> {station[1]}')

def req5(catalog):
    lim_date_inf = input("Ingrese la fecha inicial: ")
    lim_date_sup = input("Ingrese la fecha final: ")
    resp = controller.req5(catalog, lim_date_inf, lim_date_sup)
    out_hours = resp[0]
    out_stations = resp[1]
    in_hours = resp[2]
    in_stations = resp[3]
    size_time = resp[4]
    size_viajes = resp[5]
    print("========== Req No. 5 Inputs ==========")
    print("Analyze trips between " + lim_date_inf + " and " + lim_date_sup + "\n")
    print("========== Req No. 5 Answer ==========")
    print(str(size_viajes) + " trips between " + lim_date_inf + " and " + lim_date_sup + "\n")
    print("Total trip time: " + str(size_time) + " [sec].")
    print("Total trip time: " + str(size_time/3600) + " [h]." + "\n")
   

    print(f'\nThe top out station(s) is:')
    for i in lt.iterator(out_stations[1]):
        print(f'{i} with {out_stations[0]} trips')

    print(f'\nThe top in station(s) is:')
    for j in lt.iterator(in_stations[1]):
        print(f'{j} with {in_stations[0]} trips')

    print(f'\nThe top out trips rush hour is: ')
    for k in lt.iterator(out_hours[1]):
        print(f'{k} with {out_hours[0]} trips')

    print(f'\nThe top in trips rush hour is: ')
    for l in lt.iterator(in_hours[1]):
        print(f'{l} with {in_hours[0]} trips')

def req6(catalog):
    bike_id = int(float(input("Ingrese el ID de la bicicleta: "))) 
    resp = controller.req6(catalog, bike_id)
    print("========== Req No. 6 Inputs ==========")
    print("Analyze trips with the bike ID" + str(bike_id) + "\n")
    print("========== Req No. 6 Answer ==========")
    print(str(resp[0]) + " trips with bike ID " + str(bike_id))
    print("Total trip time: " + str(resp[1]) + " [sec].")
    print("Total trip time: " + str(resp[1]/3600) + " [h].")


    print('\n=======================================================================================\n')
    size_viajes_origen = me.getKey(resp[2])
    lista_estaciones_origen = me.getValue(resp[2])
    print("Top out station data: " + "\n")
    print(f'Out trips: {size_viajes_origen}')
    for i in lt.iterator(lista_estaciones_origen):
        print(f'Station Name -> {i} / Out Trips -> {size_viajes_origen}')
    print('\n=======================================================================================\n')
    size_viajes_destino = me.getKey(resp[3])
    lista_estaciones_destino = me.getValue(resp[3])
    print("Top in station data: " + "\n")
    print(f'Out trips: {size_viajes_destino}')
    for j in lt.iterator(lista_estaciones_destino):
        print(f'Station Name -> {j} / Out trips -> {size_viajes_destino}')
    print('\n=======================================================================================\n')



while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 0:
        print("Cargando información de los archivos ....")

        catalog = newController()

        trips = loadTrips()
        resp = controller.charge(catalog)

        print("===== Bike-Trips-Time DiGraphs =====")
        print(str(trips[4] + trips[1]) + " trips in CSV file...")
        print(str(trips[1]) + " trips with no self-reference data...")
        print(str((trips[4] + trips[1])-trips[0]) + " trips with complete data...")
        print(str(trips[0]) + " trips with incomplete data...")
        print(str(trips[4]) + " trips with 0.0 in 'Trip duration'..."+"\n")
        print(str(resp[0]) + " unique stations loaded...")
        print(str(resp[1]) + " clean avg trips data loaded..."+"\n")
        print("--- DiGraph specs ---")
        print("Nodes: " + str(resp[0]) + " & Edges: " + str(resp[1]))
        print("First 5 & Last 5 Stations loaded in the DiGraph.")

        tabla_final = []

        for station in lt.iterator(resp[4]):
            station_id = station["station_id"]
            station_name = station["station_name"]
            station_indegree = station["indegree"]
            station_outdegree = station["outdegree"]
            station_out = station["out_trips"]
            station_in = station["in_trips"]
            linea = [station_id, station_name, station_indegree, station_outdegree, station_out, station_in]
            tabla_final.append(linea)
    
        print(tabulate(tabla_final, headers=["Station ID", "Station Name", "In Degree (Routes)", "Out Degree (Routes)","In Trips", "Out Trips"], tablefmt="grid"))

  
        

        
    elif int(inputs[0]) == 1:
        req1(catalog)
        
    elif int(inputs[0]) == 2:
        req2(catalog)
    
    elif int(inputs[0]) == 3:
        req3(catalog)

    elif int(inputs[0]) == 4:
        req4(catalog)

    elif int(inputs[0]) == 5:
        req5(catalog)
        
    elif int(inputs[0]) == 6:
        req6(catalog)
    
  
        
    else:
        sys.exit(0)
sys.exit(0)