import sqlite3
import matplotlib.pyplot as plt
import pandas as pd
import fuzzy


# Aggiorno i valori della serie con quelli dell'affidabilità ottenuta tramite logica fuzzy
def update_value(serie, conn):
    for i, value in enumerate(serie):
        id = serie.index[i][0]
        std_pct = serie.iloc[i]
        query = f"SELECT distance FROM route WHERE id = {id}"
        distance = conn.execute(query).fetchone()
        reliability = fuzzy.get_reliability(distance, std_pct)
        serie.iloc[i] = reliability
    return serie


def set_plot(type):
    plt.xlabel('Ora')
    if type == 'std':
        plt.ylabel('Deviazione standard (%)')
        plt.ylim(0, 30)
    elif type == 'rel':
        plt.ylabel('Affidabilità (%)')
        plt.ylim(45, 90)
    elif type == 'mean':
        plt.ylabel('Media delle stime del tempo di percorrenza (min)')
        plt.ylim(15, 55)
    plt.xticks([0, 4, 8, 12, 16, 20, 24], ['00:00', '4:00', '08:00', '12:00', '16:00', '20:00', '00:00'])
    pass


# Creo i grafici per deviazione standard e affidabilità
def create_plots(series, type):
    # Creo un dizionario per memorizzare i dati dei diversi route
    data = {}

    # Scorro la serie per estrarre i dati delle route
    for index, value in series.items():

        # Aggiungo la route al dizionario se non esiste ancora
        if index[0] not in data:
            data[index[0]] = {0: [], 1: []}

        # Aggiungo i dati della route al dizionario
        data[index[0]][index[2]].append(((index[1].hour + index[1].minute / 60), value))

    # Inizializzo un dizionario per memorizzare i dati dei grafici
    plots = {0: [], 1: []}

    # Per ogni route nel dizionario, creo un grafico per ciascun day_type
    for route, day_types in data.items():
        for day_type, values in day_types.items():
            # Crea un grafico con hour_block sulle ascisse e value sulle ordinate per la deviazione standard
            x_std = [val[0] for val in values]
            y_std = [val[1] for val in values]
            plots[day_type].append((x_std, y_std))

    # Creo il primo grafico con i dati dei giorni feriali
    plt.figure(figsize=(20, 10))
    plt.rcParams.update({'font.size': 24})
    labels = ['Percorso A', 'Percorso B', 'Percorso C', 'Percorso D']
    i = 0
    set_plot(type)
    plt.title('Giorni feriali')

    # Cicla attraverso i dati e disegna ciascuna linea sul grafico
    for x, y in plots[0]:
        plt.plot(x, y, label=labels[i], lw=3)
        plt.legend(labels)
    plt.savefig('assets/plots/' + type + '_fer')
    plt.clf()

    # Creo il secondo grafico con i dati dei giorni festivi
    plt.figure(figsize=(20, 10))
    plt.rcParams.update({'font.size': 24})
    i = 0
    set_plot(type)
    plt.title('Giorni festivi')

    # Ciclo attraverso i dati e disegna ciascuna linea sul grafico
    for x, y in plots[1]:
        plt.plot(x, y, label=labels[i], lw=3)
        i += 1
        plt.legend()
    plt.savefig('assets/plots/' + type + '_fes')
    plt.clf()


# Connessione al database
conn = sqlite3.connect('database.db')

# Recupero dei dati
query = 'SELECT * FROM traffic_route WHERE route in (26, 27, 28, 29)'
data = pd.read_sql_query(query, conn)

# Creo una nuova colonna per la fascia oraria ogni 15 minuti
data['datetime'] = pd.to_datetime(data['datetime']) + pd.Timedelta(hours=1)
data['datetime'] = data['datetime'].round('15min')
data['hour_block'] = data['datetime'].dt.time

# Creo una nuova colonna per distinguere tra giorni feriali e festivi
data['day_type'] = 0
data.loc[data['day'].isin([5, 6]), 'day_type'] = 1

# Raggruppo i dati per ID del percorso, fascia oraria e giorno della settimana
data_grouped = data.groupby(['route', 'hour_block', 'day_type'])['duration_in_traffic']

# Calcolo la percentuale di deviazione standard per ogni gruppo
data_grouped_std = data_grouped.std()
data_grouped_mean = data_grouped.mean()
data_grouped_std_pct = (data_grouped_std / data_grouped_mean * 100)
create_plots(data_grouped_std_pct, 'std')
data_grouped_rel_pct = update_value(data_grouped_std_pct, conn)
create_plots(data_grouped_rel_pct, 'rel')
create_plots(data_grouped_mean / 60, 'mean')

conn.close()
