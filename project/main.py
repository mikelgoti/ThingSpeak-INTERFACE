from src import Utils, ThingSpeak, Canal, subir_datos_practica
import time

# VARIABLES 

# TITULO
titulo = f"\t+-----------------------------¬\n" \
        f"\t| ThingSpeak Prompt Interface |\n" \
        f"\t+-----------------------------+\n\n"

class Main:

    def __init__(self, usuario_api_key, data) -> None:
        self.u = Utils()
        self.usuario_api_key = usuario_api_key
        self.data = data
        self.ts = ThingSpeak(self.usuario_api_key, "nombrecuenta", "correocuenta")
    
    def realizar_practica(self):
        Utils.clear()
        print("Ejecutando 1º practica.")
        Utils.wait(1)

        Utils.clear()
        print("1. Parte")
        Utils.wait(1)
        r = Utils.realizar_peticion(method="get",
                            url=f"https://api.thingspeak.com/channels.json?api_key={self.usuario_api_key}")
        if Utils.check_cs(r.status_code):
            data = r.json()
            self.ts.crear_canal("1º Practica [CPU & RAM]", data, "USO CPU", "USO RAM")
        with open("1º Practica [CPU & RAM].txt", "r") as fichero:
            lines = fichero.readlines()
            primera_linea = lines[0].split(": "[1])
            segunda_linea = lines[1].split(": ")
            c_id = primera_linea[3]
            c_api_key = segunda_linea[1]
        Utils.clear()
        print("Subiendo datos de la CPU y la RAM. Presiona [ctl+c] para parar.\n")
        try:
            while True:
                subir_datos_practica(c_api_key)
                time.sleep(15)
        except KeyboardInterrupt:
            print("\n")
        Utils.clear()
        Utils.crear_xlsx(2, "backup", "", "", "", "", c_id, self.usuario_api_key)
        Utils.clear()
        print("Borrando datos del canal")
        Utils.wait(2)
        Canal.borrar_datos(c_id, self.usuario_api_key)

        Utils.clear()
        print("2. Parte")
        Utils.wait(1)
        Utils.ejercicio_2()
        Utils.clear()
        print("Terminando script.")
        Utils.clear()
        print("\t\tSaliendo de ")
        print(titulo)
        Utils.wait(3)
        quit()


    def run(self):
        def manejar_menu_canal(c):
            opcion_canal = c.menu_canal()
            if opcion_canal is "1":
                print(c.__str__())
                Utils.teclado_infinito("0 para volver.", None, "0")
                manejar_menu_canal(c)
            elif opcion_canal == "2":
                c.actualizar_campos_canal()
                self.run()
            elif opcion_canal == "3":
                print("NO esta implementado porque es depende lo que quieras subir")
                Utils.wait(2)
                self.run()
                """i = input("Introduce la frecuencia con la que quieres subir los datos.")
                frec = i if i is not None else None"""
                #hardware.subir_datos_practica()
            elif opcion_canal == "4":
                print("NO esta implementado porque es depende lo que quieras subir")
                Utils.wait(2)
                self.run()
                #c.obtener_datos_subidos()
            elif opcion_canal == "5":
                c.opciones_exportar()
            elif opcion_canal == "6":
                self.python_basic_server()
            elif opcion_canal == "7":
                c.borrar()
                self.run()
            elif opcion_canal == "8":
                self.run()
            elif opcion_canal == "9":
                print("Ir ATARAS")

        # MENU PRINCIPAL DEL USUARIO
        Utils.clear()
        i = Utils.teclado_infinito(titulo+"\t--------------------------\n\t|0º     Realizar practica|\n\t--------------------------\n\n" 
                + f"BIENVENIDO! USUARIO {self.usuario_api_key}\n\n\n"
                "\t__MENU PRINCIPAL__\n" \
                "\t------------------\n\n" \
                "1º     Informacion de la cuenta ThingSpeak!\n\n" \
                "2º     Ver lista de canales.\n\n" \
                "3º     Salir del programa.", None, "0", "1", "2", "3")
        if i == "0":
            self.realizar_practica()
        elif i == "1" or i == "2":
            #ts = ThingSpeak(self.usuario_api_key, "nombrecuenta", "correocuenta")
            if i == "1":
                Utils.clear()
                self.ts.__str__()
                self.run()
            elif i == "2":
                # ACCESO A LISTA CANALES
                r = Utils.realizar_peticion(method="get", url=f"https://api.thingspeak.com/channels.json?api_key={self.usuario_api_key}")
                actualizar_data = r.json()
                opcion = int(self.ts.listar_canales(actualizar_data))
                if opcion is 0:
                    self.ts.crear_canal(input("Introduce el nombre del canal: \n"), actualizar_data,"cpu","ram")
                    self.run()
                else:
                    opcion -= 1
                    c = Canal(self.usuario_api_key, actualizar_data[opcion]["api_keys"][0]["api_key"], opcion+1,
                                    actualizar_data[opcion]["id"], actualizar_data[opcion]["name"],
                                    actualizar_data[opcion]["created_at"],
                                    actualizar_data[opcion]["public_flag"])
                    manejar_menu_canal(c)
                    
        elif i == "3":
            Utils.clear()
            print("\t\tSaliendo de ")
            print(titulo)
            Utils.wait(3)
            quit()

def logear():
    Utils.clear()
    print(titulo)
    print("EJEMPLO ===> \"VGNO2C3Q3N9ZXH3G\"")
    i = input("Indentificador API-KEY de la cuenta: ")
    time.sleep(1)
    return Utils.realizar_peticion(method="get", url=f"https://api.thingspeak.com/channels.json?api_key={i}"), i
        
if __name__ == "__main__":
    r,i = logear()

    while r.status_code is not 200:
        Utils.clear()
        print(titulo)
        print("La cuenta con la API-KEY introducida no existe.\nComprueba que las has introducido bien.")
        time.sleep(5)
        r,i = logear()
    data = r.json()
    mc = Main(i,data)
    mc.run()