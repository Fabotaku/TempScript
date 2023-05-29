import psutil
import time


print("Escribe el nombre del proceso del juego que quieres limitar, por ejemplo: cod *(sin el .exe)*)")
process_name = input()
process_name = process_name + ".exe"
min_wait_time = 60 * 60 * 20  # tienes que esperar 20 horas para poder abrir el juego
wait_time = 0
last_kill_time = 0

while True:
    # checar si el proceso sigue corriendo
    for process in psutil.process_iter(['pid', 'name']):
        if process.name() == process_name:
            # obtener el tiempo de creacion del proceso
            process_create_time = process.create_time()
            # obtener el tiempo actual
            current_time = time.time()
            # checar si el proceso lleva mas de 2 horas abierto
            if current_time - process_create_time >= 7200: ##ver proceso que se quiere matar y cambiar el tiempo en segundos, por ejemplo 3600 para que se cierre cada hora y no lo pueda usar por el tiempo minimo
                # matar proceso y resetear tiempo de espera
                process.kill()
                wait_time = min_wait_time
                last_kill_time = time.time()
                print("El proceso ha terminado. necesitas esperar {} segundos para abrirlo de nuevo.".format(wait_time))
            else:
                # checar si el tiempo de espera es mayor a 0
                if wait_time > 0:
                    # matar proceso y resetear tiempo de espera
                    if time.time() - last_kill_time >= wait_time:
                        process.kill()
                        last_kill_time = time.time()
                        print("El proceso ha terminado. necesitas esperar {} segundos para abrirlo de nuevo.".format(wait_time))
                    else:
                        remaining_time = int(wait_time - (time.time() - last_kill_time))
                        process.kill()
                        print("El proceso no puede ser abierto. Necesitas esperar {} segundos.".format(remaining_time))
        else:
            # checar si el tiempo de espera es mayor a 0
            if wait_time > 0:
                if time.time() - last_kill_time >= wait_time:
                    # resetear tiempo de espera
                    wait_time = 0
                    last_kill_time = 0
                    print("Ya puedes abrir el proceso.")
                else:
                    remaining_time = int(wait_time - (time.time() - last_kill_time))
                    print("El proceso no puede ser abierto. Necesitas esperar {} segundos.".format(remaining_time))
            else:
                print("El proceso no se ha iniciado.")
