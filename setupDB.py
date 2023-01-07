import json
import requests
import database


def fillRoute(start, end, waypoints=None):
    # Costruisco l'url della richiesta
    if waypoints:
        url = "https://maps.googleapis.com/maps/api/directions/json?" \
              f"origin={start}&" \
              "unit=metric&" \
              "mode=driving&" \
              f"destination={end}&" \
              "alternatives=false&" \
              f"waypoints={waypoints}&" \
              "departure_time=now&" \
              f"key=AIzaSyD_mPNgr6gPLNcbVPXbZWJFAj6ns4A1nr8"
    else:
        url = "https://maps.googleapis.com/maps/api/directions/json?" \
              f"origin={start}&" \
              "unit=metric&" \
              "mode=driving&" \
              f"destination={end}&" \
              "alternatives=false&" \
              "departure_time=now&" \
              f"key=AIzaSyD_mPNgr6gPLNcbVPXbZWJFAj6ns4A1nr8"

    response = requests.get(url)

    # Verifico se la richiesta ha avuto successo
    if response.status_code == 200:
        # Estraggo la distanza e la durata dalla risposta
        data = json.loads(response.text)
        distance = data['routes'][0]['legs'][0]['distance']['value']
        duration = data['routes'][0]['legs'][0]['duration']['value']

        params = (start, end, distance, duration)

        database.insert_row('route', params, ('start', 'end', 'distance', 'duration'))

    else:
        # Gestisco l'errore
        print("Errore {}: {}".format(response.status_code, response.text))

    return


database = database.Database('database.db')

database.create_table('route', ('id INTEGER PRIMARY KEY AUTOINCREMENT',
                                'start VARCHAR(30) NOT NULL',
                                'end VARCHAR(30) NOT NULL',
                                'distance INTEGER NOT NULL',
                                'duration INTEGER NOT NULL'))

database.create_table('route_link', ('route1 INTEGER NOT NULL',
                                     'route2 INTEGER NOT NULL',
                                     'sequence INTEGER NOT NULL',
                                     'PRIMARY KEY(route1, sequence)',
                                     'FOREIGN KEY(route1) REFERENCES route(id)',
                                     'FOREIGN KEY(route2) REFERENCES route(id)'))

database.create_table('traffic_route', ('route INTEGER NOT NULL',
                                        'datetime DATETIME NOT NULL',
                                        'day INTEGER NOT NULL',
                                        'duration_in_traffic INTEGER NOT NULL',
                                        'PRIMARY KEY(route, datetime)',
                                        'FOREIGN KEY(route) REFERENCES route(id)'))

fillRoute('40.806127,14.203833', '40.823204,14.217794')  # origine-posillipo
fillRoute('40.823204,14.217794', '40.826937,14.220331')  # posillipo-caracciolo
fillRoute('40.826937,14.220331', '40.829067,14.222180')  # caracciolo-campanella
fillRoute('40.829067,14.222180', '40.830315,14.219758')  # campanella-piedigrotta
fillRoute('40.830315,14.219758', '40.833584,14.221689')  # piedigrotta-ruiz
fillRoute('40.833584,14.221689', '40.836614,14.229264')  # ruiz-emanuele
fillRoute('40.836614,14.229264', '40.851575,14.242111')  # emanuele-rosa
fillRoute('40.851575,14.242111', '40.850151,14.235977')  # rosa-suarez
fillRoute('40.850151,14.235977', '40.850595,14.230794')  # suarez-destinazione
fillRoute('40.836614,14.229264', '40.837858,14.218120')  # emanuele-falcone1
fillRoute('40.806127,14.203833', '40.804322,14.186283')  # origine-manzoni1
fillRoute('40.804322,14.186283', '40.815001,14.199940')  # manzoni1-manzoni2
fillRoute('40.815001,14.199940', '40.825560,14.212163')  # manzoni2-manzoni3
fillRoute('40.825560,14.212163', '40.836749,14.213329')  # manzoni3-manzoni4
fillRoute('40.836749,14.213329', '40.839057,14.216845')  # manzoni4-europa
fillRoute('40.839057,14.216845', '40.842627,14.219541')  # europa-cilea
fillRoute('40.842627,14.219541', '40.843463,14.224989')  # cilea-gemito1
fillRoute('40.843463,14.224989', '40.845712,14.225048')  # gemito1-gemito2
fillRoute('40.845712,14.225048', '40.849772,14.225122')  # gemito2-altamura
fillRoute('40.849772,14.225122', '40.850595,14.230794')  # altamura-destinazione
fillRoute('40.836749,14.213329', '40.837858,14.218120')  # manzoni4-falcone1
fillRoute('40.837858,14.218120', '40.839722,14.226611')  # falcone1-falcone2
fillRoute('40.839722,14.226611', '40.842562,14.227428')  # falcone2-cimarosa
fillRoute('40.842562,14.227428', '40.844318,14.231716')  # cimarosa-bernini
fillRoute('40.844318,14.231716', '40.850595,14.230794')  # bernini-destinazione
fillRoute('40.806127,14.203833', '40.850595,14.230794', 'via:40.823204,14.217794|via:40.826937,14.220331|'
                                                        'via:40.829067,14.222180|via:40.830315,14.219758|'
                                                        'via:40.833584,14.221689|via:40.836614,14.229264|'
                                                        'via:40.851575,14.242111|via:40.850151,14.235977')
