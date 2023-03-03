import json
from datetime import datetime
import requests
import database


def fill_traffic_route(num, now=None, day=None, old_durations_in_traffic=None):
    """
    Imposto le coordinate di origini e destinazioni, copiate dal file setupDB
    e inserite nello stesso ordine. Divido in tre parti i venticinque percorsi
    perche' l'API Distance Matrix di Google è limitata a 100 elementi
    'i' rappresenta l'id del primo percorso di quella richiesta
    """
    if num == 1:
        id = 1
        origins = ['40.806127,14.203833',
                   '40.823204,14.217794',
                   '40.826937,14.220331',
                   '40.829067,14.222180',
                   '40.830315,14.219758',
                   '40.833584,14.221689',
                   '40.836614,14.229264',
                   '40.851575,14.242111'
                   ]
        destinations = ['40.823204,14.217794',
                        '40.826937,14.220331',
                        '40.829067,14.222180',
                        '40.830315,14.219758',
                        '40.833584,14.221689',
                        '40.836614,14.229264',
                        '40.851575,14.242111',
                        '40.850151,14.235977'
                        ]

    elif num == 2:
        id = 9
        origins = ['40.850151,14.235977',
                   '40.836614,14.229264',
                   '40.806127,14.203833',
                   '40.804322,14.186283',
                   '40.815001,14.199940',
                   '40.825560,14.212163',
                   '40.836749,14.213329',
                   '40.839057,14.216845'
                   ]
        destinations = ['40.850595,14.230794',
                        '40.837858,14.218120',
                        '40.804322,14.186283',
                        '40.815001,14.199940',
                        '40.825560,14.212163',
                        '40.836749,14.213329',
                        '40.839057,14.216845',
                        '40.842627,14.219541'
                        ]

    else:
        id = 17
        origins = ['40.842627,14.219541',
                   '40.843463,14.224989',
                   '40.845712,14.225048',
                   '40.849772,14.225122',
                   '40.836749,14.213329',
                   '40.837858,14.218120',
                   '40.839722,14.226611',
                   '40.842562,14.227428',
                   '40.844318,14.231716'
                   ]
        destinations = ['40.845712,14.225048',
                        '40.849772,14.225122',
                        '40.850595,14.230794',
                        '40.837858,14.218120',
                        '40.839722,14.226611',
                        '40.842562,14.227428',
                        '40.844318,14.231716',
                        '40.850595,14.230794',
                        '40.850595,14.230794'
                        ]

    if now is None and day is None:
        # Recupero il datetime e il giorno della settimana
        now = datetime.now()
        day = now.weekday()
        now = now.strftime('%Y-%m-%d %H:%M:%S')

    baseUrl = "https://maps.googleapis.com/maps/api/distancematrix/json?"
    url = baseUrl + "origins=" + '|'.join(origins) + "&destinations=" + '|'.join(
        destinations) + "&unit=metric&" + "mode=driving&departure_time=now&key=AIzaSyD_mPNgr6gPLNcbVPXbZWJFAj6ns4A1nr8"

    response = requests.get(url)
    durations_in_traffic = []

    if response.status_code == 200:
        data = json.loads(response.text)

        # Per ogni elemento della matrice di distanza
        j = 0
        for element in data["rows"]:
            # Appendo le informazioni di distanza, durata e durata con il traffico alla lista
            durations_in_traffic.append(element["elements"][j]["duration_in_traffic"]["value"])
            j += 1

        # Inserisco i dati ottenuti nel database
        db = database.Database('database.db')
        for element in durations_in_traffic:
            db.insert_row('traffic_route', (id, now, day, element))
            id += 1

        if old_durations_in_traffic is not None:
            old_durations_in_traffic += durations_in_traffic
            durations_in_traffic = old_durations_in_traffic

    else:
        # Gestisco l'errore
        print("Errore {}: {}".format(response.status_code, response.text))

    return now, day, durations_in_traffic


def fill_total_traffic_routes(now, day, durations_in_traffic):
    route_ids = [26, 27, 28, 29]
    db = database.Database('database.db')

    for route_id in route_ids:
        # Eseguo una query sulla tabella route_link per recuperare i valori di 'route2'
        route_links = db.query("SELECT route2 FROM route_link WHERE route1 = %s ORDER BY sequence", (route_id,))
    
        # Inizializzare una variabile 'dit_sum' a zero
        dit_sum = 0
    
        # Iterare attraverso i valori di 'route2'
        for route in route_links:
            route2 = route[0]
            dit_sum += durations_in_traffic[route2 - 1]
    
        # Inserire la somma totale di 'dit' nella tabella traffic_route
        db.insert_row('traffic_route', (route_id, now, day, dit_sum))

    pass


data = fill_traffic_route(1)
data = fill_traffic_route(2, data[0], data[1], data[2])
data = fill_traffic_route(3, data[0], data[1], data[2])
fill_total_traffic_routes(data[0], data[1], data[2])
