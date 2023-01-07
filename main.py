import croniter
import time
import subprocess

# Definisco l'intervallo di tempo in cui il cron job deve essere eseguito
cron = croniter.croniter('*/5 * * * *', time.time())

while True:

    # Ottiengo il prossimo momento in cui il cron job deve essere eseguito
    next_execution = cron.get_next()

    # Calcolo il tempo che manca alla prossima esecuzione
    sleep_time = next_execution - time.time()

    # Dormo per il tempo necessario
    time.sleep(sleep_time)

    # Eseguo il file fillTrafficRoutes.py usando subprocess
    subprocess.run(["python", "fillTrafficRoutes.py"])
    print('Eseguito ' + next_execution)