fillRoute('40.806127,14.203833', '40.850595,14.230794', 'via:40.823204,14.217794|via:40.826937,14.220331|'
                                                        'via:40.829067,14.222180|via:40.830315,14.219758|'
                                                        'via:40.833584,14.221689|via:40.836614,14.229264|'
                                                        'via:40.837858,14.218120|via:40.839722,14.226611|'
                                                        'via:40.842562,14.227428|via:40.844185,14.231731')
fillRoute('40.806127,14.203833', '40.850595,14.230794', 'via:40.804322,14.186283|via:40.815001,14.199940|'
                                                        'via:40.825560,14.212163|via:40.836749,14.213329|'
                                                        'via:40.837858,14.218120|via:40.839722,14.226611|'
                                                        'via:40.842562,14.227428|via:40.844318,14.231716')
fillRoute('40.806127,14.203833', '40.850595,14.230794', 'via:40.804322,14.186283|via:40.815001,14.199940|'
                                                        'via:40.825560,14.212163|via:40.836749,14.213329|'
                                                        'via:40.839057,14.216845|via:40.842627,14.219541|'
                                                        'via:40.843463,14.224989|via:40.845712,14.225048|'
                                                        'via:40.849772,14.225122')

database.insert_row('route_link', (26, 1, 1))
database.insert_row('route_link', (26, 2, 2))
database.insert_row('route_link', (26, 3, 3))
database.insert_row('route_link', (26, 4, 4))
database.insert_row('route_link', (26, 5, 5))
database.insert_row('route_link', (26, 6, 6))
database.insert_row('route_link', (26, 7, 7))
database.insert_row('route_link', (26, 8, 8))
database.insert_row('route_link', (26, 9, 9))
database.insert_row('route_link', (27, 1, 1))
database.insert_row('route_link', (27, 2, 2))
database.insert_row('route_link', (27, 3, 3))
database.insert_row('route_link', (27, 4, 4))
database.insert_row('route_link', (27, 5, 5))
database.insert_row('route_link', (27, 6, 6))
database.insert_row('route_link', (27, 10, 7))
database.insert_row('route_link', (27, 22, 8))
database.insert_row('route_link', (27, 23, 9))
database.insert_row('route_link', (27, 24, 10))
database.insert_row('route_link', (27, 25, 11))
database.insert_row('route_link', (28, 11, 1))
database.insert_row('route_link', (28, 12, 2))
database.insert_row('route_link', (28, 13, 3))
database.insert_row('route_link', (28, 14, 4))
database.insert_row('route_link', (28, 15, 5))
database.insert_row('route_link', (28, 16, 6))
database.insert_row('route_link', (28, 17, 7))
database.insert_row('route_link', (28, 18, 8))
database.insert_row('route_link', (28, 19, 9))
database.insert_row('route_link', (28, 20, 10))
database.insert_row('route_link', (29, 11, 1))
database.insert_row('route_link', (29, 12, 2))
database.insert_row('route_link', (29, 13, 3))
database.insert_row('route_link', (29, 14, 4))
database.insert_row('route_link', (29, 21, 5))
database.insert_row('route_link', (29, 22, 6))
database.insert_row('route_link', (29, 23, 7))
database.insert_row('route_link', (29, 24, 8))
database.insert_row('route_link', (29, 25, 9))
