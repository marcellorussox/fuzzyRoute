from datetime import datetime
import croniter
import time
import subprocess

# Definisco l'intervallo di tempo in cui il cron job deve essere eseguito
cron = croniter.croniter('*/5 * * * *', time.time())

while True:

    # Ottengo il prossimo momento in cui il cron job deve essere eseguito
    next_execution = cron.get_next()

    # Calcolo il tempo che manca alla prossima esecuzione
    sleep_time = next_execution - time.time()

    # Dormo per il tempo necessario
    time.sleep(sleep_time)

    # Eseguo il file fill_traffic_routes.py usando subprocess
    subprocess.run(["python", "fill_traffic_routes.py"])
    print('Eseguito ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
