from src import Utils
import psutil


"""# SOLAMENTE ESTA PROGRAMADO PARA OBTENER LA INFORMACION DE LA CPU Y LA RAM
def obtener_recursos_hardware(canal_api_key, lista_campos, menu_canal, frecuencia):
    if len(lista_campos) < 2:
        print("El canal no tiene dos campos para subir la informacion.\nPuedes crear campos accediendo al menu.")
        time.sleep(1)
        menu_canal()
    elif len(lista_campos) >= 2:
        print("Selecionar los campos que se quieran")
        while True:
            cpu = psutil.cpu_percent()  # USO DE LA CPU
            vm = psutil.virtual_memory()
            ram = vm.percent  # USO DE LA RAM

            r = realizar_peticion(method="post", url="https://api.thingspeak.com/update.json", json={
                "api_key": canal_api_key,
                "field1": cpu,
                "field2": ram
            })
            if r.status_code == 200:
                if frecuencia is None:
                    time.sleep(5)
                else:
                    time.sleep(int(frecuencia))
            else:
                print(r.status_code)
                print("A habido algun error con la peticion")
                break"""

def subir_datos_practica(c_a_k):
    cpu = psutil.cpu_percent()  # USO DE LA CPU
    vm = psutil.virtual_memory()
    ram = vm.percent  # USO DE LA RAM
    mostrar_recursos_hardware(cpu, ram, size=30)
    r = Utils.realizar_peticion(method="post", url="https://api.thingspeak.com/update.json", json={
        "api_key": c_a_k,
        "field1": cpu,
        "field2": ram
    })

# GRAFICO TIMIDO para que se vea algo al subir los datos
# Se podria implementar con un thread y meterle la actualizacion cada 2 segundos para que se vea mas real
def mostrar_recursos_hardware(cpu, ram, size=50):
    # print("\033c", end="")  # limpiar terminal
    cpu_p = (cpu / 100.0)
    cpu_carga = ">" * int(cpu_p * size) + "-" * (size - int(cpu_p * size))

    ram_p = (ram / 100.0)
    ram_carga = ">" * int(ram_p * size) + "-" * (size - int(ram_p * size))

    print(f"\rUSO DE LA CPU: |{cpu_carga}| {cpu:.2f}%", end="")
    print(f"\tUSO DE LA RAM: |{ram_carga}| {ram:.2f}%", end="\r")